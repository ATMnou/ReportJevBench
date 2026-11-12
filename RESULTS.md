# 신고 유효성 벤치마크 결과 (19개 모델)

- 데이터: `data.txt` 실제 신고 사례 90건 (유효 45 / 무효 45, 사람 판정)
- 데이터셋: `report-validity-public.jsonl` (JevBench noul 형식, 사전검사형 프롬프트)
- 하네스: jevbench v1.2 순정 (typesafe 어댑터, OpenRouter Decisions 라우터)
- 실행일: 2026-09-29~11-12 / 90건씩 0 실패, 스키마 유효 100%
- 실행 비용: Jev $0.0028 · Solar Decide $0.0036 · Kev 4B $0.0017 · Mercury free $0 · Tev1 4B $0.0019 · Liquid D1 $0.0017 · Clef Flash $0.0044 · Clef $0.0118 · PPLX Decider $0.0018 · GPT-6 Luna $0.0049 · Clef Omni $0.0076 · PPLX Decider v1.1 $0.0009 · MS Decision-1 $0.0017 · DREX v2.0 $0.0024 · Jev 1.14 $0.0028 · Liquid D1 Ultra $0.0017 · Gemini Decision-1 $0.0049 · PPLX Decider v1.2 $0.0009 · DREX Max $0.0027
- 결과 원본: `C:\Users\gambit\Desktop\BACKEND\jevbench-runs\` 아래 각 `report-*` 디렉터리
- 재생성: `python build_dataset.py` (data.txt → report-validity-public.jsonl)
- 미측정: `scaledown/classify-1` — state 형식 제약(문자열/{text,document} 전용)으로 제외

## 모델별 해석 ID 및 요금

| 모델 | 요청 슬러그 | 해석 ID | 요금 |
|---|---|---|---|
| GPT-6 Luna Decisions | `openai/gpt-6-luna-decisions` | `openai/gpt-6-luna-decisions-20261006` | $0.10/M in, $0 out |
| PPLX Decider v1.1 | `perplexity/pplx-decider-v1.1-27b` | `perplexity/pplx-decider-v1.1-27b-20261006` | $0.02/M in, $0 out |
| Gemini Decision-1 | `google/gemini-decision-1` | `google/gemini-decision-1-20261111` | $0.10/M in, $0 out |
| Liquid D1 Ultra | `liquid/d1-ultra` | `liquid/d1-ultra-20261015` | $0.042/M in, $0 out |
| PPLX Decider v1.2 | `perplexity/pplx-decider-v1.2` | `perplexity/pplx-decider-v1.2-20261016` | $0.02/M in, $0 out |
| PPLX Decider v1 | `perplexity/pplx-decider-v1-27b` | `perplexity/pplx-decider-v1-27b-20261001` | $0.04/M in, $0 out |
| Jev 1.13 | `~typesafe/jev-latest` | `typesafe/jev-1.13-20260917` | $0.042/M in, $0 out |
| Clef | `cloudflare/clef` | `cloudflare/clef` | $0.24/M in, $0 out |
| Jev 1.14 | `typesafe/jev-1.14` | `typesafe/jev-1.14-20261014` | $0.042/M in, $0 out |
| Liquid D1 | `liquid/d1` | `liquid/d1-20260930` | $0.04/M in, $0 out |
| MS Decision-1 | `microsoft/microsoft-decision-1` | `microsoft/microsoft-decision-1-20261009` | $0.042/M in, $0 out |
| DREX Max | `nace-ai/drex-max` | `nace-ai/drex-max-20261016` | $0.06/M in, $0 out |
| Clef Omni | `cloudflare/clef-omni` | `cloudflare/clef-omni-20261009` | $0.15/M in, $0 out |
| Clef Flash | `cloudflare/clef-flash` | `cloudflare/clef-flash` | $0.09/M in, $0 out |
| Kev 4B | `jaredpalmer/kev-4b` | `jaredpalmer/kev-4b-20260924` | $0.042/M in, $0 out |
| DREX v2.0 | `nace-ai/drex-v2.0` | `nace-ai/drex-v2.0-20261009` | $0.06/M in, $0 out |
| Mercury Decide (free) | `inception/mercury-decide:free` | `inception/mercury-decide-20260930` | 무료 |
| Tev1 4B | `togethercomputer/tev1-4b-experimental` | `togethercomputer/tev1-4b-experimental-20260923` | $0.042/M in, $0 out |
| Solar Decide | `upstage/solar-decide` | `upstage/solar-decide-20260928` | $0.05/M in, $0 out |

## 상위권 지표 (정확도 80% 이상, 10개 모델)

| 지표 | GPT-6 Luna | PPLX v1.1 | Gemini D-1 | Liquid D1 Ultra | PPLX v1 | Jev 1.13 | Clef | PPLX v1.2 | Jev 1.14 | Liquid D1 |
|---|---|---|---|---|---|---|---|---|---|---|
| 정확도 | **90.0%** | 88.9% | 86.7% | 85.6% | 84.4% | 83.3% | 83.3% | 83.3% | 82.2% | 80.0% |
| Brier | **0.174** | 0.220 | 0.221 | 0.216 | 0.275 | 0.270 | 0.237 | 0.253 | 0.266 | 0.280 |
| ECE | 0.112 | 0.068 | 0.097 | 0.078 | 0.101 | 0.100 | **0.054** | 0.058 | 0.057 | 0.068 |
| 지연 p50 / p95 | 0.70 / 1.19 | 0.53 / 0.62 | 0.57 / 0.74 | 0.54 / 0.78 | **0.32** / 0.37 | **0.24** / 0.36 | 0.52 / 1.02 | 0.56 / 0.85 | 0.40 / 0.45 | 0.39 / 0.52 |
| 카테고리별 | other 37/41 · swearing 28/33 · sexual 9/9 · griefing 7/7 | other 35/41 · swearing 29/33 · sexual 9/9 · griefing 7/7 | other 36/41 · swearing 26/33 · sexual 9/9 · griefing 7/7 | other 35/41 · swearing 27/33 · sexual 8/9 · griefing 7/7 | other 34/41 · swearing 27/33 · sexual 8/9 · griefing 7/7 | other 34/41 · swearing 27/33 · sexual 7/9 · griefing 7/7 | other 34/41 · swearing 25/33 · sexual 9/9 · griefing 7/7 | other 33/41 · swearing 26/33 · sexual 9/9 · griefing 7/7 | other 34/41 · swearing 26/33 · sexual 8/9 · griefing 6/7 | other 30/41 · swearing 26/33 · sexual 9/9 · griefing 7/7 |

## 하위권 지표 (정확도 80% 미만, 9개 모델 — 전원 부적합)

| 지표 | MS Decision-1 | DREX Max | Clef Omni | Clef Flash | Kev 4B | DREX v2.0 | Mercury free | Tev1 4B | Solar Decide |
|---|---|---|---|---|---|---|---|---|---|
| 정확도 | 76.7% | 76.7% | 74.4% | 73.3% | 72.2% | 71.1% | 66.7% | 63.3% | 57.8% |
| Brier | 0.321 | 0.303 | 0.338 | 0.347 | 0.386 | 0.390 | 0.551 | 0.460 | 0.642 |
| ECE | 0.077 | 0.093 | 0.069 | 0.104 | 0.069 | 0.128 | 0.286 | 0.111 | 0.299 |
| 지연 p50 | 0.65초 | 0.90초 | 0.34초 | 0.31초 | 2.45초 | 0.83초 | 0.31초 | 0.26초 | 0.37초 |
| 카테고리별 | other 31/41 · swearing 26/33 · sexual 7/9 · griefing 5/7 | other 31/41 · swearing 23/33 · sexual 8/9 · griefing 7/7 | other 28/41 · swearing 24/33 · sexual 8/9 · griefing 7/7 | other 30/41 · swearing 22/33 · sexual 7/9 · griefing 7/7 | other 26/41 · swearing 25/33 · sexual 7/9 · griefing 7/7 | other 28/41 · swearing 21/33 · sexual 8/9 · griefing 7/7 | other 29/41 · swearing 18/33 · sexual 7/9 · griefing 6/7 | other 22/41 · swearing 22/33 · sexual 7/9 · griefing 6/7 | other 26/41 · swearing 21/33 · sexual 3/9 · griefing 2/7 |

## 임계값 0.5 기준 혼동 행렬

### 상위권 (정확도 순)

| | GPT-6 Luna | PPLX v1.1 | Gemini D-1 | Liquid D1 Ultra | PPLX v1 | Jev 1.13 | Clef | PPLX v1.2 | Jev 1.14 | Liquid D1 |
|---|---|---|---|---|---|---|---|---|---|---|
| 유효 신고 정확 판정 (TP) | 37 | 37 | 34 | 34 | 37 | 42 | 35 | 37 | 44 | 31 |
| 무효 신고 → 통과 오판 (FP) | 1 | 2 | 1 | 2 | 6 | 11 | 5 | 7 | 15 | 4 |
| 무효 신고 정확 기각 (TN) | 44 | 43 | 44 | 43 | 39 | 34 | 40 | 38 | 30 | 41 |
| **유효 신고 → 기각 오판 (FN)** | 8 | 8 | **11** | 11 | 8 | **3** | 10 | 8 | 1 | 14 |
| 기각 절감율 | 57.8% | 56.7% | 61.1% | 60.0% | 52.2% | 41.1% | 55.6% | 51.1% | 34.4% | 61.1% |
| 기각 정밀도 | 84.6% | 84.3% | 80.0% | 79.6% | 86.7% | 79.2% | 88.9% | 82.6% | 96.8% | 91.1% |

### 하위권 (전원 부적합)

| | MS Decision-1 | DREX Max | Clef Omni | Clef Flash | Kev 4B | DREX v2.0 | Mercury free | Tev1 4B | Solar Decide |
|---|---|---|---|---|---|---|---|---|---|
| 유효 신고 정확 판정 (TP) | 36 | 25 | 24 | 24 | 32 | 21 | 17 | 40 | 44 |
| 무효 신고 → 통과 오판 (FP) | 12 | 1 | 2 | 3 | 12 | 2 | 2 | 29 | 37 |
| 무효 신고 정확 기각 (TN) | 33 | 44 | 43 | 42 | 33 | 43 | 43 | 16 | 8 |
| **유효 신고 → 기각 오판 (FN)** | 9 | **20** | **21** | **21** | 13 | **24** | **28** | 5 | 1 |
| 기각 절감율 | 46.7% | 71.1% | 71.1% | 70.0% | 51.1% | 74.4% | 78.9% | 23.3% | 10.0% |
| 기각 정밀도 | 78.6% | 68.8% | 67.2% | 93.3% | 73.3% | 64.2% | 95.6% | 76.2% | 54.3% |

## 임계값별 스윕 (FN = 유효 신고를 기각하는 오판)

### 상위권

| 임계값 | GPT-6 Luna | PPLX v1.1 | Gemini D-1 | Liquid D1 Ultra | PPLX v1 | Jev 1.13 | Clef | PPLX v1.2 | Jev 1.14 | Liquid D1 |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.2 | 0 / 33.3% | 3 / 34.4% | 7 / 53.3% | 5 / 46.7% | 1 / 18.9% | 0 / 8.9% | 2 / 28.9% | 1 / 23.3% | 1 / 10.0% | 5 / 47.8% |
| 0.3 | 2 / 40.0% | 6 / 41.1% | 9 / 56.7% | 6 / 51.1% | 2 / 33.3% | 1 / 20.0% | 4 / 43.3% | 2 / 31.1% | 1 / 21.1% | 7 / 52.2% |
| 0.4 | 4 / 51.1% | 8 / 51.1% | 10 / 57.8% | 8 / 55.6% | 6 / 44.4% | 1 / 32.2% | 9 / 52.2% | 6 / 43.3% | 1 / 27.8% | 10 / 55.6% |
| 0.5 | 8 / 57.8% | 8 / 56.7% | 11 / 61.1% | 11 / 60.0% | 8 / 52.2% | 3 / 41.1% | 10 / 55.6% | 8 / 51.1% | 1 / 34.4% | 14 / 61.1% |
| 0.7 | 17 / 68.9% | 16 / 67.8% | 22 / 74.4% | 20 / 72.2% | 25 / 74.4% | 18 / 66.7% | 16 / 65.6% | 18 / 67.8% | 6 / 47.8% | 22 / 72.2% |

### 하위권

| 임계값 | MS Decision-1 | DREX Max | Clef Omni | Clef Flash | Kev 4B | DREX v2.0 | Mercury free | Tev1 4B | Solar Decide |
|---|---|---|---|---|---|---|---|---|---|
| 0.2 | 3 / 31.1% | 6 / 48.9% | 6 / 42.2% | 4 / 40.0% | 0 / 4.4% | 10 / 54.4% | 25 / 73.3% | 0 / 1.1% | 0 / 1.1% |
| 0.3 | 5 / 40.0% | 13 / 60.0% | 13 / 53.3% | 13 / 55.6% | 4 / 21.1% | 16 / 63.3% | 26 / 76.7% | 2 / 8.9% | 0 / 5.6% |
| 0.4 | 5 / 42.2% | 17 / 67.8% | 16 / 61.1% | 19 / 66.7% | 8 / 38.9% | 20 / 70.0% | 28 / 78.9% | 2 / 14.4% | 0 / 7.8% |
| 0.5 | 9 / 46.7% | 20 / 71.1% | 21 / 71.1% | 21 / 70.0% | 13 / 51.1% | 24 / 74.4% | 28 / 78.9% | 5 / 23.3% | 1 / 10.0% |
| 0.7 | 16 / 60.0% | 24 / 76.7% | 28 / 80.0% | 28 / 80.0% | 34 / 86.7% | 34 / 85.6% | 29 / 81.1% | 13 / 51.1% | 1 / 16.7% |

## 모델별 분석

### GPT-6 Luna Decisions — 1위 (프로덕션 사용 중)
정확도 90.0%(1위), Brier 0.174(1위), FP 1건. FN-절감 안전 구간 지배: FN 0건에 기각 33.3%
(그 어떤 모델도 달성 못함), FN 2건에 40.0%. 대가는 요금 2.4배($0.10/M)와 p50 0.70초.
FN 8건(0.5)이 부담이면 0.2~0.3 운영 권장.

### PPLX Decider v1.1 — 2위, 가성비 1위 (v1.2 등장으로도 유지)
88.9%로 여전히 2위. 요금 $0.02/M — 전체 최저. 신규 v1.2(83.3%)가 v1.1에 미달하면서
v1.1의 가치가 더 명확해짐. PPLX 계열 선택 시 v1.1 고정 권장.

### Gemini Decision-1 — 3위. 우수하나 Luna와 동일 요금이라 대체 불가
정확도 86.7%(3위), FP 1건의 Luna급 정밀 기각(절감 61.1%, 정밀도 80%). 다만 FN-절감
경선 전체가 Luna에 흡수됨: Luna는 더 낮은 FN(0~4건)으로 동등 이상의 절감을 달성.

### Liquid D1 Ultra — 4위
D1(80.0%) 대비 +5.6%p, FN 14→11건, 절감 61.1% 유지. 경선은 Luna/Jev 하위.
D1 사용 중이라면 Ultra로, 상위 2개 모델 대체는 아님.

### PPLX Decider v1.2 — 신규. v1.1 대비 레그레션
정확도 83.3%(v1.1 대비 -5.6%p), FP 7건(v1.1 2건). TP 37건은 v1.1과 같지만 FP 증가로
정확도 하락. ECE 0.058과 0.2 저임계(FN 1건/23.3%)는 나쁘지 않으나 전 구간에서 v1.1 하위.
PPLX 계열은 v1.1 사용 권장.

### Jev 1.13 / Jev 1.14 — FN 최소 기록 보유 (순위는 중위)
Jev 1.13: FN 3건/41.1% 절감, FN 0건 운영 가능(0.2), p50 0.24초 최속.
Jev 1.14: FN 1건 고정 곡선(기각 정밀도 96.8% 최상위), ECE 0.057. 정확도 82.2%.
두 모델 모두 "FN을 극도로 줄이는" 용도에는 유효하나 절감율은 상위권 대비 낮음.

### 나머지 — 부적합
Clef 83.3%(보정 최고지만 FN 10건, $0.24/M 6배) · Liquid D1 80.0%(Ultra 대체됨) ·
MS Decision-1 76.7%(FN 9건, 같은 요금대 Jev 하위) · DREX Max 76.7%(FN 20건, v2.0보단 개선
됐으나 여전히 극단 보수 — "상위권" 주장은 실데이터 미확인) · Clef Omni 74.4%(FN 21건) ·
Clef Flash 73.3%(FN 21건) · Kev 4B 72.2%(FN 13건, p50 2.45초) · DREX v2.0 71.1%(FN 24건) ·
Mercury free 66.7%(FN 28건) · Tev1 63.3%(전 구간 하위) · Solar Decide 57.8%(기준선 수준).

## 공통 관찰

- 실제 신고 사례는 공개 합성 코호트보다 훨씬 어려움 (Jev 1.13: 합성 98.6% → 실데이터 83.3%).
  예외는 GPT-6 Luna(90.0%), PPLX v1.1(88.9%), Gemini D-1(86.7%) — 최신 대형 decide 모델과
  실데이터 격차가 줄어드는 추세가 뚜렷함.
- 확률 보정(ECE)이 좋아도 분류 분리가 안 되면 사전검사로 쓸 수 없음 (Kev 4B 사례).
- 기각 절감율과 FN은 강한 트레이드오프 관계이며, 모델 선택 시 FN 허용 한도가 기준이 되어야 함.
- 버전 업그레이드가 항상 개선을 보장하지 않음: PPLX v1→v1.1(+4.5%p) 성공,
  PPLX v1.1→v1.2(-5.6%p) 레그레션, Liquid D1→Ultra(+5.6%p) 성공, Jev 1.13→1.14 근소 열세.
- Cloudflare Clef 계열은 플래시/옴니 변형이 모두 본체보다 FN이 많음 — 변형보다 본체 권장.
- DREX 계열(v2.0, max) 모두 FN 과다 극단 보수 패턴 — max도 실데이터 "상위권" 아님.

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
