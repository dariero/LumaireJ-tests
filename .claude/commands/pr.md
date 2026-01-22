# Create Pull Request

Create a pull request with test report summary.

## Arguments
- `$ARGUMENTS` - (Optional) Additional context for PR description

## Instructions

1. **Ensure code quality** before creating PR:
   ```bash
   pdm run lint
   pdm run pytest -v --tb=short
   ```
   Fix any issues before proceeding.

2. **Collect test metrics**:
   ```bash
   pdm run pytest --collect-only -q 2>/dev/null | tail -1
   pdm run pytest -v --tb=no 2>&1 | grep -E "passed|failed|skipped|error"
   ```

3. **Get branch and issue info**:
   ```bash
   git branch --show-current
   git log main..HEAD --oneline
   git diff main...HEAD --stat
   ```

4. **Extract issue number** from branch name (e.g., `test/42-description` -> `42`)

5. **Determine PR type** from branch prefix:

   | Branch Prefix | PR Type |
   |---------------|---------|
   | `test/` | `TEST` |
   | `fix/` | `FIX` |
   | `infra/` | `INFRA` |
   | `refactor/` | `REFACTOR` |

6. **Push branch** if not already pushed:
   ```bash
   git push -u origin <branch-name>
   ```

7. **Create PR** with test report format:
   ```bash
   gh pr create --repo dariero/lumairej-tests \
     --title "[TYPE #issue] Description" \
     --body "## Summary
   - Change 1
   - Change 2

   ## Test Report

   | Metric | Count |
   |--------|-------|
   | Total Tests | X |
   | Passed | X |
   | Failed | 0 |
   | Skipped | X |

   ### Tests Added/Modified
   - \`test_example_scenario\` - Description
   - \`test_another_case\` - Description

   ## Test Plan
   - [ ] All tests pass locally (\`pdm run test\`)
   - [ ] Linting passes (\`pdm run lint\`)
   - [ ] New tests have appropriate markers
   - [ ] Page Objects follow POM pattern (E2E)
   - [ ] Fixtures properly scoped

   Closes #<issue-number>" \
     --assignee dariero
   ```

8. **Add to project board**:
   ```bash
   gh project item-add 1 --owner dariero --url <pr-url>
   ```

9. **Report PR URL** to user.

## Author
Darie Ro <glicerinn@gmail.com>

## Additional Context
$ARGUMENTS
