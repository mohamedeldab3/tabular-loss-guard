"""Install the built wheel in isolation and exercise the installed console entry."""
import json
import os
import subprocess
import tempfile
import venv
from pathlib import Path

root = Path(__file__).resolve().parents[1]
wheel = next((root / "dist").glob("*.whl"))
env = dict(os.environ)
env.pop("PYTHONPATH", None)
with tempfile.TemporaryDirectory() as folder:
    folder = Path(folder)
    venv.EnvBuilder(with_pip=True).create(folder / "venv")
    scripts = folder / "venv" / ("Scripts" if os.name == "nt" else "bin")
    python = scripts / ("python.exe" if os.name == "nt" else "python")
    command = scripts / ("tabular-loss-guard.exe" if os.name == "nt" else "tabular-loss-guard")
    subprocess.run([str(python), "-m", "pip", "install", str(wheel)], check=True, cwd=folder, env=env)
    for target, expected in [("preserved.md", 0), ("lossy.md", 1)]:
        result = subprocess.run([str(command), str(root / "examples/source.csv"),
                                 str(root / "examples" / target)], cwd=folder, env=env,
                                capture_output=True, text=True, encoding="utf-8")
        assert result.returncode == expected, (result.stdout, result.stderr)
        assert json.loads(result.stdout)["status"] == ("PASS" if expected == 0 else "FAIL")
    result = subprocess.run([str(command), "missing.xlsx", "missing.md"], cwd=folder,
                            env=env, capture_output=True, text=True)
    assert result.returncode == 2
print("Clean wheel: preserving control, loss mutation and missing input exit codes passed")
