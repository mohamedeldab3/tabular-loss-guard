# Value contract v1

A command compares one selected XLSX sheet or UTF-8 CSV file against one selected
plain pipe table. Multiple tables require a 1-based --table index; table order
is part of the contract, and headers/cells are still compared after selection. Row 1 is the header. Order and shape are contractual: reordering
is a failure even if a reader could infer an equivalent table. No fuzzy matching.

XLSX uses stored values, not displayed number formats. Decimal(str(openpyxl value))
is the numeric reference; this does not recover precision already lost in Excel.
Equivalent finite scientific notation passes. Text, saved Excel errors, booleans
(True/False), and blanks require exact equality. CSV fields are always text.
Leading zeros in text are significant. Blank is empty, never NaN/null.

Markdown structural padding is stripped; source edge whitespace is unsupported.
Escaped pipes/backslashes are decoded. Inline markup, HTML, formulas, dates,
multiline cells, merges, unselected multiple tables and ambiguous inputs are UNVERIFIED.
Formulas are never evaluated. Hidden rows/columns are included; formatting and
visibility are not validated. There is no claim of complete Markdown support.

PASS means only that this bounded value contract passed. FAIL means a shape or
value mismatch. UNVERIFIED and ERROR both fail CI with exit 2. Input hashes and
policy version make reports attributable. Reports contain source values: keep
sensitive reports private.

## Frictionless decision

Frictionless is a mature table/schema validation framework. Its documented
Markdown format exports metadata rather than providing this paired conversion
contract: https://framework.frictionlessdata.io/docs/formats/markdown.html .
The local spike (see evidence/frictionless-spike.json) examines actual readback of
saved errors and table ingestion. The spike preserved saved Excel errors but detected Markdown as ArticleResource,
with no read_rows method. The focused comparator must retain typed source
errors and ordered source/output identity. We do not claim Frictionless cannot be
extended to implement it; reusing its validation engine adds little to this small
paired comparison. A future adapter should reuse these contract results rather
than introduce another general validation framework.

## Comparison contracts

Saved reports must be schema 1, verified PASS/FAIL, consistent with their findings,
and use the same source SHA-256, policy, sheet and table index. Unknown/inconsistent
findings and duplicate identities are rejected. Input Markdown hashes may differ.
Added or changed findings count as regressions; removed findings are resolved.
Unchanged known failures can produce exit 0 for comparison while audit still fails.
This gate is observation-based, not an attestation or a converter authenticity check.

## Pipe-table boundaries

Both outer-pipe and no-outer-pipe styles are supported; the header determines the
style, preserving trailing empty cells in the latter. A table requires a pipe in
the header and a delimiter row with at least three dashes per cell. A single-column
csvtomd output containing no pipes is UNVERIFIED rather than treated as a table.
Code fences and four-space indented code are excluded. This remains a bounded
plain-cell parser, not a complete CommonMark/GFM implementation.
