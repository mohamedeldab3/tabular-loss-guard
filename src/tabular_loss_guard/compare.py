"""Compare two saved audit reports for the same source contract."""

import argparse
import json
import re
from pathlib import Path

from openpyxl.utils import get_column_letter

from . import __version__


def validate(report):
    if (
        not isinstance(report, dict)
        or type(report.get("schema_version")) is not int
        or report["schema_version"] != 1
    ):
        raise ValueError("Unsupported report schema")
    if report.get("policy") != "ordered-stored-values-v1":
        raise ValueError("Unknown value policy")
    for key in ("source_sha256", "markdown_sha256"):
        if not isinstance(report.get(key), str) or not re.fullmatch("[0-9a-f]{64}", report[key]):
            raise ValueError("Missing or malformed input fingerprint")
    if not isinstance(report.get("sheet"), str) or not report["sheet"]:
        raise ValueError("Missing source sheet")
    if type(report.get("table_index", 1)) is not int or report.get("table_index", 1) < 1:
        raise ValueError("Invalid table selection")
    status, findings = report.get("status"), report.get("findings")
    if status not in {"PASS", "FAIL"}:
        raise ValueError("Only verified PASS/FAIL reports can be compared")
    if (
        not isinstance(findings, list)
        or (status == "PASS" and findings)
        or (status == "FAIL" and not findings)
    ):
        raise ValueError("Findings contradict report status")
    identities = set()
    for item in findings:
        if not isinstance(item, dict):
            raise ValueError("Malformed finding")
        if item.get("reason") == "value_changed":
            row, column = item.get("row"), item.get("column")
            if (
                type(row) is not int
                or type(column) is not int
                or row < 1
                or not 1 <= column <= 16384
            ):
                raise ValueError("Invalid cell coordinates")
            if item.get("cell") != f"{get_column_letter(column)}{row}":
                raise ValueError("Cell coordinates disagree")
            if item.get("kind") not in {"text", "number", "blank"}:
                raise ValueError("Invalid cell kind")
            if (
                not isinstance(item.get("expected"), str)
                or "observed" not in item
                or not (item["observed"] is None or isinstance(item["observed"], str))
            ):
                raise ValueError("Invalid cell values")
            if item["expected"] == item["observed"]:
                raise ValueError("Finding does not describe a change")
            identity = item["cell"]
        elif item.get("reason") == "shape_changed":
            for key in ("expected", "observed"):
                shape = item.get(key)
                if (
                    not isinstance(shape, list)
                    or len(shape) != 2
                    or any(type(n) is not int or n < 0 for n in shape)
                ):
                    raise ValueError("Invalid table shape")
            if item["expected"] == item["observed"]:
                raise ValueError("Finding does not describe a shape change")
            identity = "shape"
        else:
            raise ValueError("Unknown finding reason")
        if identity in identities:
            raise ValueError("Duplicate finding identity")
        identities.add(identity)
    return {json.dumps(item, sort_keys=True, ensure_ascii=False) for item in findings}


def compare(before, after):
    old, new = validate(before), validate(after)
    for key in ("source_sha256", "policy", "sheet"):
        if before[key] != after[key]:
            raise ValueError(f"Reports use different {key}")
    if before.get("table_index", 1) != after.get("table_index", 1):
        raise ValueError("Reports select different tables")
    added, resolved = new - old, old - new
    return {
        "schema_version": 1,
        "tool_version": __version__,
        "status": "REGRESSION" if added else ("IMPROVED" if resolved else "UNCHANGED"),
        "source_sha256": before["source_sha256"],
        "policy": before["policy"],
        "before_status": before["status"],
        "after_status": after["status"],
        "added_findings": [json.loads(x) for x in sorted(added)],
        "resolved_findings": [json.loads(x) for x in sorted(resolved)],
    }


def main():
    parser = argparse.ArgumentParser(
        description=__doc__ + " Exit 0: no new findings; 1: regression; 2: invalid/unverified."
    )
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--json", type=Path, dest="output")
    args = parser.parse_args()
    if args.output and args.output.resolve() in {args.before.resolve(), args.after.resolve()}:
        parser.error("Report output must not overwrite an input")
    try:
        before = json.loads(args.before.read_text(encoding="utf-8-sig"))
        after = json.loads(args.after.read_text(encoding="utf-8-sig"))
        result = compare(before, after)
    except Exception as exc:
        result = {"schema_version": 1, "status": "ERROR", "reason": str(exc)}
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    try:
        if args.output:
            args.output.write_text(output, encoding="utf-8")
    except OSError as exc:
        parser.exit(2, f"Cannot write report: {exc}\n")
    print(output, end="")
    return 1 if result["status"] == "REGRESSION" else (2 if result["status"] == "ERROR" else 0)


if __name__ == "__main__":
    raise SystemExit(main())
