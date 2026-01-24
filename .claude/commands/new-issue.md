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

3. **Determine labels** based on issue type and content:

   | Issue Type | Labels to Apply |
   |------------|-----------------|
   | `[TEST]` + API tests | `API` |
   | `[TEST]` + E2E tests | `E2E` |
   | `[TEST]` + both | `API`, `E2E` |
   | `[BUG]` + flaky test | `E2E` or `API` (based on test type) |
   | `[INFRA]` | `infra` |
   | `[REFACTOR]` | `infra` (if CI/tooling) or test type labels |

4. **Create the issue with labels**:
   ```bash
   gh issue create --repo dariero/lumairej-tests \
     --title "[TYPE] Description" \
     --body "<template content>" \
     --label "<labels>" \
     --assignee dariero
   ```

   Examples:
   - `--label "infra"` for infrastructure issues
   - `--label "E2E"` for E2E test issues
   - `--label "API"` for API test issues
   - `--label "E2E,infra"` for E2E infrastructure issues

5. **Determine Priority** based on issue urgency:

   | Priority | When to Use |
   |----------|-------------|
   | 🔴 Critical | Blocking issue, CI broken, tests failing in prod |
   | 🟠 High | Important feature, significant flakiness |
   | 🟡 Medium | Normal priority work (default) |
   | 🟢 Low | Nice-to-have, minor improvements |

6. **Estimate Size** based on effort:

   | Size | Effort |
   |------|--------|
   | XS | < 1 hour, trivial fix |
   | S | 1-2 hours, small change |
   | M | Half day, moderate scope (default) |
   | L | Full day, significant work |
   | XL | Multi-day, large feature |

7. **Add to project board and set fields**:
   ```bash
   # Add issue to project
   ISSUE_URL=<issue-url>
   gh project item-add 1 --owner dariero --url $ISSUE_URL

   # Get issue and item IDs for field updates
   ISSUE_NUMBER=<issue-number>
   ISSUE_NODE_ID=$(gh issue view $ISSUE_NUMBER --repo dariero/lumairej-tests --json id --jq '.id')

   ITEM_ID=$(gh api graphql -f query='
     mutation($project: ID!, $content: ID!) {
       addProjectV2ItemById(input: {projectId: $project, contentId: $content}) {
         item { id }
       }
     }' -f project="PVT_kwHODR8J4s4A9wbx" -f content="$ISSUE_NODE_ID" --jq '.data.addProjectV2ItemById.item.id')

   # Set Priority (choose one option ID)
   # Critical: 79628723 | High: 0a877460 | Medium: da944a9c | Low: 56c1c445
   gh api graphql -f query='
     mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {
       updateProjectV2ItemFieldValue(input: {projectId: $project, itemId: $item, fieldId: $field, value: {singleSelectOptionId: $value}}) {
         projectV2Item { id }
       }
     }' -f project="PVT_kwHODR8J4s4A9wbx" -f item="$ITEM_ID" -f field="PVTSSF_lAHODR8J4s4A9wbxzgxXT_I" -f value="<priority-option-id>"

   # Set Size (choose one option ID)
   # XS: 6c6483d2 | S: f784b110 | M: 7515a9f1 | L: 817d0097 | XL: db339eb2
   gh api graphql -f query='
     mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {
       updateProjectV2ItemFieldValue(input: {projectId: $project, itemId: $item, fieldId: $field, value: {singleSelectOptionId: $value}}) {
         projectV2Item { id }
       }
     }' -f project="PVT_kwHODR8J4s4A9wbx" -f item="$ITEM_ID" -f field="PVTSSF_lAHODR8J4s4A9wbxzgxXT_M" -f value="<size-option-id>"
   ```

8. **Report the issue** to the user with:
   - Issue number and URL
   - Priority and Size assigned
   - Labels applied

## Author
Darie Ro <glicerinn@gmail.com>

## User Request
$ARGUMENTS
