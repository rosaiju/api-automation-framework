# API Automation Framework

A production-grade REST API test automation framework built with Python, pytest, and Pydantic. Tests real public APIs with schema validation, data-driven parameterization, and full CI/CD integration.

[![API Test Suite](https://github.com/rosaiju/api-automation-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/rosaiju/api-automation-framework/actions/workflows/ci.yml)
[![Allure Report](https://img.shields.io/badge/Allure-Report-orange)](https://rosaiju.github.io/api-automation-framework)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue)](https://python.org)

## Live Test Report

[**View Allure Report →**](https://rosaiju.github.io/api-automation-framework)

## Features

- **Pydantic schema validation** — any API field change or type drift fails the test automatically
- **Data-driven tests** — parameterized with `pytest.mark.parametrize` using JSON/CSV datasets
- **Fixture-based auth** — session-scoped token refresh, no hardcoded credentials
- **Schema drift detection** — detects unexpected new fields added by the API
- **Response time assertions** — SLO enforcement on every smoke test
- **Multi-version CI** — runs against Python 3.11 and 3.12 in parallel
- **Allure reporting** — published to GitHub Pages after every push to main
- **Environment config** — swap base URLs via `.env` without touching test code

## Project Structure

```
api-automation-framework/
├── clients/                  # HTTP client layer (one per API domain)
│   ├── base_client.py        # Shared session, headers, timeout management
│   ├── user_client.py        # Reqres.in /users endpoints
│   ├── auth_client.py        # Reqres.in /login, /register endpoints
│   └── brewery_client.py     # OpenBreweryDB endpoints
├── models/                   # Pydantic response models (schema validation)
│   ├── user.py
│   ├── auth.py
│   └── brewery.py
├── config/
│   └── settings.py           # Environment variable loading
├── tests/
│   ├── conftest.py           # Shared fixtures (clients, auth token, datasets)
│   ├── users/
│   │   ├── test_get_users.py
│   │   └── test_create_update_delete.py
│   ├── auth/
│   │   └── test_auth.py
│   └── breweries/
│       └── test_breweries.py
├── .github/workflows/
│   └── ci.yml                # GitHub Actions: test matrix + Allure Pages deploy
├── pytest.ini
├── requirements.txt
└── .env.example
```

## APIs Under Test

| API | Base URL | Coverage |
|-----|----------|----------|
| [Reqres.in](https://reqres.in) | `https://reqres.in/api` | Users CRUD, Auth (login/register) |
| [Open Brewery DB](https://www.openbrewerydb.org) | `https://api.openbrewerydb.org/v1` | List, search, filter by type/city |

## Quick Start

```bash
git clone https://github.com/rosaiju/api-automation-framework.git
cd api-automation-framework

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env

# Run all tests
pytest

# Run by marker
pytest -m smoke
pytest -m regression
pytest -m negative
pytest -m schema

# Run with Allure report (requires allure CLI)
pytest --alluredir=allure-results
allure serve allure-results

# Run in parallel (4 workers)
pytest -n 4
```

## Test Markers

| Marker | Description |
|--------|-------------|
| `smoke` | Fast core happy-path tests — run these first |
| `regression` | Full regression suite including edge cases |
| `negative` | 4xx error handling and invalid input tests |
| `schema` | Pydantic schema validation and drift detection |

## Architecture Decisions

**Why a client layer instead of raw `requests` calls in tests?**
Separating HTTP logic from test assertions means changing a base URL or adding an auth header happens in one place, not across 30 test files. This mirrors how production SDKs are structured.

**Why Pydantic for schema validation?**
Pydantic validates field names, types, and required/optional structure in one line: `UserListResponse(**response.json())`. If the API adds an unexpected field or changes a type, the test fails with a human-readable error — not a silent data corruption.

**Why session-scoped fixtures for auth tokens?**
Auth tokens are fetched once per test session and reused. This avoids hammering the login endpoint on every test, mirrors real client behavior, and keeps the suite fast.

**Why pytest markers?**
Markers let CI run just `smoke` tests on every push (fast feedback) and the full suite on schedule or before release. This is the standard pattern at companies running large test suites.

## CI/CD Pipeline

Every push to `main` or `develop`:
1. Runs the full test suite against Python 3.11 and 3.12 in parallel
2. Uploads Allure results as artifacts (30-day retention)
3. On `main` pushes: generates and publishes the Allure report to GitHub Pages

Scheduled run at 8 AM UTC every weekday catches API regressions introduced by third-party changes.
