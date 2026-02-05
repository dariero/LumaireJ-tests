# Project Board Configuration

Canonical reference for GitHub Projects V2 infrastructure IDs.
Referenced by: `start-work`, `complete-issue`, `new-issue`, `pr`, `review-pr` commands.

<project_board>
  <project_id>PVT_kwHODR8J4s4A9wbx</project_id>
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

## Maintenance

When project board fields are reconfigured, update the IDs above and propagate to all referencing command files:

| Command | IDs Used |
|---------|----------|
| `start-work.md` | In Progress status, Priority, Size |
| `complete-issue.md` | Done status |
| `new-issue.md` | Priority, Size |
| `pr.md` | AI Review status |
| `review-pr.md` | Approved status |
