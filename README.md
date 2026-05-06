# OOP and Software Architecture for Data Scientists

**Data Science Retreat · 2 days · 16 hours**

This course teaches OOP and software engineering/architecture fundamentals through the lens of data science. We are not going to build abstract toy examples, but to apply every concept to real ML problems: feature pipelines, training loops, config management, and production hardening.

---

## The Through-Line

We start with a broken notebook (session 00). We end with production-grade code (session 14). Every concept in between is a tool that fixes something wrong with that original code.

---

## Structure

### Day 1 - Writing Code That Doesn't Rot

| # | Notebook | Time | What you learn |
|---|---|---|---|
| 00 | Warmup: What's Wrong With This Code? | 30 min | Diagnose a realistic messy notebook |
| 01 | Intro to OOP | 90 min | Classes, objects, `__init__`, methods, properties |
| 02 | Inheritance | 60 min | Subclasses, method overriding, `super()`, MRO |
| 03 | Docstrings and Type Hints | 75 min | Google-style docstrings, type annotations, DS-specific patterns, `Callable`, `TypeAlias`, `TYPE_CHECKING` |
| 04 | Special Methods | 60 min | `__str__`, `__len__`, `__getitem__`, context managers |
| 05 | Encapsulation, Abstraction & Layering | 90 min | `_protected` attributes, ABCs, data leakage, layered architecture |
| 06 | Polymorphism, Duck Typing & Protocols | 75 min | Polymorphic pipelines, duck typing, the tension with type hints, structural typing with `Protocol` |

### Day 2 - Code That Works in Production

| # | Notebook | Time | What you learn |
|---|---|---|---|
| 07 | UML Class Diagrams | 30 min | Sketch first, code second |
| 08 | Dataclasses and Pydantic | 60 min | Structured config, validation, `@classmethod` factories |
| 09 | Project Structure | 60 min | `src` layout, `pyproject.toml`, `__init__.py` |
| 10 | Logging | 60 min | Log levels, handlers, JSON logs, loguru |
| 11 | Handling Exceptions | 60 min | Custom hierarchies, propagation, when NOT to catch |
| 12 | Testing with pytest | 90 min | Fixtures, parametrize, ML-specific tests, mocking |
| 13 | Capstone: Refactoring | 120 min | Transform the warm-up spaghetti into production code |
| 14 | Git, DVC, and MLflow | 60 min | Reproducible experiments end-to-end |

---

## Setup

This repo uses **uv** for dependency management and **VS Code** as the IDE.

```bash
# 1. Clone
git clone <repo-url>
cd oop_software_arch_DSR

# 2. Create the venv and install all dependencies (reads uv.lock for exact pins)
uv sync --extra dev

# 3. Open in VS Code — it will detect .venv automatically
code .
```

VS Code will prompt you to install the recommended extensions on first open (Jupyter, Ruff, mypy, Mermaid preview). Accept them all.

**Selecting the kernel in a notebook:**
Open any `.ipynb` → click the kernel picker (top right) → choose the interpreter at `.venv/bin/python` (it should have the same name as the project). VS Code remembers this per-workspace.

**Running tests:**

```bash
uv run pytest
```

**Adding a new dependency:**

```bash
uv add <package>          # runtime
uv add --dev <package>    # dev only
```

Python 3.13 required (pinned in `.python-version`).

---

## Prerequisites

- Python basics (functions, lists, dicts)
- pandas and sklearn at a "I've used them before" level
- Git basics (if not: go to [learngitbranching.js.org](https://learngitbranching.js.org/) first)

---

## What's Not Here

- Deep dive into design patterns (Factory, Observer, Strategy) — that's a separate course
- Concurrency and async — out of scope for batch ML
- API deployment (FastAPI) — mentioned in the capstone as a "next step" option
