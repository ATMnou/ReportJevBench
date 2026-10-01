# 신고 유효성 벤치마크 결과 (Jev / Solar Decide / Kev 4B / Mercury Decide free)

- 데이터: `data.txt` 실제 신고 사례 90건 (유효 45 / 무효 45, 사람 판정)
- 데이터셋: `report-validity-public.jsonl` (JevBench noul 형식, 사전검사형 프롬프트)
- 하네스: jevbench v1.2 순정 (typesafe 어댑터, OpenRouter Decisions 라우터)
- 실행일: 2026-09-29~30 / 90건씩 0 실패, 스키마 유효 100%
- 실행 비용: Jev $0.0028 · Solar Decide $0.0036 · Kev 4B $0.0017 · Mercury Decide free $0
- 결과 원본: `C:\Users\gambit\Desktop\BACKEND\jevbench-runs\report-jev` / `report-solar-decide` / `report-kev-4b` / `report-mercury-decide-free`
- 재생성: `python build_dataset.py` (data.txt → report-validity-public.jsonl)

## 모델별 해석 ID 및 요금

| 모델 | 요청 슬러그 | 해석 ID | 요금 |
|---|---|---|---|
| Jev | `~typesafe/jev-latest` | `typesafe/jev-1.13-20260917` | $0.042/M in, $0 out |
| Solar Decide | `upstage/solar-decide` | `upstage/solar-decide-20260928` | $0.05/M in, $0 out |
| Kev 4B | `jaredpalmer/kev-4b` | `jaredpalmer/kev-4b-20260924` | $0.042/M in, $0 out |
| Mercury Decide (free) | `inception/mercury-decide:free` | `inception/mercury-decide-20260930` | 무료 |

## 헤드라인 지표

| 지표 | Jev | Solar Decide | Kev 4B | Mercury Decide free |
|---|---|---|---|---|
| 정확도 | **83.3%** (75/90) | 57.8% (52/90) | 72.2% (65/90) | 66.7% (60/90) |
| Brier | **0.270** | 0.642 | 0.386 | 0.551 |
| ECE | 0.100 | 0.299 | **0.069** | 0.286 |
| 지연 p50 / p95 | **0.24초 / 0.36초** | 0.37초 / 0.62초 | 2.45초 / 5.39초 | 0.31초 / 0.37초 |
| 카테고리별 | other 34/41 · swearing 27/33 · sexual 7/9 · griefing 7/7 | other 26/41 · swearing 21/33 · sexual 3/9 · griefing 2/7 | other 26/41 · swearing 25/33 · sexual 7/9 · griefing 7/7 | other 29/41 · swearing 18/33 · sexual 7/9 · griefing 6/7 |

## 임계값 0.5 기준 혼동 행렬

| | Jev | Solar Decide | Kev 4B | Mercury Decide free |
|---|---|---|---|---|
| 유효 신고 정확 판정 (TP) | 42 | 44 | 32 | 17 |
| 무효 신고 → 통과 오판 (FP) | 11 | 37 | 12 | 2 |
| 무효 신고 정확 기각 (TN) | **34** | 8 | 33 | 43 |
| **유효 신고 → 기각 오판 (FN)** | **3** | 1 | **13** | **28** |
| 기각 절감율 | 41.1% | 10.0% | 51.1% | 78.9% |
| 기각 정밀도 | 79.2% | 54.3% | 73.3% | 95.6% |

## 임계값별 스윕 (FN = 유효 신고를 기각하는 오판)

| 임계값 | Jev FN / 기각율 | Solar Decide FN / 기각율 | Kev 4B FN / 기각율 | Mercury free FN / 기각율 |
|---|---|---|---|---|
| 0.2 | 0 / 8.9% | 0 / 1.1% | 0 / 4.4% | 25 / 73.3% |
| 0.3 | 1 / 20.0% | 0 / 5.6% | 4 / 21.1% | 26 / 76.7% |
| 0.4 | 1 / 32.2% | 0 / 7.8% | 8 / 38.9% | 28 / 78.9% |
| 0.5 | 3 / 41.1% | 1 / 10.0% | 13 / 51.1% | 28 / 78.9% |
| 0.7 | 18 / 66.7% | 1 / 16.7% | 34 / 86.7% | 29 / 81.1% |

## 모델별 분석

### Jev — 종합 1위
정확도 83.3%로 가장 높고, FN 3건을 유지하면서 41%의 기각 절감을 달성한 유일한 모델.
임계값을 낮추면 FN 1건(0.4) 또는 0건(0.2)까지 줄일 수 있어 안전도-절감 트레이드오프 조절이 가능한
유일한 후보. 지연도 가장 빠름 (p50 0.24초).

### Solar Decide — 부적합
정확도 57.8%는 50% 기준선과 구분이 안 되는 수준. ECE 0.30으로 확률 자체가 신뢰 불가.
기각을 거의 시도하지 않아(0.5 기준 10% 절감) 사전검사 용도로 가치가 없음.

### Kev 4B — 부적합
정확도 72.2%이지만 확률이 중간대(0.2~0.5)에 몰려 유효/무효 분리가 안 됨.
0.5 기준 FN 13건(유효의 28.9%), 0.2로 내려야 FN 0이지만 기각 절감 4.4%에 그침.
p50 2.45초로 4개 모델 중 가장 느림. ECE 0.069로 확률 보정은 좋으나 분류 경계가 흐려 무의미.

### Mercury Decide free — 부적합
무료이고 빠르지만(p50 0.31초) 극단적 보수 성향: 유효 신고 45건 중 28건을 기각 오판.
임계값 0.2까지 내려도 FN 25건. swearing 카테고리 18/33으로 한국어 은어 우회 표현에 특히 약함.
정확도 66.7%는 대부분 무효 라벨 정답에서 나온 것.

## 공통 관찰

- 실제 신고 사례는 공개 합성 코호트보다 훨씬 어려움 (Jev: 합성 98.6% → 실데이터 83.3%).
  원인: 근거가 없거나 모호한 신고 사유, 짧은 로그, 경계 사례.
- 확률 보정(ECE)이 좋아도 분류 분리가 안 되면 사전검사로 쓸 수 없음 (Kev 4B 사례).
- 기각 절감율과 FN은 강한 트레이드오프 관계이며, 모델 선택 시 FN 허용 한도가 기준이 되어야 함.

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
