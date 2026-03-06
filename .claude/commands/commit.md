# Create Commit

Create a commit following test automation conventions.

<meta version="1.1.0" updated="2026-03-06" />

<variables>
  <commit_description>$ARGUMENTS</commit_description>
</variables>

<constraints>
- MUST verify there are staged changes before committing. If `git diff --staged` is empty, ask the user what to stage.
- MUST extract the issue number from the branch name. If the branch name does not contain a number, ask the user for the issue number.
- MUST match the branch prefix to the commit type table below. If the prefix is not recognized, ask the user which commit type to use — do NOT guess or invent a type.
- MUST NOT amend previous commits unless the user explicitly requests it.
- MUST NOT use `git add .` or `git add -A`. Stage specific files only.
- MUST quote all shell variables to prevent word splitting (e.g., "$BRANCH" not $BRANCH).
</constraints>

## Branch Prefix → Commit Type

| Branch Prefix  | Commit Type       | Example |
|----------------|-------------------|---------|
| `test/`        | `test:`           | `test: add journal API validation tests (#42)` |
| `fix/`         | `fix(tests):`     | `fix(tests): resolve flaky E2E timeout (#43)` |
| `infra/`       | `ci:` or `chore:` | `ci: parallelize API and E2E jobs (#44)` |
| `refactor/`    | `refactor(tests):`| `refactor(tests): extract common fixtures (#45)` |

If the branch prefix does not match any row, ask the user: "Branch prefix '<prefix>' is not
recognized. Which commit type should I use?" and present the options from the table.

## Instructions

1. **Check current status**:
   ```bash
   git status
   git diff --staged
   ```
   If no changes are staged, ask the user: "No staged changes found. Which files should I stage?"
   Do NOT proceed with an empty commit.

2. **Extract issue number** from the current branch name:
   ```bash
   git branch --show-current
   ```
   Pattern: `<prefix>/<issue-number>-<description>` → extract the number.
   - `test/42-journal-api` → `42`
   - `fix/43-flaky-timeout` → `43`

   If no issue number is found, ask the user for it.

3. **Determine commit type** from the branch prefix using the table above.

4. **Build commit message**:
   - Subject line: `<type>: <description> (#<issue>)`
   - If `$ARGUMENTS` is non-empty, use it as the description.
   - If `$ARGUMENTS` is empty, derive a concise description from the staged diff.
   - Keep subject line ≤ 72 characters.

5. **Create the commit**:
   ```bash
   git commit -m "<type>: <description> (#<issue>)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
   ```

   Examples:
   - `test: add journal entry validation tests (#42)`
   - `fix(tests): increase timeout for slow CI (#43)`
   - `ci: add cross-browser matrix (#44)`

6. **Verify the commit** was created:
   ```bash
   git log -1 --oneline
   ```
   Report the resulting commit hash and subject line.

<eval_output>
At completion, output a one-line structured summary:
`COMMIT: type=<type> issue=#<N> hash=<short-hash> subject="<subject>"`
</eval_output>

## Commit Description
$ARGUMENTS
