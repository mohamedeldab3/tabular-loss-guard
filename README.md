# tabular-loss-guard

Catch cell values lost or changed when XLSX or CSV becomes Markdown.
Built for document ingestion and RAG pipelines: a successful conversion does not
necessarily preserve numeric precision, spreadsheet errors or identifier text.

```console
python -m pip install .
tabular-loss-guard examples/source.csv examples/preserved.md
# PASS, exit 0

tabular-loss-guard examples/source.csv examples/lossy.md --json report.json --html report.html
# FAIL, exit 1: changed cells include B2 and B3
```

For Excel, use `input.xlsx converted.md --sheet Results`. Each invocation compares
one source table with an output table. For a multi-table document, select the
1-based output index explicitly: `--sheet Results --table 2`. Without `--table`,
multiple tables are UNVERIFIED. No API keys or model calls.

## What it checks

- Stored numeric values using exact Decimal equality; equivalent scientific notation passes.
- Saved Excel errors versus empty cells, Unicode and text identifiers with leading zeros.
- Ordered headers, rows and columns; missing/extra rows or columns fail.
- Cell locations, expected/observed values, policy/tool versions and input SHA-256 in reports.

Exit codes: **0 PASS**, **1 FAIL**, **2 UNVERIFIED or ERROR**. Unsupported inputs do
not pass. The initial plain pipe-table contract excludes formulas, dates, merges,
inline Markdown/HTML, multiline cells and ambiguous table alignment. XLSX display
formatting is outside scope; `00000` number formats do not make a numeric cell a
text identifier. CSV values are all text. See [the policy](docs/DESIGN.md).

## Detect regressions across converter upgrades

Save audit reports for the **same source file, sheet, policy and table index**:

```console
tabular-loss-guard input.xlsx old-output.md --json before.json
tabular-loss-guard input.xlsx new-output.md --json after.json
tabular-loss-compare before.json after.json --json comparison.json
```

Comparison exits 1 for added/changed findings, 0 for unchanged or improved results,
and 2 for incompatible, inconsistent or unverified reports. A 0 here does not
mean the latest audit passed: existing failures can remain. For a strict quality
gate, require the audit command itself to exit 0. Identical finding counts can
still hide a new failure; comparison checks finding contents, not just counts.
Reports compare observations; they do not verify who produced the inputs.

## CI

```yaml
- run: python -m pip install .
- run: tabular-loss-guard input.xlsx converted.md --json report.json
```

Run this after your converter. A FAIL is evidence against this contract, not a
claim that every downstream application needs identical presentation. Reports
include cell values; review them before publishing sensitive source data.

## Evidence and related work

Twenty retained runs exercise ten original XLSX fixtures through MarkItDown 0.1.9
and an independent `xlsx2csv 0.8.6 -> csvtomd 0.3.0` pipeline. Raw files,
configuration, hashes and unsupported cases are retained. These are bounded
contract results, not a general engine ranking. See [reproducible evidence](evidence/README.md).
The underlying issues were already reported upstream:
[#2728](https://github.com/microsoft/markitdown/issues/2728) and
[#2532](https://github.com/microsoft/markitdown/issues/2532), with existing proposed
fixes [#2732](https://github.com/microsoft/markitdown/pull/2732) and
[#2664](https://github.com/microsoft/markitdown/pull/2664).
This tool checks the conversion boundary independently; it is not affiliated with
Microsoft or those contributors. It does not implement a replacement converter.

Frictionless and Great Expectations already provide general data validation.
Our bounded scope is paired source/output value preservation; the
[Frictionless spike and design decision](docs/DESIGN.md) document this distinction.
We make no claim of downstream adoption or independent user feedback.

## Development

```console
python -m pip install -e ".[test]"
python -m pytest -q
python tools/verify_evidence.py
python -m build
python tools/verify_installed.py
```

MIT licensed. Contributions with minimal shareable reproductions are welcome;
see [CONTRIBUTING.md](CONTRIBUTING.md).
