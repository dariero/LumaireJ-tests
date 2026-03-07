# Project Board Configuration

Canonical reference for GitHub Projects V2 IDs and reusable board procedures.
Referenced by: `start`, `issue`, `ship`, `fix`, `done`.

<meta version="1.1.0" updated="2026-03-06" />

<project_board>
  <project_id>PVT_kwHODR8J4s4A9wbx</project_id>
  <repo>dariero/lumairej-tests</repo>
  <fields>
    <status>PVTSSF_lAHODR8J4s4A9wbxzgxXTgM</status>
    <priority>PVTSSF_lAHODR8J4s4A9wbxzgxXT_I</priority>
    <size>PVTSSF_lAHODR8J4s4A9wbxzgxXT_M</size>
  </fields>
  <status_options>
    <in_progress>47fc9ee4</in_progress>
    <ai_review>61e4505c</ai_review>
    <approved>df73e18b</approved>
    <done>caff0873</done>
  </status_options>
  <priority_options>
    <critical>79628723</critical>
    <high>0a877460</high>
    <medium>da944a9c</medium>
    <low>56c1c445</low>
  </priority_options>
  <size_options>
    <xs>6c6483d2</xs>
    <s>f784b110</s>
    <m>7515a9f1</m>
    <l>817d0097</l>
    <xl>db339eb2</xl>
  </size_options>
</project_board>

## Reusable Board Procedures

Commands that perform board operations MUST load this file first, then execute the
named procedures below. Substitute `<PLACEHOLDER>` values from the calling command's
context. Stop immediately and report if any step produces an empty result or an error.

---

### Procedure: `get-item-id`

Resolves or creates a board item for a given issue. Stores the result in `$ITEM_ID`.
Run this before any `update-board-*` procedure.

```bash
ISSUE_NODE_ID=$(gh issue view "<ISSUE_NUMBER>" --repo dariero/lumairej-tests \
  --json id --jq '.id')

if [ -z "$ISSUE_NODE_ID" ]; then
  echo "ERROR: Could not resolve node ID for issue #<ISSUE_NUMBER>. Stopping." && exit 1
fi

ITEM_ID=$(gh api graphql -f query='
  mutation($project: ID!, $content: ID!) {
    addProjectV2ItemById(input: {projectId: $project, contentId: $content}) {
      item { id }
    }
  }' \
  -f project="PVT_kwHODR8J4s4A9wbx" \
  -f content="$ISSUE_NODE_ID" \
  --jq '.data.addProjectV2ItemById.item.id')

if [ -z "$ITEM_ID" ]; then
  echo "ERROR: Failed to add issue #<ISSUE_NUMBER> to project board. Stopping." && exit 1
fi
```

---

### Procedure: `update-board-status`

Updates the Status field. Requires `$ITEM_ID` from `get-item-id`.
`<STATUS_OPTION_ID>` is the hex option ID from `<status_options>` above.

```bash
UPDATE_RESULT=$(gh api graphql -f query='
  mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {
    updateProjectV2ItemFieldValue(input: {
      projectId: $project, itemId: $item, fieldId: $field,
      value: {singleSelectOptionId: $value}
    }) { projectV2Item { id } }
  }' \
  -f project="PVT_kwHODR8J4s4A9wbx" \
  -f item="$ITEM_ID" \
  -f field="PVTSSF_lAHODR8J4s4A9wbxzgxXTgM" \
  -f value="<STATUS_OPTION_ID>" \
  --jq '.data.updateProjectV2ItemFieldValue.projectV2Item.id')

if [ -z "$UPDATE_RESULT" ]; then
  echo "ERROR: Status update failed for item $ITEM_ID."
  echo "REMEDIATION: Manually set status on https://github.com/users/dariero/projects/1"
  echo "Stopping — no further automated actions will be taken."
  exit 1
fi
```

---

### Procedure: `update-board-field`

Updates Priority or Size. Requires `$ITEM_ID`.
`<FIELD_ID>` is the priority or size field ID. `<OPTION_ID>` is the chosen hex value.

```bash
gh api graphql -f query='
  mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {
    updateProjectV2ItemFieldValue(input: {
      projectId: $project, itemId: $item, fieldId: $field,
      value: {singleSelectOptionId: $value}
    }) { projectV2Item { id } }
  }' \
  -f project="PVT_kwHODR8J4s4A9wbx" \
  -f item="$ITEM_ID" \
  -f field="<FIELD_ID>" \
  -f value="<OPTION_ID>"
```

---

### Procedure: `verify-board-fields`

Reads current Status, Priority, and Size for a board item. Requires `$ITEM_ID`.
If Priority or Size return null, warn the user and ask them to set values.

```bash
gh api graphql -f query='
  query($item: ID!) {
    node(id: $item) {
      ... on ProjectV2Item {
        fieldValueByName(name: "Status")   { ... on ProjectV2ItemFieldSingleSelectValue { name } }
        fieldValueByName(name: "Priority") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
        fieldValueByName(name: "Size")     { ... on ProjectV2ItemFieldSingleSelectValue { name } }
      }
    }
  }' -f item="$ITEM_ID"
```

---

## Maintenance

To update IDs after a project board reconfiguration: edit the `<project_board>` block
above only. No other command files contain hardcoded board IDs.

| Command       | Status Used  | Fields Used          |
|---------------|--------------|----------------------|
| `start.md`    | `in_progress`| Priority, Size       |
| `ship.md`     | `ai_review`  | —                    |
| `done.md`     | `done`       | —                    |
| `issue.md`    | —            | Priority, Size       |
