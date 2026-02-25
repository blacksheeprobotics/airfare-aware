# Airfare Tracker 1.0

**A Python-based utility to monitor airfare prices and alert travelers to travel deals.**

This project will track airfare prices and notify users of deals.  
Development begins in Python with a planned port to Rust in the future.

## Structure

- `src/` – application source code
- `tests/` – unit tests
- `requirements.txt` – Python dependencies

## Getting Started

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate it:
   - Windows (PowerShell): `venv\Scripts\Activate.ps1`
   - Unix/macOS: `source venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # the requirements include Playwright; after installing the Python package,
   # you also need to fetch browser binaries:
   python -m playwright install
   ```
4. Run the app:
   ```bash
   python src/main.py
   ```
