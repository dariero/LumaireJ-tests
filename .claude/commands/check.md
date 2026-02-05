# Pre-Push Check

Run linting and tests before pushing.

<variables>
  <test_args>$ARGUMENTS</test_args>
</variables>

<constraints>
- MUST run linting before tests.
- MUST report all failures with file:line references.
- MUST NOT push code or modify any files unless explicitly running auto-fix.
- If lint errors are found, ask the user: "Lint errors found. Run `pdm run fix` to auto-fix?" — only run auto-fix if the user confirms.
</constraints>

## Instructions

1. **Run linting**:
   ```bash
   pdm run lint
   ```
   If errors are found, ask the user: "Lint errors found. Run `pdm run fix` to auto-fix?"
   Only run `pdm run fix` if the user confirms.

2. **Collect tests first** (dry run):
   ```bash
   pdm run pytest --collect-only -q
   ```
   Report: Total tests collected, breakdown by marker (api/e2e).

3. **Run test suite**:
   ```bash
   pdm run pytest -v --tb=short
   ```

   If `$ARGUMENTS` specifies a test path or marker, use the appropriate filter:
   - API only: `pdm run pytest -m api -v`
   - E2E only: `pdm run pytest -m e2e -v`
   - Smoke only: `pdm run pytest -m smoke -v`

4. **Report results**:

   | Status | Message |
   |--------|---------|
   | All pass | "Ready to push" |
   | Failures | List specific failures with file:line references |
   | Collection errors | Show import/fixture issues |

5. **Show git status** for awareness:
   ```bash
   git status
   git diff --stat
   ```

## Test Arguments
$ARGUMENTS
