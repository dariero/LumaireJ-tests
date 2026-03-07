# Ship Issue

Commit, lint, test, push, and open a PR in one command.
Absorbs the old `commit`, `check`, and `pr` commands.

<meta version="2.0.0" updated="2026-03-07" />

<variables>
  <commit_description>$ARGUMENTS</commit_description>
</variables>

<constraints>
- MUST verify the current branch is NOT `main`. If on `main`, stop immediately.
- MUST check for an existing PR before proceeding. If one exists, report its URL and stop.
- MUST NOT create a PR if lint or tests fail.
- MUST extract issue number and branch prefix. If prefix is unrecognized, ask — do NOT guess.
- MUST use `git add -u` to stage tracked changes. Never `git add .` or `git add -A`.
- MUST parse actual test output for PR metrics — never hardcode counts.
- MUST NOT proceed if any GraphQL mutation fails — report with manual remediation steps and stop.
- Auto-fix lint errors without asking. Re-run lint to verify clean.
- Push without asking for confirmation (feature branch — low risk).
- Load `.claude/commands/_project-board.md` before board operations.
</constraints>

<!-- Board status used: ai_review = 61e4505c. All other IDs from _project-board.md -->

## Branch Prefix → Commit Type / PR Type

| Branch Prefix | Commit Type        | PR Type    |
|---------------|--------------------|------------|
| `test/`       | `test:`            | `TEST`     |
| `fix/`        | `fix(tests):`      | `FIX`      |
| `infra/`      | `ci:` or `chore:`  | `INFRA`    |
| `refactor/`   | `refactor(tests):` | `REFACTOR` |

If the branch prefix is unrecognized, ask: "Branch prefix '<prefix>' is not recognized. Which type should I use?"

## Instructions

1. **Validate branch**:
   ```bash
   BRANCH=$(git branch --show-current)
   ```
   If on `main`, stop: "Cannot ship from main. Switch to a feature branch first."

2. **Check for existing PR**:
   ```bash
   gh pr list --repo dariero/lumairej-tests \
     --head "$BRANCH" \
     --json number,url --jq '.[0]'
   ```
   If a PR exists, report: "PR already exists: <url>" and stop.

3. **Show current state and stage tracked changes**:
   ```bash
   git status
   git diff --stat
   git add -u
   git diff --staged --stat
   ```
   If `git diff --staged` is empty after `git add -u`, ask: "No staged changes found. Which files should I stage?"
   List any untracked files from `git status` but do NOT auto-stage them — mention them to the user.

4. **Extract issue number** from the branch name:
   ```bash
   ISSUE=$(echo "$BRANCH" | grep -oE '[0-9]+' | head -1)
   ```
   If no issue number is found, ask: "No issue number in branch name. Which issue does this address?"

5. **Determine commit type and PR type** from the branch prefix using the table above.

6. **Lint** (auto-fix without asking):
   ```bash
   pdm run lint
   ```
   If errors found:
   ```bash
   pdm run fix
   git add -u
   pdm run lint
   ```
   If lint still fails after auto-fix, report errors and stop.

7. **Test** (single invocation — capture output for metrics):
   ```bash
   TEST_OUTPUT=$(pdm run pytest --override-ini="addopts=" -v --tb=short 2>&1)
   echo "$TEST_OUTPUT"
   ```
   If tests fail, report each failure with file:line and stop. Do NOT proceed.

8. **Parse test metrics**:
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

9. **Build and create the commit**:
   - If `$ARGUMENTS` is non-empty, use it as the commit description.
   - If empty, derive a concise description from the staged diff.
   - Subject line: `<type>: <description> (#<issue>)`, max 72 chars.
   ```bash
   git commit -m "<type>: <description> (#<issue>)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
   ```
   Verify with `git log -1 --oneline`.

10. **Gather diff info for PR body**:
    ```bash
    git log main..HEAD --oneline
    git diff main...HEAD --stat
    ```

11. **Fetch labels from linked issue**:
    ```bash
    LABELS=$(gh issue view "$ISSUE" --repo dariero/lumairej-tests \
      --json labels --jq '[.labels[].name] | join(",")')
    ```

12. **Push**:
    ```bash
    git push -u origin "$BRANCH"
    ```

13. **Create PR** with test report and review checklist in body:
    ```bash
    gh pr create --repo dariero/lumairej-tests \
      --title "[<TYPE> #$ISSUE] <description>" \
      --label "$LABELS" \
      --assignee dariero \
      --body "## Summary
    $ARGUMENTS

    ## Test Report

    | Metric      | Count    |
    |-------------|----------|
    | Total Tests | $TOTAL   |
    | Passed      | $PASSED  |
    | Failed      | $FAILED  |
    | Skipped     | $SKIPPED |

    ### Tests Added / Modified
    [List specific test functions changed in this PR]

    ## Review Checklist

    ### Page Object Model (E2E)
    - [ ] Selectors defined as class constants, not inline strings in tests
    - [ ] Methods encapsulate user actions
    - [ ] No direct \`page.locator()\` calls in test files
    - [ ] Proper wait strategies — \`expect()\` API, not \`time.sleep()\` or \`wait_for_timeout()\`

    ### Fixture Scoping
    - [ ] Session scope for expensive resources (\`playwright\`, \`browser\`)
    - [ ] Function scope for test isolation (\`page\`, \`api_client\`)
    - [ ] No fixture side effects bleeding across tests

    ### Wait Strategies
    - [ ] No hardcoded \`time.sleep()\` or \`page.wait_for_timeout()\`
    - [ ] \`expect()\` assertions with explicit timeouts
    - [ ] All timeout values reference \`DEFAULT_TIMEOUT_MS\` from \`constants.py\`

    ### Test Design
    - [ ] Descriptive names: \`test_<action>_<expected_outcome>\`
    - [ ] Appropriate markers: \`@pytest.mark.api\` / \`@pytest.mark.e2e\` / \`@pytest.mark.smoke\`
    - [ ] Test data from fixtures, not hardcoded literals

    ### API Tests
    - [ ] Pydantic schema validation for all API responses
    - [ ] HTTP status codes explicitly asserted

    Closes #$ISSUE"
    ```
    Capture the PR URL and number.

14. **Move issue to AI Review on the project board**:
    Load `.claude/commands/_project-board.md` and execute:
    - `get-item-id` with issue number = `$ISSUE`
    - `update-board-status` with `STATUS_OPTION_ID` = `61e4505c` (AI Review)
    - `verify-board-fields` — if Priority or Size are null, warn the user

    If mutation fails:
    > "ERROR: Board update failed. REMEDIATION: Manually move issue #$ISSUE to 'AI Review'
    > at https://github.com/users/dariero/projects/1."

15. **Add PR to project board**:
    ```bash
    gh project item-add 1 --owner dariero --url "<pr-url>"
    ```

16. **Offer merge** (optional — only after CI passes):
    Ask: "PR created. Merge now with squash? (Only do this after CI passes)"
    Only if confirmed:
    ```bash
    gh pr merge "$PR_NUMBER" --repo dariero/lumairej-tests --squash --delete-branch
    ```
    After merge, suggest: "Run `/done` to finalize local cleanup."

17. **Report** PR URL and summary.

<eval_output>
At completion, output a one-line structured summary:
`SHIP: issue=#<N> commit=<hash> lint=<PASS|FAIL> tests=<N>p/<N>f/<N>s pr=<url> board=<AI Review|FAILED>`
</eval_output>

## Commit Description / PR Context
$ARGUMENTS
