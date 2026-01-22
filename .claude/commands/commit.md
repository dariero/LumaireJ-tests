# Create Commit

Create a commit following test automation conventions.

## Arguments
- `$ARGUMENTS` - (Optional) Commit message or description of changes

## Instructions

1. **Check current status**:
   ```bash
   git status
   git diff --staged
   ```

2. **Extract issue number** from current branch name:
   - `test/42-description` -> `42`
   - `fix/43-flaky-test` -> `43`

3. **Determine commit type** from branch prefix:

   | Branch Prefix | Commit Prefix | Example |
   |---------------|---------------|---------|
   | `test/` | `test:` | `test: add journal API validation tests` |
   | `fix/` | `fix(tests):` | `fix(tests): resolve flaky E2E timeout` |
   | `infra/` | `ci:` or `chore:` | `ci: parallelize API and E2E jobs` |
   | `refactor/` | `refactor(tests):` | `refactor(tests): extract common fixtures` |

4. **Stage relevant changes** if not already staged:
   ```bash
   git add <files>
   ```

5. **Create commit** with proper format:
   ```bash
   git commit -m "<type>: <description> (#<issue>)

   Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
   ```

   Examples:
   - `test: add journal entry validation tests (#42)`
   - `fix(tests): increase timeout for slow CI (#43)`
   - `ci: add cross-browser matrix (#44)`

6. **Verify commit** was created successfully:
   ```bash
   git log -1 --oneline
   ```

## Commit Message Guidelines

- **test:** New test cases or test coverage
- **fix(tests):** Bug fixes in test code
- **refactor(tests):** Test code restructuring
- **ci:** CI/CD pipeline changes
- **chore:** Dependency updates, config changes

## Author
Darie Ro <glicerinn@gmail.com>

## Commit Description
$ARGUMENTS
