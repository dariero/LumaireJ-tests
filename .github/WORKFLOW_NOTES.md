# Workflow Optimization Notes

## Setup Job Removal (Recommended)

The current `setup` job prepares caches but provides no reliability benefit:

### Why Remove It?

1. **No Artifact Output**: The setup job doesn't produce artifacts consumed by downstream jobs
2. **Cache Unreliability**: GitHub Actions caches are not guaranteed across jobs (eviction, race conditions)
3. **Redundant Work**: Test jobs re-install all dependencies regardless of setup job completion
4. **Wasted Resources**: Adds ~5-10 minutes to every workflow run with no value

### How to Remove

1. Delete the entire `setup` job (lines 18-113)
2. Update `test-api` job:
   - Remove `needs: setup`
3. Update `test-e2e` job:
   - Change `needs: [setup, test-api]` to `needs: test-api`

Each test job already self-bootstraps (installs deps, browsers, Allure CLI), so removing setup has no negative impact.

## Additional Workflow Improvements

### Permissions Scoping

The top-level `permissions` has been simplified to `contents: read`. Individual jobs that need additional permissions should declare them at the job level:

```yaml
test-api:
  permissions:
    contents: read
    checks: write  # For dorny/test-reporter
  steps:
    # ...
```

### SUT Checkout Hardening

The `start-sut` composite action now:
- Validates that only `darie/LumaireJ` can be checked out (line 33 reference should be `darie/LumaireJ`, not `${{ github.repository_owner }}/LumaireJ`)
- Checks PID liveness after starting the SUT
- Uses `BASE_URL` env var for health checks instead of hardcoded localhost

Update line 33 in ci.yml:
```yaml
repository: darie/LumaireJ  # Hardcoded for security
```

### Browser Installation Matrix

The setup job installs only `chromium`, but the E2E matrix tests `chromium`, `firefox`, and `webkit`. Since setup is redundant anyway, each E2E job correctly installs its own browser.

If keeping setup job, install all three browsers:
```yaml
run: pdm run playwright install chromium firefox webkit --with-deps
```

## Monitoring & Alerts

Consider adding:
- Slack/email notifications on workflow failures
- Allure TestOps integration for historical test trends
- GitHub Discussions bot to post test summaries
