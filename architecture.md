
name: AI Quality Dashboard CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Lint
        run: |
          ruff check .

      - name: Run unit tests
        env:
          AI_ENABLED: "false"
          OPENAI_API_KEY: ""
        run: |
          pytest --cov=src --cov-report=term-missing

      - name: Compile Python
        run: |
          python -m compileall -q app.py src config tests
