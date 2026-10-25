# DECISIONS.md

Operator decisions taken during the Zero-Red Mandate reliability pass (mission rule 11.6:
choose the safest reversible option, record it, keep the tree green, flag in FINAL_REPORT).

## D-001 (2026-10-25) Drop Python 3.9 from CI matrix and package metadata

- Context: CI matrix was [3.9, 3.10, 3.11]; pyproject classifiers listed 3.9. CPython 3.9
  reached end-of-life 2025-10-31; security fixes no longer published.
- Decision: matrix and `requires-python` now 3.10-3.12. This is a support-scope decision,
  not a failure dodge: the 3.9 job was failing on the same ruff gate as every other job
  (install itself succeeded), so no failure is being hidden.
- Reversible: re-adding a matrix entry is a one-line change if a 3.9 consumer appears.

## D-002 (2026-10-25) Remove fabricated "dummy scores" fallback in system_launcher.py

- Context: on scoring failure the launcher invented `score = 85` rows so report generation
  could proceed ("Creating dummy scores for report generation...").
- Options: (a) keep fabrication with a label, (b) fail the pipeline loudly, (c) generate
  reports without the scores section.
- Decision: (b) fail loud (`SystemExit(1)` + traceback log). Invented quality scores in
  county/donor reports are data fabrication; a red pipeline is recoverable, a fabricated
  report is not. (c) was rejected for now because every downstream report template expects
  the scores frame; adding an optional-scores mode is a feature, out of scope for a
  reliability pass (rule 11.1).
- Reversible: yes, via a future feature PR implementing (c) properly.

## D-003 (2026-10-25) Replace Codecov upload step with enforced local coverage floor

- Context: CI ended with `codecov/codecov-action@v3` (unpinned major, no token configured,
  no codecov account evidence). The step never gated anything: uploads to an unconfigured
  account are decoration, and v3 is deprecated.
- Decision: drop the upload; enforce `pytest --cov ... --cov-fail-under=35` in CI instead.
  Measured coverage at fix time: 38% (term report committed in docs/qa/artifacts). Floor
  set at 35 to absorb minor variance while ratcheting: it has never been higher, so this
  is not a lowering (no prior floor existed). Raise the floor as tests are added.
- Reversible: re-add an upload step once a codecov account + token exist.

## D-004 (2026-10-25) pre-commit hooks aligned to CI; isort removed; mypy deferred

- Context: `pre-commit-config.yaml` was misnamed (no leading dot) so no hook ever ran
  (defect #4). Revs were ancient (ruff v0.0.244 vs CI 0.17.2) and isort conflicts with
  ruff's I001 import sorting (two sorters = flip-flop).
- Decision: renamed to `.pre-commit-config.yaml`, revs pinned to the exact CI toolchain
  (ruff v0.17.2, black 26.10.1), isort hook removed (ruff owns import order). The mypy
  hook is deferred until a typecheck gate is wired in CI and the codebase passes it;
  a hook that fails every commit without CI signal trains developers to use --no-verify.
  Tracked in issue #4.

## D-005 (2026-10-25) pandas floor raised to >=2.2.0

- Context: code and tests now use the `ME` month-end offset alias (required since pandas
  2.2 removed `M`). Keeping `pandas>=1.5.0` would let environments install a version where
  `ME` does not exist.
- Decision: `pandas>=2.2.0`. Aligns the declared floor with what CI actually installs and
  what the code requires. Not a pin-to-avoid-error: the newer API is the target.

## D-006 (2026-10-25) Alert email failures now raise; run_alerts continues but exits non-zero

- Context: `send_alert_email` swallowed all exceptions with a print; a broken alerter
  reported success (silent-failure class, mission section 7: a dead worker must be loud).
- Decision: narrow catch to message-construction errors, log traceback, re-raise as
  RuntimeError. `run_alerts` catches per alert (so one malformed alert cannot drop the
  rest), counts failures, and raises SystemExit if any occurred.

## D-007 (2026-10-25) Support floor raised to Python 3.11; pillow>=13 declared; CI upgrades setuptools

- Context: first CI run of the new gate suite failed at pip-audit on all three
  matrix jobs: pillow 12.3.0 (22 published CVEs incl. CVE-2026-96636..44,
  CVE-2026-112391..401; fixed in pillow 13.0.0) and setuptools 79.0.1
  (PYSEC-2026-3447, GHSA-xmj3-9gf7-h52w; fixed in 83.0.0/84.1.0).
- Constraint discovered: pillow 13.0.0 requires Python >=3.11. Python 3.10
  itself reached end-of-life 2026-10-04. A py3.10 environment therefore CANNOT
  have a vulnerability-free pillow: staying on 3.10 means shipping known-vulnerable
  imaging code (mission rule 11.7: never weaken security to stay green).
- Decision: matrix and requires-python now 3.11/3.12/3.13; pillow>=13.0.0
  declared as an explicit security floor (transitive via matplotlib before);
  CI install step upgrades pip+setuptools+wheel so the audited environment
  carries patched tooling. Evidence: run 40196587310 (red), fixed run linked in PR #8.
- Reversible: yes, but only by re-accepting vulnerable dependencies on 3.10.
