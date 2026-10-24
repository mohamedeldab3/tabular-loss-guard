# Codex for Open Source application draft

Verified against the official form on 2026-10-24:
https://openai.com/form/codex-for-oss/
Program: https://developers.openai.com/community/codex-for-oss

Repository URL: https://github.com/mohamedeldab3/tabular-loss-guard
GitHub username: mohamedeldab3
Role selection: Primary maintainer

Use the name and email associated with your own ChatGPT account. If requesting
API credits, enter your actual OpenAI Organization ID, not the GitHub username.
Select API credits and Codex Security only if you intend to use the workflows
below. Security access remains conditional. Each response below is under the
form's 500-character limit (including the optional Security rationale).

## Why does this repository qualify?

Tabular Loss Guard checks whether XLSX/CSV-to-Markdown conversion preserves numeric values, Excel errors, text identifiers and table associations before data enters RAG pipelines. It provides reproducible fixtures, 20 recorded runs across two conversion paths, cell-level evidence and CI gates. Its ecosystem value is detecting silent source-data changes that can corrupt retrieval context, with unsupported cases explicitly failing verification.

## How will you use API credits for your project?

I will use API credits to turn reproducible conversion failures into candidate regression tests, assist code review of parser and adapter changes, and draft release notes from verified diffs. Generated changes will require deterministic tests and human review; stored source values will remain the ground truth. The guard itself will stay usable offline without an API key.

## Why does your project need Codex Security?

The project parses externally supplied XLSX/CSV and Markdown and produces reports containing source values. I would use Codex Security to review file parsing, dependency risks, resource exhaustion, output-path handling and HTML escaping, then add regression tests for confirmed findings. The goal is safer use in document-ingestion CI workflows.

## Anything else we should know?

I am the repository owner and primary maintainer, responsible for implementation, tests, reproducible evidence, documentation and releases. The repository includes 64 automated tests, Windows/Linux CI, raw conversion artifacts and input fingerprints. Next work focuses on additional converter integrations and independent trials. All published examples use original synthetic data.

## Evidence links

- https://github.com/mohamedeldab3/tabular-loss-guard/tree/main/evidence
- https://github.com/mohamedeldab3/tabular-loss-guard/actions
- https://github.com/mohamedeldab3/tabular-loss-guard/blob/main/docs/DESIGN.md
- https://github.com/mohamedeldab3/tabular-loss-guard/blob/main/docs/MAINTENANCE_PLAN.md

These statements describe repository evidence and planned use. They do not claim
upstream endorsement, independent complaints, package download counts or adoption.
Refresh numerical claims if the project changes before submitting. The program
makes selection decisions; this draft cannot guarantee acceptance.
