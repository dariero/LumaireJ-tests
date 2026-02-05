# Complete Issue

Clean up local environment after PR is merged.

<variables>
  <issue_number>$ARGUMENTS</issue_number>
</variables>

<constraints>
- MUST validate that $ARGUMENTS is a non-empty numeric value. If empty, ask: "Which issue number should I complete?"
- MUST verify the PR is actually merged before proceeding with cleanup.
- MUST NOT run `git branch -D` without explicit user confirmation. Always try `git branch -d` first.
- MUST NOT proceed if any GraphQL mutation fails — report the error and stop.
- If the issue does not exist or is not found, report the error and stop.
</constraints>

<!-- Project board IDs: see _project-board.md for canonical reference -->
<project_board_ids>
  <project_id>PVT_kwHODR8J4s4A9wbx</project_id>
  <status_field>PVTSSF_lAHODR8J4s4A9wbxzgxXTgM</status_field>
  <done_status>caff0873</done_status>
</project_board_ids>

## Instructions

1. **Validate input**: If `$ARGUMENTS` is empty or non-numeric, ask the user: "Which issue number should I complete?"

2. **Verify PR is merged**:
   ```bash
   gh issue view $ARGUMENTS --repo dariero/lumairej-tests
   gh pr list --repo dariero/lumairej-tests --state merged --search "$ARGUMENTS"
   ```
   If no merged PR is found, report: "No merged PR found for issue #$ARGUMENTS. Verify the PR was merged before running this command." and stop.

3. **Switch to main branch**:
   ```bash
   git checkout main
   ```

4. **Pull latest changes**:
   ```bash
   git pull origin main
   ```

5. **Delete local feature branch**:
   ```bash
   git branch -d <branch-name>
   ```
   If this fails because the branch is not fully merged, ask the user: "Branch '<branch-name>' is not fully merged. Force-delete with `git branch -D`?"
   Only run `git branch -D` if the user confirms.

6. **Verify remote branch is deleted** (should be auto-deleted by merge):
   ```bash
   git remote prune origin
   git branch -r
   ```

7. **Move issue to Done** on the project board (preserves Priority/Size):
   ```bash
   ISSUE_NODE_ID=$(gh issue view $ARGUMENTS --repo dariero/lumairej-tests --json id --jq '.id')

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
     }' -f project="PVT_kwHODR8J4s4A9wbx" -f item="$ITEM_ID" -f field="PVTSSF_lAHODR8J4s4A9wbxzgxXTgM" -f value="caff0873"
   ```
   If any GraphQL mutation returns an error, report the error to the user and stop.

   ```bash
   # Verify final state includes Priority and Size
   gh api graphql -f query='
     query($item: ID!) {
       node(id: $item) {
         ... on ProjectV2Item {
           fieldValueByName(name: "Status") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
           fieldValueByName(name: "Priority") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
           fieldValueByName(name: "Size") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
         }
       }
     }' -f item="$ITEM_ID"
   ```

8. **Close the issue** (if not auto-closed by PR merge):
   ```bash
   gh issue close $ARGUMENTS --repo dariero/lumairej-tests
   ```

9. **Run smoke tests** to verify everything still works:
   ```bash
   pdm run pytest -m smoke -v
   ```

10. **Confirm cleanup complete** and report:
    - Issue closed and moved to Done
    - Priority and Size preserved on project board
    - Local branch deleted
    - Main branch updated with merged changes
    - Smoke tests pass
    - Ready to start next issue with `/start-work`

## Issue Number
$ARGUMENTS
