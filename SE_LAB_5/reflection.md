# Reflection

## 1. What did you learn from static code analysis?

I learned that a program can run and produce output while still containing security weaknesses, maintainability problems, and coding-standard violations. Pylint helped identify naming, documentation, and code-structure issues. Flake8 highlighted formatting and style violations. Bandit identified potentially unsafe operations such as `eval()`, pickle deserialization, hardcoded credentials, weak hashing, and shell execution.

## 2. Which important issues did you fix?

I replaced unsafe `eval()` usage with a restricted arithmetic evaluator, replaced pickle storage with JSON, removed the hardcoded password, changed MD5 to SHA-256, and removed the shell command used for printing labels. I also added validation to prevent invalid quantities, missing medicines, and dispensing more stock than is available.

## 3. How did these changes improve the program?

The changes make the program safer when processing dosage expressions and loading saved inventory. Input validation helps maintain accurate stock values. Clearer function names, docstrings, and formatting make the code easier to understand and maintain.

## 4. Are static analysis tools enough to guarantee that software is secure?

No. Static analysis tools are useful because they detect many likely problems without executing the program. However, their results need to be reviewed, and the program still needs functional testing, input testing, and appropriate security review. A clean tool report alone does not prove that software is completely secure.

## 5. What would you improve next?

I would add automated unit tests for stock addition, dispensing, expiry checks, billing, dosage calculations, login, and saving/loading inventory. I would also add stronger authentication, role-based access, and a database for a production-ready pharmacy application.
