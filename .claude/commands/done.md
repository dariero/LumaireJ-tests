# Done

Clean up local environment after a PR is merged.

<meta version="2.0.0" updated="2026-03-07" />

<variables>
  <issue_number>$ARGUMENTS</issue_number>
</variables>

<constraints>
- If $ARGUMENTS is empty, infer the issue number from the current branch name. If inference fails, ask: "Which issue number should I complete?"
- MUST verify the PR is actually merged before any cleanup. If no merged PR is found, stop.
- MUST NOT proceed if any board mutation fails — report the inconsistent state with manual remediation steps and stop.
- If the issue does not exist, report the error and stop.
- Load `.claude/commands/_project-board.md` before executing any board operation.
</constraints>

<!-- Board status used: done = caff0873. All other IDs from _project-board.md -->

## Instructions

1. **Resolve issue number**:
   If `$ARGUMENTS` is non-empty, use it.
   If empty, infer from the current branch:
   ```bash
   git branch --show-current | grep -oE '[0-9]+' | head -1
   ```
   If inference returns nothing, ask: "Which issue number should I complete?"

2. **Verify PR is merged**:
   ```bash
   gh issue view "$ISSUE" --repo dariero/lumairej-tests
   gh pr list --repo dariero/lumairej-tests --state merged --search "#$ISSUE" --json number,url,mergedAt
   ```
   If no merged PR is found, stop:
   > "No merged PR found for issue #$ISSUE. Verify the PR was merged before running this command."

3. **Switch to main and pull latest**:
   ```bash
   git checkout main
   git pull origin main
   ```

4. **Identify and delete the local feature branch**:
   ```bash
   git branch --list "*/$ISSUE-*"
   ```
   If found, delete it (safe since the PR is verified merged):
   ```bash
   git branch -d <branch-name>
   ```
   If this fails (e.g., squash merge not recognized locally), force-delete:
   ```bash
   git branch -D <branch-name>
   ```

5. **Prune stale remote refs**:
   ```bash
   git remote prune origin
   ```

6. **Move issue to Done on the project board**:
   Load `.claude/commands/_project-board.md` and execute procedures in order:
   - `get-item-id` with issue number = `$ISSUE`
   - `update-board-status` with `STATUS_OPTION_ID` = `caff0873` (Done)
   - `verify-board-fields` — confirm Status=Done

   If any mutation fails:
   > "ERROR: Board update failed. REMEDIATION: Manually move issue #$ISSUE to Done at
   > https://github.com/users/dariero/projects/1. Local cleanup is complete."
   Stop — do not close the issue automatically.

7. **Close the issue** (idempotent — safe to run even if already closed):
   ```bash
   gh issue close "$ISSUE" --repo dariero/lumairej-tests
   ```

8. **Report completion**:
   - Issue #N closed and moved to Done
   - Local branch deleted
   - Main updated
   - Next step: `/start <next-issue-number>`

<eval_output>
At completion, output a one-line structured summary:
`DONE: issue=#<N> branch=<deleted|not-found> board=<Done|FAILED>`
</eval_output>

## Issue Number (optional — inferred from branch if omitted)
$ARGUMENTS
