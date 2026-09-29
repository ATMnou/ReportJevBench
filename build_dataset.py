# -*- coding: utf-8 -*-
"""Build a JevBench-format public dataset from production report cases (data.txt).

Input format (data.txt), blocks separated by a lone case number line:
    <case number>
    사유: <report reason>
    채팅 로그:
    <timestamped log lines...>
    정답: 유효|무효

Output: report-validity-public.jsonl — one noul task per case. The state and
question mirror the production prescreen call in SOLIS solis.js exactly
(state = {report_reason, chat_logs}, same instructions and criteria), so the
benchmark measures the same decision the live system makes.
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "data.txt"
OUT = HERE / "report-validity-public.jsonl"

INSTRUCTIONS = (
    "Does chat_logs contain messages violating Roblox community rules "
    "(swearing, spamming, sexual or inappropriate content, racism)? "
    "Treat report_reason only as a hint. Korean slang may be masked with "
    "numbers or English letters (ex: ㅂ1ㅈ)."
)
CRITERIA = {
    "true": "At least one message in chat_logs violates Roblox community rules.",
    "false": "Every message in chat_logs is normal or innocent - the report is false.",
}

FAMILY_RULES = [
    ("sexual", ("성적", "신음", "부적절", "헌팅", "여미새")),
    ("swearing", ("욕", "패드립", "비방", "비난", "심한말", "防")),
    ("griefing", ("테러", "방해", "노이즈", "freeze", "스팸", "예약")),
]


def family_for(reason: str) -> str:
    low = reason.lower()
    for fam, keys in FAMILY_RULES:
        if any(k.lower() in low for k in keys):
            return fam
    return "other"


def parse_blocks(text: str):
    """Return [(case_number, body_lines), ...] keyed off the lone-number headers."""
    lines = text.splitlines()
    blocks = []
    cur = None
    for line in lines:
        if re.fullmatch(r"\d+", line.strip()):
            if cur is not None:
                blocks.append(cur)
            cur = (int(line.strip()), [])
            continue
        if cur is not None:
            cur[1].append(line)
    if cur is not None:
        blocks.append(cur)
    return blocks


def main() -> int:
    records = []
    problems = []
    for num, block in parse_blocks(SRC.read_text(encoding="utf-8")):
        reason = None
        logs = []
        expected = None
        in_logs = False
        for raw in block:
            line = raw.rstrip()
            if line.startswith("사유:") and reason is None:
                reason = line[len("사유:"):].strip()
                continue
            if line.strip() == "채팅 로그:":
                in_logs = True
                continue
            if line.startswith("정답:"):
                expected = line[len("정답:"):].strip()
                in_logs = False
                continue
            if in_logs and line.strip():
                logs.append(line)
        if reason is None or expected is None or not logs:
            problems.append((num, block[:2]))
            continue
        records.append({
            "num": num,
            "reason": reason,
            "logs": logs,
            "expected": "yes" if expected.startswith("유효") else "no",
        })

    if problems:
        print(f"warning: {len(problems)} blocks skipped: {[p[0] for p in problems]}", file=sys.stderr)

    with OUT.open("w", encoding="utf-8") as fh:
        for rec in records:
            task = {
                "id": f"report-validity-{rec['num']:03d}",
                "family": family_for(rec["reason"]),
                "group": None,
                "state": {
                    "report_reason": rec["reason"],
                    "chat_logs": "채팅 로그:\n" + "\n".join(rec["logs"]),
                },
                "question": {
                    "type": "noul",
                    "instructions": INSTRUCTIONS,
                    "criteria": CRITERIA,
                },
                "labels": ["no", "yes"],
                "expected": rec["expected"],
                "split": "public",
                "provenance": {
                    "source": "ATM STUDIO production Roblox chat reports (anonymized ids omitted)",
                    "source_id": f"data.txt case {rec['num']}",
                    "label_basis": "Human operator judgment (production moderation decision)",
                    "license": "MIT",
                    "imported_at": "2026-09-29",
                    "exclude_reason": None,
                },
            }
            fh.write(json.dumps(task, ensure_ascii=False, sort_keys=True) + "\n")

    yes = sum(1 for r in records if r["expected"] == "yes")
    print(f"wrote {len(records)} tasks -> {OUT.name}  (yes={yes}, no={len(records) - yes})")
    fams = {}
    for r in records:
        f = family_for(r["reason"])
        fams[f] = fams.get(f, 0) + 1
    print("families:", json.dumps(fams, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
