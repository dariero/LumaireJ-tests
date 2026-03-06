# Create Pull Request

Create a pull request with a live test report summary.

<meta version="1.1.0" updated="2026-03-06" />

<variables>
  <additional_context>$ARGUMENTS</additional_context>
</variables>

<constraints>
- MUST verify the current branch is NOT `main`. If on `main`, stop immediately.
- MUST check for an existing PR before running tests. If one exists, report its URL and stop.
- MUST run lint and tests exactly once before creating the PR. Do NOT create a PR if either fails.
- MUST parse actual test output to populate the PR test report — never hardcode counts.
- MUST match the branch prefix to the PR type table. If unrecognized, ask the user — do NOT guess.
- MUST ask the user for confirmation before running `git push`.
- MUST NOT proceed if any GraphQL mutation fails — report with manual remediation steps and stop.
- Load `.claude/commands/_project-board.md` before executing any board operation.
</constraints>

<!-- Board status used: ai_review = 61e4505c. All other IDs from _project-board.md -->

## Branch Prefix → PR Type

| Branch Prefix | PR Type    |
|---------------|------------|
| `test/`       | `TEST`     |
| `fix/`        | `FIX`      |
| `infra/`      | `INFRA`    |
| `refactor/`   | `REFACTOR` |

If the prefix is unrecognized, ask the user which PR type to use.

## Instructions

1. **Validate branch**:
   ```bash
   git branch --show-current
   ```
   If on `main`, stop: "Cannot create a PR from the main branch. Switch to a feature branch first."

2. **Check for an existing PR**:
   ```bash
   gh pr list --repo dariero/lumairej-tests \
     --head "$(git branch --show-current)" \
     --json number,url --jq '.[0]'
   ```
   If a PR exists, report: "PR already exists: <url>" and stop.

3. **Run quality gate** (single invocation — output captured for metrics):
   ```bash
   pdm run lint
   ```
   If lint fails, report errors and do NOT proceed.

   ```bash
   TEST_OUTPUT=$(pdm run pytest --override-ini="addopts=" -v --tb=short 2>&1)
   echo "$TEST_OUTPUT"
   ```
   If tests fail, report each failure with file:line and do NOT proceed.

4. **Parse test metrics** from captured output:
   ```bash
   PASSED=$(echo "$TEST_OUTPUT" | python3 -c "
   import sys, re; t=sys.stdin.read()
   m=re.search(r'(\d+) passed', t); print(m.group(1) if m else '0')")

   FAILED=$(echo "$TEST_OUTPUT" | python3 -c "
   import sys, re; t=sys.stdin.read()
   m=re.search(r'(\d+) failed', t); print(m.group(1) if m else '0')")

   SKIPPED=$(echo "$TEST_OUTPUT" | python3 -c "
   import sys, re; t=sys.stdin.read()
   m=re.search(r'(\d+) skipped', t); print(m.group(1) if m else '0')")

   TOTAL=$(( PASSED + FAILED + SKIPPED ))
   ```

5. **Gather branch and commit info**:
   ```bash
   BRANCH=$(git branch --show-current)
   git log main..HEAD --oneline
   git diff main...HEAD --stat
   ```

6. **Extract issue number** from branch name (e.g., `test/42-desc` → `42`).
   If none found, ask the user for it.

7. **Determine PR type** from branch prefix using the table above.

8. **Fetch labels from the linked issue**:
   ```bash
   LABELS=$(gh issue view "<issue-number>" --repo dariero/lumairej-tests \
     --json labels --jq '[.labels[].name] | join(",")')
   ```

9. **Push branch** (requires user confirmation):
   Ask: "Ready to push branch '<branch>' to remote?"
   Only if confirmed:
   ```bash
   git push -u origin "$BRANCH"
   ```

10. **Create PR** with live metrics:
    ```bash
    gh pr create --repo dariero/lumairej-tests \
      --title "[<TYPE> #<issue>] <description>" \
      --label "$LABELS" \
      --assignee dariero \
      --body "## Summary
    $ARGUMENTS

    ## Test Report

    | Metric      | Count   |
    |-------------|---------|
    | Total Tests | $TOTAL  |
    | Passed      | $PASSED |
    | Failed      | $FAILED |
    | Skipped     | $SKIPPED|

    ### Tests Added / Modified
    [List specific test functions changed in this PR]

    ## Test Plan
    - [ ] All tests pass locally (\`pdm run pytest\`)
    - [ ] Linting passes (\`pdm run lint\`)
    - [ ] New tests have appropriate markers
    - [ ] Page Objects follow POM pattern (E2E)
    - [ ] Fixtures properly scoped

    Closes #<issue-number>"
    ```
    Capture the PR URL.

11. **Move issue to AI Review on the project board**:
    Load `.claude/commands/_project-board.md` and execute:
    - `get-item-id` with the linked issue number
    - `update-board-status` with `STATUS_OPTION_ID` = `61e4505c` (AI Review)
    - `verify-board-fields` — if Priority or Size are null, warn the user

    If any mutation fails:
    > "ERROR: Board update failed. REMEDIATION: Manually move issue #<N> to 'AI Review'
    > at https://github.com/users/dariero/projects/1."

12. **Add the PR itself to the project board**:
    ```bash
    gh project item-add 1 --owner dariero --url "<pr-url>"
    ```

13. **Report PR URL** and summary to the user.

<eval_output>
At completion, output a one-line structured summary:
`PR: #<N> type=<TYPE> issue=#<issue> tests=<PASSED>p/<FAILED>f/<SKIPPED>s board=<AI Review|FAILED> url=<url>`
</eval_output>

## Additional Context
$ARGUMENTS
