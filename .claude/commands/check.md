# Pre-Push Check

Run linting and tests before pushing.

## Arguments
- `$ARGUMENTS` - (Optional) Specific test path, markers, or flags

## Instructions

1. **Run linting**:
   ```bash
   pdm run lint
   ```
   If errors found, offer to run `pdm run fix` to auto-fix.

2. **Collect tests first** (dry run):
   ```bash
   pdm run pytest --collect-only -q
   ```
   Report: Total tests collected, breakdown by marker (api/e2e).

3. **Run test suite**:
   ```bash
   pdm run pytest -v --tb=short
   ```

   For specific test types:
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

## Author
Darie Ro <glicerinn@gmail.com>

## Test Arguments
$ARGUMENTS
