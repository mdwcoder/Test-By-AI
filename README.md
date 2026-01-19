# test-by-ai (PROVISIONAL)

> [!IMPORTANT]
> This project is currently in active development. This documentation is provisional.

A stateless, cross-platform CLI tool for automated API testing using OpenAPI specifications.

## Installation

### Linux / macOS
```bash
./init.sh
source ~/.bashrc  # Or ~/.zshrc / ~/.config/fish/config.fish
```

### Windows (PowerShell)
```powershell
.\init.ps1
# Restart your terminal
```

## Features

- **Smoke Tests**: Verify API health and reachability.
- **Contract Tests**: Validate response status codes against OpenAPI spec.
- **Negative Tests**: Send invalid requests to ensure proper error handling.
- **AI Analysis**: Optional integration with Gemini to analyze failure patterns.
- **Rich Output**: Beautiful terminal interface using `rich`.

## Usage

Basic run:
```bash
test-by-ai path/to/openapi.json
```

With AI (Gemini):
```bash
export GEMINI_API_KEY="your_key"
test-by-ai openapi.json --ai gemini
```

See help:
```bash
test-by-ai --help
```
