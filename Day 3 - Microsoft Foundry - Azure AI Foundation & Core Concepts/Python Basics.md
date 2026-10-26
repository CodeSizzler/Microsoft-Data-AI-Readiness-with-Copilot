# Python Basics

Microsoft Data & AI Readiness for SATORP · Pre-reading before Day 3 · CodeSizzler

## Contents

1. [Why Python, and why now](#why-python-and-why-now)
2. [Set up your laptop and run your first program](#set-up-your-laptop-and-run-your-first-program)
3. [Variables and data types](#variables-and-data-types)
4. [Text and f-strings](#text-and-f-strings)
5. [Lists and dictionaries](#lists-and-dictionaries)
6. [Making decisions with if, elif and else](#making-decisions-with-if-elif-and-else)
7. [Repeating work with for loops](#repeating-work-with-for-loops)
8. [Functions](#functions)
9. [Packages: pip install and import](#packages-pip-install-and-import)
10. [Reading a CSV file with pandas](#reading-a-csv-file-with-pandas)
11. [Sneak peek: calling an AI model on Day 3](#sneak-peek-calling-an-ai-model-on-day-3)
12. [Reading error messages](#reading-error-messages)
13. [Practice before Day 3](#practice-before-day-3)
14. [Cheat sheet](#cheat-sheet)

## Why Python, and why now

On Day 3 you will call AI models in Microsoft Foundry from Python, so you need to read and run short Python scripts. You do not need to become a programmer: about one hour with this guide is enough.

Python is the most widely used language for data and AI because it reads almost like English. Microsoft Foundry, Azure AI Search, Microsoft Fabric notebooks and the Day 4 data lab all use it.

How to use this guide:

- Type every example yourself instead of copying it. Typing builds memory.
- Change one thing in each example and run it again to see what happens.
- Errors are normal. Section 12 shows how to read them.

## Set up your laptop and run your first program

Install these before Day 3. The Day 3 labs are tested with Python 3.13; avoid 3.14, because some packages are not built for it yet.

| Tool | Where to get it | Check it works |
| --- | --- | --- |
| Python 3.13 | [python.org/downloads](https://www.python.org/downloads/) | `python --version` (Windows) or `python3 --version` (Mac) |
| Visual Studio Code | [code.visualstudio.com](https://code.visualstudio.com/) | Opens without errors |
| Python extension for VS Code | VS Code → Extensions → search “Python” (by Microsoft) | Shows as installed |
| Git | [git-scm.com](https://git-scm.com/install/) | `git --version` |
| Azure CLI | [Install the Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) | `az --version` |

On Windows, tick **Add python.exe to PATH** on the first installer screen. If you forget, the `python` command will not be found.

Your first program:

1. Create a folder called `python-basics` and open it in VS Code (**File → Open Folder**).
2. Create a file called `hello.py`.
3. Type this line and save:

```python
print("Hello, SATORP!")
```

4. Open a terminal (**Terminal → New Terminal**) and run it:

```bash
python hello.py
```

You should see `Hello, SATORP!`. On a Mac, use `python3` instead of `python` in every command in this guide.

Two more things to know:

- Lines starting with `#` are comments. Python ignores them; they are notes for people.
- Indentation (spaces at the start of a line) has meaning in Python. Use 4 spaces; VS Code does this for you when you press Tab.

## Variables and data types

A variable is a labelled box that holds a value. You create one with `=` and use its name later.

```python
unit_name = "Fluid Catalytic Cracker"   # text
open_work_orders = 3                     # whole number
attainment = 0.94                        # decimal number
is_critical = True                       # yes / no

print(unit_name)
print(open_work_orders + 2)              # 5
```

| Type | Python name | Example | Used for |
| --- | --- | --- | --- |
| Text | `str` | `"P-201"` | Names, IDs, prompts to an AI model |
| Whole number | `int` | `42` | Counts |
| Decimal number | `float` | `192.5` | Hours, percentages, costs |
| True or False | `bool` | `True` | Yes/no checks |
| Nothing | `None` | `None` | A value that is missing |

Useful rules:

- Names use lowercase words joined by underscores: `planned_throughput`, not `Planned Throughput`.
- Names are case-sensitive: `Unit` and `unit` are different variables.
- `type(x)` tells you what type a value is: `type(192.5)` gives `float`.
- Maths works as you expect: `+  -  *  /`. `**` is power, so `2 ** 3` is 8.

## Text and f-strings

Text goes inside quotes, single or double. An f-string (an `f` before the quotes) lets you drop variables straight into text with `{ }`. You will use f-strings constantly to build prompts for AI models.

```python
asset = "AST-2001"
hours = 192.5

print(f"Asset {asset} was down for {hours} hours.")
# Asset AST-2001 was down for 192.5 hours.

prompt = f"Summarise the fault history of {asset} in 3 bullet points."
print(prompt)
```

Handy things you can do with text:

| Code | Result | What it does |
| --- | --- | --- |
| `"usa".upper()` | `"USA"` | Upper case |
| `"  Canada ".strip()` | `"Canada"` | Removes spaces at both ends |
| `"Hot Work SOP".lower()` | `"hot work sop"` | Lower case |
| `"AST-2001".startswith("AST")` | `True` | Checks the start |
| `len("P-201")` | `5` | Counts characters |
| `"FCC" + " unit"` | `"FCC unit"` | Joins text |

On Day 4 you will use exactly these, `.lower()` and `.strip()`, to clean 32 country spellings down to 10.

## Lists and dictionaries

A list holds several values in order. A dictionary holds labelled values, like one row of a table. Most data you meet on Days 3 to 5, including AI model responses, arrives as lists and dictionaries.

**Lists** use square brackets. Counting starts at 0.

```python
units = ["CDU", "Hydrocracker", "FCC", "Coker"]

print(units[0])        # CDU  (the first item)
print(units[-1])       # Coker (the last item)
print(len(units))      # 4

units.append("Aromatics")   # add an item to the end
```

**Dictionaries** use curly brackets with `key: value` pairs.

```python
work_order = {
    "id": "WO-1042",
    "priority": "P1",
    "status": "Open",
    "cost_sar": 12500,
}

print(work_order["priority"])     # P1
work_order["status"] = "Completed"  # change a value
```

A list of dictionaries is how a table looks in Python: each dictionary is one row.

```python
work_orders = [
    {"id": "WO-1042", "priority": "P1"},
    {"id": "WO-1043", "priority": "P3"},
]
```

This is also the shape of JSON, the format AI services and web APIs send and receive.

## Making decisions with if, elif and else

`if` runs a block of code only when a condition is true. The indented lines under it belong to it.

```python
priority = "P1"

if priority == "P1":
    print("Critical: a dispatcher must approve before the truck rolls.")
elif priority == "P2":
    print("High: respond within the service-plan time.")
else:
    print("Normal: schedule in the next free slot.")
```

| Comparison | Meaning |
| --- | --- |
| `==` | equal to (two `=` signs; one `=` assigns a value) |
| `!=` | not equal to |
| `>`  `<`  `>=`  `<=` | greater / less than |
| `and`  `or`  `not` | combine conditions |
| `in` | is inside a list or text, e.g. `"smoke" in report` |

A safety rule like the one in the Day 2 agent, written in Python:

```python
report = "Burning smell and smoke from the generator"

if "smoke" in report.lower() or "burning" in report.lower():
    print("STOP WORK. Call the Duty Manager.")
```

Remember the colon `:` at the end of `if`, `elif` and `else` lines.

## Repeating work with for loops

A `for` loop runs the same lines once for every item in a list. This is how you process every row, document or question without copying code.

```python
units = ["CDU", "Hydrocracker", "FCC"]

for unit in units:
    print(f"Checking {unit}...")
```

Loop over a list of dictionaries and combine it with `if`:

```python
work_orders = [
    {"id": "WO-1042", "priority": "P1", "status": "Open"},
    {"id": "WO-1043", "priority": "P3", "status": "Completed"},
    {"id": "WO-1044", "priority": "P1", "status": "In progress"},
]

open_p1 = 0
for wo in work_orders:
    if wo["priority"] == "P1" and wo["status"] != "Completed":
        open_p1 = open_p1 + 1

print(f"Open P1 work orders: {open_p1}")   # 2
```

Two more tools:

- `range(5)` gives the numbers 0 to 4: `for i in range(5):` repeats 5 times.
- `while` repeats as long as a condition is true. Use it rarely; a `for` loop is safer because it always ends.

## Functions

A function is a named, reusable recipe. You give it inputs, it does the work and `return`s a result. Write it once, use it many times.

```python
def attainment_percent(actual, planned):
    """Actual throughput divided by planned, as a percentage."""
    return round(actual / planned * 100, 1)

print(attainment_percent(94, 100))     # 94.0
print(attainment_percent(180, 200))    # 90.0
```

The parts:

- `def` starts the function, followed by its name and inputs in brackets, then `:`.
- The indented lines are the body.
- The text in triple quotes describes what it does. AI agents read descriptions like this to decide when to call a tool.
- `return` sends the answer back. Without it, the function gives back `None`.

You have already used built-in functions: `print()`, `len()`, `round()` and `type()`.

Why this matters for AI: the tools an agent calls (Day 1 and Day 2) are functions. An MCP server like `check_part_stock(part, city)` is simply a set of Python functions with clear names and descriptions.

## Packages: pip install and import

Packages are ready-made code written by others. You install a package once with `pip`, then `import` it in any script that needs it.

First, create a virtual environment: a private folder of packages for one project, so projects don’t clash. Run these in the VS Code terminal inside your `python-basics` folder:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac
source .venv/bin/activate
```

Your terminal prompt now starts with `(.venv)`. Install packages into it:

```bash
pip install pandas azure-identity azure-ai-projects
```

Then use them in a script:

```python
import pandas as pd                     # "as pd" gives it a short nickname
from datetime import date               # take one thing from a package

print(date.today())
```

| Package | What it does | When you use it |
| --- | --- | --- |
| `azure-ai-projects` | Talks to your Microsoft Foundry project and models | Day 3 |
| `azure-identity` | Signs in to Azure securely, with no keys in code | Day 3 |
| `pandas` | Reads, cleans and analyses tables (CSV, Excel) | Day 4 |
| `faker` | Generates realistic test data | Day 4 data lab |

If VS Code asks which Python interpreter to use, pick the one inside `.venv`.

## Reading a CSV file with pandas

pandas turns a CSV or Excel file into a table you can filter, count and summarise in a few lines. It is the bridge to the Day 4 data lab and to Fabric notebooks on Day 5.

Save this as `units.csv` in your folder:

```csv
UnitId,UnitName,DesignCapacity_kbbl
U100,Crude Distillation Unit,400
U200,Hydrocracker 1,60
U300,Hydrocracker 2,60
U400,Fluid Catalytic Cracker,90
```

Then run:

```python
import pandas as pd

df = pd.read_csv("units.csv")      # df = "data frame", a table

print(df.head())                    # first 5 rows
print(df.shape)                     # (rows, columns): (4, 3)
print(df["UnitName"])               # one column

big_units = df[df["DesignCapacity_kbbl"] > 80]   # filter rows
print(big_units)

print(df["DesignCapacity_kbbl"].sum())           # 610
```

The sample figures are invented for practice and do not represent SATORP operations.

## Sneak peek: calling an AI model on Day 3

This is the kind of script you will run on Day 3. Don’t run it yet; you need a Foundry project first. Just check you can read every line using what you learned above.

```python
from azure.identity import DefaultAzureCredential     # import (section 9)
from azure.ai.projects import AIProjectClient

PROJECT_ENDPOINT = "<your project endpoint>"         # a str variable (section 3)

project = AIProjectClient(                            # calling a function (section 8)
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential())

client = project.get_openai_client()

questions = ["What is a P1 work order?",             # a list (section 5)
             "Why do we isolate a pump before maintenance?"]

for q in questions:                                   # a loop (section 7)
    response = client.responses.create(
        model="gpt-5-mini",
        instructions="Answer in 3 short bullet points.",
        input=q)
    print(f"Q: {q}")                                  # an f-string (section 4)
    print(response.output_text)
```

Before this runs you sign in once with `az login` in the terminal. `DefaultAzureCredential` then uses that sign-in, so there is no password or key in the code.

## Reading error messages

Read an error from the bottom up: the last line names the problem, and the line above it shows the file and line number. Most beginner errors are one of these seven.

| Error (last line) | What it usually means | Fix |
| --- | --- | --- |
| `SyntaxError: expected ':'` | Missing colon after `if`, `for` or `def` | Add `:` at the end of the line |
| `IndentationError` | Spaces at the start of lines don’t line up | Indent the block by exactly 4 spaces |
| `NameError: name 'x' is not defined` | Typo in a name, or used before it was created | Check spelling and case |
| `TypeError: can only concatenate str (not "int") to str` | Joining text and a number with `+` | Use an f-string: `f"Total: {total}"` |
| `KeyError: 'priority'` | That key is not in the dictionary | Check the exact key name and case |
| `IndexError: list index out of range` | Asking for an item past the end of a list | Remember counting starts at 0 |
| `ModuleNotFoundError: No module named 'pandas'` | Package not installed, or wrong environment | Activate `.venv`, then `pip install pandas` |

If you are stuck for more than five minutes, paste the full error into Microsoft 365 Copilot Chat and ask “explain this error simply”, or ask the trainer.

## Practice before Day 3

Tick each one off when it runs without errors. Together they take about 30 minutes.

- [ ] Print your name and team with an f-string: `My name is Sara and I work in Reliability.`
- [ ] Create `hours = [12.5, 40, 8, 3.5]` and print the total with `sum(hours)` and the count with `len(hours)`.
- [ ] Write an `if` that prints “High” when downtime hours are over 24, otherwise “Normal”. Test it with 30 and with 10.
- [ ] Loop over `["usa", " USA", "Usa "]` and print each one cleaned with `.strip().upper()`.
- [ ] Write a function `cost_with_labour(parts_cost, hours)` that returns parts cost plus 85 per hour of labour. Check that `cost_with_labour(400, 2)` gives 570.
- [ ] Read `units.csv` with pandas and print only the units with a design capacity of 60.
- [ ] Break something on purpose (remove a `:`), run it, and read the error.

## Cheat sheet

| I want to… | Python |
| --- | --- |
| Show something | `print("text")` |
| Store a value | `name = "FCC"` |
| Put a value in text | `f"Unit: {name}"` |
| Make a list | `units = ["CDU", "FCC"]` |
| Get the first item | `units[0]` |
| Make a dictionary | `wo = {"id": "WO-1", "priority": "P1"}` |
| Read a value | `wo["priority"]` |
| Decide | `if x > 10:` … `elif` … `else:` |
| Repeat for each item | `for u in units:` |
| Make a function | `def name(a, b): return a + b` |
| Install a package | `pip install pandas` |
| Use a package | `import pandas as pd` |
| Read a CSV | `df = pd.read_csv("file.csv")` |
| Run a script | `python file.py` (Mac: `python3 file.py`) |

Want more practice? The free official tutorial at [docs.python.org/3/tutorial](https://docs.python.org/3/tutorial/) covers everything here in more depth.
