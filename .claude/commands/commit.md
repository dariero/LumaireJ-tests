# Create Commit

Create a commit following test automation conventions.

<variables>
  <commit_description>$ARGUMENTS</commit_description>
</variables>

<constraints>
- MUST verify there are staged changes before committing. If `git diff --staged` is empty, ask the user what to stage.
- MUST extract the issue number from the branch name. If the branch name does not contain a number, ask the user for the issue number.
- MUST match the branch prefix to the commit type table below. If the prefix is not recognized, ask the user which commit type to use — do NOT guess or invent a prefix.
- MUST NOT amend previous commits unless the user explicitly requests it.
- MUST NOT use `git add .` or `git add -A`. Stage specific files only.
</constraints>

## Instructions

1. **Check current status**:
   ```bash
   git status
   git diff --staged
   ```
   If no changes are staged, ask the user: "No staged changes found. Which files should I stage?"
   Do NOT proceed with an empty commit.

2. **Extract issue number** from current branch name:
   - `test/42-description` -> `42`
   - `fix/43-flaky-test` -> `43`

   If no issue number is found in the branch name, ask the user for it.

3. **Determine commit type** from branch prefix:

   | Branch Prefix | Commit Prefix | Example |
   |---------------|---------------|---------|
   | `test/` | `test:` | `test: add journal API validation tests` |
   | `fix/` | `fix(tests):` | `fix(tests): resolve flaky E2E timeout` |
   | `infra/` | `ci:` or `chore:` | `ci: parallelize API and E2E jobs` |
   | `refactor/` | `refactor(tests):` | `refactor(tests): extract common fixtures` |

   If the branch prefix does not match any row, ask the user: "Branch prefix '<prefix>' is not recognized. Which commit type should I use?" and present the options from the table.

4. **Stage relevant changes** if not already staged:
   ```bash
   git add <specific-files>
   ```

5. **Create commit** with proper format:
   ```bash
   git commit -m "<type>: <description> (#<issue>)

   Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
   ```

   Examples:
   - `test: add journal entry validation tests (#42)`
   - `fix(tests): increase timeout for slow CI (#43)`
   - `ci: add cross-browser matrix (#44)`

6. **Verify commit** was created successfully:
   ```bash
   git log -1 --oneline
   ```

## Commit Message Guidelines

- **test:** New test cases or test coverage
- **fix(tests):** Bug fixes in test code
- **refactor(tests):** Test code restructuring
- **ci:** CI/CD pipeline changes
- **chore:** Dependency updates, config changes

## Commit Description
$ARGUMENTS
