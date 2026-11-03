#!/usr/bin/env python3
"""Calculate descriptive CTR/CPC from local CSV; never calls a model or network."""
import argparse
import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

HEADERS = {
    "素材id": "creative_id", "素材编号": "creative_id",
    "曝光": "impressions", "展现": "impressions", "展现量": "impressions",
    "点击": "clicks", "点击量": "clicks", "花费": "spend", "消耗": "spend",
}


def parse_value(text, name):
    text = str(text).strip()
    if not text:
        return None
    try:
        value = Decimal(text)
    except InvalidOperation:
        raise ValueError(f"{name}: expected a raw number") from None
    if not value.is_finite() or value < 0:
        raise ValueError(f"{name}: expected a finite, non-negative number")
    if name in ("impressions", "clicks") and value != value.to_integral_value():
        raise ValueError(f"{name}: expected an integer count")
    return value


def compute_csv(path):
    results = []
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        original_headers = next(reader, None)
        if not original_headers:
            raise ValueError("CSV header is required")
        headers = [HEADERS.get(h.strip().lower(), h.strip().lower()) for h in original_headers]
        if len(headers) != len(set(headers)):
            raise ValueError("Duplicate or synonymous columns: resolve them before calculation")
        required = {"creative_id", "impressions", "clicks", "spend"}
        if not required.issubset(headers):
            raise ValueError("Required columns: creative_id, impressions, clicks, spend")
        seen = set()
        for values in reader:
            if not any(x.strip() for x in values):
                continue
            line = reader.line_num
            if len(values) != len(headers):
                raise ValueError(f"Line {line}: column count does not match the header")
            row = dict(zip(headers, values))
            identity = row["creative_id"].strip()
            if not identity:
                raise ValueError(f"Line {line}: creative_id is missing")
            try:
                exposed = parse_value(row["impressions"], "impressions")
                clicked = parse_value(row["clicks"], "clicks")
                spent = parse_value(row["spend"], "spend")
            except ValueError as exc:
                raise ValueError(f"Line {line}: {exc}") from None
            notes = []
            if identity in seen:
                notes.append("Repeated creative_id; rows remain separate. Verify date, version and context.")
            seen.add(identity)
            if exposed is not None and clicked is not None and clicked > exposed:
                notes.append("Clicks exceed impressions; verify event definitions and units.")
            try:
                ctr = float(clicked / exposed * 100) if clicked is not None and exposed else None
                cpc = float(spent / clicked) if spent is not None and clicked else None
            except (InvalidOperation, OverflowError):
                raise ValueError(f"Line {line}: numeric range is not supported") from None
            for result in (ctr, cpc):
                if result is not None and (result == float("inf") or result != result):
                    raise ValueError(f"Line {line}: result is not finite")
            results.append({
                "source_line": line,
                "creative_id": identity,
                "ctr_pct": round(ctr, 6) if ctr is not None else None,
                "cpc": round(cpc, 6) if cpc is not None else None,
                "notes": notes,
            })
    return {
        "kind": "descriptive_metrics",
        "rows": results,
        "note": "CTR is a percentage. CPC uses the input spend currency. Missing/zero denominators yield null. No purchase CVR, aggregation, winner selection or causal analysis is performed.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--output", type=Path, help="Optional new JSON file; existing files are preserved")
    args = parser.parse_args()
    try:
        report = compute_csv(args.csv_file)
        text = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8") as handle:
                handle.write(text)
        else:
            print(text, end="")
    except (OSError, ValueError, UnicodeError, csv.Error) as exc:
        parser.exit(2, f"Cannot calculate: {exc}\n")


if __name__ == "__main__":
    main()
