"""Simple E2E test configuration."""

import os
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


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, is_ci: bool) -> Generator[Browser]:
    """Provide a browser instance (session-scoped for performance)."""
    headless = is_ci
    browser_name = os.getenv("BROWSER", "chromium")

    # Get the browser launcher based on browser name
    if browser_name == "firefox":
        browser = playwright_instance.firefox.launch(headless=headless)
    elif browser_name == "webkit":
        browser = playwright_instance.webkit.launch(headless=headless)
    else:  # Default to chromium
        browser = playwright_instance.chromium.launch(headless=headless)

    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser: Browser, request: pytest.FixtureRequest) -> Generator[Page]:
    """Provide a new page for each test with failure artifacts capture."""
    context = browser.new_context()
    page = context.new_page()

    # Create artifact directories with absolute paths
    project_root = Path(__file__).resolve().parent.parent.parent
    screenshots_dir = project_root / "screenshots"
    traces_dir = project_root / "traces"
    screenshots_dir.mkdir(exist_ok=True)
    traces_dir.mkdir(exist_ok=True)

    # Start tracing (sources=True only if TRACE_SOURCES env var is set)
    enable_sources = os.getenv("TRACE_SOURCES", "false").lower() in ("1", "true")
    context.tracing.start(screenshots=True, snapshots=True, sources=enable_sources)

    yield page

    try:
        # Check if test failed
        test_failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else False

        if test_failed:
            # Generate safe filename from test name
            test_name = request.node.name
            safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in test_name)

            # Capture screenshot
            screenshot_path = screenshots_dir / f"{safe_name}.png"
            page.screenshot(path=str(screenshot_path))

            # Save trace
            trace_path = traces_dir / f"{safe_name}.zip"
            context.tracing.stop(path=str(trace_path))
        else:
            # Stop tracing without saving if test passed
            context.tracing.stop()
    finally:
        # Always close context even if artifact capture fails
        context.close()
