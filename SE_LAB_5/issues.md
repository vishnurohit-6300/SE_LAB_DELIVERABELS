# Static Analysis Issue Table

Project: Pharmacy Manager

The original source was checked with Pylint, Bandit, and Flake8. The tools reported code-quality and security concerns. The following table records the important findings and the corrective action taken in the revised program.

| No. | Finding in original program | Risk / impact | Correction in revised program |
|---:|---|---|---|
| 1 | `eval()` used for dosage calculation | Could execute arbitrary Python expressions | Replaced with a restricted AST-based arithmetic evaluator allowing only numeric values and `+`, `-`, `*`, `/` |
| 2 | `pickle` used to load stock data | Loading untrusted pickle data can execute unsafe code | Replaced pickle storage with JSON |
| 3 | Password stored directly in source code | Exposes credentials to anyone who can read the source | Reads the configured password from the `PHARMACY_PASSWORD` environment variable |
| 4 | MD5 used for patient identifier | MD5 is not suitable for security-sensitive hashing | Replaced with SHA-256 |
| 5 | `os.system()` used to print a label | Unnecessary shell invocation and possible command-injection risk | Replaced with a normal Python `print()` call |
| 6 | Bare `except` silently ignored errors | Hides unexpected failures and makes debugging difficult | Uses explicit validation and specific exceptions |
| 7 | Dispensing could reduce stock below zero or silently ignore a missing medicine | Produces incorrect inventory records | Validates medicine existence, positive quantity, and available stock |
| 8 | Negative quantities and invalid medicine names could enter inventory | Causes unreliable stock and billing data | Added input validation in inventory and billing functions |
| 9 | Several names and formatting rules failed style checks | Makes code harder to maintain | Used snake_case, docstrings, and clearer formatting |

## Verification note

The revised program must be tested again in the user's local virtual environment. The issue table describes the changes made in this revised source; it does not claim that the latest Pylint, Bandit, or Flake8 runs have already passed. Save fresh tool outputs after running the commands listed in the report.
