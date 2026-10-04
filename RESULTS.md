# 신고 유효성 벤치마크 결과 (Jev / Solar Decide / Kev 4B / Mercury Decide free / Tev1 4B / Liquid D1 / Clef / Clef Flash / PPLX Decider)

- 데이터: `data.txt` 실제 신고 사례 90건 (유효 45 / 무효 45, 사람 판정)
- 데이터셋: `report-validity-public.jsonl` (JevBench noul 형식, 사전검사형 프롬프트)
- 하네스: jevbench v1.2 순정 (typesafe 어댑터, OpenRouter Decisions 라우터)
- 실행일: 2026-09-29~10-01 / 90건씩 0 실패, 스키마 유효 100%
- 실행 비용: Jev $0.0028 · Solar Decide $0.0036 · Kev 4B $0.0017 · Mercury free $0 · Tev1 4B $0.0019 · Liquid D1 $0.0017 · Clef Flash $0.0044 · Clef $0.0118 · PPLX Decider $0.0018
- 결과 원본: `C:\Users\gambit\Desktop\BACKEND\jevbench-runs\` 아래 `report-jev` / `report-solar-decide` / `report-kev-4b` / `report-mercury-decide-free` / `report-tev1-4b` / `report-liquid-d1` / `report-clef-flash` / `report-clef` / `report-pplx-decider`
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

## 헤드라인 지표

| 지표 | Jev | Solar Decide | Kev 4B | Mercury free | Tev1 4B | Liquid D1 | Clef Flash | Clef | PPLX Decider |
|---|---|---|---|---|---|---|---|---|---|
| 정확도 | 83.3% (75/90) | 57.8% | 72.2% | 66.7% | 63.3% | 80.0% | 73.3% | 83.3% (75/90) | **84.4%** (76/90) |
| Brier | 0.270 | 0.642 | 0.386 | 0.551 | 0.460 | 0.280 | 0.347 | **0.237** | 0.275 |
| ECE | 0.100 | 0.299 | 0.069 | 0.286 | 0.111 | 0.068 | 0.104 | **0.054** | 0.101 |
| 지연 p50 / p95 | **0.24초 / 0.36초** | 0.37 / 0.62 | 2.45 / 5.39 | 0.31 / 0.37 | 0.26 / 0.33 | 0.39 / 0.52 | 0.31 / 0.53 | 0.52 / 1.02 | 0.32 / 0.37 |
| 카테고리별 | other 34/41 · swearing 27/33 · sexual 7/9 · griefing 7/7 | other 26/41 · swearing 21/33 · sexual 3/9 · griefing 2/7 | other 26/41 · swearing 25/33 · sexual 7/9 · griefing 7/7 | other 29/41 · swearing 18/33 · sexual 7/9 · griefing 6/7 | other 22/41 · swearing 22/33 · sexual 7/9 · griefing 6/7 | other 30/41 · swearing 26/33 · sexual 9/9 · griefing 7/7 | other 30/41 · swearing 22/33 · sexual 7/9 · griefing 7/7 | other 34/41 · swearing 25/33 · sexual 9/9 · griefing 7/7 | other 34/41 · swearing 27/33 · sexual 8/9 · griefing 7/7 |

## 임계값 0.5 기준 혼동 행렬

| | Jev | Solar Decide | Kev 4B | Mercury free | Tev1 4B | Liquid D1 | Clef Flash | Clef | PPLX Decider |
|---|---|---|---|---|---|---|---|---|---|
| 유효 신고 정확 판정 (TP) | 42 | 44 | 32 | 17 | 40 | 31 | 24 | 35 | 37 |
| 무효 신고 → 통과 오판 (FP) | 11 | 37 | 12 | 2 | 29 | 4 | 3 | 5 | 6 |
| 무효 신고 정확 기각 (TN) | 34 | 8 | 33 | 43 | 16 | 41 | **42** | 40 | 39 |
| **유효 신고 → 기각 오판 (FN)** | **3** | 1 | **13** | **28** | 5 | 14 | **21** | 10 | 8 |
| 기각 절감율 | 41.1% | 10.0% | 51.1% | 78.9% | 23.3% | 61.1% | 70.0% | 55.6% | 52.2% |
| 기각 정밀도 | 79.2% | 54.3% | 73.3% | 95.6% | 76.2% | 91.1% | 93.3% | 88.9% | 86.7% |

## 임계값별 스윕 (FN = 유효 신고를 기각하는 오판)

| 임계값 | Jev | Solar Decide | Kev 4B | Mercury free | Tev1 4B | Liquid D1 | Clef Flash | Clef | PPLX Decider |
|---|---|---|---|---|---|---|---|---|---|
| 0.2 | 0 / 8.9% | 0 / 1.1% | 0 / 4.4% | 25 / 73.3% | 0 / 1.1% | 5 / 47.8% | 4 / 40.0% | 2 / 28.9% | 1 / 18.9% |
| 0.3 | 1 / 20.0% | 0 / 5.6% | 4 / 21.1% | 26 / 76.7% | 2 / 8.9% | 7 / 52.2% | 13 / 55.6% | 4 / 43.3% | 2 / 33.3% |
| 0.4 | 1 / 32.2% | 0 / 7.8% | 8 / 38.9% | 28 / 78.9% | 2 / 14.4% | 10 / 55.6% | 19 / 66.7% | 9 / 52.2% | 6 / 44.4% |
| 0.5 | 3 / 41.1% | 1 / 10.0% | 13 / 51.1% | 28 / 78.9% | 5 / 23.3% | 14 / 61.1% | 21 / 70.0% | 10 / 55.6% | 8 / 52.2% |
| 0.7 | 18 / 66.7% | 1 / 16.7% | 34 / 86.7% | 29 / 81.1% | 13 / 51.1% | 22 / 72.2% | 28 / 80.0% | 16 / 65.6% | 25 / 74.4% |

## 모델별 분석

### Jev — FN-절감 경선 1위 (유지)
FN 3건으로 41.1% 절감은 여전히 최고 수준. 정확도 83.3%는 Clef과 동률, PPLX에 1.1%p 뒤짐.
지연 p50 0.24초로 최속. 임계값 조절로 FN 0건(0.2)까지 가능한 유일한 모델.

### PPLX Decider — 정확도 1위, Jev와 사실상 동급 진입
정확도 84.4%로 9개 모델 중 1위(실데이터에서 Jev를 앞선 첫 사례). 요금 최저부대($0.04/M),
지연도 Jev급(0.32초). 다만 FN-절감 경선은 Jev와 사실상 동일: Jev FN 1건/20.0% vs PPLX
FN 1건/18.9%, Jev FN 3건/41.1% vs PPLX FN 6건/44.4%. 0.5 기준 FN은 8건으로 Jev(3건)보다
많아, FN 허용 한도를 넓게 잡는다면 Jev의 대안이 될 수 있는 유일한 모델.

### Clef — 보정 1위, Jev와 정확도 동률 (단, 비용 6배)
정확도 83.3%로 Jev와 동률, Brier 0.237/ECE 0.054는 전 모델 중 최고. sexual 9/9 완판.
다만 FN-절감 경선 역시 Jev에 근소하게 밀리고(0.2 기준 FN 2/28.9% vs Jev FN 1/32.2%),
입력 단가 $0.24/M로 Jev의 6배, 지연도 2배. 비용 대비 Jev 우위.

### Liquid D1 — 3위
정확도 80.0%, ECE 0.068, 단가 최저부대($0.04/M). FN-절감 경선은 Jev 하위.
기각을 공격적으로 쓰고 FN을 감수할 경우의 차선.

### Clef Flash — 부적합
정확도 73.3%. 0.5 기준 FN 21건(유효의 46.7%) — Clef과 달리 한국어 실데이터 판별력 부족.
0.2 기준에서도 FN 4건에 기각 40%로 균형이 나쁨.

### Solar Decide / Kev 4B / Mercury Decide free / Tev1 4B — 부적합 (이전 결론 유지)
Solar 57.8%(기준선 수준) · Kev 72.2%(FN 13건, 2.45초) · Mercury 66.7%(FN 28건) ·
Tev1 63.3%(전 구간 Jev 하위). 상세는 이전 버전 기록 및 아래 표 참고.

## 공통 관찰

- 실제 신고 사례는 공개 합성 코호트보다 훨씬 어려움 (Jev: 합성 98.6% → 실데이터 83.3%).
- 확률 보정(ECE)이 좋아도 분류 분리가 안 되면 사전검사로 쓸 수 없음 (Kev 4B 사례).
- 기각 절감율과 FN은 강한 트레이드오프 관계이며, 모델 선택 시 FN 허용 한도가 기준이 되어야 함.
- 최근 출시된 대형 decide 모델(Clef, PPLX Decider)이 처음으로 Jev에 근접/동률을 기록.
  특히 PPLX Decider는 정확도 1위에 최저 요금부대로, Jev 대비 FN 여유가 있다면 교체 고려 대상.
- 4B급 오픈 실험 모델(kev-4b, tev1)과 무료/1세대 decide 변형(solar-decide, mercury free)은
  여전히 실데이터 정확도가 10~25%p 낮음.

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
