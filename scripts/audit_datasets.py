"""Audit review datasets and write reproducible JSON/Markdown health reports."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.sentiment_analysis.preprocessing.labels import normalize_rating, sentiment_from_rating

RATING_COLUMNS = ("stars", "rating", "امتیاز")
TEXT_COLUMNS = ("comment", "متن نظر", "text")
LABEL_COLUMNS = ("sentiment", "label")
IDENTITY_COLUMNS = ("id", "review_id")


def _first_column(fieldnames: list[str], candidates: tuple[str, ...]) -> str | None:
    return next((name for name in candidates if name in fieldnames), None)


def _normalize_text(value: str) -> str:
    """Normalize text for duplicate detection without changing source values."""
    value = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"\s+", " ", value).strip()


def audit_csv(path: Path) -> dict[str, Any]:
    """Return deterministic integrity statistics for a single review CSV."""
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    rating_column = _first_column(fieldnames, RATING_COLUMNS)
    text_column = _first_column(fieldnames, TEXT_COLUMNS)
    label_column = _first_column(fieldnames, LABEL_COLUMNS)
    identity_column = _first_column(fieldnames, IDENTITY_COLUMNS)
    rating_counts: Counter[str] = Counter()
    label_counts: Counter[str] = Counter()
    invalid_ratings = neutral_ratings = label_mismatches = invalid_labels = 0

    for row in rows:
        if rating_column:
            rating = normalize_rating(row.get(rating_column, ""))
            rating_counts[str(rating) if rating is not None else "invalid/unknown"] += 1
            if rating is None:
                invalid_ratings += 1
            elif rating == 3:
                neutral_ratings += 1
            if label_column and rating is not None:
                expected = sentiment_from_rating(rating)
                raw_label = (row.get(label_column) or "").strip()
                if expected is not None and raw_label != str(expected):
                    label_mismatches += 1

        if label_column:
            raw_label = (row.get(label_column) or "").strip()
            label_counts[raw_label or "missing"] += 1
            if raw_label not in ("", "0", "1"):
                invalid_labels += 1

    missing_by_column = {
        key: sum(not (row.get(key) or "").strip() for row in rows)
        for key in fieldnames
    }
    exact_duplicates = len(rows) - len({tuple(row.get(key) or "" for key in fieldnames) for row in rows})
    normalized_texts = [
        _normalize_text(row.get(text_column) or "")
        for row in rows
        if text_column and _normalize_text(row.get(text_column) or "")
    ]
    text_duplicates = len(normalized_texts) - len(set(normalized_texts))
    identity_values = [
        (row.get(identity_column) or "").strip()
        for row in rows
        if identity_column and (row.get(identity_column) or "").strip()
    ]
    duplicate_ids = len(identity_values) - len(set(identity_values))
    replacement_characters = sum(
        (row.get(key) or "").count("\ufffd") for row in rows for key in fieldnames
    )
    malformed_rows = sum(None in row for row in rows)
    missing_review_text = missing_by_column.get(text_column, 0) if text_column else None

    issues = []
    if missing_review_text:
        issues.append("missing_review_text")
    if exact_duplicates or text_duplicates or duplicate_ids:
        issues.append("duplicate_records_or_text")
    if invalid_ratings:
        issues.append("invalid_or_missing_ratings")
    if label_mismatches or invalid_labels:
        issues.append("invalid_or_inconsistent_labels")
    if replacement_characters:
        issues.append("encoding_replacement_characters")
    if malformed_rows:
        issues.append("malformed_csv_rows")

    return {
        "file": path.as_posix(),
        "rows": len(rows),
        "columns": fieldnames,
        "exact_duplicates": exact_duplicates,
        "duplicate_ids": duplicate_ids,
        "normalized_text_duplicates": text_duplicates,
        "missing_by_column": missing_by_column,
        "rating_column": rating_column,
        "rating_distribution": dict(sorted(rating_counts.items())),
        "invalid_or_missing_ratings": invalid_ratings,
        "neutral_three_star_ratings": neutral_ratings,
        "label_column": label_column,
        "label_distribution": dict(sorted(label_counts.items())),
        "invalid_labels": invalid_labels,
        "rating_label_mismatches": label_mismatches,
        "missing_review_text": missing_review_text,
        "encoding_replacement_characters": replacement_characters,
        "malformed_rows": malformed_rows,
        "issues": issues,
        "status": "needs_attention" if issues else "healthy",
    }


def _markdown_report(reports: list[dict[str, Any]]) -> str:
    lines = [
        "# Dataset Health Report",
        "",
        "Generated by `python scripts/audit_datasets.py`.",
        "Source CSV files are audited read-only; repeated text is reported, not deleted automatically.",
        "",
        "| Dataset | Rows | Exact duplicates | Repeated text | Missing text | Invalid ratings | 3-star | Label mismatches | Status |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for report in reports:
        name = Path(report["file"]).parent.name + "/" + Path(report["file"]).name
        lines.append(
            f"| `{name}` | {report['rows']} | {report['exact_duplicates']} | "
            f"{report['normalized_text_duplicates']} | {report['missing_review_text']} | "
            f"{report['invalid_or_missing_ratings']} | {report['neutral_three_star_ratings']} | "
            f"{report['rating_label_mismatches']} | {report['status']} |"
        )
    for report in reports:
        lines.extend(("", f"## `{report['file']}`", "", f"- Issues: {', '.join(report['issues']) or 'none'}"))
        lines.append(f"- Rating distribution: `{json.dumps(report['rating_distribution'], ensure_ascii=False)}`")
        lines.append(f"- Label distribution: `{json.dumps(report['label_distribution'], ensure_ascii=False)}`")
        lines.append(f"- Missing values by column: `{json.dumps(report['missing_by_column'], ensure_ascii=False)}`")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit review datasets for data-integrity issues")
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--output-dir", type=Path, default=Path("reports/data_integrity"))
    args = parser.parse_args(argv)

    files = sorted(args.data_dir.rglob("*.csv"))
    if not files:
        parser.error(f"No CSV files found under {args.data_dir}")

    reports = [audit_csv(path) for path in files]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "dataset_health.json").write_text(
        json.dumps(reports, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (args.output_dir / "dataset_health.md").write_text(_markdown_report(reports), encoding="utf-8")

    for report in reports:
        print(
            f"{report['status']:14} {report['file']} ({report['rows']} rows) "
            f"duplicates={report['exact_duplicates']} text_duplicates={report['normalized_text_duplicates']} "
            f"missing_text={report['missing_review_text']} invalid_ratings={report['invalid_or_missing_ratings']}"
        )
    print(f"\nReports written to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
