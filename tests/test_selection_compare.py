import copy
import json
import subprocess
import sys

import pytest

from tabular_loss_guard.compare import compare
from tabular_loss_guard.core import audit, markdown_rows


def test_outer_pipes_optional():
    assert markdown_rows("ID | Value\n--- | ---\na | 42") == [["ID", "Value"], ["a", "42"]]


def test_multiple_selection():
    text = "| A |\n| --- |\n| first |\n\n## Next\n\n| B |\n| --- |\n| second |"
    assert markdown_rows(text, 2) == [["B"], ["second"]]
    with pytest.raises(ValueError):
        markdown_rows(text)


@pytest.mark.parametrize("index", [0, -1, True, 3])
def test_invalid_selection(index):
    with pytest.raises(ValueError):
        markdown_rows("| A |\n| --- |\n| value |", index)


def test_fences_and_indentation():
    text = "~~~md\n| A |\n| --- |\n| ignored |\n```\n~~~\n\n    | B |\n    | --- |\n\n| C |\n| --- |\n| keep |"
    assert markdown_rows(text) == [["C"], ["keep"]]


def test_backslash_before_boundary():
    assert markdown_rows(r"| A |" + "\n| --- |\n" + r"| end\\|") == [["A"], ["end\\"]]
    assert markdown_rows(r"| A |" + "\n| --- |\n" + r"| end\|") == [["A"], ["end|"]]


@pytest.fixture
def reports(tmp_path):
    source, good, bad = tmp_path / "source.csv", tmp_path / "good.md", tmp_path / "bad.md"
    source.write_text("ID,Value\na,42\n", encoding="utf-8")
    good.write_text("| ID | Value |\n| --- | --- |\n| a | 42 |", encoding="utf-8")
    bad.write_text("| ID | Value |\n| --- | --- |\n| a | 43 |", encoding="utf-8")
    return audit(source, good), audit(source, bad)


def test_compare_transitions(reports):
    good, bad = reports
    assert compare(good, bad)["status"] == "REGRESSION"
    assert compare(bad, good)["status"] == "IMPROVED"
    assert compare(bad, bad)["status"] == "UNCHANGED"
    assert compare(good, good)["status"] == "UNCHANGED"


@pytest.mark.parametrize(
    "field,value",
    [
        ("source_sha256", "0" * 64),
        ("policy", "other"),
        ("sheet", "other"),
        ("table_index", 2),
        ("schema_version", True),
        ("markdown_sha256", "bad"),
        ("status", "UNVERIFIED"),
        ("status", "ERROR"),
        ("findings", None),
        ("table_index", True),
        ("status", "PASS"),
    ],
)
def test_incompatible_or_inconsistent_reports(reports, field, value):
    good, bad = reports
    bad = copy.deepcopy(bad)
    bad[field] = value
    with pytest.raises(ValueError):
        compare(good, bad)


@pytest.mark.parametrize(
    "field,value",
    [
        ("row", True),
        ("column", -1),
        ("cell", "Z99"),
        ("reason", "unknown"),
        ("expected", 42),
        ("observed", 43),
        ("kind", "unknown"),
    ],
)
def test_invalid_findings(reports, field, value):
    good, bad = reports
    bad = copy.deepcopy(bad)
    bad["findings"][0][field] = value
    with pytest.raises(ValueError):
        compare(good, bad)


def test_duplicate_findings(reports):
    good, bad = reports
    bad["findings"].append(copy.deepcopy(bad["findings"][0]))
    with pytest.raises(ValueError):
        compare(good, bad)


def test_cli_comparison(tmp_path, reports):
    good, bad = reports
    before, after, output = [
        tmp_path / name for name in ["before.json", "after.json", "compare.json"]
    ]
    before.write_text(json.dumps(good), encoding="utf-8")
    after.write_text(json.dumps(bad), encoding="utf-8")
    command = [
        sys.executable,
        "-m",
        "tabular_loss_guard.compare",
        str(before),
        str(after),
        "--json",
        str(output),
    ]
    result = subprocess.run(command, capture_output=True)
    assert result.returncode == 1
    assert json.loads(output.read_text())["status"] == "REGRESSION"
    result = subprocess.run(
        [sys.executable, "-m", "tabular_loss_guard.compare", str(after), str(before)],
        capture_output=True,
    )
    assert result.returncode == 0
    after.write_text("invalid JSON", encoding="utf-8")
    result = subprocess.run(command, capture_output=True)
    assert result.returncode == 2


def test_optional_outer_pipes_trailing_blank():
    assert markdown_rows("ID | Value\n--- | ---\na |") == [["ID", "Value"], ["a", ""]]
