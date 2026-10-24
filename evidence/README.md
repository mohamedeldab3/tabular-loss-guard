# Reproducible local evidence

All fixtures are original synthetic data. These are internal experiments, not
external complaints, adoption or an exhaustive converter benchmark.

## MarkItDown

`markitdown/` contains 10 XLSX sources, actual raw Markdown, individual guard
reports and a version/configuration summary. On MarkItDown 0.1.9, pandas 3.1.0,
openpyxl 3.1.5, Python 3.11.4: 4 PASS, 4 FAIL, 2 UNVERIFIED.

FAIL: precision loss, text leading-zero loss, saved errors/blank collapse, blank
rendering as NaN. PASS: small equivalent scientific notation, mixed Unicode,
row associations and booleans. UNVERIFIED: unescaped embedded pipe makes a ragged
table, and multiline cells are unsupported. Those cases do not pass CI.

Reproduce in a separate virtual environment:

```console
python -m pip install "markitdown[xlsx]==0.1.9" "pandas==3.1.0" "openpyxl==3.1.5"
python tools/run_markitdown.py
```

Reports hash the actual input bytes. Regenerating workbooks may change ZIP
metadata/hashes without changing cell values. No model/API calls are used.
Sources are read back from XLSX independently of converter output.

## Frictionless spike

```console
python -m pip install "frictionless[excel]==5.21.0" "openpyxl==3.1.5"
python tools/frictionless_spike.py
```

`frictionless-spike.json` shows saved errors remain distinct from blanks in its
Excel reader. Default Markdown detection is ArticleResource (text), not rows;
read_rows is unavailable. This bounded experiment does not establish that a
custom Frictionless extension cannot implement the workflow.

## Controls

The automated unit suite includes preserving controls and deliberate mutations
for numeric precision, all seven saved errors, leading zeros, Unicode, row order,
header/value associations, missing rows, unsupported cases and CLI report escaping.
The included CSV preserving/lossy examples work without MarkItDown installed.

## Independent conversion pipeline

`xlsx2csv-csvtomd/` retains CSV, raw Markdown and audit reports from the exact same
10 source XLSX files in `markitdown/`. The pipeline uses xlsx2csv 0.8.6 (its own
SAX/XML reader) and csvtomd 0.3.0 (its own table renderer), not pandas/MarkItDown.
Openpyxl is used only by the guard for source reference values.

```console
python -m pip install "xlsx2csv==0.8.6" "csvtomd==0.3.0"
python tools/run_xlsx2csv.py
python tools/verify_evidence.py
```

Observed under guard 0.2.0: **5 PASS, 1 FAIL, 4 UNVERIFIED**. Saved errors, blanks,
text identifiers, Unicode and row associations pass. Boolean values render as
TRUE/FALSE rather than this policy's True/False (2 cell findings); this is a strict
contract mismatch, not a claim that uppercase booleans are unusable. Single-column
precision/small-number outputs have no pipe-table syntax and are UNVERIFIED;
embedded unescaped pipes and multiline cells also remain UNVERIFIED. We do not
infer preservation for these unsupported outputs.

csvtomd is an archived upstream project; it is an independent compatibility target,
not a recommendation to adopt it in production. These ten cases do not establish
that either engine is better generally. No upstream project endorses this tool.
`verify_evidence.py` rechecks all 20 recorded runs, including raw-byte hashes.
