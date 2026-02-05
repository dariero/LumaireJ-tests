# Start Work on Issue

Create a branch and begin work on a GitHub issue.

<variables>
  <issue_number>$ARGUMENTS</issue_number>
</variables>

<constraints>
- MUST validate that $ARGUMENTS is a non-empty numeric value. If empty, ask: "Which issue number should I work on?"
- MUST check for uncommitted changes before switching branches. If the working tree is dirty, ask the user whether to stash, commit, or abort.
- MUST NOT create a branch if one with the same name already exists. If it exists, ask: "Branch '<name>' already exists. Switch to it instead?"
- MUST match the issue title prefix to the branch prefix table. If the prefix is not recognized, ask the user which branch prefix to use — do NOT guess.
- MUST NOT proceed if any GraphQL mutation fails — report the error and stop.
- If the issue does not exist, report the error and stop.
</constraints>

<!-- Project board IDs: see _project-board.md for canonical reference -->
<project_board_ids>
  <project_id>PVT_kwHODR8J4s4A9wbx</project_id>
  <status_field>PVTSSF_lAHODR8J4s4A9wbxzgxXTgM</status_field>
  <in_progress_status>47fc9ee4</in_progress_status>
  <priority_field>PVTSSF_lAHODR8J4s4A9wbxzgxXT_I</priority_field>
  <size_field>PVTSSF_lAHODR8J4s4A9wbxzgxXT_M</size_field>
  <priority_options>Critical: 79628723 | High: 0a877460 | Medium: da944a9c | Low: 56c1c445</priority_options>
  <size_options>XS: 6c6483d2 | S: f784b110 | M: 7515a9f1 | L: 817d0097 | XL: db339eb2</size_options>
</project_board_ids>

## Instructions

1. **Validate input**: If `$ARGUMENTS` is empty or non-numeric, ask the user: "Which issue number should I work on?"

2. **Check for uncommitted changes**:
   ```bash
   git status --porcelain
   ```
   If output is non-empty, ask the user: "You have uncommitted changes. Stash them, commit them, or abort?"
   Handle accordingly before proceeding.

3. **Fetch issue details**:
   ```bash
   gh issue view $ARGUMENTS --repo dariero/lumairej-tests
   ```
   If the issue does not exist, report the error and stop.

4. **Determine branch prefix** from issue title:

   | Issue Type | Branch Prefix |
   |------------|---------------|
   | `[TEST]` | `test/` |
   | `[BUG]` | `fix/` |
   | `[INFRA]` | `infra/` |
   | `[REFACTOR]` | `refactor/` |

   If the issue title does not match any prefix, ask the user: "Issue title doesn't match a known type. Which branch prefix should I use?" and present the options.

5. **Ensure main is up to date**:
   ```bash
   git checkout main && git pull origin main
   ```

6. **Create and checkout branch**:
   ```bash
   git checkout -b <prefix>/<issue-number>-<short-description>
   ```
   If the branch already exists, ask the user: "Branch '<name>' already exists. Switch to it instead?"

   Examples:
   - `test/24-add-auth-api-tests`
   - `fix/25-flaky-journal-e2e`
   - `infra/26-parallel-ci-jobs`

7. **Move issue to In Progress** on the project board:
   ```bash
   # Get issue node ID
   ISSUE_NODE_ID=$(gh issue view $ARGUMENTS --repo dariero/lumairej-tests --json id --jq '.id')

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
   If any GraphQL mutation fails, report the error to the user and stop.

8. **Verify Priority and Size are set** (if missing, ask user and set them):
   ```bash
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

   If Priority or Size are null, ask the user to select values and set them:
   ```bash
   # Set Priority: Critical: 79628723 | High: 0a877460 | Medium: da944a9c | Low: 56c1c445
   gh api graphql -f query='
     mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {
       updateProjectV2ItemFieldValue(input: {projectId: $project, itemId: $item, fieldId: $field, value: {singleSelectOptionId: $value}}) {
         projectV2Item { id }
       }
     }' -f project="PVT_kwHODR8J4s4A9wbx" -f item="$ITEM_ID" -f field="PVTSSF_lAHODR8J4s4A9wbxzgxXT_I" -f value="<priority-option-id>"

   # Set Size: XS: 6c6483d2 | S: f784b110 | M: 7515a9f1 | L: 817d0097 | XL: db339eb2
   gh api graphql -f query='
     mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {
       updateProjectV2ItemFieldValue(input: {projectId: $project, itemId: $item, fieldId: $field, value: {singleSelectOptionId: $value}}) {
         projectV2Item { id }
       }
     }' -f project="PVT_kwHODR8J4s4A9wbx" -f item="$ITEM_ID" -f field="PVTSSF_lAHODR8J4s4A9wbxzgxXT_M" -f value="<size-option-id>"
   ```

9. **Confirm** the branch is ready and summarize:
   - Branch name created
   - Issue moved to In Progress
   - Priority and Size confirmed/set
   - Issue summary and acceptance criteria

## Issue Number
$ARGUMENTS
