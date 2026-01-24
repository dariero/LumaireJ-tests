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

6. **Get labels from linked issue**:
   ```bash
   LABELS=$(gh issue view <issue-number> --repo dariero/lumairej-tests \
     --json labels --jq '[.labels[].name] | join(",")')
   ```

7. **Push branch** if not already pushed:
   ```bash
   git push -u origin <branch-name>
   ```

8. **Create PR** with test report format and inherited labels:
   ```bash
   gh pr create --repo dariero/lumairej-tests \
     --title "[TYPE #issue] Description" \
     --label "$LABELS" \
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

9. **Move issue to AI Review** on the project board (preserves Priority/Size):
   ```bash
   ISSUE_NODE_ID=$(gh issue view <issue-number> --repo dariero/lumairej-tests --json id --jq '.id')

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
     }' -f project="PVT_kwHODR8J4s4A9wbx" -f item="$ITEM_ID" -f field="PVTSSF_lAHODR8J4s4A9wbxzgxXTgM" -f value="61e4505c"

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
   If Priority or Size are null, warn user to set them via project board.

10. **Add PR to project board**:
    ```bash
    gh project item-add 1 --owner dariero --url <pr-url>
    ```

11. **Report PR URL** to user.

## Author
Darie Ro <glicerinn@gmail.com>

## Additional Context
$ARGUMENTS
