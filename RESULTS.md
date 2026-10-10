# 신고 유효성 벤치마크 결과 (11개 모델)

- 데이터: `data.txt` 실제 신고 사례 90건 (유효 45 / 무효 45, 사람 판정)
- 데이터셋: `report-validity-public.jsonl` (JevBench noul 형식, 사전검사형 프롬프트)
- 하네스: jevbench v1.2 순정 (typesafe 어댑터, OpenRouter Decisions 라우터)
- 실행일: 2026-09-29~10-09 / 90건씩 0 실패, 스키마 유효 100%
- 실행 비용: Jev $0.0028 · Solar Decide $0.0036 · Kev 4B $0.0017 · Mercury free $0 · Tev1 4B $0.0019 · Liquid D1 $0.0017 · Clef Flash $0.0044 · Clef $0.0118 · PPLX Decider $0.0018 · GPT-6 Luna $0.0049 · Clef Omni $0.0076 · PPLX Decider v1.1 $0.0009
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
| Clef Omni | `cloudflare/clef-omni` | `cloudflare/clef-omni-20261009` | $0.15/M in, $0 out |
| PPLX Decider v1.1 | `perplexity/pplx-decider-v1.1-27b` | `perplexity/pplx-decider-v1.1-27b-20261006` | $0.02/M in, $0 out |

## 헤드라인 지표 (정확도 순)

| 지표 | GPT-6 Luna | PPLX v1.1 | PPLX v1 | Jev | Clef | Liquid D1 | Clef Omni | Clef Flash | Kev 4B | Mercury free | Tev1 4B | Solar Decide |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 정확도 | **90.0%** | 88.9% | 84.4% | 83.3% | 83.3% | 80.0% | 74.4% | 73.3% | 72.2% | 66.7% | 63.3% | 57.8% |
| Brier | **0.174** | 0.220 | 0.275 | 0.270 | 0.237 | 0.280 | 0.338 | 0.347 | 0.386 | 0.551 | 0.460 | 0.642 |
| ECE | 0.112 | 0.068 | 0.101 | 0.100 | 0.054 | **0.068** | 0.069 | 0.104 | 0.069 | 0.286 | 0.111 | 0.299 |
| 지연 p50 / p95 | 0.70 / 1.19 | 0.53 / 0.62 | 0.32 / 0.37 | **0.24** / 0.36 | 0.52 / 1.02 | 0.39 / 0.52 | 0.34 / 0.52 | 0.31 / 0.53 | 2.45 / 5.39 | 0.31 / 0.37 | 0.26 / 0.33 | 0.37 / 0.62 |
| 카테고리별 | other 37/41 · swearing 28/33 · sexual 9/9 · griefing 7/7 | other 35/41 · swearing 29/33 · sexual 9/9 · griefing 7/7 | other 34/41 · swearing 27/33 · sexual 8/9 · griefing 7/7 | other 34/41 · swearing 27/33 · sexual 7/9 · griefing 7/7 | other 34/41 · swearing 25/33 · sexual 9/9 · griefing 7/7 | other 30/41 · swearing 26/33 · sexual 9/9 · griefing 7/7 | other 28/41 · swearing 24/33 · sexual 8/9 · griefing 7/7 | other 30/41 · swearing 22/33 · sexual 7/9 · griefing 7/7 | other 26/41 · swearing 25/33 · sexual 7/9 · griefing 7/7 | other 29/41 · swearing 18/33 · sexual 7/9 · griefing 6/7 | other 22/41 · swearing 22/33 · sexual 7/9 · griefing 6/7 | other 26/41 · swearing 21/33 · sexual 3/9 · griefing 2/7 |

## 임계값 0.5 기준 혼동 행렬 (정확도 순)

| | GPT-6 Luna | PPLX v1.1 | PPLX v1 | Jev | Clef | Liquid D1 | Clef Omni | Clef Flash | Kev 4B | Mercury free | Tev1 4B | Solar Decide |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 유효 신고 정확 판정 (TP) | 37 | 37 | 37 | 42 | 35 | 31 | 24 | 24 | 32 | 17 | 40 | 44 |
| 무효 신고 → 통과 오판 (FP) | 1 | 2 | 6 | 11 | 5 | 4 | 2 | 3 | 12 | 2 | 29 | 37 |
| 무효 신고 정확 기각 (TN) | 44 | 43 | 39 | 34 | 40 | 41 | 43 | 42 | 33 | 43 | 16 | 8 |
| **유효 신고 → 기각 오판 (FN)** | 8 | 8 | 8 | **3** | 10 | 14 | **21** | **21** | 13 | **28** | 5 | 1 |
| 기각 절감율 | 57.8% | 56.7% | 52.2% | 41.1% | 55.6% | 61.1% | 71.1% | 70.0% | 51.1% | 78.9% | 23.3% | 10.0% |
| 기각 정밀도 | 84.6% | 84.3% | 86.7% | 79.2% | 88.9% | 91.1% | 67.2% | 93.3% | 73.3% | 95.6% | 76.2% | 54.3% |

## 임계값별 스윕 (FN = 유효 신고를 기각하는 오판)

| 임계값 | GPT-6 Luna | PPLX v1.1 | PPLX v1 | Jev | Clef | Liquid D1 | Clef Omni | Clef Flash | Kev 4B | Mercury free | Tev1 4B | Solar Decide |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.2 | 0 / 33.3% | 3 / 34.4% | 1 / 18.9% | 0 / 8.9% | 2 / 28.9% | 5 / 47.8% | 6 / 42.2% | 4 / 40.0% | 0 / 4.4% | 25 / 73.3% | 0 / 1.1% | 0 / 1.1% |
| 0.3 | 2 / 40.0% | 6 / 41.1% | 2 / 33.3% | 1 / 20.0% | 4 / 43.3% | 7 / 52.2% | 13 / 53.3% | 13 / 55.6% | 4 / 21.1% | 26 / 76.7% | 2 / 8.9% | 0 / 5.6% |
| 0.4 | 4 / 51.1% | 8 / 51.1% | 6 / 44.4% | 1 / 32.2% | 9 / 52.2% | 10 / 55.6% | 16 / 61.1% | 19 / 66.7% | 8 / 38.9% | 28 / 78.9% | 2 / 14.4% | 0 / 7.8% |
| 0.5 | 8 / 57.8% | 8 / 56.7% | 8 / 52.2% | 3 / 41.1% | 10 / 55.6% | 14 / 61.1% | 21 / 71.1% | 21 / 70.0% | 13 / 51.1% | 28 / 78.9% | 5 / 23.3% | 1 / 10.0% |
| 0.7 | 17 / 68.9% | 16 / 67.8% | 25 / 74.4% | 18 / 66.7% | 16 / 65.6% | 22 / 72.2% | 28 / 80.0% | 28 / 80.0% | 34 / 86.7% | 29 / 81.1% | 13 / 51.1% | 1 / 16.7% |

## 모델별 분석

### GPT-6 Luna Decisions — 1위
정확도 90.0%(1위), Brier 0.174(1위), FP 1건. FN-절감 안전 구간을 지배: FN 0건에 기각 33.3%
(Jev는 FN 0이면 8.9% 한계), FN 2건에 40.0%. 대가는 요금 2.4배($0.10/M)와 p50 0.70초.
FN 8건(0.5)이 부담이면 0.2~0.3 운영 권장.

### PPLX Decider v1.1 — 2위, 가성비 1위
정확도 88.9%로 v1(84.4%)을 4.5%p 상회하면서 요금은 절반($0.02/M — 전체 최저). p50 0.53초.
ECE 0.068, Brier 0.220. 같은 FN에서 v1보다 기각 절감이 항상 높아(v1 완전 대체) 저비용 운영의
1순위. Luna 대비 정확도 -1.1%p, 요금 1/5, 속도 1.3배.

### Jev — 3위 (FN 최소 기록 보유)
FN 3건은 전 모델 중 최소이며 FN 0건 운영도 가능(0.2, 절감 8.9%). 요금 $0.042/M, p50 0.24초 최속.
정확도는 1위권(PPLX v1.1, Luna)에 밀림.

### Clef — 4위
정확도 83.3%(Jev 동률), Brier/ECE 보정 최상위권. FN 10건, 단가 $0.24/M(최고), p50 0.52초.
비용 대비 메리트 부족.

### Liquid D1 — 5위
80.0%, ECE 0.068, $0.04/M. FN-절감 경선은 상위 4개 모델 하위.

### 나머지 — 부적합
Clef Omni 74.4%(FN 21건, clef-flash와 동일한 FN 과다 패턴 — Omni 업그레이드 실패) ·
Clef Flash 73.3%(FN 21건) · Kev 4B 72.2%(FN 13건, p50 2.45초) · Mercury free 66.7%(FN 28건) ·
Tev1 63.3%(전 구간 Jev 하위) · Solar Decide 57.8%(기준선 수준).

## 공통 관찰

- 실제 신고 사례는 공개 합성 코호트보다 훨씬 어려움 (Jev: 합성 98.6% → 실데이터 83.3%).
  유일한 예외는 GPT-6 Luna(90.0%), PPLX v1.1(88.9%) — 최신 대형 decide 모델과 실데이터 격차가 줄어드는 추세.
- 확률 보정(ECE)이 좋아도 분류 분리가 안 되면 사전검사로 쓸 수 없음 (Kev 4B 사례).
- 기각 절감율과 FN은 강한 트레이드오프 관계이며, 모델 선택 시 FN 허용 한도가 기준이 되어야 함.
- Cloudflare Clef 계열은 플래시/옴니 변형이 모두 본체(clef)보다 FN이 많음 — 변형보다 본체 권장.
- PPLX v1 → v1.1은 동일 요금 대비 정확도 +4.5%p, 절감 +4.5%p로 명확한 업그레이드. v1은 대체됨.

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
