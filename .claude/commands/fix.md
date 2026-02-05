# Fix Post-Review Changes

Handle requested changes after PR review.

<variables>
  <pr_context>$ARGUMENTS</pr_context>
</variables>

<constraints>
- MUST validate that a PR number is available. If $ARGUMENTS is empty, detect from current branch with `gh pr list --head <branch>`. If no PR is found, ask the user for the PR number.
- MUST address every review comment — do NOT skip any.
- MUST run lint and tests before pushing. Do NOT push if tests or linting fail.
- MUST ask user for confirmation before running `git push`.
- MUST NOT use `git add .` or `git add -A`. Stage specific files only.
</constraints>

## Instructions

1. **Determine PR number**: If `$ARGUMENTS` is empty, detect from the current branch:
   ```bash
   gh pr list --repo dariero/lumairej-tests --head $(git branch --show-current) --json number --jq '.[0].number'
   ```
   If no PR is found, ask the user: "Which PR number should I fix?"

2. **Fetch latest review feedback**:
   ```bash
   gh pr view <pr-number> --repo dariero/lumairej-tests
   gh pr checks <pr-number> --repo dariero/lumairej-tests
   ```

3. **Display requested changes** from the review to the user clearly.

4. **Implement fixes based on review feedback**:
   - Analyze each requested change from step 2.
   - For each change, locate the relevant file and apply the fix.
   - If a requested change is ambiguous or requires architectural decisions, ask the user for clarification before proceeding.

5. **Run quality checks**:
   ```bash
   pdm run lint
   pdm run pytest -v --tb=short
   ```
   If lint errors are found, ask the user: "Lint errors found. Run `pdm run fix` to auto-fix?"
   If tests fail, report failures and do NOT proceed to push.

6. **Create fix commit**:
   - Extract issue number from branch
   - Determine commit type from branch prefix
   - Create commit with descriptive message:
     ```bash
     git add <changed-files>
     git commit -m "fix(tests): address review feedback (#<issue>)

     - Fixed: [specific change 1]
     - Fixed: [specific change 2]

     Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
     ```

7. **Push changes** (requires user confirmation):
   Ask the user: "Ready to push changes to the remote branch?"
   Only push if the user confirms:
   ```bash
   git push
   ```

8. **Notify reviewer**:
   ```bash
   gh pr comment <pr-number> --repo dariero/lumairej-tests \
     --body "Review feedback addressed:
   - [x] Change 1
   - [x] Change 2

   Ready for re-review."
   ```

9. **Report** to user: "Changes pushed successfully. PR updated and ready for re-review."

## PR or Context
$ARGUMENTS
