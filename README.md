[![Python 3.14+](https://img.shields.io/badge/Python-3.14+-black.svg)](https://www.python.org/)
[![PyTest](https://img.shields.io/badge/PyTest-blue?logo=pytest)](https://pytest.org/)
[![Playwright](https://img.shields.io/badge/Playwright-lightblue?logo=playwright)](https://playwright.dev/)
[![Allure TestOps](https://img.shields.io/badge/Allure-blueviolet?logo=allure)](https://docs.qameta.io/allure-testops/)

# LumaireJ Test Automation Framework

Dedicated test automation repository for [LumaireJ](https://github.com/darliaro/LumaireJ) - a journaling and mood tracking application.

---

## Testing Strategy

### Test Pyramid

```
        /\
       /  \       E2E Tests (Playwright)
      /----\      UI validation, user journeys
     /      \
    /--------\    API Tests (Requests + Pydantic)
   /          \   Contract testing, business logic
  /------------\
 /              \ Unit Tests (pytest)
/________________\ Isolated component testing
```

| Layer | Framework | Purpose | Current Coverage |
|-------|-----------|---------|------------------|
| **E2E** | Playwright | User journey validation | 3 tests |
| **API** | Requests + Pydantic | Contract & integration testing | 3 tests |
| **Unit** | pytest | Isolated component testing | TBD |

### Test Categories (Markers)

| Marker | Description | Usage |
|--------|-------------|-------|
| `@pytest.mark.smoke` | Critical path tests | Fast feedback, PR gates |
| `@pytest.mark.regression` | Full regression suite | Nightly/release validation |
| `@pytest.mark.api` | API integration tests | Backend contract testing |
| `@pytest.mark.e2e` | End-to-end UI tests | User journey validation |
| `@pytest.mark.journal` | Journal feature tests | Feature-specific grouping |

### Design Patterns

- **Page Object Model (POM)**: E2E tests use encapsulated page objects (`tests/e2e/pages/`)
- **Schema Validation**: API responses validated via Pydantic models (`tests/api/schemas/`)
- **Fixture-Based DI**: Test data and clients injected via pytest fixtures
- **Factory Pattern**: Test data generated using Faker with dataclass factories

---

## Project Structure

```
lumairej-tests/
├── .github/
│   └── workflows/
│       └── ci.yml              # CI/CD pipeline
├── tests/
│   ├── api/
│   │   ├── clients/
│   │   │   └── api_client.py   # HTTP client wrapper
│   │   ├── schemas/
│   │   │   └── journal_schema.py # Pydantic response models
│   │   └── tests/
│   │       └── test_journal_api.py
│   ├── e2e/
│   │   ├── conftest.py         # Playwright fixtures
│   │   ├── pages/
│   │   │   └── journal_page.py # Page Object Model
│   │   └── tests/
│   │       └── test_journaling_ui.py
│   └── shared/
│       ├── constants.py        # Timeout configuration
│       ├── fixtures.py         # Shared pytest fixtures
│       └── test_data.py        # Faker-based data factories
├── conftest.py                 # Root fixture configuration
├── pyproject.toml              # Project config & pytest settings
└── .env.template               # Environment variable template
```

---

## Running Tests

### Prerequisites

1. Install [Python 3.14+](https://www.python.org/downloads/)
2. Install [PDM](https://pdm-project.org/latest/#recommended-installation-method)
3. Install [Allure CLI](https://docs.qameta.io/allure/#_installing_a_commandline) (for reports)

### Initial Setup

```bash
# Install dependencies
pdm install -G dev

# Install Playwright browsers
pdm run playwright install chromium

# Install pre-commit hooks
pdm run pre-commit install

# Configure environment
cp .env.template .env
# Edit .env with your BASE_URL
```

### API Tests

```bash
# Run all API tests
pdm run pytest -m api

# Run smoke tests only
pdm run pytest -m "api and smoke"

# Run with verbose output
pdm run pytest -m api -v
```

### E2E Tests

```bash
# Run all E2E tests
pdm run pytest -m e2e

# Run specific feature tests
pdm run pytest -m "e2e and journal"

# Run headed (visible browser)
CI=false pdm run pytest -m e2e
```

### Full Test Suite

```bash
# Run everything
pdm run test

# Run with Allure results collection
pdm run test-allure
```

---

## Quality Gates

### CI/CD Pipeline

The GitHub Actions workflow enforces the following quality gates:

| Gate | Trigger | Action |
|------|---------|--------|
| **API Tests** | PR to main, dispatch | Must pass for E2E to run |
| **E2E Tests** | After API tests pass | Browser automation validation |
| **Status Report** | On dispatch events | Reports back to main repo |

### Execution Flow

```
┌─────────────────┐
│  Setup Job      │  Checkout, install deps, cache Playwright
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  API Tests      │  Start SUT → Run API tests → Upload results
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  E2E Tests      │  Start SUT → Run E2E tests → Upload results
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Report Status  │  Post commit status back to LumaireJ repo
└─────────────────┘
```

### Local Quality Checks

```bash
# Lint code
pdm run lint

# Auto-fix lint issues
pdm run fix

# Format code
pdm run format
```

---

## Test Reporting

### Allure Reports

```bash
# Generate report from results
pdm run report

# Open report in browser
pdm run open_report
```

### CI Artifacts

Each CI run uploads:
- `allure-report-api/` - API test results
- `allure-report-e2e/` - E2E test results
- `app-logs-*` - SUT (System Under Test) logs

---

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `BASE_URL` | Application base URL | Yes | - |
| `CI` | CI environment flag | No | `false` |
| `DATABASE_URL` | Database connection (CI only) | CI only | - |

### Local Development

```bash
# .env file
BASE_URL=http://localhost:8000
CI=false
```

### GitHub Actions

Configure as repository secrets:
- `BASE_URL` - SUT endpoint URL
- `DATABASE_URL` - Test database connection
- `PAT_FOR_MAIN_REPO` - Token for cross-repo status reporting

---

## Contributing

### Adding New Tests

1. **API Tests**: Add to `tests/api/tests/`, use `@pytest.mark.api`
2. **E2E Tests**: Add to `tests/e2e/tests/`, create Page Objects in `pages/`
3. **Shared Data**: Add fixtures to `tests/shared/test_data.py`

### Test Naming Convention

```python
def test_<action>_<expected_outcome>():
    """Test that <action> results in <expected_outcome>."""
```

### Commit Standards

Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `test:` New test cases or test coverage
- `fix(tests):` Bug fixes in test code
- `refactor(tests):` Test code restructuring
- `ci:` CI/CD pipeline changes
- `chore:` Dependency updates, config changes

---

## Author

**Darie Ro** - [glicerinn@gmail.com](mailto:glicerinn@gmail.com)
