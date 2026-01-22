# Create New GitHub Issue

Create a new GitHub issue for test automation tasks.

## Arguments
- `$ARGUMENTS` - Issue description or title

## Instructions

1. **Determine issue type** by analyzing the request:

   | Type | Description | Title Prefix |
   |------|-------------|--------------|
   | `[TEST]` | New test scenario or coverage | New test case |
   | `[BUG]` | Test framework bug or flaky test | Test bug/flakiness |
   | `[INFRA]` | CI/CD, tooling, dependencies | Infrastructure |
   | `[REFACTOR]` | Test code improvement | Code quality |

2. **Select appropriate template** based on type:

   **For `[TEST]` - Test Scenario:**
   ```markdown
   ## Test Scenario
   **Feature:** [Feature being tested]
   **Type:** API / E2E / Both

   ## Test Cases
   - [ ] Test case 1: [Description]
   - [ ] Test case 2: [Description]

   ## Acceptance Criteria
   - [ ] Tests pass locally
   - [ ] Tests pass in CI
   - [ ] Appropriate markers applied (@pytest.mark.api/e2e/smoke/regression)

   ## Test Data Requirements
   - [Data needed for tests]
   ```

   **For `[BUG]` - Bug Report:**
   ```markdown
   ## Bug Description
   [What's happening]

   ## Expected Behavior
   [What should happen]

   ## Steps to Reproduce
   1. Run: `pdm run pytest -m <marker> -v`
   2. Observe: [failure description]

   ## Environment
   - Python: 3.14
   - OS: [local/CI]
   - Flaky: Yes/No (if yes, frequency)

   ## Logs/Screenshots
   [Attach relevant output]
   ```

3. **Create the issue**:
   ```bash
   gh issue create --repo dariero/lumairej-tests \
     --title "[TYPE] Description" \
     --body "<template content>" \
     --assignee dariero
   ```

4. **Add to project board**:
   ```bash
   gh project item-add 1 --owner dariero --url <issue-url>
   ```

5. **Report the issue number and URL** to the user.

## Author
Darie Ro <glicerinn@gmail.com>

## User Request
$ARGUMENTS
