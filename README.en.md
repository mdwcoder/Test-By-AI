[Español](README.es.md) | [English](README.en.md)

---

# test-by-ai

**test-by-ai** is a stateless, cross-platform CLI tool that executes automated tests against REST APIs using an OpenAPI specification. It detects health issues, contract violations, and error handling flaws with minimal configuration.

---

## 🚀 Installation Guide

### Linux & macOS

We provide an automated script that sets up a virtual environment and registers the `test-by-ai` alias for you.

1.  **Run the installer:**
    ```bash
    ./init.sh
    ```
    This script will:
    *   Create a `.venv` directory.
    *   Install Python dependencies.
    *   Add an alias to your shell config (`.bashrc`, `.zshrc`, or `config.fish`).

2.  **Reload your shell:**
    ```bash
    source ~/.bashrc  # OR source ~/.zshrc
    ```

3.  **Verify installation:**
    ```bash
    test-by-ai --help
    ```

### Windows (PowerShell)

We provide a PowerShell script that configures the environment and adds a function to your user profile.

1.  **Run the installer:**
    ```powershell
    .\init.ps1
    ```
    *Note: If you see an Execution Policy error, you may need to run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`.*

2.  **Restart your terminal.**

3.  **Verify installation:**
    ```powershell
    test-by-ai --help
    ```

### Manual Installation (Advanced)

If you prefer to manage dependencies manually:

```bash
git clone https://github.com/yourusername/test-by-ai.git
cd test-by-ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run directly
python3 -m test_by_ai.cli --help
```

---

## 📖 User Manual

### Basic Usage

The only required argument is the path (or URL) to your OpenAPI definition file (`openapi.json` or `swagger.json`).

```bash
test-by-ai path/to/openapi.json
```
*This runs all default test suites (Smoke, Contract, Negative) against the server defined in the spec.*

### Command Options

| Flag | Description | Example |
|------|-------------|---------|
| `openapi_path` | **Required.** Path or URL to the OpenAPI spec. | `api-spec.json` or `http://api.com/spec` |
| `--base-url` | Override the API host found in the spec. | `--base-url http://localhost:8000` |
| `--suite` | Select specific test suite. Default: `all`. | `--suite smoke` |
| `--ai` | Enable AI analysis (requires API Key). | `--ai gemini` |
| `--save` | Save results to JSON file. | `--save results.json` or `--save auto` |

### Test Suites explained

*   **🟢 Smoke Suite**: Checks if endpoints are reachable and healthy (returns non-5xx status).
*   **🔵 Contract Suite**: Validates that successful responses (2xx) match the OpenAPI schema status codes.
*   **🔴 Negative Suite**: Sends invalid data (empty bodies, wrong types) and verifies the API returns client errors (4xx) instead of crashing (5xx).

### AI Analysis (Optional)

**test-by-ai** can use Google Gemini to analyze test failures and suggest fixes.

1.  **Set the Environment Variable:**
    ```bash
    # Linux/macOS
    export GEMINI_API_KEY="your_api_key_here"

    # Windows (PowerShell)
    $env:GEMINI_API_KEY="your_api_key_here"
    ```

2.  **Run with AI:**
    ```bash
    test-by-ai openapi.json --ai gemini
    ```

The AI analysis will appear at the bottom of the report if failures are detected.

### Saving Results

Useful for CI/CD pipelines or audit trails.

-   **Ask interactively:** Run without `--save`.
-   **Auto-save:** `test-by-ai openapi.json --save auto` (creates `results_<timestamp>.json`).
-   **Specific file:** `test-by-ai openapi.json --save my_report.json`.

---

## 📊 Understanding the Output

The terminal output is designed to be minimal and actionable.

1.  **Header**: Shows context (Host, Duration, Source).
2.  **Summary Table**: Quick glance at passed/failed counts.
3.  **Failures Detected**: ONLY shown if something broke.
    *   `❌ Method Path (Status)`
    *   `↳ Error cause`
4.  **AI Analysis**: Insights and suggestions (if enabled).

*If all tests pass, you will see a green "✔ All tests passed" message and nothing else.*
