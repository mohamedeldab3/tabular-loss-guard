# Value contract v1

A command compares one selected XLSX sheet or UTF-8 CSV file against exactly one
plain pipe table. Row 1 is the header. Order and shape are contractual: reordering
is a failure even if a reader could infer an equivalent table. No fuzzy matching.

XLSX uses stored values, not displayed number formats. Decimal(str(openpyxl value))
is the numeric reference; this does not recover precision already lost in Excel.
Equivalent finite scientific notation passes. Text, saved Excel errors, booleans
(True/False), and blanks require exact equality. CSV fields are always text.
Leading zeros in text are significant. Blank is empty, never NaN/null.

Markdown structural padding is stripped; source edge whitespace is unsupported.
Escaped pipes/backslashes are decoded. Inline markup, HTML, formulas, dates,
multiline cells, merges, multiple tables and ambiguous inputs are UNVERIFIED.
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
