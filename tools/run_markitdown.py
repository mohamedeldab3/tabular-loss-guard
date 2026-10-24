"""Generate original fixtures and retain actual pinned converter results."""
import io
import json
import platform
import sys
from importlib.metadata import version
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from openpyxl import Workbook
from markitdown import MarkItDown, StreamInfo
from tabular_loss_guard.core import audit

cases = {
    "precision": [["Value"], [123456789.123]],
    "small-number": [["Value"], [0.1], [1e-10]],
    "text-identifier": [["ID", "Value"], ["00123", "keep"]],
    "saved-errors": [["Case", "Value"], *[[str(i), v] for i, v in enumerate(
        ["#DIV/0!", "#REF!", "#VALUE!", "#N/A", "#NUM!", "#NAME?", "#NULL!"])], ["blank", None]],
    "unicode": [["ID", "Name"], ["a", "مرحبا بالعالم"], ["b", "English عربي"]],
    "pipe": [["ID", "Value"], ["a", "left | right"]],
    "multiline": [["Value"], ["line1\nline2"]],
    "blank": [["ID", "Value"], ["a", None], ["b", "filled"]],
    "row-associations": [["ID", "Value"], ["a", 10], ["b", 20]],
    "boolean": [["ID", "Value"], ["a", True], ["b", False]],
}
out = ROOT / "evidence" / "markitdown"
out.mkdir(parents=True, exist_ok=True)
results = []
converter = MarkItDown(enable_plugins=False)
for name, rows in cases.items():
    book = Workbook()
    for row in rows:
        book.active.append(row)
    stream = io.BytesIO()
    book.save(stream)
    book.close()
    source, target = out / (name + ".xlsx"), out / (name + ".md")
    source.write_bytes(stream.getvalue())
    stream.seek(0)
    converted = converter.convert_stream(stream, stream_info=StreamInfo(extension=".xlsx"))
    target.write_text(converted.markdown, encoding="utf-8")
    report = audit(source, target)
    (out / (name + ".json")).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    results.append({"case": name, "status": report["status"], "findings": len(report["findings"])})
summary = {"python": platform.python_version(), "versions": {n: version(n) for n in ["markitdown", "pandas", "openpyxl"]},
           "configuration": {"enable_plugins": False}, "cases": results}
(out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))
