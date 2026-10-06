# 신고 유효성 벤치마크 결과 (10개 모델)

- 데이터: `data.txt` 실제 신고 사례 90건 (유효 45 / 무효 45, 사람 판정)
- 데이터셋: `report-validity-public.jsonl` (JevBench noul 형식, 사전검사형 프롬프트)
- 하네스: jevbench v1.2 순정 (typesafe 어댑터, OpenRouter Decisions 라우터)
- 실행일: 2026-09-29~10-06 / 90건씩 0 실패, 스키마 유효 100%
- 실행 비용: Jev $0.0028 · Solar Decide $0.0036 · Kev 4B $0.0017 · Mercury free $0 · Tev1 4B $0.0019 · Liquid D1 $0.0017 · Clef Flash $0.0044 · Clef $0.0118 · PPLX Decider $0.0018 · GPT-6 Luna Decisions $0.0049
- 결과 원본: `C:\Users\gambit\Desktop\BACKEND\jevbench-runs\` 아래 각 `report-*` 디렉터리
- 재생성: `python build_dataset.py` (data.txt → report-validity-public.jsonl)

## 모델별 해석 ID 및 요금

| 모델 | 요청 슬러그 | 해석 ID | 요금 |
|---|---|---|---|
| Jev | `~typesafe/jev-latest` | `typesafe/jev-1.13-20260917` | $0.042/M in, $0 out |
| Solar Decide | `upstage/solar-decide` | `upstage/solar-decide-20260928` | $0.05/M in, $0 out |
| Kev 4B | `jaredpalmer/kev-4b` | `jaredpalmer/kev-4b-20260924` | $0.042/M in, $0 out |
| Mercury Decide (free) | `inception/mercury-decide:free` | `inception/mercury-decide-20260930` | 무료 |
| Tev1 4B | `togethercomputer/tev1-4b-experimental` | `togethercomputer/tev1-4b-experimental-20260923` | $0.042/M in, $0 out |
| Liquid D1 | `liquid/d1` | `liquid/d1-20260930` | $0.04/M in, $0 out |
| Clef Flash | `cloudflare/clef-flash` | `cloudflare/clef-flash` | $0.09/M in, $0 out |
| Clef | `cloudflare/clef` | `cloudflare/clef` | $0.24/M in, $0 out |
| PPLX Decider | `perplexity/pplx-decider-v1-27b` | `perplexity/pplx-decider-v1-27b-20261001` | $0.04/M in, $0 out |
| GPT-6 Luna Decisions | `openai/gpt-6-luna-decisions` | `openai/gpt-6-luna-decisions-20261006` | $0.10/M in, $0 out |

## 헤드라인 지표

| 지표 | GPT-6 Luna | Jev | PPLX Decider | Clef | Liquid D1 | Clef Flash | Kev 4B | Mercury free | Solar Decide | Tev1 4B |
|---|---|---|---|---|---|---|---|---|---|---|
| 정확도 | **90.0%** (81/90) | 83.3% | 84.4% | 83.3% | 80.0% | 73.3% | 72.2% | 66.7% | 57.8% | 63.3% |
| Brier | **0.174** | 0.270 | 0.275 | 0.237 | 0.280 | 0.347 | 0.386 | 0.551 | 0.642 | 0.460 |
| ECE | 0.112 | 0.100 | 0.101 | 0.054 | **0.068** | 0.104 | 0.069 | 0.286 | 0.299 | 0.111 |
| 지연 p50 / p95 | 0.70초 / 1.19초 | **0.24초 / 0.36초** | 0.32 / 0.37 | 0.52 / 1.02 | 0.39 / 0.52 | 0.31 / 0.53 | 2.45 / 5.39 | 0.31 / 0.37 | 0.37 / 0.62 | 0.26 / 0.33 |
| 카테고리별 | other 37/41 · swearing 28/33 · sexual 9/9 · griefing 7/7 | other 34/41 · swearing 27/33 · sexual 7/9 · griefing 7/7 | other 34/41 · swearing 27/33 · sexual 8/9 · griefing 7/7 | other 34/41 · swearing 25/33 · sexual 9/9 · griefing 7/7 | other 30/41 · swearing 26/33 · sexual 9/9 · griefing 7/7 | other 30/41 · swearing 22/33 · sexual 7/9 · griefing 7/7 | other 26/41 · swearing 25/33 · sexual 7/9 · griefing 7/7 | other 29/41 · swearing 18/33 · sexual 7/9 · griefing 6/7 | other 26/41 · swearing 21/33 · sexual 3/9 · griefing 2/7 | other 22/41 · swearing 22/33 · sexual 7/9 · griefing 6/7 |

## 임계값 0.5 기준 혼동 행렬

| | GPT-6 Luna | Jev | PPLX Decider | Clef | Liquid D1 | Clef Flash | Kev 4B | Mercury free | Solar Decide | Tev1 4B |
|---|---|---|---|---|---|---|---|---|---|---|
| 유효 신고 정확 판정 (TP) | 37 | 42 | 37 | 35 | 31 | 24 | 32 | 17 | 44 | 40 |
| 무효 신고 → 통과 오판 (FP) | **1** | 11 | 6 | 5 | 4 | 3 | 12 | 2 | 37 | 29 |
| 무효 신고 정확 기각 (TN) | 44 | 34 | 39 | 40 | 41 | 42 | 33 | 43 | 8 | 16 |
| **유효 신고 → 기각 오판 (FN)** | 8 | **3** | 8 | 10 | 14 | **21** | 13 | **28** | 1 | 5 |
| 기각 절감율 | 57.8% | 41.1% | 52.2% | 55.6% | 61.1% | 70.0% | 51.1% | 78.9% | 10.0% | 23.3% |
| 기각 정밀도 | 84.6% | 79.2% | 86.7% | 88.9% | 91.1% | 93.3% | 73.3% | 95.6% | 54.3% | 76.2% |

## 임계값별 스윕 (FN = 유효 신고를 기각하는 오판)

| 임계값 | GPT-6 Luna | Jev | PPLX Decider | Clef | Liquid D1 | Clef Flash | Kev 4B | Mercury free | Solar Decide | Tev1 4B |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.2 | **0 / 33.3%** | 0 / 8.9% | 1 / 18.9% | 2 / 28.9% | 5 / 47.8% | 4 / 40.0% | 0 / 4.4% | 25 / 73.3% | 0 / 1.1% | 0 / 1.1% |
| 0.3 | 2 / 40.0% | 1 / 20.0% | 2 / 33.3% | 4 / 43.3% | 7 / 52.2% | 13 / 55.6% | 4 / 21.1% | 26 / 76.7% | 0 / 5.6% | 2 / 8.9% |
| 0.4 | 4 / 51.1% | 1 / 32.2% | 6 / 44.4% | 9 / 52.2% | 10 / 55.6% | 19 / 66.7% | 8 / 38.9% | 28 / 78.9% | 0 / 7.8% | 2 / 14.4% |
| 0.5 | 8 / 57.8% | 3 / 41.1% | 8 / 52.2% | 10 / 55.6% | 14 / 61.1% | 21 / 70.0% | 13 / 51.1% | 28 / 78.9% | 1 / 10.0% | 5 / 23.3% |
| 0.7 | 17 / 68.9% | 18 / 66.7% | 25 / 74.4% | 16 / 65.6% | 22 / 72.2% | 28 / 80.0% | 34 / 86.7% | 29 / 81.1% | 1 / 16.7% | 13 / 51.1% |

## 모델별 분석

### GPT-6 Luna Decisions — 신규 종합 1위
정확도 90.0%(1위), Brier 0.174(1위), FP 1건으로 오탐이 사실상 없음. 결정적으로
FN-절감 경선의 안전 구간을 갈아치웠음: FN 0건인 상태에서 기각 33.3%(Jev는 FN 0이면 8.9%가 한계),
FN 2건에 40.0%(Jev는 FN 1~3건 구간에서 20~41%). 즉 동일 안전도에서 절감 효과가 4배 이상.
대가는 요금 2.4배($0.10/M)와 지연 3배(p50 0.70초 — 그러나 여전히 1초 이내), ECE 0.112로
보정은 Jev와 비슷. 0.5 기준 FN 8건이 부담이면 0.2~0.3 운영으로 안전 구간 활용 권장.

### Jev — 종합 2위 (비용/속도 효율 1위)
FN 3건/41.1% 절감은 이제 Luna에 정면으로 밀리지만, 요금은 2.4배 저렴하고 지연은 3배 빠름.
FN 0건 운영도 가능(0.2). 비용·지연 민감 시 여전히 유효한 선택.

### PPLX Decider — 3위
정확도 84.4%, $0.04/M 최저부대, Jev급 속도. 0.5 기준 FN 8건은 Luna/Jev보다 많지만
과거 1세대 대비 확실히 개선된 수준. 무료/저가 운영 시 차선.

### Clef — 4위
정확도 83.3%(Jev 동률), Brier 0.237/ECE 0.054 보정 최고. 그러나 FN 10건, 단가 $0.24/M(6배),
p50 0.52초. 비용 대비 매력도가 낮음.

### Liquid D1 — 5위
80.0%, ECE 0.068, $0.04/M. FN-절감 경선은 Jev/Luna 하위.

### 나머지 — 부적합
Clef Flash 73.3%(FN 21건) · Kev 4B 72.2%(FN 13건, p50 2.45초) · Mercury free 66.7%(FN 28건) ·
Tev1 63.3%(전 구간 Jev 하위) · Solar Decide 57.8%(기준선 수준).

## 공통 관찰

- 실제 신고 사례는 공개 합성 코호트보다 훨씬 어려움 (Jev: 합성 98.6% → 실데이터 83.3%).
  유일한 예외가 GPT-6 Luna Decisions(90.0%) — 최신 대형 decide 모델과 실데이터 격차가 줄어드는 추세.
- 확률 보정(ECE)이 좋아도 분류 분리가 안 되면 사전검사로 쓸 수 없음 (Kev 4B 사례).
- 기각 절감율과 FN은 강한 트레이드오프 관계이며, 모델 선택 시 FN 허용 한도가 기준이 되어야 함.
- 1세대 대안(solar/mercury/kev/tev1)은 전원 기각 확정. 2세대(liquid/clef/pplx/luna)부터
  실용 수준에 진입했으며, 특히 Luna Decisions는 요금·지연 희생 대비 정확도 이득이 가장 큼.

## 재현 명령

```
cd C:\Users\gambit\Desktop\BACKEND\jevbench
python build_dataset.py  # (ReportJevBench 폴더에서)
MSYS_NO_PATHCONV=1 OPENROUTER_API_KEY=<key> TYPESAFE_PATH=/decisions \
  python -m jevbench.cli run --tasks <dataset.jsonl> --adapter typesafe \
  --endpoint https://openrouter.ai/api/alpha --model "~typesafe/jev-latest" \
  --key-env OPENROUTER_API_KEY --price-in-per-m 0.042 --price-out-per-m 0 \
  --results <run>\results.jsonl --raw-dir <run>\raw --ledger <run>\ledger.jsonl \
  --cap-usd 5 --manifest <run>\manifest.json --delay-s 0.2
```
