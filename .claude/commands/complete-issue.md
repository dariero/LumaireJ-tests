# Complete Issue

Clean up local environment after PR is merged.

## Arguments
- `$ARGUMENTS` - Issue number

## Instructions

1. **Verify PR is merged**:
   ```bash
   gh issue view <issue-number> --repo dariero/lumairej-tests
   gh pr list --repo dariero/lumairej-tests --state merged --search "<issue-number>"
   ```

2. **Switch to main branch**:
   ```bash
   git checkout main
   ```

3. **Pull latest changes**:
   ```bash
   git pull origin main
   ```

4. **Delete local feature branch**:
   ```bash
   git branch -d <branch-name>
   ```
   If branch not fully merged, use `-D` flag.

5. **Verify remote branch is deleted** (should be auto-deleted by merge):
   ```bash
   git remote prune origin
   git branch -r
   ```

6. **Run tests** to verify everything still works:
   ```bash
   pdm run pytest -m smoke -v
   ```

7. **Confirm cleanup complete** and report:
   - Local branch deleted
   - Main branch updated with merged changes
   - Smoke tests pass
   - Ready to start next issue with `/start-work`

## Author
Darie Ro <glicerinn@gmail.com>

## Issue Number
$ARGUMENTS
