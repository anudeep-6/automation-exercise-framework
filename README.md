# automation-exercise-framework

Automation framework for [Automation Exercise](https://automationexercise.com) 
built with Python, Playwright, and pytest.

## Project Description

A robust test automation framework for the Automation Exercise website, implementing both UI and API testing capabilities. The framework follows the Page Object Model (POM) design pattern and supports hybrid testing scenarios that combine UI and API validation.

**Key Features:**
- Page Object Model (POM) architecture with 12+ page objects
- Support for UI, API, and hybrid test scenarios
- Cross-browser testing (Chromium, Firefox, WebKit)
- Parallel test execution with pytest-xdist
- Network interception for API validation during UI tests
- Per-test artifact infrastructure (traces, logs, downloads)
- Custom utilities for config reading, data handling, and decorators
- Allure reporting with step-level documentation
- Browser authentication state persistence
- Modular and scalable design

---

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.12 | Core programming language |
| **Playwright** | >=1.40.0 | Browser automation |
| **pytest** | >=7.4.0 | Testing framework |
| **pytest-playwright** | >=0.4.0 | Playwright plugin for pytest |
| **pytest-xdist** | >=3.5.0 | Parallel test execution |
| **Allure** | >=2.13.0 | Rich test reporting and documentation |
| **Requests** | >=2.31.0 | HTTP client for API testing |

---

## Project Structure

```
automation-exercise-framework/
│
├── .vscode/                    # VS Code workspace settings
│
├── allure-results/             # Allure test report data
│
├── artifacts/                  # Test artifacts and files
│
├── auth/                       # Browser authentication state
│   └── state.json              # Saved browser auth state for reuse
│
├── config/                     # Configuration files
│   └── config.json             # Environment configurations
│
├── docs/                       # Project documentation
│
├── downloads/                  # Downloaded files during tests
│
├── reports/                    # Test execution reports
│
├── scripts/                    # Utility scripts
│   └── save_auth_state.py      # Script to save browser authentication state
│
├── src/
│   ├── pages/                  # Page Object Model classes
│   │   ├── __init__.py
│   │   ├── base_page.py                # Base page with common methods
│   │   ├── account_created_page.py     # Account created confirmation POM
│   │   ├── account_deleted_page.py     # Account deleted confirmation POM
│   │   ├── cart_page.py                # Cart page POM
│   │   ├── checkout_page.py            # Checkout page POM
│   │   ├── contact_us_page.py          # Contact us page POM
│   │   ├── home_page.py                # Home page POM
│   │   ├── login_page.py               # Login/Signup page POM
│   │   ├── order_confirmation_page.py  # Order confirmation page POM
│   │   ├── payment_page.py             # Payment page POM
│   │   ├── product_page.py             # Products page POM
│   │   └── registration_page.py        # Registration page POM
│   │
│   ├── api/                    # API client and helpers
│   │   ├── __init__.py
│   │   └── .gitkeep            # Placeholder for API implementations
│   │
│   └── utils/                  # Utility classes and helpers
│       ├── __init__.py
│       ├── config_reader.py    # Configuration file reader
│       ├── data_reader.py      # Test data reader (CSV, JSON, etc.)
│       ├── decorators.py       # Custom decorators (@retry, @log_test, etc.)
│       ├── exceptions.py       # Custom exceptions
│       └── log_manager.py      # Logging configuration and management
│
├── test_data/                  # Test data files
│   ├── users_test_data.csv                    # User credentials for login/registration tests
│   ├── register_user_test_data.json           # User registration test data
│   ├── product_test_data.json                 # Product information test data
│   ├── payment_test_data.json                 # Payment form test data
│   ├── contact_us_test_data.json              # Contact form test data
│   └── files/
│       └── contact_us_test_upload_file.txt    # Test file for contact form file upload
│
├── tests/
│   ├── conftest.py             # Shared pytest fixtures and configuration
│   │
│   ├── ui/                     # UI automated tests
│   │   ├── __init__.py
│   │   ├── conftest.py         # UI test specific fixtures
│   │   ├── test_auth_state.py  # Browser authentication tests
│   │   ├── test_cart.py        # Shopping cart tests
│   │   ├── test_checkout.py    # Checkout flow tests
│   │   ├── test_contact_us.py  # Contact form tests
│   │   ├── test_login.py       # Login and signup tests
│   │   ├── test_network.py     # Network interception tests
│   │   ├── test_products.py    # Product browsing tests
│   │   └── test_register_user.py # User registration tests
│   │
│   ├── api/                    # API automated tests
│   │   ├── __init__.py
│   │   └── .gitkeep            # Placeholder for API tests
│   │
│   └── hybrid/                 # Combined UI + API tests
│       ├── __init__.py
│       └── .gitkeep            # Placeholder for hybrid tests
│
├── venv/                       # Virtual environment (git ignored)
│
├── .flake8                     # Flake8 linting configuration
├── .gitignore                  # Git ignore rules
├── .pre-commit-config.yaml     # Pre-commit hooks configuration
├── pyproject.toml              # Project metadata and dependencies
├── README.md                   # Project documentation (this file)
└── __init__.py                 # Package initializer
```

---

## Getting Started

### Prerequisites
- Python 3.12
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/anudeep-6/automation-exercise-framework.git
   cd automation-exercise-framework
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # OR if using pyproject.toml
   pip install -e .
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Install Playwright browsers**
   ```bash
   playwright install
   ```

---

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test suites
```bash
pytest tests/ui/                    # UI tests only
pytest tests/api/                   # API tests only
pytest tests/hybrid/                # Hybrid tests only
pytest tests/ui/test_login.py       # Specific test file
pytest tests/ui/test_login.py::test_login_valid_user  # Specific test case
```

### Run tests in parallel
```bash
pytest -n auto                      # Use all CPU cores
pytest -n 4                         # Use 4 workers
```

### Run tests in headed mode (visible browser)
```bash
pytest --headed
```

### Run on specific browser
```bash
pytest --browser firefox
pytest --browser webkit
pytest --browser chromium
```

### Generate Allure reports
```bash
# Run tests and generate Allure results
pytest --alluredir=allure-results

# Open Allure report (requires allure CLI installed)
allure serve allure-results
```

### View test traces and artifacts
```bash
# Traces are automatically recorded for failed tests in allure-results/
# Artifacts (screenshots, logs, downloaded files) are saved per-test in:
# - allure-results/ (Allure attachments)
# - artifacts/ (raw artifacts organized by test)

# View test traces and attachments in Allure report
allure serve allure-results
```

### Run with verbose output
```bash
pytest -v                           # Verbose output
pytest -vv                          # Very verbose (show print statements)
```

### Run with specific markers
```bash
pytest -m "smoke"                   # Run smoke tests only
pytest -m "regression"              # Run regression tests only
pytest -m "not slow"                # Skip slow tests
```

### Debug mode with pdb
```bash
pytest --pdb                        # Drop into debugger on failures
pytest -s                           # Show print statements and logging
```

---

## Utilities & Helpers

### Configuration Management
```python
from src.utils.config_reader import ConfigReader

config = ConfigReader()
base_url = config.base_url
timeout = config.get('timeout')
headless = config.get('headless', default=True)
```

### Test Data Reader
```python
from src.utils.data_reader import DataReader

reader = DataReader()
# Load CSV rows (returns list of dictionaries)
users = reader.load_csv_rows('test_data/users_test_data.csv')
# Load with filtering
admins = reader.load_csv_rows('test_data/users_test_data.csv', filter_by={'role': 'admin'})
```

### Custom Decorators
```python
from src.utils.decorators import retry, log_test

@retry(max_attempts=3, delay=1)
@log_test
def test_with_retry(page):
    """Test will retry up to 3 times on failure"""
    pass
```

### Logging Management
```python
import logging

# Use root logger so child loggers propagate automatically
logger = logging.getLogger()
logger.info("Test started")
logger.debug("Debug information")
logger.error("Error occurred")

# LogManager handles configuration setup (called in conftest)
from src.utils.log_manager import LogManager
LogManager.setup()
```

### Custom Exceptions
```python
from src.utils.exceptions import ConfigurationException, TestDataException

try:
    config = ConfigReader()
except ConfigurationException as e:
    print(f"Configuration error: {e}")
```

### Browser Authentication State
Save and reuse browser authentication sessions:
```bash
# Save authentication state
python scripts/save_auth_state.py

# This script:
# 1. Reads credentials from test_data/users_test_data.csv via DataReader.load_csv_rows()
# 2. Logs in with the first user
# 3. Saves the authenticated browser state to auth/state.json
# 4. State is automatically loaded in conftest.py for faster test execution
```

**Security Note:** Credentials are pulled exclusively from `test_data/users_test_data.csv`, not from `config.json`. This keeps sensitive credentials separate from configuration.

---

## Writing Tests

### UI Test Example
```python
import pytest
from src.pages.home_page import HomePage

@pytest.mark.ui
@pytest.mark.smoke
def test_homepage_title(page, base_url):
    """Test homepage title is correct"""
    home = HomePage(page, base_url)
    home.navigate()
    assert home.get_title() == "Automation Exercise"
```

### Test with Custom Decorators
```python
from src.utils.decorators import retry, log_test

@pytest.mark.ui
@retry(max_attempts=3)
@log_test
def test_flaky_scenario(page, base_url):
    """Test with retry logic and logging"""
    # Your test code here
    pass
```

### Parameterized Test with CSV Data
```python
import pytest
from src.utils.data_reader import DataReader

data_reader = DataReader()
users = data_reader.load_csv_rows('test_data/users_test_data.csv')

@pytest.mark.parametrize("user", users)
def test_login_with_multiple_users(page, base_url, user):
    """Test login with different users from CSV"""
    from src.pages.login_page import LoginPage
    login_page = LoginPage(page, base_url)
    login_page.navigate()
    login_page.login(user['email'], user['password'])
```

### Hybrid Test (UI + API)
```python
def test_register_user_and_verify(page, base_url):
    """Test registers user via UI and verifies registration"""
    from src.pages.registration_page import RegistrationPage
    from src.pages.login_page import LoginPage
    from src.pages.home_page import HomePage
    
    # UI: Register user
    reg_page = RegistrationPage(page, base_url)
    reg_page.navigate()
    reg_page.fill_account_info('Mr', 'password123', '15', '6', '1990')
    reg_page.fill_address_info('John', 'Doe', '123 Main St', 'India', 'TX', 'Austin', '78701', '1234567890')
    reg_page.submit_create_account()
    
    # Verify: Login with same credentials
    login_page = LoginPage(page, base_url)
    login_page.navigate()
    login_page.login('john.doe@example.com', 'password123')
    home_page = HomePage(page, base_url)
    home_page.expect_logged_in()
```

---

## Configuration

### config/config.json
Main configuration file for environment settings:

```json
{
  "base_url": "https://automationexercise.com",
  "timeout": 30000,
  "headless": true,
  "browser": "chromium",
  "slow_mo": 0
}
```

**Configuration Options:**
- `base_url`: Target application URL
- `timeout`: Default timeout in milliseconds for element interactions
- `headless`: Run browser in headless mode (true/false)
- `browser`: Browser engine (chromium/firefox/webkit)
- `slow_mo`: Slow down interactions by N milliseconds (for debugging)

### Accessing Configuration in Tests
```python
from src.utils.config_reader import ConfigReader

config = ConfigReader()
base_url = config.base_url                    # Direct access to base_url
timeout = config.get('timeout')               # Generic access
slow_mo = config.get('slow_mo', default=0)   # With default fallback
```

---

## Page Object Model (POM)

All page classes inherit from `BasePage` and follow the POM pattern:

```python
from src.pages.base_page import BasePage
import allure

class ExamplePage(BasePage):
    """Page object for Example page (/example)."""
    
    PATH = "/example"
    
    # Locators
    SUBMIT_BUTTON = "button[data-qa='submit']"
    SUCCESS_MESSAGE = "div.success"
    
    @allure.step("Click Submit button")
    def click_submit(self):
        """Clicks the submit button."""
        self.click(self.SUBMIT_BUTTON)
    
    @allure.step("Expect success message")
    def expect_success(self):
        """Asserts success message is visible."""
        self.expect_visible(self.SUCCESS_MESSAGE)
```

### Available Page Objects
- **HomePage** - Main landing page and navigation
- **LoginPage** - Login and signup forms
- **RegistrationPage** - User account registration
- **ProductsPage** - Product browsing and search
- **ProductPage** - Individual product details
- **CartPage** - Shopping cart management
- **CheckoutPage** - Order review and address verification
- **PaymentPage** - Card payment details
- **OrderConfirmationPage** - Order confirmation and invoice download
- **ContactUsPage** - Contact form submission
- **AccountCreatedPage** - Account creation confirmation
- **AccountDeletedPage** - Account deletion confirmation

### Base Page Methods
Common methods available to all page objects:

**Navigation & Verification:**
- `navigate()` - Go to the page URL
- `get_title()` - Get page title
- `get_current_url()` - Get current URL

**Interaction:**
- `click(locator)` - Click an element
- `fill(locator, value)` - Fill input field
- `get_text(locator)` - Get element text
- `hover(element)` - Hover over element
- `upload_file(locator, path)` - Upload file

**Assertion:**
- `expect_visible(locator)` - Assert element is visible
- `expect_text(locator, text)` - Assert element has exact text
- `expect_contains_text(locator, text)` - Assert text presence
- `expect_url_contains(fragment)` - Assert URL contains text

---

## Allure Integration

Allure provides detailed test reports with steps and attachments.

### Generate Reports
```bash
# Run tests and generate Allure results
pytest --alluredir=allure-results

# View the report
allure serve allure-results
```

### Add Steps to Tests
```python
import allure

@allure.step("Login with email {email}")
def login(email, password):
    # Test code
    pass

@allure.title("User Login Test")
@allure.description("Verify user can login with valid credentials")
def test_login():
    login("user@example.com", "password")
```

### Attach Files and Screenshots
```python
import allure

@allure.step("Take screenshot")
def take_screenshot(page, filename):
    screenshot = page.screenshot()
    allure.attach.file(
        screenshot,
        name=filename,
        attachment_type=allure.attachment_type.PNG
    )
```

---

## Code Quality

### Linting with Flake8
Check code style and quality:
```bash
# Lint all source and test code
flake8 src/ tests/

# Lint specific file
flake8 src/pages/home_page.py

# Show statistics
flake8 --statistics src/
```

### Pre-commit Hooks
Automatically run quality checks before commits via `.pre-commit-config.yaml`:

**Configured hooks:**
- Trailing whitespace removal
- End-of-file fixer
- YAML syntax checker
- Flake8 linting
- Code formatter (if configured)

**Setup:**
```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files

# Run on specific file
pre-commit run --files src/pages/home_page.py
```

### Code Formatting
Follow PEP 8 standards and project conventions:
- Line length: 88 characters (or configured limit)
- Use type hints where applicable
- Document complex logic with comments
- Write descriptive docstrings (Google format)

### Testing Best Practices
- One assertion per test (or related assertions)
- Descriptive test names: `test_<feature>_<scenario>_<expected_result>`
- Use fixtures for setup/teardown
- Mark tests with appropriate markers (@pytest.mark.ui, @pytest.mark.smoke, etc.)
- Avoid hardcoded waits; use Playwright's auto-waiting

---

## Test Organization

### Test Structure
```
tests/
├── ui/              # UI/end-to-end tests
│   ├── conftest.py  # UI-specific fixtures
│   ├── test_*.py    # Individual test modules
│
├── api/             # API tests
│   ├── conftest.py  # API-specific fixtures
│   ├── test_*.py
│
├── hybrid/          # Tests combining UI + API
│   ├── conftest.py
│   ├── test_*.py
│
└── conftest.py      # Shared fixtures and configuration
```

### Test Markers
Organize tests with pytest markers:
```python
@pytest.mark.ui          # UI tests
@pytest.mark.api         # API tests
@pytest.mark.smoke       # Smoke tests
@pytest.mark.regression  # Regression tests
@pytest.mark.slow        # Slow tests
```

Run by marker:
```bash
pytest -m "smoke"                    # Only smoke tests
pytest -m "not slow"                 # Skip slow tests
pytest -m "smoke and ui"             # Smoke AND UI tests
pytest -m "regression or smoke"      # Regression OR smoke tests
```

---

## Directory Reference

### allure-results/
Generated Allure test results and reports data. Git-ignored.

### artifacts/
Test-generated artifacts (downloads, uploads, etc.). Git-ignored.

### auth/
Stores browser session authentication state (`state.json`). Used to reuse login sessions across tests.

### config/
- `config.json` - Main configuration file (environment settings, timeouts, etc.)

### docs/
Project documentation files and guides.

### downloads/
Files downloaded during test execution. Git-ignored.

### reports/
Generated HTML test reports. Git-ignored.

### scripts/
Utility scripts:
- `save_auth_state.py` - Save authenticated browser session for reuse

### test_data/
Test data files for parameterized and data-driven tests, organized by feature:

- `users_test_data.csv` - User credentials (email, password) for authentication tests
- `register_user_test_data.json` - User registration form data (name, address, phone, etc.)
- `product_test_data.json` - Product details (names, prices, categories) for product tests
- `payment_test_data.json` - Payment card information (number, CVC, expiry) for payment tests
- `contact_us_test_data.json` - Contact form data (names, emails, messages) for contact tests
- `files/contact_us_test_upload_file.txt` - Test file for contact form file upload validation

---

## Fixtures

### Session-Scoped Fixtures (shared across all tests)
- `config_reader` - ConfigReader instance
- `base_url` - Application base URL
- `playwright` - Playwright sync context

### Module/Test-Scoped Fixtures
- `browser_name` - Browser type to test on (set via `--browser` CLI flag, default: chromium)
- `browser` - Browser instance
- `context` - Browser context with cookies/localStorage and authenticated state
- `page` - Individual page/tab in the browser

### Function-Scoped Fixtures
- Custom fixtures defined in conftest.py files

**Note:** The `browser_name` fixture is used instead of plain `browser` to avoid collision with pytest-playwright's built-in `browser` fixture. Tests request `page` and `base_url` which are automatically wired through the fixture dependency chain.

### Creating Custom Fixtures
```python
@pytest.fixture
def authenticated_page(page, base_url):
    """Provides an authenticated page session."""
    from src.pages.login_page import LoginPage
    login_page = LoginPage(page, base_url)
    login_page.navigate()
    login_page.login("test@example.com", "password")
    return page
```

---

## Test Artifacts & Debugging

### Per-Test Artifact Infrastructure
The `per_test_artifacts` autouse fixture (in `tests/ui/conftest.py`) automatically collects and organizes artifacts for each test:

**Trace Files:** Comprehensive Playwright traces for failed tests
```bash
# Located in: allure-results/
# View traces in Allure report with timeline visualization
allure serve allure-results
```

**Test Logs:** Structured per-test logging
```bash
# Located in: artifacts/{test_name}/test.log
# Contains all test-level operations and assertions
```

**Downloads:** Files downloaded during test execution
```bash
# Located in: artifacts/{test_name}/downloads/
# Automatically organized and attached to Allure reports
```

**Screenshots & Attachments:** Test-generated files
```bash
# Located in: artifacts/{test_name}/
# Automatically attached to Allure reports for easy access
```

### Network Interception
Mock or record network requests during UI tests:
```python
@pytest.mark.ui
def test_product_with_network_intercept(page, base_url):
    """Test with network request recording and validation"""
    # Tests can record API calls made by the browser
    # See test_network.py for examples
    pass
```

**Use Cases & Patterns:**
- **Mock API response:** `route.fulfill(status=200, body=json.dumps(data))` - Override API response
- **Block requests:** `route.abort()` - Simulate network errors or test error handling
- **Modify request headers:** `resp = route.fetch(); route.fulfill(response=resp, headers={**resp.headers, "X-Custom": "value"})` - Add auth tokens or custom headers to intercepted requests
- **Record responses:** `page.expect_response(lambda r: "api" in r.url)` - Validate API calls made by frontend

---

### Common Issues

**Issue: Playwright browsers not installed**
```bash
# Solution: Install Playwright browsers
playwright install

# Or specify specific browsers
playwright install chromium firefox
```

**Issue: Config file not found**
```bash
# Ensure config.json exists in config/ directory
# ConfigReader looks for: config/config.json
```

**Issue: Tests running too fast (elements not found)**
```python
# Add explicit waits in conftest.py
@pytest.fixture
def page(context):
    page = context.new_page()
    page.set_default_timeout(30000)  # 30 seconds
    return page
```

**Issue: Flake8 not found**
```bash
# Install flake8
pip install flake8

# Or include in development dependencies
pip install -e ".[dev]"
```

**Issue: Allure command not found**
```bash
# Install Allure CLI
# On Windows: download from https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/
# On macOS: brew install allure
# On Linux: apt-get install allure (or similar)
```

---

## Best Practices

### Test Writing
- ✅ Use descriptive test names
- ✅ One logical assertion per test
- ✅ Use fixtures for setup/teardown
- ✅ Mock external dependencies
- ✅ Add @allure.step decorators for clarity
- ❌ Don't use hardcoded waits (page.wait_for_timeout)
- ❌ Don't share state between tests
- ❌ Don't use sleep() in tests

### Page Objects
- ✅ Define locators as class constants
- ✅ Keep methods single-purpose
- ✅ Use descriptive method names
- ✅ Add comprehensive docstrings
- ✅ Inherit common methods from BasePage
- ❌ Don't hardcode selectors in methods
- ❌ Don't mix business logic with UI interactions

### Code Organization
- ✅ Group related tests in modules
- ✅ Use conftest.py for shared fixtures
- ✅ Organize test data by feature
- ✅ Keep imports organized and minimal
- ❌ Don't create circular imports
- ❌ Don't hardcode test data

---

## Contributing

This is a personal learning project for SDET upskilling. 

**To contribute or suggest improvements:**
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes and test thoroughly
3. Follow the code quality guidelines (Flake8, docstrings)
4. Commit with clear messages: `git commit -m "Add: description of changes"`
5. Push to your branch: `git push origin feature/your-feature-name`
6. Create a Pull Request with details of changes

**Contribution Guidelines:**
- Write tests for new features
- Update documentation
- Follow PEP 8 and existing code style
- Add docstrings to all public methods
- Include @allure.step decorators for Allure reporting

---

## Dependencies

Managed via `pyproject.toml`. 

**Core Dependencies:**
- `playwright` (>=1.40.0) - Browser automation and control
- `pytest` (>=7.4.0) - Testing framework and test runner
- `pytest-playwright` (>=0.4.0) - Pytest plugin for Playwright fixtures
- `pytest-xdist` (>=3.5.0) - Parallel test execution support
- `allure-pytest` (>=2.13.0) - Allure reporting integration
- `requests` (>=2.31.0) - HTTP client for API testing

**Development Dependencies** (optional):
- `flake8` - Code linting
- `black` - Code formatting
- `pre-commit` - Git hooks

**Note:** `pytest-html` is not used. Allure is the sole reporting solution, providing richer test documentation with steps, attachments, and timeline views.

### Install All Dependencies
```bash
# Install from pyproject.toml
pip install -e .

# Or install from requirements.txt
pip install -r requirements.txt
```

### Update Dependencies
```bash
# Check for outdated packages
pip list --outdated

# Upgrade specific package
pip install --upgrade playwright

# Upgrade all packages
pip install --upgrade -r requirements.txt
```

---

## Contact

**Anudeep T** - Python Automation Engineer (SDET)  
📧 Email: anudeep6142@gmail.com  
🔗 LinkedIn: linkedin.com/in/anudeep-thodupunoori-361979180

---

## Acknowledgments

- **[Automation Exercise](https://automationexercise.com)** - Excellent practice website for automation testing
- **[Playwright Documentation](https://playwright.dev)** - Comprehensive browser automation documentation
- **[pytest Documentation](https://docs.pytest.org)** - Powerful testing framework documentation
- **[Allure Framework](https://docs.qameta.io/allure/)** - Rich test reporting capabilities
- **Community** - Python testing best practices and SDET resources

---

## License

This project is open source and available for educational purposes.

---

## Changelog

### [v0.1.0] - April 2026

**Framework Foundation:**
- Initial framework setup with POM (Page Object Model) pattern
- 12 page objects covering full Automation Exercise user flows
- Allure reporting integration with @allure.step decorators

**UI Test Coverage:**
- Account creation and management tests
- Authentication and login tests
- Product browsing and search tests
- Shopping cart and checkout flow tests
- Contact form tests
- User registration and profile tests

**Advanced Features:**
- Network interception tests (test_network.py) for API validation
- Per-test artifact infrastructure with autouse fixture
- Trace recording for failed tests
- Structured test.log generation
- Browser authentication state persistence (auth/state.json)

**Utilities & Infrastructure:**
- Configuration management (ConfigReader)
- Test data handling (DataReader with CSV filtering)
- Custom decorators (@retry, @log_test)
- Logging management (LogManager)
- Custom exception hierarchy

**Quality & Documentation:**
- Comprehensive documentation and examples
- Pre-commit hooks for code quality
- Flake8 linting configuration
- Best practices guide
- Contributing guidelines

---
