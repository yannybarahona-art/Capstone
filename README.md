# Open Library Capstone

A Python CLI application for retrieving, cleaning, storing, analyzing, and reporting book data using the Open Library API.

## Main Features

- Retrieve book data from the Open Library API
- Support synchronous and asynchronous API requests
- Import and process book data from CSV files
- Clean and validate book information
- Store and update book records using SQLite
- Analyze publication years and languages
- Generate Excel, CSV, and JSON reports
- Run code quality checks with Ruff
- Run automated tests with Pytest
- CI workflow using GitHub Actions

## Project Structure

- `main.py` - Application entry point
- `src/api/` - Synchronous and asynchronous API clients
- `src/cli/` - CLI menu
- `src/db/` - SQLite database management
- `src/processing/` - Data cleaning, processing, and analytics
- `src/reporting/` - Report generation
- `data/` - Database and sample CSV files
- `data/outputs/` - Generated Excel, CSV, and JSON reports
- `tests/` - Automated tests
- `.github/workflows/` - CI workflow

## Installation

Install the project dependencies:

```bash
uv sync
```

## Run the Application

```bash
uv run python main.py
```

## Testing

Run all automated tests:

```bash
uv run pytest
```

## Code Quality

Run Ruff checks:

```bash
uv run ruff check .
uv run ruff format --check .
```

## Reports

Generated reports are saved in:

```text
data/outputs/
```

The application supports Excel, CSV, and JSON reports.

## Technologies

- Python
- SQLite
- Pandas
- Requests
- OpenPyXL
- Pytest
- Ruff
- uv
- GitHub Actions
