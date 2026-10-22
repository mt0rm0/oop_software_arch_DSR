# OOP and Software Architecture for Data Scientists

Data Science Retreat · 2-day workshop

Most data science starts in a notebook, and that is fine for exploring. It stops being fine when the code has to be reused, trusted, tested, scheduled or handed to a colleague. This workshop teaches object-oriented programming (OOP) and the software engineering habits around it, using one realistic project the whole way through: predicting which customers of a telecom company are about to cancel their contract.

We start from a messy notebook that works but hides a real bug (notebook 00). Every concept after that is a tool that fixes one of its problems, and on day 2 you turn it into a small, tested Python package.

This repository is meant to stay useful after the workshop. Every notebook explains its ideas in writing, contains solutions, and points to further reading, so you can come back to it whenever you meet a class, a decorator or a design you do not understand.

---

## Who this is for

People moving into data science and AI from other careers. You do not need a computer science background. You should be comfortable with:

- Python basics: variables, functions, lists, dictionaries, loops, `import`
- pandas at the "I have loaded a CSV and filtered rows" level
- the idea of training and evaluating a model with scikit-learn

Not sure? Work through [`notebooks/P0_python_refresher.ipynb`](notebooks/P0_python_refresher.ipynb) before day 1. It ends with a short self-check. If you already write classes regularly, look out for the **Challenge** exercises and the `X` notebooks: they are there for you.

## What you will be able to do afterwards

- Write your own classes with attributes, methods and properties, and decide when a class is better than a function.
- Read unfamiliar code (scikit-learn, pandas, your colleagues' projects) and recognise inheritance, abstract base classes, protocols, special methods and mixins.
- Use encapsulation and abstraction to make preprocessing steps that behave the same on training data and on next month's data.
- Structure a project in layers, so data access, modelling and the entry point can change independently.
- Make code readable for others with type hints, docstrings and dataclasses.
- Fail loudly with meaningful exceptions, log what your pipeline does, and test it with pytest.
- Turn notebook code into an installable package with a command line entry point.

You will not be an expert after two days. You will know what good code looks like, why it looks that way, and where to look things up.

---

## Agenda

Both days run from 09:30 to 17:30, with coffee breaks at 11:00 and 15:45 (15 minutes each) and lunch from 13:00 to 14:00.

### Day 1: OOP foundations, from scripts to objects

| Time | Notebook | What you learn |
| --- | --- | --- |
| 09:30 | Opening | Goals, buddy pairs, setup check |
| 09:50 | [00 Warm-up: what's wrong with this code?](notebooks/00_warmup_whats_wrong.ipynb) | Diagnose a working but fragile notebook, and find its hidden bug |
| 10:20 | [01 Classes and objects](notebooks/01_classes_and_objects.ipynb) | Classes, instances, `__init__`, `self`, methods, properties, class methods |
| 12:00 | [02 Inheritance](notebooks/02_inheritance.ipynb) | Subclasses, overriding, `super()`, when not to inherit |
| 14:00 | [03 Special methods](notebooks/03_special_methods.ipynb) | `__repr__`, `__len__`, `__iter__`, `__eq__`, `__add__`, `__call__` |
| 14:45 | [04 Encapsulation and abstraction](notebooks/04_encapsulation_and_abstraction.ipynb) | Learned state, public vs internal, properties, abstract base classes |
| 16:00 | [05 Polymorphism, duck typing and protocols](notebooks/05_polymorphism_duck_typing_protocols.ipynb) | One function for many models, `typing.Protocol`, ABC vs Protocol |
| 16:50 | [06 Code safari: reading real code](notebooks/06_code_safari_reading_real_code.ipynb) | Find today's concepts in scikit-learn and the standard library |
| 17:20 | Exit ticket | What is still unclear? |

### Day 2: Software engineering and architecture, from objects to software

| Time | Notebook | What you learn |
| --- | --- | --- |
| 09:30 | Recap | Your open questions from day 1 |
| 09:45 | [07 Type hints, docstrings and dataclasses](notebooks/07_type_hints_docstrings_dataclasses.ipynb) | Code that explains itself, validated configuration |
| 11:15 | [08 Design and architecture](notebooks/08_design_and_architecture.ipynb) | Single responsibility, composition, layers, dependency injection, UML |
| 12:15 | [09 Exceptions and logging](notebooks/09_exceptions_and_logging.ipynb) | Custom exceptions, where to catch, logging done right |
| 14:00 | [10 Testing with pytest](notebooks/10_testing_with_pytest.ipynb) | Tests, fixtures, parametrize, what to test in data science code |
| 15:00 | [11 From notebook to package](notebooks/11_from_notebook_to_package.ipynb) | `src` layout, `pyproject.toml`, imports, entry points |
| 15:25 | [12 Capstone](notebooks/12_capstone.ipynb) | Refactor the warm-up into a tested package, in pairs |
| 17:00 | Show and tell, retrospective | What you built, what you take home |

### Self-study and challenge track

| Notebook | For whom |
| --- | --- |
| [P0 Python refresher](notebooks/P0_python_refresher.ipynb) | Before day 1, if your Python feels rusty |
| [X1 Git, DVC and MLflow](notebooks/X1_git_dvc_mlflow.ipynb) | Everyone, after the workshop: versioning code, data and experiments |
| [X2 Build a scikit-learn compatible estimator](notebooks/X2_sklearn_compatible_estimator.ipynb) | Experienced participants, or anyone after the workshop |
| [X3 Design patterns in data science libraries](notebooks/X3_design_patterns_in_ds_libraries.ipynb) | Experienced participants |

---

## How the notebooks work

Every notebook follows the same pattern: a problem from the churn project, the concept that solves it, a short demo, and exercises. Exercises come in three levels:

- **Core**: everyone does these. They practise the main idea with guidance.
- **Stretch**: for when you finish early. Same idea, less guidance.
- **Challenge**: for people who already know OOP. Open questions about design and about how real libraries do it.

Each exercise has a **check cell** with a few `assert` statements. It fails until you have solved the exercise; that is expected. Hints and full solutions are hidden in collapsible blocks below each exercise. Try first, then peek.

Sections called **Going further** are not part of the live session. They are there for later.

Work in your buddy pair. Explaining your code to someone else is one of the fastest ways to find out what you have not understood yet.

---

## Repository map

```text
├── notebooks/            the course: 00-12 live, P0 and X1-X3 self-study
├── src/
│   ├── churn/            reference package: the finished, tested version of the warm-up
│   └── churn_capstone/   your package for the capstone (starts empty)
├── tests/                tests for src/churn (run: uv run pytest)
├── tests_capstone/       acceptance tests for your capstone package
├── configs/              experiment configurations (JSON)
├── data/raw/             the Telco churn dataset, see data/README.md
├── docs/                 cheat sheet, further reading, trainer guide
├── playground/           your scratch space, ignored by git
├── scripts/check_setup.py
└── pyproject.toml        dependencies and tool settings
```

`src/churn` is worth reading on its own: every file is small and its docstring says which notebook it illustrates. Read it after you have tried the capstone yourself.

---

## Setup

You need [git](https://git-scm.com/downloads), [uv](https://docs.astral.sh/uv/getting-started/installation/) and [VS Code](https://code.visualstudio.com/). uv installs the right Python version for you.

```bash
git clone <repo-url>
cd oop_software_arch_DSR
uv sync                                   # creates .venv and installs everything from uv.lock
uv run python scripts/check_setup.py      # every line should say OK
code .
```

In VS Code, accept the recommended extensions (Python, Jupyter, Ruff, Mermaid). Open a notebook, click the kernel picker in the top right corner and choose the interpreter in `.venv` (`.venv/bin/python`, or `.venv\Scripts\python.exe` on Windows).

Please do this before the workshop. If something fails, bring the error message; we will sort it out in the first 20 minutes.

### Commands you will use

```bash
uv run pytest                                  # tests of the reference package
uv run pytest tests_capstone                   # acceptance tests of your capstone package
uv run pytest playground                       # your own experiments with tests
uv run python -m churn --config configs/baseline.json   # train and evaluate the reference model
uv run ruff check . && uv run ruff format .    # lint and format
uv run mypy                                    # type-check src/churn
uv add <package>                               # add a dependency
```

The tracking tools for notebook X1 are optional and large: `uv sync --extra tracking`.

---

## After the workshop

A realistic next step is to take one notebook from your own work and apply the capstone recipe to it: move the reusable parts into a package, put configuration into a dataclass, add three tests, and run it from the command line. Then come back to this repository when you need it:

1. [`docs/cheatsheet.md`](docs/cheatsheet.md) for syntax you have forgotten.
2. [`docs/further_reading.md`](docs/further_reading.md) for books, articles, papers and talks, ordered as a learning path.
3. The **Sources and further reading** section at the end of every notebook, for the references on that one topic.
4. Notebook 08 when you are about to design something bigger, X1 when you start running many experiments, X2 and X3 when you want to write code that plugs into scikit-learn.

If you only read one thing after the workshop, make it [*Architecture Patterns with Python*](https://www.cosmicpython.com/) (free online). If you want to understand Python itself more deeply, read Luciano Ramalho's *Fluent Python*.

## Credits

Dataset: IBM Telco Customer Churn sample, Apache License 2.0, see [`data/README.md`](data/README.md).
