"""CLI exit codes: 0 pass, 1 loss, 2 unverified/input error."""

import argparse
import html
import json
from pathlib import Path

from . import __version__
from .core import audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("source", type=Path)
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--sheet")
    parser.add_argument(
        "--table", type=int, help="1-based output table index (required for multiple tables)"
    )
    parser.add_argument("--json", type=Path, dest="json_path")
    parser.add_argument("--html", type=Path, dest="html_path")
    args = parser.parse_args()
    paths = [p.resolve() for p in [args.source, args.markdown, args.json_path, args.html_path] if p]
    if len(paths) != len(set(paths)):
        parser.error("Input and output paths must be distinct")
    try:
        report = audit(args.source, args.markdown, args.sheet, args.table)
    except Exception as exc:
        report = {"schema_version": 1, "status": "ERROR", "reason": str(exc)}
    report["tool_version"] = __version__
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.json_path:
        args.json_path.write_text(output, encoding="utf-8")
    if args.html_path:
        args.html_path.write_text(
            "<!doctype html><meta charset=utf-8><title>Tabular loss report</title>"
            "<h1>Tabular loss guard: "
            + report["status"]
            + "</h1><pre>"
            + html.escape(output)
            + "</pre>",
            encoding="utf-8",
        )
    print(output, end="")
    return {"PASS": 0, "FAIL": 1}.get(report["status"], 2)


if __name__ == "__main__":
    raise SystemExit(main())
