# Fix Post-Review Changes

Address requested changes after a PR review, then push.

<meta version="1.1.0" updated="2026-03-06" />

<variables>
  <pr_number>$ARGUMENTS</pr_number>
</variables>

<constraints>
- MUST resolve a PR number before proceeding. If $ARGUMENTS is empty, detect from the current branch. If no PR is found, ask the user for the PR number.
- MUST address every review comment — do NOT skip any.
- MUST run lint and tests before pushing. Do NOT push if either fails.
- MUST ask the user for confirmation before running `git push`.
- MUST NOT use `git add .` or `git add -A`. Stage specific files only.
- MUST NOT amend previous commits unless the user explicitly requests it.
- Commit body MUST list the actual changes made, not placeholder text.
</constraints>

## Instructions

1. **Resolve PR number**:
   If `$ARGUMENTS` is non-empty, use it directly.
   If empty, detect from the current branch:
   ```bash
   gh pr list --repo dariero/lumairej-tests \
     --head "$(git branch --show-current)" \
     --json number,url --jq '.[0]'
   ```
   If no PR is found, ask: "Which PR number should I fix?"

2. **Fetch latest review feedback**:
   ```bash
   gh pr view "<pr-number>" --repo dariero/lumairej-tests --json title,body,reviews,comments
   gh pr checks "<pr-number>" --repo dariero/lumairej-tests
   ```

3. **Display all requested changes** clearly to the user before implementing anything.
   List each requested change as a numbered item.

4. **Implement fixes** — for each requested change:
   - Locate the relevant file and line.
   - Apply the fix.
   - If a requested change is ambiguous or requires an architectural decision, ask
     the user before proceeding. Do NOT guess intent.

5. **Run quality gate** (single invocation, no Allure):
   ```bash
   pdm run lint
   ```
   If lint errors are found, ask: "Lint errors found. Run `pdm run fix` to auto-fix?"
   Only auto-fix if the user confirms. Re-run lint after to verify clean.

   ```bash
   pdm run pytest --override-ini="addopts=" -v --tb=short
   ```
   If tests fail, report each failure with file:line and do NOT proceed to push.

6. **Extract issue number** from branch name and determine commit type from prefix
   (see commit type table in `commit.md`).

7. **Stage and commit** — list only files actually changed:
   ```bash
   git add <changed-file-1> <changed-file-2> ...
   ```
   Build the commit body from the actual changes implemented in step 4:
   ```bash
   git commit -m "fix(tests): address review feedback (#<issue>)

   - Fixed: <actual change 1 from review>
   - Fixed: <actual change 2 from review>
   - Fixed: <actual change N from review>

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
   ```
   The bullet list MUST reflect the real changes — not placeholder text.

8. **Push** (requires user confirmation):
   Ask: "Ready to push changes to '<branch-name>'?"
   Only if confirmed:
   ```bash
   git push
   ```

9. **Notify reviewer**:
   Build the comment body from the actual changes in step 4:
   ```bash
   gh pr comment "<pr-number>" --repo dariero/lumairej-tests \
     --body "Review feedback addressed:
   - [x] <actual change 1>
   - [x] <actual change 2>
   - [x] <actual change N>

   Ready for re-review."
   ```

10. **Report**: "Changes pushed. PR #<N> updated and ready for re-review."

<eval_output>
At completion, output a one-line structured summary:
`FIX: pr=#<N> changes=<count> lint=<PASS|FAIL> tests=<N passed, N failed> pushed=<YES|NO>`
</eval_output>

## PR Number or Context
$ARGUMENTS
