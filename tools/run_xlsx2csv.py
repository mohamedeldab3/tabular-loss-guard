"""Independent XLSX -> CSV -> Markdown pipeline on the same original XLSX bytes."""

import csv
import io
import json
import platform
import sys
from importlib.metadata import version
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from csvtomd import md_table
from xlsx2csv import Xlsx2csv

from tabular_loss_guard.core import audit

out = ROOT / "evidence" / "xlsx2csv-csvtomd"
out.mkdir(parents=True, exist_ok=True)
results = []
for source in sorted((ROOT / "evidence" / "markitdown").glob("*.xlsx")):
    stream = io.StringIO()
    converter = Xlsx2csv(str(source), outputencoding="utf-8")
    try:
        converter.convert(stream, sheetid=1)
    finally:
        converter.close()
    raw_csv = stream.getvalue()
    (out / (source.stem + ".csv")).write_text(raw_csv, encoding="utf-8", newline="")
    target = out / (source.stem + ".md")
    target.write_text(
        md_table(list(csv.reader(io.StringIO(raw_csv)))), encoding="utf-8", newline=""
    )
    report = audit(source, target)
    (out / (source.stem + ".json")).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline=""
    )
    results.append(
        {"case": source.stem, "status": report["status"], "findings": len(report["findings"])}
    )
summary = {
    "python": platform.python_version(),
    "versions": {n: version(n) for n in ["xlsx2csv", "csvtomd", "openpyxl"]},
    "configuration": {
        "xlsx2csv": {"sheetid": 1, "outputencoding": "utf-8"},
        "csvtomd": "md_table defaults",
    },
    "source_directory": "evidence/markitdown",
    "cases": results,
}
(out / "summary.json").write_text(
    json.dumps(summary, indent=2) + "\n", encoding="utf-8", newline=""
)
print(json.dumps(summary, indent=2))
