# Issues Found and Fixed — smart_home.py

**Name:** YASHRAJ M  **SRN:** PES1UG24CS700  **Section:** L
5
Line numbers refer to the original `smart_home.py`. Reports are in `reports_before` and `reports_after`.

## Summary

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.80/10 (25 messages) | 10.00/10 (0 messages) |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | 0 issues |
| Flake8 | 4 violations | 0 violations |

## Issue table (high and medium severity first)

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | B602 `subprocess_popen_with_shell_equals_true` (Bandit, **High**) | Security | 51 | `subprocess.call("bash scenes/" + sceneScript, shell=True)` passes user input to a shell. A name like `x; rm -rf ~` runs arbitrary commands (command injection), and `../` escapes the scenes folder. | Use `subprocess.run(["/bin/bash", script_path], check=True)` with an argument list and no shell. Resolve the path with `os.path.realpath` and reject anything outside `scenes/`. |
| 2 | W0102 `dangerous-default-value` (Pylint) | Bug | 11 | `settings={}` is created once and shared by every device that uses the default. `setTemperature("Thermostat", 35)` wrote `temperature: 30` into that shared dict, so the program printed `Light settings: {'temperature': 30}` for a light. | Default to `settings=None` and create a new `{}` inside the function. Output is now `Light settings: {}`. |
| 3 | B104 `hardcoded_bind_all_interfaces` (Bandit, **Medium**) | Security | 4 | `HUB_HOST = "0.0.0.0"` exposes the hub on every network interface, including public ones. | Default to `127.0.0.1`, overridable with the `SMART_HUB_HOST` environment variable. |
| 4 | R1710 `inconsistent-return-statements` (Pylint) | Bug | 16–20 | `toggleDevice` returns a bool for known devices but falls off the end (implicit `None`) for unknown ones. | Check for the unknown device first and `return None` explicitly. |
| 5 | B105 `hardcoded_password_string` (Bandit, Low) | Security | 7 | `HUB_PASSWORD = "smarthome-demo"` stores a credential in source code, where it ends up in Git history. | Read it from the `SMART_HUB_PASSWORD` environment variable. |
| 6 | W1514 `unspecified-encoding` (Pylint) | Bug / portability | 41 | `open(fileName, "w")` uses the platform's default encoding, so the JSON can differ between Windows and Linux. | `open(file_name, "w", encoding="utf-8")`. |
| 7 | KeyError in `setTemperature` (found by testing, not by a tool) | Bug | 24 | `devices[deviceName]` crashes with `KeyError` for an unknown device, unlike `toggleDevice`, which prints a message. | Use `devices.get()` and print "Device not found", returning `False`. |
| 8 | B404 `blacklist` subprocess import (Bandit, Low) | Security | 2 | Bandit flags any `subprocess` import for review. | Kept, because `run_scene` needs it, but the only call is now shell-free with a validated path. Annotated `# nosec B404` / `# nosec B603` with the reason. |
| 9 | C0103 `invalid-name` (Pylint, 14 messages) | Style | 11–49 | camelCase functions and arguments (`addDevice`, `deviceName`, …) break PEP 8 snake_case. | Renamed to `add_device`, `device_name`, `toggle_device`, `set_temperature`, `devices_in_room`, `power_usage`, `save_state`, `hub_address`, `run_scene`. |
| 10 | C0114 / C0116 missing docstrings (Pylint, 9 messages) | Style | 1, 11–54 | No module or function docstrings. | Added a module docstring and one per function. |
| 11 | E203 whitespace before ':' (Flake8) | Style | 6 | `{"light" : 10, ...}` | `{"light": 10, ...}` |
| 12 | E302 expected 2 blank lines (Flake8) | Style | 40 | Only one blank line before `def saveState`. | Added a second blank line. |
| 13 | E261 inline comment spacing (Flake8) | Style | 66 | One space before `# for app setup`. | Two spaces. |
| 14 | E501 line too long (Flake8) | Style | 68 | 80 characters (> 79). | Moved the list comprehension into a `devices_on` variable. |
| 15 | Module-level `main()` call | Design | 72 | `main()` runs on import, so importing the module (e.g. for tests) prints output and writes `home_state.json`. | Wrapped in `if __name__ == "__main__":`. |
