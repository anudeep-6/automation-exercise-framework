# automation-exercise-framework

Automation framework for [Automation Exercise](https://automationexercise.com) 
built with Python, Playwright, and pytest.

## Tech Stack
- Python 3.12
- Playwright
- pytest
- Allure Reporting

## Project Structure
```
automation-exercise-framework/
├── config/         # Configuration files
├── src/
│   ├── pages/      # Page Object Model classes
│   ├── api/        # API client and helpers
│   └── utils/      # Utility classes
├── test_data/      # Test data (JSON, CSV, Excel)
└── tests/
    ├── ui/         # UI automated tests
    ├── api/        # API automated tests
    └── hybrid/     # Combined UI + API tests
```