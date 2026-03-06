# Start Work on Issue

Create a branch and begin work on a GitHub issue.

<meta version="1.1.0" updated="2026-03-06" />

<variables>
  <issue_number>$ARGUMENTS</issue_number>
</variables>

<constraints>
- MUST validate that $ARGUMENTS is a non-empty integer. If empty or non-numeric, ask: "Which issue number should I work on?"
- MUST check for uncommitted changes before switching branches. If the working tree is dirty, ask: "You have uncommitted changes. Stash, commit, or abort?"
- MUST NOT create a branch if one with the same name already exists. If it exists, ask: "Branch '<name>' already exists. Switch to it instead?"
- MUST match the issue title prefix to the branch prefix table below. If unrecognized, ask the user — do NOT guess.
- MUST NOT proceed if any GraphQL mutation fails — report with manual remediation steps and stop.
- If the issue does not exist, report the error and stop.
- Load `.claude/commands/_project-board.md` before executing any board operation.
</constraints>

<!-- Board status used: in_progress = 47fc9ee4. Field IDs from _project-board.md -->

## Issue Type → Branch Prefix

| Issue Title Prefix | Branch Prefix |
|--------------------|---------------|
| `[TEST]`           | `test/`       |
| `[BUG]`            | `fix/`        |
| `[INFRA]`          | `infra/`      |
| `[REFACTOR]`       | `refactor/`   |

If the issue title does not match, ask: "Issue type is unclear. Which branch prefix should I use?"
and present the table.

## Instructions

1. **Validate input**: Confirm `$ARGUMENTS` is a non-empty integer.
   If not, ask: "Which issue number should I work on?"

2. **Check for uncommitted changes**:
   ```bash
   git status --porcelain
   ```
   If output is non-empty, ask: "You have uncommitted changes. Stash them, commit them, or abort?"
   Handle accordingly before proceeding.

3. **Fetch issue details**:
   ```bash
   gh issue view "$ARGUMENTS" --repo dariero/lumairej-tests
   ```
   If the issue does not exist, report the error and stop.

4. **Determine branch prefix** from the issue title prefix using the table above.

5. **Ensure main is up to date**:
   ```bash
   git checkout main
   git pull origin main
   ```

6. **Build branch name** from: `<prefix>/<issue-number>-<kebab-case-title>`
   Keep the slug concise (≤ 40 chars total).
   Examples:
   - `test/24-add-auth-api-tests`
   - `fix/25-flaky-journal-e2e`
   - `infra/26-parallel-ci-jobs`
   - `refactor/27-extract-fixtures`

   Check if branch already exists:
   ```bash
   git branch --list "<branch-name>"
   ```
   If it exists, ask: "Branch '<branch-name>' already exists. Switch to it instead?"

7. **Create and checkout the branch**:
   ```bash
   git checkout -b "<branch-name>"
   ```

8. **Move issue to In Progress on the project board**:
   Load `.claude/commands/_project-board.md` and execute in order:
   - `get-item-id` with issue number = `$ARGUMENTS`
   - `update-board-status` with `STATUS_OPTION_ID` = `47fc9ee4` (In Progress)

   If any mutation fails:
   > "ERROR: Board update failed. REMEDIATION: Manually move issue #$ARGUMENTS to 'In Progress'
   > at https://github.com/users/dariero/projects/1. The branch '<branch-name>' was created
   > successfully — you can continue working."

9. **Verify Priority and Size are set**:
   Execute `verify-board-fields` from `_project-board.md`.
   If Priority or Size are null, ask the user to select values and set them using
   `update-board-field` with the appropriate field/option IDs from `_project-board.md`.

10. **Confirm readiness** and summarize:
    - Branch name created and checked out
    - Issue moved to In Progress
    - Priority and Size confirmed or set
    - Issue title, description, and acceptance criteria displayed

<eval_output>
At completion, output a one-line structured summary:
`START: issue=#<N> branch=<branch-name> board=<In Progress|FAILED> priority=<P> size=<S>`
</eval_output>

## Issue Number
$ARGUMENTS
