# Reflection — Lab 5: Static Code Analysis

**Name:** YASHRAJ M  **SRN:** PES1UG24CS700  **Section:** L

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest were the Flake8 style issues and Pylint's naming and docstring messages. Each one points to an exact line and the fix is mechanical: add a blank line, remove a space, rename `addDevice` to `add_device`. Renaming only needed care to update every call site in `main()`.

The hardest was the `shell=True` call in `runScene` (Bandit B602). Removing `shell=True` alone is not enough, because the scene name still controls which file runs and `../` could escape the `scenes/` folder. I had to pass the command as an argument list and also resolve and check the path. The mutable default argument was easy to change but harder to understand: the tool only says "dangerous default value", and I had to connect it to the wrong output, where the Ceiling Light showed `{'temperature': 30}` because it shared one settings dict with the Thermostat.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Yes. Bandit B404 flags every `import subprocess` as Low severity, whether or not it is used safely. After the fix, `run_scene` uses an argument list, no shell and a validated path, so the import is not a real risk. I marked it with `# nosec B404` and wrote the reason on the line above, so a reviewer can see why it was suppressed. B105 on `HUB_PASSWORD` is borderline: in this demo the password is never used, but hardcoding credentials is still a bad habit, so I fixed it anyway.

The tools also missed a real bug. `setTemperature` crashed with a `KeyError` for an unknown device, and none of the three tools flagged it. I only found it by reading the code.

## 3. How would you integrate static analysis tools into your actual software development workflow?

- **Locally:** run Flake8 and Pylint in the editor so problems show up while typing, and add a `pre-commit` hook so a commit fails on Flake8 errors or High-severity Bandit findings.
- **In CI:** add a GitHub Actions job that runs all three tools on every pull request, fails on any Bandit Medium/High issue or a Pylint score below a threshold (for example 9.5), and stores the reports as build artifacts.
- **Configuration:** keep shared settings in `pyproject.toml` / `.flake8` so everyone uses the same rules, and require a written reason for every `# nosec` or `# pylint: disable` so suppressions are reviewed rather than used to hide warnings.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Correctness:** the light no longer shows thermostat settings (`Light settings: {}`), `toggle_device` always returns a value, and `set_temperature` handles unknown devices instead of crashing.
- **Security:** no shell command injection or path traversal in `run_scene`, the hub listens only on localhost by default, and no password is stored in the code.
- **Readability:** consistent snake_case names, docstrings on every function, and named constants (`MIN_TEMPERATURE`, `MAX_TEMPERATURE`) instead of magic numbers.
- **Reusability:** the `if __name__ == "__main__":` guard means the module can be imported for testing without running the demo.
- **Measured result:** Pylint went from 4.80 to 9.84, Bandit from 4 issues to 0, and Flake8 from 4 violations to 0, while the program still produces the same intended output.
