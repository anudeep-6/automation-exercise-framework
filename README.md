# automation-exercise-framework

Automation framework for [Automation Exercise](https://automationexercise.com) 
built with Python, Playwright, and pytest.

## Project Description

A robust test automation framework for the Automation Exercise website, implementing both UI and API testing capabilities. The framework follows the Page Object Model (POM) design pattern and supports hybrid testing scenarios that combine UI and API validation.

**Key Features:**
- Page Object Model (POM) architecture
- Support for UI, API, and hybrid test scenarios
- Cross-browser testing (Chromium, Firefox, WebKit)
- Parallel test execution
- Custom utilities for config reading, data handling, and decorators
- Modular and scalable design

---

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.12 | Core programming language |
| **Playwright** | Latest | Browser automation |
| **pytest** | Latest | Testing framework |

---

## Project Structure

```
automation-exercise-framework/
│
├── .vscode/                    # VS Code workspace settings
│
├── config/                     # Configuration files
│   └── config.json             # Environment configurations
│
├── docs/                       # Project documentation
│
├── src/
│   ├── pages/                  # Page Object Model classes
│   │   ├── __init__.py
│   │   ├── base_page.py        # Base page with common methods
│   │   ├── cart_page.py        # Cart page POM
│   │   ├── home_page.py        # HomePage POM
│   │   ├── login_page.py       # Login page POM
│   │   └── product_page.py     # Product page POM
│   │
│   ├── api/                    # API client and helpers (planned)
│   │
│   └── utils/                  # Utility classes
│       ├── __init__.py
│       ├── config_reader.py    # Configuration file reader
│       ├── data_reader.py      # Test data reader
│       ├── decorators.py       # Custom decorators
│       └── exceptions.py       # Custom exceptions
│
├── test_data/                  # Test data files
│   └── users.csv               # User test data
│
├── tests/
│   ├── ui/                     # UI automated tests
│   │   └── __init__.py
│   │
│   ├── api/                    # API automated tests
│   │   └── __init__.py
│   │
│   └── hybrid/                 # Combined UI + API tests
│       └── __init__.py
│
├── venv/                       # Virtual environment
│
├── .flake8                     # Flake8 linting configuration
├── .gitignore                  # Git ignore rules
├── .gitkeep                    # Keep empty directories in git
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

### Run UI tests only
```bash
pytest tests/ui/
```

### Run API tests only
```bash
pytest tests/api/
```

### Run hybrid tests
```bash
pytest tests/hybrid/
```

### Run tests in parallel
```bash
pytest -n auto
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

### Run with verbose output
```bash
pytest -v
```

---

## Writing Tests

### UI Test Example
```python
import pytest
from src.pages.home_page import HomePage

def test_homepage_title(page):
    """Test homepage title is correct"""
    home = HomePage(page)
    home.navigate()
    assert home.get_title() == "Automation Exercise"
```

### Using Custom Decorators
```python
from src.utils.decorators import retry, log_test

@retry(max_attempts=3)
@log_test
def test_flaky_scenario(page):
    """Test with retry logic"""
    # Your test code here
    pass
```

### Reading Test Data
```python
from src.utils.data_reader import DataReader

def test_with_csv_data():
    """Test using CSV data"""
    data_reader = DataReader()
    users = data_reader.read_csv('test_data/users.csv')
    
    for user in users:
        # Use user data in test
        pass
```

---

## Configuration

### config/config.json
Configure base URLs, timeouts, and environment settings:

```json
{
  "base_url": "https://automationexercise.com",
  "timeout": 30000,
  "headless": true,
  "browser": "chromium"
}
```

Access in tests using `config_reader.py`:
```python
from src.utils.config_reader import ConfigReader

config = ConfigReader()
base_url = config.get('base_url')
```

---

## Code Quality

### Linting with Flake8
```bash
flake8 src/ tests/
```

### Pre-commit Hooks
Configured via `.pre-commit-config.yaml` to run automatically on commit:
- Code formatting checks
- Linting
- Trailing whitespace removal

Run manually:
```bash
pre-commit run --all-files
```

---

## Git Workflow

This project follows a feature branch workflow:

1. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and commit**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   ```

3. **Push to remote**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create Pull Request** on GitHub

5. **Review and merge** to `main`

---

## Dependencies

Managed via `pyproject.toml`. Key dependencies:
- `playwright` - Browser automation
- `pytest` - Testing framework
- `pytest-playwright` - Playwright plugin for pytest
- `pytest-xdist` - Parallel execution
- `flake8` - Code linting
- `pre-commit` - Git hooks

---

## Contributing

This is a personal learning project as part of SDET upskilling. Feedback and suggestions are welcome!

---

## Contact

**Anudeep T** - Python Automation Engineer  
linkedin.com/in/anudeep-thodupunoori-361979180 | anudeep6142@gmail.com

---

## Acknowledgments

- [Automation Exercise](https://automationexercise.com) for providing the test website
- Playwright and pytest communities
- Python testing best practices guides

---
