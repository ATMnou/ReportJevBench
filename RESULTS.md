# 신고 유효성 벤치마크 결과 (14개 모델)

- 데이터: `data.txt` 실제 신고 사례 90건 (유효 45 / 무효 45, 사람 판정)
- 데이터셋: `report-validity-public.jsonl` (JevBench noul 형식, 사전검사형 프롬프트)
- 하네스: jevbench v1.2 순정 (typesafe 어댑터, OpenRouter Decisions 라우터)
- 실행일: 2026-09-29~10-14 / 90건씩 0 실패, 스키마 유효 100%
- 실행 비용: Jev $0.0028 · Solar Decide $0.0036 · Kev 4B $0.0017 · Mercury free $0 · Tev1 4B $0.0019 · Liquid D1 $0.0017 · Clef Flash $0.0044 · Clef $0.0118 · PPLX Decider $0.0018 · GPT-6 Luna $0.0049 · Clef Omni $0.0076 · PPLX Decider v1.1 $0.0009 · MS Decision-1 $0.0017 · DREX v2.0 $0.0024 · Jev 1.14 $0.0028
- 결과 원본: `C:\Users\gambit\Desktop\BACKEND\jevbench-runs\` 아래 각 `report-*` 디렉터리
- 재생성: `python build_dataset.py` (data.txt → report-validity-public.jsonl)
- 미측정: `scaledown/classify-1` — state 형식 제약(문자열/{text,document} 전용)으로 제외

## 모델별 해석 ID 및 요금 (정확도 순)

| 모델 | 요청 슬러그 | 해석 ID | 요금 |
|---|---|---|---|
| GPT-6 Luna Decisions | `openai/gpt-6-luna-decisions` | `openai/gpt-6-luna-decisions-20261006` | $0.10/M in, $0 out |
| PPLX Decider v1.1 | `perplexity/pplx-decider-v1.1-27b` | `perplexity/pplx-decider-v1.1-27b-20261006` | $0.02/M in, $0 out |
| PPLX Decider | `perplexity/pplx-decider-v1-27b` | `perplexity/pplx-decider-v1-27b-20261001` | $0.04/M in, $0 out |
| Jev 1.13 | `~typesafe/jev-latest` | `typesafe/jev-1.13-20260917` | $0.042/M in, $0 out |
| Clef | `cloudflare/clef` | `cloudflare/clef` | $0.24/M in, $0 out |
| Liquid D1 | `liquid/d1` | `liquid/d1-20260930` | $0.04/M in, $0 out |
| MS Decision-1 | `microsoft/microsoft-decision-1` | `microsoft/microsoft-decision-1-20261009` | $0.042/M in, $0 out |
| Jev 1.14 | `typesafe/jev-1.14` | `typesafe/jev-1.14-20261014` | $0.042/M in, $0 out |
| Clef Omni | `cloudflare/clef-omni` | `cloudflare/clef-omni-20261009` | $0.15/M in, $0 out |
| Clef Flash | `cloudflare/clef-flash` | `cloudflare/clef-flash` | $0.09/M in, $0 out |
| Kev 4B | `jaredpalmer/kev-4b` | `jaredpalmer/kev-4b-20260924` | $0.042/M in, $0 out |
| DREX v2.0 | `nace-ai/drex-v2.0` | `nace-ai/drex-v2.0-20261009` | $0.06/M in, $0 out |
| Mercury Decide (free) | `inception/mercury-decide:free` | `inception/mercury-decide-20260930` | 무료 |
| Tev1 4B | `togethercomputer/tev1-4b-experimental` | `togethercomputer/tev1-4b-experimental-20260923` | $0.042/M in, $0 out |
| Solar Decide | `upstage/solar-decide` | `upstage/solar-decide-20260928` | $0.05/M in, $0 out |

## 헤드라인 지표 (정확도 순)

| 지표 | GPT-6 Luna | PPLX v1.1 | PPLX v1 | Jev 1.13 | Clef | Liquid D1 | MS Decision-1 | Jev 1.14 | Clef Omni | Clef Flash | Kev 4B | DREX v2.0 | Mercury free | Tev1 4B | Solar Decide |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 정확도 | **90.0%** | 88.9% | 84.4% | 83.3% | 83.3% | 80.0% | 76.7% | 82.2% | 74.4% | 73.3% | 72.2% | 71.1% | 66.7% | 63.3% | 57.8% |
| Brier | **0.174** | 0.220 | 0.275 | 0.270 | 0.237 | 0.280 | 0.321 | 0.266 | 0.338 | 0.347 | 0.386 | 0.390 | 0.551 | 0.460 | 0.642 |
| ECE | 0.112 | 0.068 | 0.101 | 0.100 | 0.054 | 0.068 | 0.077 | **0.057** | 0.069 | 0.104 | 0.069 | 0.128 | 0.286 | 0.111 | 0.299 |
| 지연 p50 | 0.70초 | 0.53초 | 0.32초 | **0.24초** | 0.52초 | 0.39초 | 0.65초 | 0.40초 | 0.34초 | 0.31초 | 2.45초 | 0.83초 | 0.31초 | 0.26초 | 0.37초 |
| 카테고리별 | other 37/41 · swearing 28/33 · sexual 9/9 · griefing 7/7 | other 35/41 · swearing 29/33 · sexual 9/9 · griefing 7/7 | other 34/41 · swearing 27/33 · sexual 8/9 · griefing 7/7 | other 34/41 · swearing 27/33 · sexual 7/9 · griefing 7/7 | other 34/41 · swearing 25/33 · sexual 9/9 · griefing 7/7 | other 30/41 · swearing 26/33 · sexual 9/9 · griefing 7/7 | other 31/41 · swearing 26/33 · sexual 7/9 · griefing 5/7 | other 34/41 · swearing 26/33 · sexual 8/9 · griefing 6/7 | other 28/41 · swearing 24/33 · sexual 8/9 · griefing 7/7 | other 30/41 · swearing 22/33 · sexual 7/9 · griefing 7/7 | other 26/41 · swearing 25/33 · sexual 7/9 · griefing 7/7 | other 28/41 · swearing 21/33 · sexual 8/9 · griefing 7/7 | other 29/41 · swearing 18/33 · sexual 7/9 · griefing 6/7 | other 22/41 · swearing 22/33 · sexual 7/9 · griefing 6/7 | other 26/41 · swearing 21/33 · sexual 3/9 · griefing 2/7 |

## 임계값 0.5 기준 혼동 행렬 (정확도 순)

| | GPT-6 Luna | PPLX v1.1 | PPLX v1 | Jev 1.13 | Clef | Liquid D1 | MS Decision-1 | Jev 1.14 | Clef Omni | Clef Flash | Kev 4B | DREX v2.0 | Mercury free | Tev1 4B | Solar Decide |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 유효 신고 정확 판정 (TP) | 37 | 37 | 37 | 42 | 35 | 31 | 36 | 44 | 24 | 24 | 32 | 21 | 17 | 40 | 44 |
| 무효 신고 → 통과 오판 (FP) | 1 | 2 | 6 | 11 | 5 | 4 | 12 | 15 | 2 | 3 | 12 | 2 | 2 | 29 | 37 |
| 무효 신고 정확 기각 (TN) | 44 | 43 | 39 | 34 | 40 | 41 | 33 | 30 | 43 | 42 | 33 | 43 | 43 | 16 | 8 |
| **유효 신고 → 기각 오판 (FN)** | 8 | 8 | 8 | **3** | 10 | 14 | 9 | 1 | **21** | **21** | 13 | **24** | **28** | 5 | 1 |
| 기각 절감율 | 57.8% | 56.7% | 52.2% | 41.1% | 55.6% | 61.1% | 46.7% | 34.4% | 71.1% | 70.0% | 51.1% | 74.4% | 78.9% | 23.3% | 10.0% |
| 기각 정밀도 | 84.6% | 84.3% | 86.7% | 79.2% | 88.9% | 91.1% | 78.6% | 96.8% | 67.2% | 93.3% | 73.3% | 64.2% | 95.6% | 76.2% | 54.3% |

## 임계값별 스윕 (FN = 유효 신고를 기각하는 오판)

| 임계값 | GPT-6 Luna | PPLX v1.1 | PPLX v1 | Jev 1.13 | Clef | Liquid D1 | MS Decision-1 | Jev 1.14 | Clef Omni | Clef Flash | Kev 4B | DREX v2.0 | Mercury free | Tev1 4B | Solar Decide |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.2 | 0 / 33.3% | 3 / 34.4% | 1 / 18.9% | 0 / 8.9% | 2 / 28.9% | 5 / 47.8% | 3 / 31.1% | 1 / 10.0% | 6 / 42.2% | 4 / 40.0% | 0 / 4.4% | 10 / 54.4% | 25 / 73.3% | 0 / 1.1% | 0 / 1.1% |
| 0.3 | 2 / 40.0% | 6 / 41.1% | 2 / 33.3% | 1 / 20.0% | 4 / 43.3% | 7 / 52.2% | 5 / 40.0% | 1 / 21.1% | 13 / 53.3% | 13 / 55.6% | 4 / 21.1% | 16 / 63.3% | 26 / 76.7% | 2 / 8.9% | 0 / 5.6% |
| 0.4 | 4 / 51.1% | 8 / 51.1% | 6 / 44.4% | 1 / 32.2% | 9 / 52.2% | 10 / 55.6% | 5 / 42.2% | 1 / 27.8% | 16 / 61.1% | 19 / 66.7% | 8 / 38.9% | 20 / 70.0% | 28 / 78.9% | 2 / 14.4% | 0 / 7.8% |
| 0.5 | 8 / 57.8% | 8 / 56.7% | 8 / 52.2% | 3 / 41.1% | 10 / 55.6% | 14 / 61.1% | 9 / 46.7% | 1 / 34.4% | 21 / 71.1% | 21 / 70.0% | 13 / 51.1% | 24 / 74.4% | 28 / 78.9% | 5 / 23.3% | 1 / 10.0% |
| 0.7 | 17 / 68.9% | 16 / 67.8% | 25 / 74.4% | 18 / 66.7% | 16 / 65.6% | 22 / 72.2% | 16 / 60.0% | 6 / 47.8% | 28 / 80.0% | 28 / 80.0% | 34 / 86.7% | 34 / 85.6% | 29 / 81.1% | 13 / 51.1% | 1 / 16.7% |

## 모델별 분석

### GPT-6 Luna Decisions — 1위
정확도 90.0%(1위), Brier 0.174(1위), FP 1건. FN-절감 안전 구간 지배: FN 0건에 기각 33.3%
(Jev는 FN 0이면 8.9% 한계), FN 2건에 40.0%. 대가는 요금 2.4배($0.10/M)와 p50 0.70초.
FN 8건(0.5)이 부담이면 0.2~0.3 운영 권장.

### PPLX Decider v1.1 — 2위, 가성비 1위
88.9%로 v1(84.4%) 대비 +4.5%p, 요금은 절반($0.02/M — 전체 최저). 같은 FN에서 v1보다
절감이 항상 높아 v1 완전 대체. Luna 대비 정확도 -1.1%p, 요금 1/5.

### Jev 1.13 — 3위, FN 최소 기록 보유
FN 3건/41.1% 절감, FN 0건 운영 가능(0.2). p50 0.24초 최속.

### Jev 1.14 — 신규. 1.13과 사실상 동급, 그러나 이 워크로드에서는 업그레이드 아님
정확도 82.2%(1.13 대비 -1.1%p), ECE 0.057로 보정은 개선. FN 곡선이 0.2~0.5 전 구간에서
1건으로 매우 안정적(1.13은 0→3건 상승)이고 기각 정밀도 96.8%로 최상위. 다만 같은 FN에서
절감이 1.13보다 낮고(1건: 34.4% vs 1.13 32.2%는 근소 우위나, 1.13은 FN 0/8.9%와 3건/41.1%
구간이 존재), 정확도도 근소 열세. 1.13 유지 권장 — 1.14는 FN을 1건으로 고정하고 싶을 때의 대안.

### Clef — 5위
83.3%(Jev 동률), Brier/ECE 최상위권. FN 10건, 단가 $0.24/M(6배), p50 0.52초. 비용 대비 열세.

### MS Decision-1 — 신규. 중위권 (기대 이하)
76.7%, FN 9건/46.7% 절감. ECE 0.077로 보정은 준수하고 지연도 양호(0.65초)하나,
같은 요금대($0.042/M)에서 Jev 1.13(83.3%, FN 3건/41.1%)에 전 항목 밀림.

### DREX v2.0 — 신규. 부적합
71.1%에 FN 24건/기각 74.4% — Mercury free와 같은 극단적 보수 패턴. 0.2로 내려도 FN 10건.
요금도 $0.06/M으로 비쌈.

### 나머지 — 부적합 (이전 결론 유지)
Liquid D1 80.0%(FN 14건) · Clef Omni 74.4%(FN 21건) · Clef Flash 73.3%(FN 21건) ·
Kev 4B 72.2%(FN 13건, p50 2.45초) · Mercury free 66.7%(FN 28건) · Tev1 63.3%(전 구간 하위) ·
Solar Decide 57.8%(기준선 수준).

## 공통 관찰

- 실제 신고 사례는 공개 합성 코호트보다 훨씬 어려움 (Jev 1.13: 합성 98.6% → 실데이터 83.3%).
  유일한 예외는 GPT-6 Luna(90.0%), PPLX v1.1(88.9%) — 최신 대형 decide 모델과 실데이터 격차가 줄어드는 추세.
- 확률 보정(ECE)이 좋아도 분류 분리가 안 되면 사전검사로 쓸 수 없음 (Kev 4B 사례).
- 기각 절감율과 FN은 강한 트레이드오프 관계이며, 모델 선택 시 FN 허용 한도가 기준이 되어야 함.
- 버전 업그레이드가 항상 개선을 보장하지 않음: PPLX v1→v1.1은 명확한 개선(+4.5%p, 절감 +4.5%p),
  Jev 1.13→1.14는 이 워크로드에서 근소 열세(정확도 -1.1%p, 저 FN 절감 하락). 마이그레이션 전 벤치마크 필수.
- Cloudflare Clef 계열은 플래시/옴니 변형이 모두 본체보다 FN이 많음 — 변형보다 본체 권장.

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
