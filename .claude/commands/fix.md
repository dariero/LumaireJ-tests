# Fix Post-Review Changes

Handle requested changes after PR review.

## Arguments
- `$ARGUMENTS` - (Optional) PR number or additional context

## Instructions

1. **Fetch latest review feedback**:
   ```bash
   gh pr view <pr-number> --repo dariero/lumairej-tests
   gh pr checks <pr-number> --repo dariero/lumairej-tests
   ```

2. **Display requested changes** from the review to user clearly.

3. **Guide through fix workflow**:
   - Instruct user: "Make the necessary code changes to address the feedback"
   - Wait for user confirmation that changes are made

4. **Run quality checks**:
   ```bash
   pdm run lint
   pdm run pytest -v --tb=short
   ```
   If lint errors found, offer to run `pdm run fix` to auto-fix.

5. **Create fix commit**:
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

6. **Push changes**:
   ```bash
   git push
   ```

7. **Notify reviewer** (optional):
   ```bash
   gh pr comment <pr-number> --repo dariero/lumairej-tests \
     --body "Review feedback addressed:
   - [x] Change 1
   - [x] Change 2

   Ready for re-review."
   ```

8. **Report** to user: "Changes pushed successfully. PR updated and ready for re-review."

## Author
Darie Ro <glicerinn@gmail.com>

## PR or Context
$ARGUMENTS
