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

   # Move to In Progress (Status field)
   gh api graphql -f query='
     mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {
       updateProjectV2ItemFieldValue(input: {projectId: $project, itemId: $item, fieldId: $field, value: {singleSelectOptionId: $value}}) {
         projectV2Item { id }
       }
     }' -f project="PVT_kwHODR8J4s4A9wbx" -f item="$ITEM_ID" -f field="PVTSSF_lAHODR8J4s4A9wbxzgxXTgM" -f value="47fc9ee4"
   ```

6. **Confirm** the branch is ready and summarize:
   - Branch name created
   - Issue moved to In Progress
   - Issue summary and acceptance criteria

## Author
Darie Ro <glicerinn@gmail.com>

## Issue Number
$ARGUMENTS
