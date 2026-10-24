# Contributing

Install `python -m pip install -e ".[test]"`, then run `python -m pytest -q`.
Add an original minimal source fixture with an independently specified expected
value, a preserving control and a lossy mutation. Do not use private documents.
For ambiguous alignment, return UNVERIFIED rather than assuming success.
Bug reports should include tool versions, command, expected/observed values and
a shareable minimal reproducer. No external reports or adoption are implied by
our internal test cases.
