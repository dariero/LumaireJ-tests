# Review Pull Request

Review a test automation pull request.

<variables>
  <pr_number>$ARGUMENTS</pr_number>
</variables>

<constraints>
- MUST validate that $ARGUMENTS contains a PR number. If empty, ask: "Which PR number should I review?"
- MUST evaluate every item in the review checklist before making a decision.
- MUST NOT merge a PR without explicit user confirmation. Always ask before merging.
- MUST NOT approve a PR if any checklist item fails — request changes instead.
- MUST NOT proceed if any GraphQL mutation fails — report the error and stop.
- MUST run tests locally for ALL PRs before making a decision.
- When extracting issue numbers from the PR body, use only the first match from `Closes #XX`.
</constraints>

<!-- Project board IDs: see _project-board.md for canonical reference -->
<project_board_ids>
  <project_id>PVT_kwHODR8J4s4A9wbx</project_id>
  <status_field>PVTSSF_lAHODR8J4s4A9wbxzgxXTgM</status_field>
  <approved_status>df73e18b</approved_status>
</project_board_ids>

## Instructions

1. **Validate input**: If `$ARGUMENTS` is empty or non-numeric, ask the user: "Which PR number should I review?"

2. **Fetch PR details**:
   ```bash
   gh pr view <pr-number> --repo dariero/lumairej-tests
   gh pr diff <pr-number> --repo dariero/lumairej-tests
   gh pr checks <pr-number> --repo dariero/lumairej-tests
   ```
   If the PR does not exist, report the error and stop.

3. **Test Automation Review Checklist** — evaluate every item:

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

4. **Check related issue**:
   ```bash
   gh issue view <linked-issue-number> --repo dariero/lumairej-tests
   ```

5. **Run tests locally**:
   ```bash
   git fetch origin pull/<pr-number>/head:pr-<pr-number>
   git checkout pr-<pr-number>
   pdm run pytest -v
   ```

6. **Make decision** based on review:

   **If ALL checklist items pass — APPROVE:**
   ```bash
   gh pr review <pr-number> --repo dariero/lumairej-tests --approve \
     --body "LGTM - Test automation changes look good.

   Verified:
   - [x] Page Objects follow POM pattern
   - [x] Fixtures properly scoped
   - [x] No hardcoded waits
   - [x] Tests pass locally"
   ```

   Move linked issue to Approved status (preserves Priority/Size):
   ```bash
   # Extract first issue number only from PR body
   ISSUE_NUMBER=$(gh pr view <pr-number> --repo dariero/lumairej-tests --json body --jq '.body' | grep -oE 'Closes #[0-9]+' | head -1 | grep -oE '[0-9]+')

   ISSUE_NODE_ID=$(gh issue view $ISSUE_NUMBER --repo dariero/lumairej-tests --json id --jq '.id')

   ITEM_ID=$(gh api graphql -f query='
     mutation($project: ID!, $content: ID!) {
       addProjectV2ItemById(input: {projectId: $project, contentId: $content}) {
         item { id }
       }
     }' -f project="PVT_kwHODR8J4s4A9wbx" -f content="$ISSUE_NODE_ID" --jq '.data.addProjectV2ItemById.item.id')

   # Update Status only - Priority and Size are preserved
   gh api graphql -f query='
     mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {
       updateProjectV2ItemFieldValue(input: {projectId: $project, itemId: $item, fieldId: $field, value: {singleSelectOptionId: $value}}) {
         projectV2Item { id }
       }
     }' -f project="PVT_kwHODR8J4s4A9wbx" -f item="$ITEM_ID" -f field="PVTSSF_lAHODR8J4s4A9wbxzgxXTgM" -f value="df73e18b"

   # Verify Priority and Size are still set
   gh api graphql -f query='
     query($item: ID!) {
       node(id: $item) {
         ... on ProjectV2Item {
           fieldValueByName(name: "Priority") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
           fieldValueByName(name: "Size") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
         }
       }
     }' -f item="$ITEM_ID"
   ```
   If any GraphQL mutation fails, report the error to the user and stop.

   **Merge requires explicit user confirmation.**
   Ask the user: "PR #<pr-number> is approved. Merge with squash and delete the branch?"
   Only if the user confirms:
   ```bash
   gh pr merge <pr-number> --repo dariero/lumairej-tests --squash --delete-branch
   ```
   NEVER merge without user confirmation.

   After merge, suggest: "Run `/complete-issue <issue-number>` to finalize cleanup."

   **If ANY checklist item fails — REQUEST CHANGES:**
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

## PR to Review
$ARGUMENTS
