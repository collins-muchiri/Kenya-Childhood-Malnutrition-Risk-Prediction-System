# Hostile review: PR #8 (fix/zero-red-python-gates)

Reviewer: same operator, hostile-reviewer mode (mission rule 11.2). Date: 2026-10-25.
Scope: `git diff origin/main...fix/zero-red-python-gates` at the time of review
(75 files, +11001/-1974; insertions dominated by committed evidence logs).

## Checks performed

1. **Forbidden-pattern scan over every added line** (`# noqa`, `type: ignore`,
   `@pytest.mark.skip`, `xfail`, `continue-on-error`, `allow_failure`, `|| true`,
   `set +e`, `--no-verify`, `except: pass`): all textual hits are documentation
   quotes (SILENT_FAILURES.md, DECISIONS.md), the suppression auditor's own regex
   literals, or sweep evidence. **Zero operative suppressions added.**
   One pre-existing `|| true` exists in `web/package.json` "prepare" (husky install
   guard for environments without devDependencies) - web scope, dispositioned in
   the web PR review, not introduced here.

2. **Assertion integrity**: per-file assertion census main vs branch:
   56 -> 57 total. Only test_configuration.py changed (+1): the
   try/except-`self.fail` anti-pattern was replaced with a direct call plus an
   effect assertion (`PROCESSED_DATA_DIR.exists()`). The 25 `-`-prefixed assert
   lines in the raw diff are black re-indentation pairs, verified by census.
   **No assertion deleted or weakened; no test file deleted** (only
   pre-commit-config.yaml -> .pre-commit-config.yaml rename, content modernised).

3. **Coverage floor**: `--cov-fail-under=35` is a NEW gate (none existed); measured
   38.15%. Establishment, not lowering (rule 4.1 inapplicable).

4. **CI matrix change**: 3.9/3.10 dropped for EOL + dependency-floor reasons
   (CPython 3.9 EOL 2025-10-31, 3.10 EOL 2026-10-04, pillow 13 requires >=3.11),
   decisions D-001/D-007. Not failure-dodging: those legs failed identically to
   the others (ruff), and the successor matrix runs the same full gate set.

5. **Codecov step removal**: replaced by an enforced local coverage floor (D-003).
   The removed step was decoration (no token/account, deprecated action version,
   never gated). Strengthening, not weakening.

6. **Behaviour changes beyond formatting** (each recorded in docs/DECISIONS.md or
   docs/qa/SILENT_FAILURES.md): dummy score=85 fabrication removed (fail loud);
   run_test_pipeline exit 1 on failure; alert email failures raise; except-clauses
   narrowed or made loud+logged; F821 `pd` NameError fixed (was masked by blind
   except); naive datetimes -> tz-aware in generators.

7. **Data integrity**: tracked `data/` byte-identical (drift guard in CI proves it
   per run; locally `git status --porcelain data/` empty after full suite).

8. **Lockfile/manifest**: no lockfile in this repo (pip, declared ranges);
   pandas floor raised to >=2.2.0 to match the `ME` API the code now requires
   (forward alignment, not a dodge-pin; D-005).

## Verdict

MERGEABLE. No rule-4 violation found. Residual risks accepted and tracked:
mypy gate not wired (documented in D-004, tracked under issue #4), tailwindcss
moderates in web scope (tracked in issue #6).
