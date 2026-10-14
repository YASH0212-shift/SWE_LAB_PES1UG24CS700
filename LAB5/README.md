# Lab 5: Static Code Analysis — Smart Home Device Controller

**Your file:** `smart_home.py`

Follow the lab handout for the full instructions.

## About the program

A controller for smart home devices. It adds devices to rooms, switches them on and off, sets the thermostat within a safe range, lists devices by room, reports power use and saves the home state to home_state.json.

The code works, but only just. It has quality, style and security problems of the kind Pylint, Flake8 and Bandit are built to find.

## What to do

1. **Run it first** and read the output carefully:

   ```
   python smart_home.py
   ```

   It runs a short demonstration and needs no input. Not every problem in this file is something a tool will flag, so pay attention to output that looks wrong. Look closely at the settings it prints for each device, and ask whether every device should really have them.

2. **Install the tools:**

   ```
   python -m pip install pylint bandit flake8
   ```

3. **Run the analysis and save the reports:**

   ```
   python -m pylint smart_home.py > pylint_report.txt
   python -m bandit -r smart_home.py > bandit_report.txt
   python -m flake8 smart_home.py > flake8_report.txt
   ```

4. **Document the issues** in `issues.md` using this table (at least 4 rows, high and medium severity first):

   | Issue | Type | Line(s) | Description | Fix Approach |
   |-------|------|---------|-------------|--------------|
   | ...   | ...  | ...     | ...         | ...          |

5. **Fix the code.** Fix at least 4 of the issues you documented, then rerun all three tools to confirm they are gone. Repeat until you are satisfied. The program should still do its job when you are done.

6. **Reflect.** Answer the four reflection questions from the handout in `reflection.md`.

## Deliverables

- `smart_home.py`: your cleaned version, with at least 4 issues fixed.
- `issues.md`: the completed issue table.
- `reflection.md`: your answers to the reflection questions.

**Target:** aim for a Pylint score above 9.5 on your final file. A perfect 10.00/10 is very good.

Be ready to explain the bugs you found and how you fixed them. You may be called on to present.
