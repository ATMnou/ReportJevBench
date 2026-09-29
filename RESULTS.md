# 신고 유효성 사전검사 벤치마크 결과 (Jev / Solar Decide / Kev 4B)

- 데이터: `data.txt` 실제 신고 사례 90건 (유효 45 / 무효 45, 운영자 수동 판정)
- 데이터셋: `report-validity-public.jsonl` (JevBench noul 형식, 프로덕션 사전검사 프롬프트와 동일)
- 하네스: jevbench v1.2 순정 (typesafe 어댑터, OpenRouter Decisions 라우터)
- 실행일: 2026-09-29 / 90건씩 0 실패, 스키마 유효 100%
- 실행 비용: Jev $0.0028 · Solar Decide $0.0036 · Kev 4B $0.0017
- 결과 원본: `C:\Users\gambit\Desktop\BACKEND\jevbench-runs\report-jev` / `report-solar-decide` / `report-kev-4b`
- 재생성: `python build_dataset.py` (data.txt → report-validity-public.jsonl)

## 모델별 해석 ID 및 요금

| 모델 | 요청 슬러그 | 해석 ID | 요금 |
|---|---|---|---|
| Jev | `~typesafe/jev-latest` | `typesafe/jev-1.13-20260917` | $0.042/M in, $0 out |
| Solar Decide | `upstage/solar-decide` | `upstage/solar-decide-20260928` | $0.05/M in, $0 out |
| Kev 4B | `jaredpalmer/kev-4b` | `jaredpalmer/kev-4b-20260924` | $0.042/M in, $0 out |

## 헤드라인 지표

| 지표 | Jev | Solar Decide | Kev 4B | 다수 클래스 기준선 |
|---|---|---|---|---|
| 정확도 | **83.3%** (75/90) | 57.8% (52/90) | 72.2% (65/90) | 50.0% |
| Brier | 0.270 | 0.642 | 0.386 | — |
| ECE | 0.100 | 0.299 | 0.069 | — |
| 지연 p50 / p95 | **0.24초 / 0.36초** | 0.37초 / 0.62초 | 2.45초 / 5.39초 | — |
| 카테고리별 | other 34/41 · swearing 27/33 · sexual 7/9 · griefing 7/7 | other 26/41 · swearing 21/33 · sexual 3/9 · griefing 2/7 | other 26/41 · swearing 25/33 · sexual 7/9 · griefing 7/7 | — |

## 운영 임계값 0.5 기준 혼동 행렬 (프로덕션 설정과 동일)

| | Jev | Solar Decide | Kev 4B |
|---|---|---|---|
| 유효 신고 정확 판정 (TP) | 42 | 44 | 32 |
| 무효 신고 → LLM 통과 (FP, 낭비) | 11 | 37 | 12 |
| 무효 신고 정확 기각 (TN, 절감) | **34** | 8 | 33 |
| **유효 신고 → 기각 사고 (FN, 허위처분)** | **3** | 1 | **13** |
| LLM 도달률 (절감 효과) | 58.9% (41.1% 절감) | 90.0% (10.0% 절감) | 48.9% (51.1% 절감) |
| 기각 정밀도 | 79.2% | 54.3% | 73.3% |

## 임계값별 안전도 (FN = 유효 신고자가 허위 신고 처분을 받는 사고)

| 임계값 | Jev FN / 기각율 | Solar Decide FN / 기각율 | Kev 4B FN / 기각율 |
|---|---|---|---|
| 0.2 | 0 / 8.9% | 0 / 1.1% | 0 / 4.4% |
| 0.3 | 1 / 20.0% | 0 / 5.6% | 4 / 21.1% |
| 0.4 | 1 / 32.2% | 0 / 7.8% | 8 / 38.9% |
| 0.5 (현재) | 3 / 41.1% | 1 / 10.0% | 13 / 51.1% |
| 0.7 | 18 / 66.7% | 1 / 16.7% | 34 / 86.7% |

## 결론

1. **Solar Decide 확정 기각**: 정확도 57.8%는 50% 기준선과 구분이 안 되는 수준이고, ECE 0.30으로
   확률 자체가 신뢰 불가. 임계값을 0.7까지 올려도 기각 절감이 16.7%밖에 안 됨.
   공개 코호트(57.8% vs Jev 83.3%)와 운영 사례 모두 일관된 결과.
2. **Kev 4B도 부적합**: 정확도 72.2%로 Solar Decide보다는 낫지만, 프로덕션 임계값 0.5에서
   FN이 13건(유효 신고의 28.9%) — 정상 유저 밴 사고가 실용적으로 감당 불가.
   확률이 중간대(0.2~0.5)에 몰려 분리가 안 되며(0.2로 낮춰야 FN 0, 기각 절감 4.4%),
   p50 2.45초로 Jev 대비 10배 느려 신고 응답 지연도 문제.
   ECE 0.069로 확률 자체는 가장 잘 보정돼 있으나, 분류 경계가 흐려서 무의미.
3. **Jev 유지 권장**, 단 현재 임계값 0.5에서 유효 신고 45건 중 3건(6.7%)이 기각 사고로 빠짐.
   사고 비용(정상 유저 밴)이 LLM 절감 비용보다 크므로 **0.4로 낮추는 것 권장**
   (FN 3→1, 기각 절감 41.1%→32.2%). 더 안전하게는 0.3 (FN 1, 절감 20%).
4. 실제 신고 사례는 공개 합성 코호트보다 훨씬 어려움 (Jev 98.6% → 83.3%).
   노이즈 원인: 근거 없는 신고 사유, 매우 짧은 로그, 판단이 애매한 경계 사례.

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
