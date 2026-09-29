# ReportJevBench

로블록스 게임(ATM STUDIO)에서 접수된 **실제 신고 사례**와 운영자가 직접 판정한
유효/무효 라벨로 만든, [JevBench](https://github.com/fstandhartinger/jevbench)
기반 신고 유효성 사전검사 벤치마크입니다.

같은 SOLIS 백엔드의 신고 사전검사(허위 신고 자동 기각)가 실제 데이터에서
얼마나 정확한지 측정하고, 사전검사 모델(Jev, Solar Decide 등)을 동일 조건으로
비교하는 것이 목적입니다.

## 폴더 구성

| 파일 | 설명 |
|---|---|
| `data.txt` | 원본 데이터. 케이스 번호 / `사유:` / `채팅 로그:` / `정답: 유효\|무효` 블록 × 90건 |
| `build_dataset.py` | `data.txt` → JevBench JSONL 변환 스크립트 |
| `report-validity-public.jsonl` | 생성된 벤치마크 데이터셋 (90건, noul, 유효 45 / 무효 45) |
| `RESULTS.md` | 실행 결과 상세 (정확도, 혼동 행렬, 임계값 스윕, 결론) |

## 데이터셋 형식

프로덕션 사전검사(solis.js `prescreenReport`)와 **동일한 호출**을 측정하도록
state와 프롬프트를 그대로 사용합니다.

- `state`: `{ "report_reason": <신고 사유>, "chat_logs": <채팅 로그 전문> }`
- `question`: noul — "chat_logs에 Roblox 커뮤니티 규칙 위반이 있는가?"
- `labels`: `["no", "yes"]` / `expected`: 무효=`no`, 유효=`yes`
- `family`: 신고 사유 키워드 기반 대분류 (swearing / sexual / griefing / other)
- `provenance.source_id`: `data.txt` 원본 케이스 번호 역추적용

데이터를 수정한 뒤에는 다시 생성합니다:

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
(예: Solar Decide → `--model upstage/solar-decide --price-in-per-m 0.05`).

요약:

```bash
python -m jevbench.cli summarize \
  --tasks "C:\Users\gambit\Desktop\BACKEND\ReportJevBench\report-validity-public.jsonl" \
  --results "C:\Users\gambit\Desktop\BACKEND\jevbench-runs\report-jev\results.jsonl" \
  --public-export "C:\Users\gambit\Desktop\BACKEND\jevbench-runs\report-jev\summary.json"
```

## 결과 요약 (2026-09-29, 90건)

| 지표 | Jev | Solar Decide | Kev 4B |
|---|---|---|---|
| 정확도 | **83.3%** | 57.8% (기준선 50%) | 72.2% |
| ECE | 0.100 | 0.299 | 0.069 |
| 임계값 0.5에서 기각 절감 | 41.1% | 10.0% | 51.1% |
| 유효 신고 기각 사고(FN) | 3건 | 1건 | **13건** |
| 지연 p50 | 0.24초 | 0.37초 | 2.45초 |

- **Solar Decide는 부적합** — 정확도가 기준선과 구분되지 않고 캘리브레이션 붕괴(ECE 0.30).
- **Kev 4B도 부적합** — 기각 절감은 가장 크지만(51%) FN이 13건(유효 신고의 29%)으로 사고
  위험이 크고, p50 2.45초로 Jev 대비 10배 느림.
- **Jev 유지 권장**, 단 임계값 0.5에서는 유효 신고의 6.7%가 기각 사고로 빠지므로
  **0.4 낮춤을 권장** (FN 3→1건, 기각 절감 41%→32%). 상세 근거는 `RESULTS.md`.

## 데이터 주의사항

- 채팅 로그는 실제 게임 채팅이므로 공개 시 플레이어 닉네임이 포함될 수 있습니다.
  외부 공개 전 익명화 여부를 확인하세요.
- 라벨은 단일 운영자 판정치라 경계 사례(특히 `other` Family 41건)에는 주관이 포함됩니다.
