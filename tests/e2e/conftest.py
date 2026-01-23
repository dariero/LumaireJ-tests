"""Simple E2E test configuration."""

from collections.abc import Generator
from pathlib import Path

import pytest
from playwright.sync_api import Browser, Page, Playwright, sync_playwright


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test outcome for failure handling."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright]:
    """Provide a Playwright instance for the test session."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="function")
def browser(playwright_instance: Playwright, is_ci: bool) -> Generator[Browser]:
    """Provide a browser instance."""
    headless = is_ci
    browser = playwright_instance.chromium.launch(headless=headless)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser: Browser, request: pytest.FixtureRequest) -> Generator[Page]:
    """Provide a new page for each test with failure artifacts capture."""
    context = browser.new_context()
    page = context.new_page()

    # Create artifact directories
    screenshots_dir = Path("screenshots")
    traces_dir = Path("traces")
    screenshots_dir.mkdir(exist_ok=True)
    traces_dir.mkdir(exist_ok=True)

    # Start tracing with screenshots and snapshots
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield page

    # Check if test failed
    test_failed = (
        request.node.rep_call.failed if hasattr(request.node, "rep_call") else False
    )

    if test_failed:
        # Generate safe filename from test name
        test_name = request.node.name
        safe_name = "".join(
            c if c.isalnum() or c in ("-", "_") else "_" for c in test_name
        )

        # Capture screenshot
        screenshot_path = screenshots_dir / f"{safe_name}.png"
        page.screenshot(path=str(screenshot_path))

        # Save trace
        trace_path = traces_dir / f"{safe_name}.zip"
        context.tracing.stop(path=str(trace_path))
    else:
        # Stop tracing without saving if test passed
        context.tracing.stop()

    context.close()
