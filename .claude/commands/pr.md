# Create Pull Request

Create a pull request with test report summary.

<variables>
  <additional_context>$ARGUMENTS</additional_context>
</variables>

<constraints>
- MUST verify the current branch is NOT `main`. If on `main`, stop and report: "Cannot create a PR from the main branch."
- MUST run lint and tests before creating the PR. Do NOT create a PR if tests or linting fail.
- MUST check if a PR already exists for this branch. If one exists, report the existing PR URL and stop.
- MUST match the branch prefix to the PR type table. If the prefix is not recognized, ask the user which PR type to use — do NOT guess.
- MUST ask user for confirmation before running `git push`.
- MUST NOT proceed if any GraphQL mutation fails — report the error and stop.
</constraints>

<!-- Project board IDs: see _project-board.md for canonical reference -->
<project_board_ids>
  <project_id>PVT_kwHODR8J4s4A9wbx</project_id>
  <status_field>PVTSSF_lAHODR8J4s4A9wbxzgxXTgM</status_field>
  <ai_review_status>61e4505c</ai_review_status>
</project_board_ids>

## Instructions

1. **Validate branch**: Verify the current branch is not `main`:
   ```bash
   git branch --show-current
   ```
   If on `main`, stop and report: "Cannot create a PR from the main branch. Switch to a feature branch first."

2. **Check for existing PR**:
   ```bash
   gh pr list --repo dariero/lumairej-tests --head $(git branch --show-current) --json number,url --jq '.[0]'
   ```
   If a PR already exists, report: "PR already exists: <url>" and stop.

3. **Run code quality checks** before creating PR:
   ```bash
   pdm run lint
   pdm run pytest -v --tb=short
   ```
   If lint or tests fail, report failures and do NOT proceed.

4. **Collect test metrics**:
   ```bash
   pdm run pytest --collect-only -q 2>/dev/null | tail -1
   pdm run pytest -v --tb=no 2>&1 | grep -E "passed|failed|skipped|error"
   ```

5. **Get branch and issue info**:
   ```bash
   git branch --show-current
   git log main..HEAD --oneline
   git diff main...HEAD --stat
   ```

6. **Extract issue number** from branch name (e.g., `test/42-description` -> `42`).
   If no issue number is found, ask the user for it.

7. **Determine PR type** from branch prefix:

   | Branch Prefix | PR Type |
   |---------------|---------|
   | `test/` | `TEST` |
   | `fix/` | `FIX` |
   | `infra/` | `INFRA` |
   | `refactor/` | `REFACTOR` |

   If the branch prefix does not match any row, ask the user: "Branch prefix '<prefix>' is not recognized. Which PR type should I use?" and present the options.

8. **Get labels from linked issue**:
   ```bash
   LABELS=$(gh issue view <issue-number> --repo dariero/lumairej-tests \
     --json labels --jq '[.labels[].name] | join(",")')
   ```

9. **Push branch** (requires user confirmation):
   Ask the user: "Ready to push branch '<branch-name>' to remote?"
   Only push if the user confirms:
   ```bash
   git push -u origin <branch-name>
   ```

10. **Create PR** with test report format and inherited labels:
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

11. **Move issue to AI Review** on the project board (preserves Priority/Size):
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
    If any GraphQL mutation fails, report the error to the user and stop.
    If Priority or Size are null, warn the user to set them via the project board.

12. **Add PR to project board**:
    ```bash
    gh project item-add 1 --owner dariero --url <pr-url>
    ```

13. **Report PR URL** to user.

## Additional Context
$ARGUMENTS
