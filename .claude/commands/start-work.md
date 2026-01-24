# Start Work on Issue

Create a branch and begin work on a GitHub issue.

## Arguments
- `$ARGUMENTS` - Issue number (e.g., "42" or "#42")

## Instructions

1. **Fetch issue details**:
   ```bash
   gh issue view <issue-number> --repo dariero/lumairej-tests
   ```

2. **Determine branch prefix** from issue title:

   | Issue Type | Branch Prefix |
   |------------|---------------|
   | `[TEST]` | `test/` |
   | `[BUG]` | `fix/` |
   | `[INFRA]` | `infra/` |
   | `[REFACTOR]` | `refactor/` |

3. **Ensure main is up to date**:
   ```bash
   git checkout main && git pull origin main
   ```

4. **Create and checkout branch**:
   ```bash
   git checkout -b <prefix>/<issue-number>-<short-description>
   ```
   Examples:
   - `test/24-add-auth-api-tests`
   - `fix/25-flaky-journal-e2e`
   - `infra/26-parallel-ci-jobs`

5. **Move issue to In Progress** on the project board:
   ```bash
   # Get issue node ID
   ISSUE_NODE_ID=$(gh issue view <issue-number> --repo dariero/lumairej-tests --json id --jq '.id')

   # Add to project and get item ID
   ITEM_ID=$(gh api graphql -f query='
     mutation($project: ID!, $content: ID!) {
       addProjectV2ItemById(input: {projectId: $project, contentId: $content}) {
         item { id }
       }
     }' -f project="PVT_kwHODR8J4s4A9wbx" -f content="$ISSUE_NODE_ID" --jq '.data.addProjectV2ItemById.item.id')

   # Move to In Progress (Status field only - preserves Priority/Size)
   gh api graphql -f query='
     mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {
       updateProjectV2ItemFieldValue(input: {projectId: $project, itemId: $item, fieldId: $field, value: {singleSelectOptionId: $value}}) {
         projectV2Item { id }
       }
     }' -f project="PVT_kwHODR8J4s4A9wbx" -f item="$ITEM_ID" -f field="PVTSSF_lAHODR8J4s4A9wbxzgxXTgM" -f value="47fc9ee4"
   ```

6. **Verify Priority and Size are set** (if missing, set them now):
   ```bash
   # Check current Priority and Size values
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

   If Priority or Size are null, prompt user and set them:
   ```bash
   # Set Priority (choose one): Critical: 79628723 | High: 0a877460 | Medium: da944a9c | Low: 56c1c445
   gh api graphql -f query='
     mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {
       updateProjectV2ItemFieldValue(input: {projectId: $project, itemId: $item, fieldId: $field, value: {singleSelectOptionId: $value}}) {
         projectV2Item { id }
       }
     }' -f project="PVT_kwHODR8J4s4A9wbx" -f item="$ITEM_ID" -f field="PVTSSF_lAHODR8J4s4A9wbxzgxXT_I" -f value="<priority-option-id>"

   # Set Size (choose one): XS: 6c6483d2 | S: f784b110 | M: 7515a9f1 | L: 817d0097 | XL: db339eb2
   gh api graphql -f query='
     mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {
       updateProjectV2ItemFieldValue(input: {projectId: $project, itemId: $item, fieldId: $field, value: {singleSelectOptionId: $value}}) {
         projectV2Item { id }
       }
     }' -f project="PVT_kwHODR8J4s4A9wbx" -f item="$ITEM_ID" -f field="PVTSSF_lAHODR8J4s4A9wbxzgxXT_M" -f value="<size-option-id>"
   ```

7. **Confirm** the branch is ready and summarize:
   - Branch name created
   - Issue moved to In Progress
   - Priority and Size confirmed/set
   - Issue summary and acceptance criteria

## Author
Darie Ro <glicerinn@gmail.com>

## Issue Number
$ARGUMENTS
