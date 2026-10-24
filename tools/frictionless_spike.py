"""Original saved-error readback and Markdown ingestion spike."""

import json
import tempfile
from importlib.metadata import version
from pathlib import Path

from frictionless import Resource
from openpyxl import Workbook

result = {"frictionless_version": version("frictionless"), "openpyxl_version": version("openpyxl")}
with tempfile.TemporaryDirectory() as folder:
    folder = Path(folder)
    source = folder / "source.xlsx"
    book = Workbook()
    book.active.append(["Case", "Value"])
    book.active.append(["error", "#DIV/0!"])
    book.active.append(["blank", None])
    book.save(source)
    book.close()
    try:
        resource = Resource(str(source))
        result["xlsx_rows"] = [dict(row) for row in resource.read_rows()]
        result["xlsx_schema"] = resource.schema.to_descriptor()
    except Exception as exc:
        result["xlsx_error"] = str(exc)
    target = folder / "target.md"
    target.write_text(
        "| Case | Value |\n| --- | --- |\n| error | #DIV/0! |\n| blank | |\n", encoding="utf-8"
    )
    try:
        resource = Resource(str(target))
        result["markdown_resource_type"] = resource.type
        result["markdown_rows"] = [dict(row) for row in resource.read_rows()]
    except Exception as exc:
        result["markdown_error"] = str(exc)
Path("evidence/frictionless-spike.json").write_text(
    json.dumps(result, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8"
)
print(json.dumps(result, ensure_ascii=False, default=str))
