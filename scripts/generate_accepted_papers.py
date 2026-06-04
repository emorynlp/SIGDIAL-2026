#!/usr/bin/env python3
"""Generate _pages/program/accepted_papers.md from downloads/accepted_papers.xlsx."""

import argparse
import re
from pathlib import Path

import openpyxl

PAPER_TYPE_ALIASES = {"submission type", "paper type", "type of paper"}
PRESENTATION_ALIASES = {
    "format": {"presentation format", "format", "presentation type", "modality"},
    "date": {"date", "session date", "presentation date", "day"},
    "time": {"time", "start time", "presentation time", "session time"},
    "location": {"location", "room", "venue", "place"},
}

TITLE_ALIASES = {"title"}
AUTHORS_ALIASES = {"authors"}

SECTION_ORDER = (
    ("long", "Long Papers"),
    ("short", "Short Papers"),
    ("demo", "Demos"),
)


def norm_header(header):
    return (header or "").strip().lower()


def column_map(headers, alias_groups):
    mapping = {}
    for index, header in enumerate(headers):
        normalized = norm_header(header)
        for key, aliases in alias_groups.items():
            if normalized in aliases and key not in mapping:
                mapping[key] = index
    return mapping


def find_column(headers, aliases, default):
    for index, header in enumerate(headers):
        if norm_header(header) in aliases:
            return index
    return default


def normalize_paper_type(raw_type):
    if not raw_type:
        return None
    value = str(raw_type).strip().lower()
    if "demo" in value:
        return "demo"
    if "short" in value:
        return "short"
    if "long" in value:
        return "long"
    return str(raw_type).strip()


def escape_markdown(text):
    """Escape characters that would break emphasis or links in Kramdown."""
    return re.sub(r"([\\*_`\[\]])", r"\\\1", text)


def format_paper_entry(row, title_column, authors_column, presentation_columns):
    title = escape_markdown(str(row[title_column]).strip())
    authors = escape_markdown(
        str(row[authors_column]).strip() if row[authors_column] else ""
    )
    lines = [f"- **{title}**  ", f"  {authors}  "]
    presentation = presentation_line(row, presentation_columns)
    if presentation != "TBA":
        lines.append(f"  *{escape_markdown(presentation)}*")
    return lines


def presentation_line(row, presentation_columns):
    parts = []
    for key in ("format", "date", "time", "location"):
        value = None
        if key in presentation_columns:
            cell = row[presentation_columns[key]]
            if cell is not None and str(cell).strip():
                value = str(cell).strip()
        parts.append(value)
    if not any(parts):
        return "TBA"
    return " · ".join(part if part else "TBA" for part in parts)


def generate(xlsx_path, output_path):
    workbook = openpyxl.load_workbook(xlsx_path, read_only=True)
    worksheet = workbook.active
    rows = list(worksheet.iter_rows(values_only=True))
    if not rows:
        raise ValueError(f"No rows found in {xlsx_path}")

    headers = [str(header) if header is not None else "" for header in rows[0]]
    presentation_columns = column_map(headers, PRESENTATION_ALIASES)
    paper_type_column = find_column(headers, PAPER_TYPE_ALIASES, None)
    title_column = find_column(headers, TITLE_ALIASES, 1)
    authors_column = find_column(headers, AUTHORS_ALIASES, 2)

    papers = [row for row in rows[1:] if row and row[title_column]]

    lines = [
        "---",
        "title: Main Conference",
        "layout: single",
        "permalink: /program/accepted_main_conference/",
        "toc: true",
        "toc_sticky: true",
        "toc_icon: \"cog\"",
        "sidebar:",
        "    nav: program",
        "---",
        "",
        "Accepted papers are grouped by type and listed alphabetically by title.",
        "",
    ]

    if paper_type_column is not None:
        grouped = {key: [] for key, _ in SECTION_ORDER}
        grouped["other"] = []
        for row in papers:
            paper_type = normalize_paper_type(row[paper_type_column])
            bucket = paper_type if paper_type in grouped else "other"
            grouped[bucket].append(row)

        for key, heading in SECTION_ORDER:
            section_papers = grouped[key]
            if not section_papers:
                continue
            section_papers.sort(key=lambda row: str(row[title_column]).lower())
            lines.extend(["", f"## {heading}", ""])
            for row in section_papers:
                lines.extend(format_paper_entry(
                    row, title_column, authors_column, presentation_columns
                ))

        if grouped["other"]:
            grouped["other"].sort(key=lambda row: str(row[title_column]).lower())
            lines.extend(["", "## Other", ""])
            for row in grouped["other"]:
                lines.extend(format_paper_entry(
                    row, title_column, authors_column, presentation_columns
                ))
    else:
        papers.sort(key=lambda row: str(row[title_column]).lower())
        for row in papers:
            lines.extend(format_paper_entry(
                row, title_column, authors_column, presentation_columns
            ))

    lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return len(papers), presentation_columns, paper_type_column is not None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--xlsx",
        default="downloads/accepted_papers.xlsx",
        help="Input spreadsheet",
    )
    parser.add_argument(
        "--out",
        default="_pages/program/accepted_papers.md",
        help="Output markdown file",
    )
    args = parser.parse_args()

    count, presentation_columns, has_paper_type = generate(Path(args.xlsx), Path(args.out))
    print(f"Wrote {count} papers to {args.out}")
    if has_paper_type:
        print("Included paper type from Submission Type column.")
    if not presentation_columns:
        print("No presentation columns found; using TBA for format, date, time, and location.")


if __name__ == "__main__":
    main()
