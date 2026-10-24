"""Install the built wheel in isolation and exercise the installed console entry."""

import json
import os
import subprocess
import tempfile
import tomllib
import venv
from pathlib import Path

root = Path(__file__).resolve().parents[1]
version = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
wheels = list((root / "dist").glob(f"tabular_loss_guard-{version}-*.whl"))
assert len(wheels) == 1, "Expected exactly one wheel for the current version"
wheel = wheels[0]
env = dict(os.environ)
env.pop("PYTHONPATH", None)
with tempfile.TemporaryDirectory() as folder:
    folder = Path(folder)
    venv.EnvBuilder(with_pip=True).create(folder / "venv")
    scripts = folder / "venv" / ("Scripts" if os.name == "nt" else "bin")
    python = scripts / ("python.exe" if os.name == "nt" else "python")
    command = scripts / ("tabular-loss-guard.exe" if os.name == "nt" else "tabular-loss-guard")
    subprocess.run(
        [str(python), "-m", "pip", "install", str(wheel)], check=True, cwd=folder, env=env
    )
    for target, expected in [("preserved.md", 0), ("lossy.md", 1)]:
        result = subprocess.run(
            [
                str(command),
                str(root / "examples/source.csv"),
                str(root / "examples" / target),
                "--json",
                str(folder / (target + ".json")),
            ],
            cwd=folder,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert result.returncode == expected, (result.stdout, result.stderr)
        assert json.loads(result.stdout)["status"] == ("PASS" if expected == 0 else "FAIL")
    compare_command = scripts / (
        "tabular-loss-compare.exe" if os.name == "nt" else "tabular-loss-compare"
    )
    for before, after, expected in [
        ("preserved.md.json", "lossy.md.json", 1),
        ("lossy.md.json", "preserved.md.json", 0),
    ]:
        result = subprocess.run(
            [str(compare_command), str(folder / before), str(folder / after)],
            cwd=folder,
            env=env,
            capture_output=True,
            text=True,
        )
        assert result.returncode == expected, (result.stdout, result.stderr)
    result = subprocess.run(
        [str(command), "missing.xlsx", "missing.md"],
        cwd=folder,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
print("Clean wheel: audit, regression comparison, improvement and input-error gates passed")
