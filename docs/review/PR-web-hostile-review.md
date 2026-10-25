# Hostile review: web security PR (issue #6, branch fix/web-cve-upgrades)

Reviewer: same operator, hostile-reviewer mode (rule 11.2). Date: 2026-10-25.

1. **No suppression added**: added-line scan for @ts-ignore/@ts-expect-error/
   eslint-disable/`.skip(`/`|| true`: zero operative hits. The pre-existing
   `|| true` in web/package.json "prepare" (husky install guard for envs without
   devDependencies) is untouched, standard, and outside any gate path.
2. **No rule downgrades**: eslint.config.mjs carries the SAME four custom rule
   severities as the removed .eslintrc.json (all `warn`, as the original author
   declared). The 3 errors that appeared under eslint-config-next@16
   (react-hooks/set-state-in-effect) were FIXED IN CODE, not downgraded:
   useSyncExternalStore for the permission probe, useMemo-derived search
   results, deferred initial poll. 16 remaining warnings are pre-existing
   `any`/img/exhaustive-deps at declared severity (backlog noted in issue #6).
3. **Major upgrade justified**: next 15.5.25 -> 16.4.3 is the audit-declared fix
   for the critical next advisory AND the high postcss advisory (no 15.x fix
   exists). Changelog-level breakage encountered and fixed: Turbopack enforces
   the CSS @import ordering spec (globals.css fixed - the old order was invalid
   CSS), `next lint` removed upstream (eslint wired directly with flat config),
   lint-staged referenced the removed command (fixed; husky hook itself caught
   this by blocking the commit - evidence the hook works).
4. **Verification width**: npm audit --omit=dev = 0 vulnerabilities; tsc --noEmit
   clean; eslint 0 errors; production build exit 0 (all logged in
   docs/qa/artifacts/ZR-005.*.green.log); Vercel preview deployment for the PR
   provides deployed-environment verification before merge.
5. **Deferred, tracked, visible**: tailwindcss 3.x moderate advisories require
   the tailwind 4 major migration (feature-scale); recorded in issue #6 and
   D-notes rather than silently accepted; the audit gate at --audit-level=high
   re-reddens CI automatically if they escalate.

## Verdict
MERGEABLE once CI (python-gates + web-gates + Vercel) green.
