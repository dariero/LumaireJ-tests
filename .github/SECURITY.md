# Security Configuration

## GitHub Secrets

The following secrets must be configured in GitHub Settings → Secrets and Variables → Actions:

### Required Secrets

1. **`BASE_URL`**
   - Description: Base URL of the System Under Test (SUT)
   - Example: `http://localhost:8000`
   - Required for: All test runs

2. **`DATABASE_URL`**
   - Description: Database connection string for test database
   - Example: `postgresql://user:pass@localhost:5432/test_db`
   - Required for: CI test runs only

3. **`PAT_FOR_MAIN_REPO`**
   - Description: Personal Access Token for cross-repo commit status reporting
   - **Minimum Required Scope**: `repo:status` on `darie/LumaireJ` repository only
   - **Token Type**: Fine-grained personal access token (recommended) or Classic PAT
   - **Setup Instructions**:
     1. Go to GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens
     2. Create a new token with:
        - Repository access: Only select repositories → `darie/LumaireJ`
        - Permissions: Commit statuses → Read and write
     3. Add the token as a repository secret named `PAT_FOR_MAIN_REPO`
   - Required for: Cross-repo status reporting from `repository_dispatch` events

4. **`DISPATCH_SECRET`** (Optional but recommended)
   - Description: Shared secret for authenticating `repository_dispatch` webhook events
   - Generate with: `openssl rand -hex 32`
   - Purpose: Prevents unauthorized actors from triggering test workflows
   - **Setup Instructions**:
     1. Generate a secure random string: `openssl rand -hex 32`
     2. Add it as a repository secret named `DISPATCH_SECRET`
     3. Configure the calling repository (LumaireJ) to include this secret in `client_payload.secret`
   - Required for: Production use (to prevent unauthorized dispatch events)

## Security Best Practices

### GitHub Actions

1. **Action Version Pinning**: All GitHub Actions are pinned to specific commit SHAs (not mutable tags) to prevent supply-chain attacks. Dependabot can be configured to keep these updated.

2. **Input Validation**: The `repository_dispatch` handler validates the SHA format before using it in API calls.

3. **Repository Restriction**: The `start-sut` composite action only allows checking out `darie/LumaireJ` and rejects any other repository input.

4. **Least Privilege Permissions**: Workflow permissions are scoped to job-level where possible.

### Environment Variables

1. **BASE_URL Validation**: The test framework fails fast if `BASE_URL` is not set, preventing accidental routing to unintended hosts.

2. **No Hardcoded Credentials**: No credentials, tokens, or sensitive URLs are hardcoded in the codebase.

### Dependencies

All dependencies specify minimum version constraints to avoid known vulnerabilities. Run `pdm update` periodically to keep dependencies current.

## Reporting Security Issues

If you discover a security vulnerability, please email the maintainer directly at [glicerinn@gmail.com](mailto:glicerinn@gmail.com) instead of creating a public issue.
