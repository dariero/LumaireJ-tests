# Review Pull Request

Review a test automation pull request.

## Arguments
- `$ARGUMENTS` - PR number or URL

## Instructions

1. **Fetch PR details**:
   ```bash
   gh pr view <pr-number> --repo dariero/lumairej-tests
   gh pr diff <pr-number> --repo dariero/lumairej-tests
   gh pr checks <pr-number> --repo dariero/lumairej-tests
   ```

2. **Test Automation Review Checklist**:

   ### Page Object Model (E2E)
   - [ ] Selectors defined as class constants
   - [ ] Methods encapsulate user actions
   - [ ] No direct locator access in tests
   - [ ] Proper wait strategies (expect API, not sleep)

   ### Fixture Scoping
   - [ ] Session scope for expensive resources (playwright, browser)
   - [ ] Function scope for test isolation (page, api_client)
   - [ ] No fixture side effects across tests

   ### Wait Strategies
   - [ ] NO hardcoded `time.sleep()` or `page.wait_for_timeout()`
   - [ ] Use `expect()` assertions with timeouts
   - [ ] Use `wait_for()` with explicit conditions
   - [ ] Timeouts from constants.py, not magic numbers

   ### Test Design
   - [ ] One assertion focus per test (when practical)
   - [ ] Descriptive test names (`test_<action>_<expected>`)
   - [ ] Proper markers applied (@api, @e2e, @smoke, @regression)
   - [ ] Test data from fixtures, not hardcoded

   ### API Tests
   - [ ] Pydantic schema validation for responses
   - [ ] Proper HTTP status code assertions
   - [ ] Request/response structure verified

3. **Check related issue**:
   ```bash
   gh issue view <linked-issue-number> --repo dariero/lumairej-tests
   ```

4. **Run tests locally** (if changes are significant):
   ```bash
   git fetch origin pull/<pr-number>/head:pr-<pr-number>
   git checkout pr-<pr-number>
   pdm run pytest -v
   ```

5. **Make decision** based on review:

   **If APPROVED:**
   ```bash
   gh pr review <pr-number> --repo dariero/lumairej-tests --approve \
     --body "LGTM - Test automation changes look good.

   Verified:
   - [ ] Page Objects follow POM pattern
   - [ ] Fixtures properly scoped
   - [ ] No hardcoded waits
   - [ ] Tests pass locally"
   ```

   Then merge:
   ```bash
   gh pr merge <pr-number> --repo dariero/lumairej-tests --squash --delete-branch
   ```

   **If CHANGES NEEDED:**
   ```bash
   gh pr review <pr-number> --repo dariero/lumairej-tests --request-changes \
     --body "Please address the following:

   - [ ] Issue 1: [specific feedback]
   - [ ] Issue 2: [specific feedback]

   Use \`/fix\` command to address these changes."
   ```

## Common Issues to Flag

| Issue | Example | Fix |
|-------|---------|-----|
| Hardcoded wait | `time.sleep(2)` | Use `expect(locator).to_be_visible()` |
| Magic timeout | `timeout=5000` | Use `DEFAULT_TIMEOUT_MS` constant |
| Direct locator | `page.locator("#id")` in test | Move to Page Object |
| Wrong scope | `@fixture(scope="session")` for page | Use `scope="function"` |
| Missing marker | No `@pytest.mark.api` | Add appropriate marker |

## Author
Darie Ro <glicerinn@gmail.com>

## PR to Review
$ARGUMENTS
