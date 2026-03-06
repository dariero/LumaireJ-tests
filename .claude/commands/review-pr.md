# Review Pull Request

Review a test automation pull request, run tests locally, then approve or request changes.

<meta version="1.1.0" updated="2026-03-06" />

<variables>
  <pr_number>$ARGUMENTS</pr_number>
</variables>

<constraints>
- MUST validate that $ARGUMENTS is a non-empty integer. If empty or non-numeric, ask: "Which PR number should I review?"
- MUST evaluate every item in the review checklist before making a decision.
- MUST record the current branch before checking out the PR branch. MUST return to it and delete the temp branch after testing.
- MUST NOT merge without explicit user confirmation. Always ask first.
- MUST NOT approve if any checklist item fails — request changes instead.
- MUST NOT proceed if any GraphQL mutation fails — report with manual remediation and stop.
- When extracting the linked issue number, use only the first match from `Closes #XX` in the PR body.
- Load `.claude/commands/_project-board.md` before executing any board operation.
</constraints>

<!-- Board status used: approved = df73e18b. All other IDs from _project-board.md -->

## Instructions

1. **Validate input**: Confirm `$ARGUMENTS` is a non-empty integer.
   If not, ask: "Which PR number should I review?"

2. **Save the current branch**:
   ```bash
   ORIGINAL_BRANCH=$(git branch --show-current)
   ```

3. **Fetch PR details**:
   ```bash
   gh pr view "$ARGUMENTS" --repo dariero/lumairej-tests --json title,body,author,labels,reviews
   gh pr diff "$ARGUMENTS" --repo dariero/lumairej-tests
   gh pr checks "$ARGUMENTS" --repo dariero/lumairej-tests
   ```
   If the PR does not exist, report the error and stop.

4. **Evaluate the checklist** — every item must be assessed:

   ### Page Object Model (E2E only)
   - [ ] Selectors defined as class constants (not inline strings in tests)
   - [ ] Methods encapsulate user actions
   - [ ] No direct `page.locator()` calls in test files
   - [ ] Proper wait strategies — `expect()` API, not `time.sleep()` or `wait_for_timeout()`

   ### Fixture Scoping
   - [ ] Session scope for expensive resources (`playwright`, `browser`)
   - [ ] Function scope for test isolation (`page`, `api_client`)
   - [ ] No fixture side effects that bleed across tests

   ### Wait Strategies
   - [ ] NO hardcoded `time.sleep()` or `page.wait_for_timeout()`
   - [ ] `expect()` assertions used with explicit timeouts
   - [ ] `wait_for()` uses explicit state conditions
   - [ ] All timeout values reference constants from `constants.py`, not magic numbers

   ### Test Design
   - [ ] Descriptive test names: `test_<action>_<expected_outcome>`
   - [ ] Appropriate markers applied: `@pytest.mark.api` / `@pytest.mark.e2e` / `@pytest.mark.smoke`
   - [ ] Test data sourced from fixtures, not hardcoded literals

   ### API Tests
   - [ ] Pydantic schema validation for all API responses
   - [ ] HTTP status codes explicitly asserted
   - [ ] Request/response structure verified

5. **Check the linked issue**:
   ```bash
   ISSUE_NUMBER=$(gh pr view "$ARGUMENTS" --repo dariero/lumairej-tests \
     --json body --jq '.body' | grep -oE 'Closes #[0-9]+' | head -1 | grep -oE '[0-9]+')
   gh issue view "$ISSUE_NUMBER" --repo dariero/lumairej-tests
   ```

6. **Run tests on the PR branch** — then restore state unconditionally:
   ```bash
   git fetch origin "pull/$ARGUMENTS/head:pr-$ARGUMENTS"
   git checkout "pr-$ARGUMENTS"

   pdm run pytest --override-ini="addopts=" -v --tb=short
   TEST_EXIT=$?

   # ALWAYS restore — run this even if tests fail
   git checkout "$ORIGINAL_BRANCH"
   git branch -d "pr-$ARGUMENTS"
   ```
   If `TEST_EXIT` is non-zero, note the failures. Do not skip the restore step.

7. **Make a decision** based on checklist results and test outcome:

   ---

   **If ALL checklist items pass AND tests pass — APPROVE:**

   ```bash
   gh pr review "$ARGUMENTS" --repo dariero/lumairej-tests --approve \
     --body "LGTM — test automation changes look good.

   Verified:
   - [x] Page Objects follow POM pattern
   - [x] Fixtures properly scoped
   - [x] No hardcoded waits or magic numbers
   - [x] Tests pass locally"
   ```

   Move linked issue to Approved on the project board:
   Load `.claude/commands/_project-board.md` and execute:
   - `get-item-id` with `ISSUE_NUMBER` from step 5
   - `update-board-status` with `STATUS_OPTION_ID` = `df73e18b` (Approved)
   - `verify-board-fields` — if Priority or Size are null, warn the user

   If any mutation fails:
   > "ERROR: Board update failed. REMEDIATION: Manually move issue #<N> to 'Approved'
   > at https://github.com/users/dariero/projects/1."

   **Merge requires explicit user confirmation:**
   Ask: "PR #$ARGUMENTS is approved. Merge with squash and delete the remote branch?"
   Only if confirmed:
   ```bash
   gh pr merge "$ARGUMENTS" --repo dariero/lumairej-tests --squash --delete-branch
   ```
   After merge, suggest: "Run `/complete-issue $ISSUE_NUMBER` to finalize cleanup."

   ---

   **If ANY checklist item fails OR tests fail — REQUEST CHANGES:**

   ```bash
   gh pr review "$ARGUMENTS" --repo dariero/lumairej-tests --request-changes \
     --body "Please address the following before this can be merged:

   - [ ] <specific issue 1 with file:line reference>
   - [ ] <specific issue 2 with file:line reference>

   Run \`/fix $ARGUMENTS\` to address these changes."
   ```

## Common Issues Reference

| Issue | Example | Fix |
|-------|---------|-----|
| Hardcoded wait | `time.sleep(2)` | Use `expect(locator).to_be_visible()` |
| Magic timeout | `timeout=5000` | Use `DEFAULT_TIMEOUT_MS` from `constants.py` |
| Direct locator in test | `page.locator("#id")` in test file | Move to Page Object class |
| Wrong fixture scope | `@pytest.fixture(scope="session")` for `page` | Use `scope="function"` |
| Missing marker | No `@pytest.mark.api` on API test | Add appropriate marker |
| Bare except | `except Exception: return False` | Catch `AssertionError` specifically |

<eval_output>
At completion, output a one-line structured summary:
`REVIEW: pr=#<N> checklist=<PASS|FAIL> tests=<N passed, N failed> decision=<APPROVED|CHANGES_REQUESTED> merged=<YES|NO>`
</eval_output>

## PR to Review
$ARGUMENTS
