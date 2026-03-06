# Pre-Push Check

Run linting and tests before pushing. Does NOT write Allure results (fast feedback mode).

<meta version="1.1.0" updated="2026-03-06" />

<variables>
  <test_filter>$ARGUMENTS</test_filter>
</variables>

<constraints>
- MUST run linting before tests.
- MUST report all failures with file:line references.
- MUST NOT push code or modify any files unless explicitly running auto-fix.
- MUST NOT write Allure results during this check — use `--override-ini="addopts="` on all pytest calls.
- If lint errors are found, ask the user: "Lint errors found. Run `pdm run fix` to auto-fix?" — only run auto-fix if the user confirms.
- If `$ARGUMENTS` is non-empty, validate it is one of: `api`, `e2e`, `smoke`, `regression`, or a valid file path. If it does not match, ask the user: "Unrecognized test filter '<value>'. Which marker or path should I use?"
</constraints>

## Instructions

1. **Run linting**:
   ```bash
   pdm run lint
   ```
   If errors are found, ask the user: "Lint errors found. Run `pdm run fix` to auto-fix?"
   Only run `pdm run fix` if the user confirms. Re-run lint after auto-fix to verify it passes.

2. **Determine test scope** from `$ARGUMENTS`:

   | `$ARGUMENTS` value | pytest command |
   |--------------------|----------------|
   | _(empty)_          | `pdm run pytest --override-ini="addopts=" -v --tb=short` |
   | `api`              | `pdm run pytest --override-ini="addopts=" -m api -v --tb=short` |
   | `e2e`              | `pdm run pytest --override-ini="addopts=" -m e2e -v --tb=short` |
   | `smoke`            | `pdm run pytest --override-ini="addopts=" -m smoke -v --tb=short` |
   | `regression`       | `pdm run pytest --override-ini="addopts=" -m regression -v --tb=short` |
   | `<file/path>`      | `pdm run pytest --override-ini="addopts=" <path> -v --tb=short` |

3. **Collect tests** (dry run, no Allure):
   ```bash
   pdm run pytest --override-ini="addopts=" --collect-only -q [<filter-if-any>]
   ```
   Report: total collected, breakdown by marker.

4. **Run the test suite** (single invocation):
   ```bash
   pdm run pytest --override-ini="addopts=" [<filter-if-any>] -v --tb=short
   ```

5. **Report results**:

   | Outcome           | Output |
   |-------------------|--------|
   | All pass          | "Ready to push. X tests passed." |
   | Failures          | List each failure: `file.py::test_name — reason (file:line)` |
   | Collection errors | Show import/fixture issue with file:line |

6. **Show git status** for awareness:
   ```bash
   git status
   git diff --stat
   ```

<eval_output>
At completion, output a one-line structured summary:
`CHECK: lint=<PASS|FAIL> tests=<N passed, N failed> scope=<filter|all> ready=<YES|NO>`
</eval_output>

## Test Filter
$ARGUMENTS
