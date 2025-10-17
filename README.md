# rr-qa-automation-assignment
Rapyuta QA Automation Assignment

# TMDB Discover Automation Framework

This project automates end-to-end functional and API validations for the **TMDB Discover** web application  
(https://tmdb-discover.surge.sh).  
It uses **Behave (BDD)** for user journey tests and **Pytest** for functional + API verification.  
**Selenium Wire** is integrated to capture and validate network API calls.

---

## Tech Stack

| Component | Purpose |
|------------|----------|
| **Python 3.10+** | Core language |
| **Behave** | BDD framework for feature scenarios |
| **Pytest** | Functional testing |
| **Selenium** | Browser automation |
| **Selenium-Wire** | Network request interception |
| **Edge WebDriver** | Browser driver |
| **Allure / HTML Reports (optional)** | Reporting support |

---

## Setup Instructions

### Create and activate virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate 
```
---

## Install Dependencies
```bash
pip install -r requirements.txt

pip install behave pytest selenium selenium-wire allure-behave
````

### Setup Edge WebDriver
Make sure Microsoft Edge WebDriver is installed and available on PATH.
Check version:
```bash
msedgedriver --version
```

## Running Tests
### Run all Behave scenarios
```bash
behave
```

### Run a single feature file
```bash
behave features/api.feature
```

### Run Behave with detailed output
```bash
behave -f pretty --no-capture
```

### Run Pytest functional tests
```bash
pytest -v tests/test_discover_movie.py
```

### Generate HTML report
```bash
pytest -v --html=report.html --self-contained-html
```

## Known Bugs & Limitations

| **Issue** | **Description** | **Impact** | **Status** |
|------------|-----------------|-------------|-------------|
| **Pagination stops working after a certain page** | Pagination beyond a few pages (for example, page > 5) becomes unresponsive or does not trigger an API call. | User cannot browse full results or verify deeper pages. | Known issue |
| **Missing Discover options (Type / Genre)** | The Discover API does not expose selectable properties for “type” and “genre”. The filters still function using hardcoded UI values, but lack of dynamic properties prevents complete discoverability. | Partial filtering experience — missing metadata limits full API coverage. | Known issue |

