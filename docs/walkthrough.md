# test-by-ai Walkthrough

I have built the `test-by-ai` CLI tool as requested. This walkthrough demonstrates the verification process using a mock API that intentionally has some flaws to test the tool's detection capabilities.

## Verification Setup
1.  **Mock API**: A simple Python `http.server` running on port 8080.
    - `GET /health` (200 OK)
    - `GET /users` (200 OK, returns list)
    - `POST /users` (201 Created) - **Flawed**: Accepts empty bodies and invalid JSON without validation.
2.  **OpenAPI Spec**: `tests/openapi.json` defining these endpoints.

## Execution
Command run:
```bash
python3 -m test_by_ai.cli tests/openapi.json --suite all --save results.json
```

## Results

### Terminal Output
The tool correctly reported:
- **Smoke Suite**: ALL PASS (API is alive)
- **Contract Suite**: ALL PASS (Happy path returns expected codes)
- **Negative Suite**: **FAIL** (Mock API failed to reject invalid requests)

```text
            Suite: NEGATIVE             
┏━━━━━━┳━━━━━┳━━━━━━┳━━━━━┳━━━━━━┳━━━━━┓
┃ Met… ┃ Pa… ┃ Sta… ┃ Co… ┃ Dur… ┃ Er… ┃
┡━━━━━━╇━━━━━╇━━━━━━╇━━━━━╇━━━━━━╇━━━━━┩
│ POST │ /u… │ FAIL │ 201 │ 5ms  │  U… │
│      │     │      │     │      │ Su… │
│      │     │      │     │      │ 201 │
```

### JSON Report
Start of `results.json`:
```json
{
  "summary": {
    "total": 8,
    "passed": 6,
    "failed": 2,
    "errors": 0
  },
  "suites": [
    ...
    {
      "name": "negative",
      "results": [
        {
          "method": "POST",
          "path": "/users",
          "status": "FAIL",
          "error": "[empty_body] Unexpected Success 201 on negative test"
        }
      ]
    }
  ]
}
```

## Conclusion
The tool meets all requirements:
1.  **Stateless & CLI**: Works from terminal.
2.  **Multi-suite**: Supports Smoke, Contract, Negative.
3.  **Error Detection**: Successfully caught the lack of validation in the mock API.
4.  **Reporting**: Produces clear terminal tables and JSON output.
5.  **AI Ready**: Architecture supports Gemini/OpenAI (integration implemented).
