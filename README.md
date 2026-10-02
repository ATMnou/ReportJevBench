# ReportJevBench

Roblox 게임 채팅에서 접수된 **실제 신고 사례**와 사람이 판정한 유효/무효 라벨로
만든, [JevBench](https://github.com/fstandhartinger/jevbench) 기반 신고 유효성
벤치마크입니다.

의사결정 모델(Jev-class)이 "이 신고가 유효한가?"를 실제 데이터에서 얼마나 잘
판정하는지 측정하고, 후보 모델들을 동일 조건에서 비교합니다.

## 폴더 구성

| 파일 | 설명 |
|---|---|
| `data.txt` | 원본 데이터. 케이스 번호 / `사유:` / `채팅 로그:` / `정답: 유효\|무효` 블록 × 90건 |
| `build_dataset.py` | `data.txt` → JevBench JSONL 변환 스크립트 |
| `report-validity-public.jsonl` | 생성된 벤치마크 데이터셋 (90건, noul, 유효 45 / 무효 45) |
| `RESULTS.md` | 실행 결과 상세 (정확도, 혼동 행렬, 임계값 스윕, 모델별 결론) |

## 데이터셋 형식

사전검사형 noul 질문 하나로 각 사례를 판정합니다.

- `state`: `{ "report_reason": <신고 사유>, "chat_logs": <채팅 로그 전문> }`
- `question`: noul — "chat_logs에 Roblox 커뮤니티 규칙 위반이 있는가?"
- `labels`: `["no", "yes"]` / `expected`: 무효=`no`, 유효=`yes`
- `family`: 신고 사유 키워드 기반 대분류 (swearing / sexual / griefing / other)
- `provenance.source_id`: `data.txt` 원본 케이스 번호 역추적용

데이터를 다시 생성합니다:

```bash
python build_dataset.py
```

## 벤치마크 실행

JevBench 클론(`C:\Users\gambit\Desktop\BACKEND\jevbench`)이 필요합니다.
Windows용 `fcntl` 셔임과 `TYPESAFE_PATH` 패치가 포함된 환경 — 자세한 내용은
그 폴더의 `PATCH-NOTE.md` 참고.

```bash
cd C:\Users\gambit\Desktop\BACKEND\jevbench
mkdir -p "C:\Users\gambit\Desktop\BACKEND\jevbench-runs\report-jev"

MSYS_NO_PATHCONV=1 \
OPENROUTER_API_KEY=<OpenRouter 키> \
TYPESAFE_PATH=/decisions \
python -m jevbench.cli run \
  --tasks "C:\Users\gambit\Desktop\BACKEND\ReportJevBench\report-validity-public.jsonl" \
  --adapter typesafe \
  --endpoint https://openrouter.ai/api/alpha \
  --model "~typesafe/jev-latest" \
  --key-env OPENROUTER_API_KEY \
  --price-in-per-m 0.042 --price-out-per-m 0 \
  --results "C:\Users\gambit\Desktop\BACKEND\jevbench-runs\report-jev\results.jsonl" \
  --raw-dir "C:\Users\gambit\Desktop\BACKEND\jevbench-runs\report-jev\raw" \
  --ledger "C:\Users\gambit\Desktop\BACKEND\jevbench-runs\report-jev\ledger.jsonl" \
  --cap-usd 5 \
  --manifest "C:\Users\gambit\Desktop\BACKEND\jevbench-runs\report-jev\manifest.json" \
  --delay-s 0.2
```

다른 모델을 돌릴 때는 `--model`과 `--price-in-per-m`만 바꾸면 됩니다
(예: Solar Decide → `--model upstage/solar-decide --price-in-per-m 0.05`,
무료 모델 → `--price-in-per-m 0 --price-out-per-m 0 --cost-basis provider_free_tier`).

요약:

```bash
python -m jevbench.cli summarize \
  --tasks "C:\Users\gambit\Desktop\BACKEND\ReportJevBench\report-validity-public.jsonl" \
  --results "C:\Users\gambit\Desktop\BACKEND\jevbench-runs\report-jev\results.jsonl" \
  --public-export "C:\Users\gambit\Desktop\BACKEND\jevbench-runs\report-jev\summary.json"
```

## 결과 요약 (2026-09-29~30, 90건)

| 지표 | Jev | Solar Decide | Kev 4B | Mercury Decide (free) | Tev1 4B | Liquid D1 |
|---|---|---|---|---|---|---|
| 정확도 | **83.3%** | 57.8% (기준선 50%) | 72.2% | 66.7% | 63.3% | 80.0% |
| ECE | 0.100 | 0.299 | 0.069 | 0.286 | 0.111 | 0.068 |
| 임계값 0.5에서 기각 절감 | 41.1% | 10.0% | 51.1% | 78.9% | 23.3% | 61.1% |
| 유효 신고 기각 오판(FN) | 3건 | 1건 | **13건** | **28건** | 5건 | 14건 |
| 지연 p50 | 0.24초 | 0.37초 | 2.45초 | 0.31초 | 0.26초 | 0.39초 |

- **Jev가 종합 1위** — 정확도와 절감 효과의 균형이 유일하게 맞습니다.
- **Liquid D1** — 2위(80.0%)이자 가장 근접한 경쟁자. ECE 최저·단가 최저지만 FN-절감
  경선에서 Jev 우위는 아님. FN 감수 시 고려 여지.
- **Solar Decide** — 판정 자체가 기준선과 구분되지 않고 캘리브레이션 붕괴(ECE 0.30).
- **Kev 4B** — 확률이 중간대에 몰려 분리가 안 됨. 0.5 기준 FN 13건, p50 2.45초로 느림.
- **Mercury Decide (free)** — 무료이지만 유효 신고의 62%를 기각하는 극단적 보수 성향.
  임계값을 0.2까지 내려도 FN 25건으로 실용 불가.
- **Tev1 4B** — 속도는 Jev급이지만 전 임계값에서 Jev에 밀림(FN 5건 때 절감 23% vs Jev FN 3건에 41%).

상세 근거(혼동 행렬, 임계값 스윕, 카테고리별)는 `RESULTS.md`.

## 데이터 주의사항

- 채팅 로그는 실제 게임 채팅이므로 공개 시 플레이어 닉네임이 포함될 수 있습니다.
  외부 공개 전 익명화 여부를 확인하세요.
- 라벨은 단일 판정자 기준이라 경계 사례(특히 `other` Family 41건)에는 주관이 포함됩니다.
