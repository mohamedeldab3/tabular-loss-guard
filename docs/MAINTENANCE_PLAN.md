# Proposed six-month maintainer plan

This is planned work, not a claim of existing sponsorship or completed adoption.

1. Harden parsing boundaries with mutation tests for syntax ambiguity, report
   consistency and unsupported data types. Keep numeric equality deterministic.
2. Expand reproducible converter integrations and retain exact versions, raw
   outputs, source provenance and contract limitations for each run.
3. Trial the CI gate in real document-ingestion workflows with permission; record
   feedback as independent only when it actually comes from independent users.
4. Introduce opt-in multiline/date policies only with independently authored
   source expectations and preserving controls; keep unsupported cases unverified.
5. Use assisted review to propose targeted fixes and tests; maintain human review
   and deterministic tests as the merge/release criteria. Do not send private
   workbooks or reports containing sensitive cell values to an API.
6. Maintain releases, installation compatibility and docs. Use security tooling
   to investigate parser, dependency and output-handling concerns and verify fixes.

Success evidence: independent integrations, reviewed reproductions, regressions
caught and useful maintainer feedback. Commit totals alone are not a success metric.
