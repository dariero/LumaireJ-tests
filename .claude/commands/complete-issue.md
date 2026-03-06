# Complete Issue

Clean up local environment after a PR is merged.

<meta version="1.1.0" updated="2026-03-06" />

<variables>
  <issue_number>$ARGUMENTS</issue_number>
</variables>

<constraints>
- MUST validate that $ARGUMENTS is a non-empty integer. If empty or non-numeric, ask: "Which issue number should I complete?"
- MUST verify the PR is actually merged before any cleanup. If no merged PR is found, stop.
- MUST NOT run `git branch -D` without explicit user confirmation. Always try `git branch -d` first.
- MUST NOT proceed if any board mutation fails — report the inconsistent state with manual remediation steps and stop.
- If the issue does not exist, report the error and stop.
- Load `.claude/commands/_project-board.md` before executing any board operation.
</constraints>

<!-- Board status used: done = caff0873. All other IDs from _project-board.md -->

## Instructions

1. **Validate input**: Confirm `$ARGUMENTS` is a non-empty integer.
   If not, ask: "Which issue number should I complete?"

2. **Verify PR is merged**:
   ```bash
   gh issue view "$ARGUMENTS" --repo dariero/lumairej-tests
   gh pr list --repo dariero/lumairej-tests --state merged --search "#$ARGUMENTS" --json number,url,mergedAt
   ```
   If no merged PR is found, stop:
   > "No merged PR found for issue #$ARGUMENTS. Verify the PR was merged before running this command."

3. **Switch to main and pull latest**:
   ```bash
   git checkout main
   git pull origin main
   ```

4. **Identify and delete the local feature branch**:
   ```bash
   git branch --list "*/$ARGUMENTS-*"
   ```
   If found, try safe delete first:
   ```bash
   git branch -d <branch-name>
   ```
   If this fails because the branch is unmerged locally (rare after a squash merge), ask:
   > "Branch '<branch-name>' is not fully merged locally. Force-delete with `git branch -D`?"
   Only run `git branch -D` if the user confirms.

5. **Prune stale remote refs**:
   ```bash
   git remote prune origin
   git branch -r | grep "$ARGUMENTS"
   ```

6. **Move issue to Done on the project board**:
   Load `.claude/commands/_project-board.md` and execute procedures in order:
   - `get-item-id` with issue number = `$ARGUMENTS`
   - `update-board-status` with `STATUS_OPTION_ID` = `caff0873` (Done)
   - `verify-board-fields` — confirm Status=Done, and that Priority/Size are still set

   If any mutation fails:
   > "ERROR: Board update failed. REMEDIATION: Manually move issue #$ARGUMENTS to Done at
   > https://github.com/users/dariero/projects/1. Local cleanup is complete."
   Stop — do not close the issue automatically.

7. **Close the issue** (idempotent — safe to run even if already closed):
   ```bash
   gh issue close "$ARGUMENTS" --repo dariero/lumairej-tests
   ```

8. **Run smoke tests** to verify main is healthy:
   ```bash
   pdm run pytest --override-ini="addopts=" -m smoke -v --tb=short
   ```

9. **Report completion**:
   - Issue #N closed and moved to Done
   - Priority and Size preserved on project board
   - Local branch deleted
   - Main updated
   - Smoke tests: PASS/FAIL
   - Next step: `/start-work <next-issue-number>`

<eval_output>
At completion, output a one-line structured summary:
`COMPLETE: issue=#<N> branch=<deleted|not-found> board=<Done|FAILED> smoke=<PASS|FAIL>`
</eval_output>

## Issue Number
$ARGUMENTS
