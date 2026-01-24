# Complete Issue

Clean up local environment after PR is merged.

## Arguments
- `$ARGUMENTS` - Issue number

## Instructions

1. **Verify PR is merged**:
   ```bash
   gh issue view <issue-number> --repo dariero/lumairej-tests
   gh pr list --repo dariero/lumairej-tests --state merged --search "<issue-number>"
   ```

2. **Switch to main branch**:
   ```bash
   git checkout main
   ```

3. **Pull latest changes**:
   ```bash
   git pull origin main
   ```

4. **Delete local feature branch**:
   ```bash
   git branch -d <branch-name>
   ```
   If branch not fully merged, use `-D` flag.

5. **Verify remote branch is deleted** (should be auto-deleted by merge):
   ```bash
   git remote prune origin
   git branch -r
   ```

6. **Move issue to Done** on the project board (preserves Priority/Size):
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
     }' -f project="PVT_kwHODR8J4s4A9wbx" -f item="$ITEM_ID" -f field="PVTSSF_lAHODR8J4s4A9wbxzgxXTgM" -f value="caff0873"

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

7. **Close the issue** (if not auto-closed by PR merge):
   ```bash
   gh issue close <issue-number> --repo dariero/lumairej-tests
   ```

8. **Run tests** to verify everything still works:
   ```bash
   pdm run pytest -m smoke -v
   ```

9. **Confirm cleanup complete** and report:
   - Issue closed and moved to Done
   - Priority and Size preserved on project board
   - Local branch deleted
   - Main branch updated with merged changes
   - Smoke tests pass
   - Ready to start next issue with `/start-work`

## Author
Darie Ro <glicerinn@gmail.com>

## Issue Number
$ARGUMENTS
