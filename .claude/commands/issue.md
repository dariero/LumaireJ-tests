# Create New GitHub Issue

Create a new GitHub issue for test automation tasks.

<meta version="2.0.0" updated="2026-03-07" />

<variables>
  <issue_description>$ARGUMENTS</issue_description>
</variables>

<constraints>
- MUST validate that $ARGUMENTS is non-empty. If empty, ask: "What issue should I create? Provide a title or description."
- MUST select the issue type from the table below. If the request does not clearly match a type, ask the user to clarify.
- MUST NOT create an issue without at least one label.
- MUST NOT proceed if any GraphQL mutation fails — report the error with manual remediation steps and stop.
- Default Priority=Medium, Size=M unless overrides are provided in $ARGUMENTS (e.g. `priority:high size:s`).
- Load `.claude/commands/_project-board.md` before executing any board operation.
</constraints>

<!-- Board field IDs: priority=PVTSSF_lAHODR8J4s4A9wbxzgxXT_I, size=PVTSSF_lAHODR8J4s4A9wbxzgxXT_M -->
<!-- All option IDs from _project-board.md -->

## Instructions

1. **Validate input**: If `$ARGUMENTS` is empty, ask: "What issue should I create? Provide a title or description."

2. **Determine issue type** from the request:

   | Type         | Use When                                  | Title Prefix  |
   |--------------|-------------------------------------------|---------------|
   | `[TEST]`     | New test scenario or coverage             | New test case |
   | `[BUG]`      | Test framework bug or flaky test          | Test bug      |
   | `[INFRA]`    | CI/CD, tooling, dependencies              | Infrastructure|
   | `[REFACTOR]` | Test code quality improvement             | Code quality  |

   If the request does not clearly match, ask: "Which issue type fits this request?" and present the table.

3. **Parse priority/size overrides** from `$ARGUMENTS`:
   - Look for `priority:<value>` (critical/high/medium/low) — case-insensitive
   - Look for `size:<value>` (xs/s/m/l/xl) — case-insensitive
   - If not provided, use defaults: **Priority=Medium, Size=M**
   - Strip these tokens from the description before using it as the issue title.

4. **Select the template** for the matched type:

   **`[TEST]` — Test Scenario:**
   ```markdown
   ## Test Scenario
   **Feature:** [Feature being tested]
   **Type:** API / E2E / Both

   ## Test Cases
   - [ ] [Describe test case 1]
   - [ ] [Describe test case 2]

   ## Acceptance Criteria
   - [ ] Tests pass locally (`pdm run pytest`)
   - [ ] Tests pass in CI
   - [ ] Appropriate markers applied (`@pytest.mark.api` / `@pytest.mark.e2e`)
   - [ ] No hardcoded waits (`time.sleep` / `wait_for_timeout`)

   ## Test Data Requirements
   [List data, fixtures, or environment prerequisites]
   ```

   **`[BUG]` — Bug Report:**
   ```markdown
   ## Bug Description
   [What is happening]

   ## Expected Behavior
   [What should happen]

   ## Steps to Reproduce
   1. Run: `pdm run pytest [path/marker] -v`
   2. Observe: [failure description]

   ## Environment
   - Python: 3.14
   - OS: [local / CI]
   - Flaky: Yes / No (if yes, approximate frequency)

   ## Logs / Output
   [Paste relevant pytest output or traceback]
   ```

   **`[INFRA]` — Infrastructure:**
   ```markdown
   ## Summary
   [What needs to change and why]

   ## Affected Components
   - [ ] CI/CD pipeline (`.github/workflows/`)
   - [ ] Dependency / tooling (`pyproject.toml`, `pdm.lock`)
   - [ ] Pre-commit hooks (`.pre-commit-config.yaml`)
   - [ ] Environment configuration (`.env`, `constants.py`)

   ## Acceptance Criteria
   - [ ] CI pipeline passes on all branches
   - [ ] No regressions in existing tests
   - [ ] Documentation updated if behaviour changes

   ## Notes
   [Migration steps, breaking changes, rollback plan]
   ```

   **`[REFACTOR]` — Refactor:**
   ```markdown
   ## Summary
   [What code is being improved and why]

   ## Scope
   - Files affected: [list]
   - Pattern being removed: [e.g., hardcoded waits, duplicated fixtures]
   - Pattern being introduced: [e.g., shared fixtures, constants]

   ## Acceptance Criteria
   - [ ] All existing tests still pass after refactor
   - [ ] No new test logic introduced (pure structural change)
   - [ ] Ruff lint passes

   ## Notes
   [Any risks or edge cases to consider]
   ```

5. **Determine labels** from type and content:

   | Issue Type       | Labels              |
   |------------------|---------------------|
   | `[TEST]` + API   | `API`               |
   | `[TEST]` + E2E   | `E2E`               |
   | `[TEST]` + both  | `API`, `E2E`        |
   | `[BUG]`          | `API` or `E2E` (match test type) |
   | `[INFRA]`        | `infra`             |
   | `[REFACTOR]`     | `infra` (tooling) or test-type labels |

6. **Create the issue**:
   ```bash
   gh issue create --repo dariero/lumairej-tests \
     --title "[TYPE] <description from $ARGUMENTS>" \
     --body "<filled template from step 4>" \
     --label "<labels from step 5>" \
     --assignee dariero
   ```
   Capture the returned issue URL and number.

7. **Set board fields**: Load `.claude/commands/_project-board.md` and execute:
   - `get-item-id` with the new issue number
   - `update-board-field` with `FIELD_ID` = `PVTSSF_lAHODR8J4s4A9wbxzgxXT_I` and the Priority option ID (default: `da944a9c` = Medium)
   - `update-board-field` with `FIELD_ID` = `PVTSSF_lAHODR8J4s4A9wbxzgxXT_M` and the Size option ID (default: `7515a9f1` = M)
   - `verify-board-fields` to confirm both are set

   If any mutation fails, report:
   > "ERROR: Board field update failed. REMEDIATION: Manually set Priority/Size at
   > https://github.com/users/dariero/projects/1 for issue #<N>."

8. **Report** to user:
   - Issue number and URL
   - Type, labels applied
   - Priority and Size set
   - Next step: `/start <issue-number>`

<eval_output>
At completion, output a one-line structured summary:
`ISSUE: #<N> type=<TYPE> labels=<labels> priority=<P> size=<S> url=<url>`
</eval_output>

## User Request
$ARGUMENTS
