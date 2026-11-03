#!/usr/bin/env python3
"""Calculate descriptive creative metrics from local CSV; no model or network calls."""
import argparse
import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

HEADERS = {
    "素材id": "creative_id", "素材编号": "creative_id",
    "曝光": "impressions", "展现": "impressions", "展现量": "impressions",
    "点击": "clicks", "点击量": "clicks", "花费": "spend", "消耗": "spend",
    "转化事件": "conversion_event", "转化数": "conversions",
    "分母事件": "conversion_base_event", "分母计数": "conversion_base_count",
    "归因窗口": "attribution_window", "渠道": "channel", "人群": "audience",
    "日期": "period", "位置": "placement",
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
    if name != "spend" and value != value.to_integral_value():
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
                converted = parse_value(row.get("conversions", ""), "conversions")
                conversion_base = parse_value(row.get("conversion_base_count", ""), "conversion_base_count")
            except ValueError as exc:
                raise ValueError(f"Line {line}: {exc}") from None
            notes = []
            if identity in seen:
                notes.append("Repeated creative_id; rows remain separate. Verify date, version and context.")
            seen.add(identity)
            if exposed is not None and clicked is not None and clicked > exposed:
                notes.append("Clicks exceed impressions; verify event definitions and units.")
            conversion_event = row.get("conversion_event", "").strip()
            base_event = row.get("conversion_base_event", "").strip()
            has_conversion_data = any(row.get(field, "").strip() for field in (
                "conversion_event", "conversions", "conversion_base_event", "conversion_base_count"))
            defined_conversion = bool(conversion_event) and converted is not None
            defined_ratio = defined_conversion and bool(base_event) and conversion_base is not None
            if has_conversion_data and not defined_ratio:
                notes.append("Conversion rate unavailable: provide both event names and raw counts.")
            if defined_ratio and converted > conversion_base:
                notes.append("Conversions exceed the stated denominator; verify units and repeat events.")
            try:
                ctr = float(clicked / exposed * 100) if clicked is not None and exposed else None
                cpc = float(spent / clicked) if spent is not None and clicked else None
                conversion_rate = float(converted / conversion_base * 100) if defined_ratio and conversion_base else None
                cost_per_conversion = float(spent / converted) if defined_conversion and spent is not None and converted else None
            except (InvalidOperation, OverflowError):
                raise ValueError(f"Line {line}: numeric range is not supported") from None
            for result in (ctr, cpc, conversion_rate, cost_per_conversion):
                if result is not None and (result == float("inf") or result != result):
                    raise ValueError(f"Line {line}: result is not finite")
            results.append({
                "source_line": line,
                "creative_id": identity,
                "ctr_pct": round(ctr, 6) if ctr is not None else None,
                "cpc": round(cpc, 6) if cpc is not None else None,
                "conversion_event": conversion_event or None,
                "conversion_base_event": base_event or None,
                "conversion_rate_pct": round(conversion_rate, 6) if conversion_rate is not None else None,
                "cost_per_conversion": round(cost_per_conversion, 6) if cost_per_conversion is not None else None,
                "context": {key: row[key].strip() for key in ("channel", "placement", "audience", "period", "attribution_window") if row.get(key, "").strip()},
                "notes": notes,
            })
    return {
        "kind": "descriptive_metrics",
        "rows": results,
        "note": "Rates are percentages; costs use the input spend currency. Conversion metrics retain the user-declared event definitions. Missing/zero denominators yield null. Supplied rate columns are not used. No aggregation, winner selection or causal analysis is performed.",
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
