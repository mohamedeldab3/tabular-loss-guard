"""Verify committed raw-byte fingerprints and re-evaluate archived runs."""

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tabular_loss_guard.core import audit  # noqa: E402

count = 0
for directory in ("markitdown", "xlsx2csv-csvtomd"):
    for target in sorted((ROOT / "evidence" / directory).glob("*.md")):
        source = ROOT / "evidence" / "markitdown" / (target.stem + ".xlsx")
        saved = json.loads(target.with_suffix(".json").read_text(encoding="utf-8"))
        for key, path in [("source_sha256", source), ("markdown_sha256", target)]:
            assert saved[key] == hashlib.sha256(path.read_bytes()).hexdigest(), (target, key)
        current = audit(source, target)
        assert current["status"] == saved["status"], (target, current)
        assert current["findings"] == saved["findings"], (target, current)
        count += 1
print(f"{count} archived runs: raw fingerprints and contract results verified")
