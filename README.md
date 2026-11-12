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

## 결과 요약 (2026-09-29~11-12, 90건, 17개 모델)

### 실용 후보군 (정확도 순)

| 지표 | GPT-6 Luna | PPLX v1.1 | Gemini D-1 | Liquid D1 Ultra | PPLX v1 | Jev 1.13 | Clef | Jev 1.14 | Liquid D1 |
|---|---|---|---|---|---|---|---|---|---|
| 정확도 | **90.0%** | 88.9% | 86.7% | 85.6% | 84.4% | 83.3% | 83.3% | 82.2% | 80.0% |
| ECE | 0.112 | 0.068 | 0.097 | 0.078 | 0.101 | 0.100 | 0.054 | 0.057 | 0.068 |
| 0.5 기준 기각 절감 | 57.8% | 56.7% | 61.1% | 60.0% | 52.2% | 41.1% | 55.6% | 34.4% | 61.1% |
| 유효 신고 기각 오판(FN) | 8건 | 8건 | 11건 | 11건 | 8건 | **3건** | 10건 | **1건** | 14건 |
| 지연 p50 | 0.70초 | 0.53초 | 0.57초 | 0.54초 | 0.32초 | **0.24초** | 0.52초 | 0.40초 | 0.39초 |
| 요금(in/M) | $0.10 | **$0.02** | $0.10 | $0.042 | $0.04 | $0.042 | $0.24 | $0.042 | $0.04 |

- **GPT-6 Luna Decisions — 1위 (프로덕션 사용 중)**: 정확도 90.0%, FP 1건의 정밀 기각.
  FN 0건 상태에서 기각 33.3%(타 모델 불가). 대가: 요금 2.4배, p50 0.70초.
  FN 부담 시 0.2~0.3 운영 권장.
- **PPLX Decider v1.1 — 2위, 가성비 1위**: 88.9%에 요금 전체 최저($0.02/M). v1 완전 대체.
- **Gemini Decision-1 — 신규 3위**: 86.7%, FP 1건의 Luna급 정밀 기각. 요금도 Luna와 동일한
  $0.10/M이나 FN-절감 경선 전체가 Luna에 흡수되어 교체 근거는 없음.
- **Liquid D1 Ultra — 4위**: D1 대비 +5.6%p 개선. 경선은 Luna/Jev 하위 — D1 사용 중이라면 Ultra로.
- **Jev 1.13 — FN 최소 기록**(3건) + 최속(0.24초). **Jev 1.14** — FN 1건 고정 곡선·ECE 개선
  이지만 정확도 -1.1%p에 저-FN 절감도 열세라 이 워크로드 기준 1.13 유지 권장.
- **Clef** — 보정 최상위, 단가 6배라 비용 대비 열세.

### 부적합 (FN 과다 또는 기준선 수준)

PPLX v1 84.4%(v1.1 대체됨) · Liquid D1 80.0%(Ultra 대체됨) · MS Decision-1 76.7%(FN 9건,
같은 요금대 Jev 하위) · Clef Omni 74.4%(FN 21건) · Clef Flash 73.3%(FN 21건) ·
Kev 4B 72.2%(FN 13건, p50 2.45초) · DREX v2.0 71.1%(FN 24건) · Mercury free 66.7%(FN 28건) ·
Tev1 4B 63.3%(전 구간 Jev 하위) · Solar Decide 57.8%(기준선 수준).
※ `scaledown/classify-1`은 state 형식 제약으로 미측정.

상세 근거(혼동 행렬, 임계값 스윕, 카테고리별)는 `RESULTS.md`.

## 데이터 주의사항

- 채팅 로그는 실제 게임 채팅이므로 공개 시 플레이어 닉네임이 포함될 수 있습니다.
  외부 공개 전 익명화 여부를 확인하세요.
- 라벨은 단일 판정자 기준이라 경계 사례(특히 `other` Family 41건)에는 주관이 포함됩니다.
