# Curriculum: OOP and Software Architecture for Data Scientists

*Subject part (Fachteil) of the "Rahmenlehrplan für AI-Workshops". Structure follows the framework template: contribution, competence areas, standards per level, topic fields, scope. German terms of the framework are given in brackets where they first appear.*

Status: version 1.0, October 2026

---

## 0. Place in the framework

The framework describes learning along three independent axes: **content** (Inhalt, here the topic fields in section 4), **competence area** (Kompetenzbereich, the same five areas for every part) and **level** (Niveaustufe, 1 to 4). A standard is one cell of that cube: a topic develops a competence at a level.

This workshop is not about a specific AI technique. It builds the programming and design foundation that every technical subject part in Teil C (RAG, agentic systems, fine-tuning, LLM engineering and operations) silently assumes: being able to read, write, structure and test Python code that other people can rely on. It is therefore proposed as a technical subject part of its own, usually taken before the Teil C workshops by participants with a technical profile.

Cross-cutting competences from **Teil B** are embedded, not taught separately (see section 5): testing, error handling and logging are the code-level form of the cluster "Quality and evaluation" (Qualität & Evaluation).

### Target group profile (Profil-Dimensionen)

| Axis | Position of the typical participant |
| --- | --- |
| Technical depth (Technische Tiefe) | Medium to high, and very heterogeneous. Everyone writes some Python; a few have years of software experience, others have only used notebooks. |
| Scope of action and responsibility (Handlungsradius & Verantwortung) | Operational: they will implement, not decide strategy. |
| Context of use (Nutzungskontext) | From personal productivity (their own notebooks) towards team scale (code others reuse, review and deploy). |

Typical participant: career changer into data science or AI, often with a PhD in another field, in a full-time bootcamp. Prior programming knowledge is a recommended entry point for self-assessment, not an entry requirement (see the self-check in `notebooks/P0_python_refresher.ipynb`).

### Target level profile

Because the group is heterogeneous, the workshop sets a target for everyone (Core) and a higher one for experienced participants (Challenge track). Every notebook offers exercises at three levels for this reason.

| Competence area | Core target (everyone) | Challenge track |
| --- | --- | --- |
| Understand (Verstehen & Einordnen) | 2 | 3 |
| Apply (Anwenden) | 2 | 3 |
| Analyse and evaluate (Analysieren & Bewerten) | 1-2 | 3 |
| Communicate (Kommunizieren) | 2 | 3 |
| Design and take responsibility (Gestalten & Verantworten) | 1-2 | 3 |

Level 4 (production readiness) is not a target of a two-day workshop. The reference package `src/churn` shows what level-4 work looks like so participants can see where the path leads.

---

## 1. Contribution to competence development (Beitrag zum Kompetenzerwerb)

Participants learn to move from notebook code that "works on my machine" to code that others can read, reuse, test and run without the author present. They learn the object-oriented vocabulary of Python (classes, inheritance, special methods, encapsulation, abstraction, polymorphism, protocols) well enough to write their own classes and, just as important, to understand the code of the libraries they use every day. On this basis they learn the basic habits of software engineering and architecture: separating responsibilities, layering, dependency injection, explicit configuration, meaningful errors, logging, automated tests and packaging.

The subject part is distinct from the AI subject parts because its content is not a model or a technique but the craft of building with them. It is the reason a RAG prototype or an agent can later be turned into something a team can maintain.

---

## 2. Competence areas (Kompetenzbereiche)

The five general competences of the framework, applied to this subject.

| Competence area | What it means here, for example |
| --- | --- |
| **Understand** (Verstehen & Einordnen) | Explain OOP concepts in your own words; recognise them in unfamiliar code (scikit-learn, pandas, colleagues' code) and explain what a given class does and why it is built that way. |
| **Apply** (Anwenden) | Write classes, subclasses, dataclasses, exceptions and tests for your own data science tasks; use the project tooling (uv, pytest, ruff, mypy). |
| **Analyse and evaluate** (Analysieren & Bewerten) | Spot fragility in code (hidden state, duplication, silent failures, data leakage through preprocessing); weigh design alternatives such as inheritance vs composition or ABC vs Protocol. |
| **Communicate** (Kommunizieren) | Make code understandable for others: names, docstrings, type hints, UML sketches, explaining a design decision in a code review. |
| **Design and take responsibility** (Gestalten & Verantworten) | Structure a small project into layers and modules, decide what to test, and stand behind the result. |

---

## 3. Standards per competence area and level

The standards are independent of the topic field: they describe what is reached at each level, whatever content it was practised on.

### Understand (Verstehen & Einordnen)

| Level | Participants can ... |
| --- | --- |
| 1 - Basics | explain what a class, an object, a method and an attribute are, using an example from their own work. |
| 2 - Application | read a class they have not seen before and describe its responsibilities, its public interface and its relation to other classes. |
| 3 - Deepening | explain how several concepts work together in a real library (for example how scikit-learn uses mixins, the template method and fitted attributes) and why the authors chose them. |
| 4 - Production readiness | derive the architecture of a larger code base from its structure and conventions and judge where a change belongs. |

### Apply (Anwenden)

| Level | Participants can ... |
| --- | --- |
| 1 - Basics | instantiate and use given classes and complete a class from a template. |
| 2 - Application | write their own classes, subclasses, properties, dataclasses and simple tests for a given data science task. |
| 3 - Deepening | combine abstract base classes, protocols, composition and custom exceptions into a small, consistent package with tests and an entry point. |
| 4 - Production readiness | build code that integrates with established frameworks (for example scikit-learn compatible estimators) and keep it reliable over time. |

### Analyse and evaluate (Analysieren & Bewerten)

| Level | Participants can ... |
| --- | --- |
| 1 - Basics | recognise that code which runs can still be wrong, fragile or hard to reuse. |
| 2 - Application | name concrete problems in a piece of code (duplication, magic numbers, hidden state, swallowed errors) using simple criteria. |
| 3 - Deepening | diagnose the cause of a subtle defect (such as re-fitting an encoder on new data) and evaluate design alternatives by their trade-offs. |
| 4 - Production readiness | assess the maintainability and risk of a code base and derive a prioritised refactoring plan. |

### Communicate (Kommunizieren)

| Level | Participants can ... |
| --- | --- |
| 1 - Basics | describe in their own words what their code does. |
| 2 - Application | document code with clear names, docstrings and type hints so a colleague can use it without asking. |
| 3 - Deepening | explain and defend a design decision in a code review or with a UML sketch, and respond to objections. |
| 4 - Production readiness | set and communicate coding and design conventions for a team. |

### Design and take responsibility (Gestalten & Verantworten)

| Level | Participants can ... |
| --- | --- |
| 1 - Basics | refactor a small piece of code under guidance. |
| 2 - Application | turn their own notebook code into functions, classes and modules with a few tests. |
| 3 - Deepening | design a small layered package on their own, weigh trade-offs and choose what to test. |
| 4 - Production readiness | own the design, quality and evolution of production code, including review and release processes. |

---

## 4. Topic fields and competence development (Themenfelder und Kompetenzerwerb)

Each topic field corresponds to one notebook. The table lists the standards a topic field can develop; Core exercises target the lower level, Stretch and Challenge exercises the higher one.

### 00 Diagnosing fragile notebook code

| Competence (level) | Competence development in this topic field |
| --- | --- |
| Analyse and evaluate (1) | recognise that a notebook which runs and prints good metrics can still be unusable for reuse and production. |
| Analyse and evaluate (2) | name concrete problems: loose state, duplicated preprocessing, magic numbers, silent data loss. |
| Communicate (2) | discuss the problems with a partner and agree on the most damaging one. |

**Tools:** Jupyter, pandas, scikit-learn. **Possible contexts:** taking over a colleague's analysis; preparing a notebook model for a monthly scoring job.

### 01 Classes and objects

| Competence (level) | Competence development in this topic field |
| --- | --- |
| Understand (1) | explain class vs instance, `__init__`, `self`, attributes and methods. |
| Apply (2) | write a class that bundles data and behaviour (a confusion matrix, a dataset wrapper), including properties and an alternative constructor. |
| Design (3) | decide whether a method should mutate the object or return a new one, and justify it. |

**Tools:** Python classes, `@property`, `@classmethod`. **Possible contexts:** replacing ten loose notebook variables with one object; evaluating a model at two thresholds.

### 02 Inheritance

| Competence (level) | Competence development in this topic field |
| --- | --- |
| Understand (2) | explain inheritance, overriding and `super()`, and read a class hierarchy. |
| Apply (2) | build a family of baseline models that share evaluation code. |
| Analyse and evaluate (3) | apply the "is-a" test and recognise when composition is the better tool. |

**Tools:** subclassing, `super()`, `isinstance`, MRO. **Possible contexts:** comparing a model against simple business rules and a majority-class baseline.

### 03 Special methods (the Python data model)

| Competence (level) | Competence development in this topic field |
| --- | --- |
| Understand (2) | explain which syntax triggers which special method (`len()`, `[]`, `for`, `==`, `+`, calling). |
| Apply (2) | make own objects printable, iterable, comparable and callable where it is meaningful. |
| Analyse and evaluate (3) | judge when operator overloading is clear (pooling confusion matrices) and when it misleads (ordering models by one metric). |

**Tools:** `__repr__`, `__len__`, `__getitem__`, `__iter__`, `__eq__`, `__add__`/`__radd__`, `__call__`, context managers. **Possible contexts:** cross-validation results, business cost metrics.

### 04 Encapsulation and abstraction

| Competence (level) | Competence development in this topic field |
| --- | --- |
| Understand (2) | explain learned state (fit/transform), public vs internal names, and abstract base classes. |
| Apply (2) | implement preprocessing steps that learn on training data and replay identically on new data. |
| Analyse and evaluate (3) | diagnose the warm-up's re-fitting bug and explain how the design prevents it. |

**Tools:** `_internal` names, properties with validation, `abc.ABC`, `@abstractmethod`. **Possible contexts:** scoring next month's customers with the same encoding as in training.

### 05 Polymorphism, duck typing and protocols

| Competence (level) | Competence development in this topic field |
| --- | --- |
| Understand (2) | explain polymorphism and duck typing and how scikit-learn relies on conventions. |
| Apply (2) | write one evaluation function that works for own models and scikit-learn models. |
| Analyse and evaluate (3) | choose between ABC and `typing.Protocol` for a given situation and justify it. |

**Tools:** `typing.Protocol`, `runtime_checkable`, mixins. **Possible contexts:** a model leaderboard; plugging a new library model into existing code.

### 06 Reading real code

| Competence (level) | Competence development in this topic field |
| --- | --- |
| Understand (2) | find and name the day's concepts in scikit-learn and standard library source code. |
| Understand (3) | explain why scikit-learn's design (parameters in `__init__`, fitted attributes, mixins) supports cloning and pipelines. |
| Communicate (2) | explain a piece of library code to peers (jigsaw). |

**Tools:** `inspect`, editor "go to definition". **Possible contexts:** debugging a library error message; learning a new framework from its source.

### 07 Type hints, docstrings and dataclasses

| Competence (level) | Competence development in this topic field |
| --- | --- |
| Communicate (2) | document functions and classes with type hints and Google-style docstrings. |
| Apply (2) | replace configuration dictionaries with validated dataclasses. |
| Analyse and evaluate (3) | decide where validation belongs (dataclass vs Pydantic at the system boundary). |

**Tools:** `typing`, mypy, `dataclasses`, Pydantic. **Possible contexts:** experiment configuration files; sharing a function with another team.

### 08 Design and architecture

| Competence (level) | Competence development in this topic field |
| --- | --- |
| Understand (2) | explain single responsibility, composition, layers and dependency injection. |
| Communicate (2) | read and sketch UML class diagrams of a small system. |
| Design (3) | split a "god class" into layered components and justify the design in a review. |

**Tools:** Mermaid class diagrams, Protocols for dependencies. **Possible contexts:** switching data source from CSV to a database; making a pipeline testable.

### 09 Exceptions and logging

| Competence (level) | Competence development in this topic field |
| --- | --- |
| Apply (2) | raise meaningful built-in and custom exceptions and catch them at the right boundary. |
| Apply (2) | log pipeline steps with module loggers and appropriate levels. |
| Analyse and evaluate (3) | explain why swallowing errors and configuring logging inside a library are harmful. |

**Tools:** exception hierarchies, `raise ... from`, `logging`, `ExceptionGroup`. **Possible contexts:** validating a monthly scoring batch; a nightly job that must fail loudly.

### 10 Testing with pytest

| Competence (level) | Competence development in this topic field |
| --- | --- |
| Apply (2) | write and run tests with asserts, fixtures, parametrize and `pytest.raises`. |
| Analyse and evaluate (3) | decide what is worth testing in data science code (cleaning rules, transformer invariants, batch independence) and what is not. |
| Design (3) | reproduce a bug as a failing test before fixing it. |

**Tools:** pytest, `conftest.py`, `tmp_path`, pytest-cov. **Possible contexts:** preventing the return of a silent preprocessing bug; refactoring safely.

### 11 From notebook to package

| Competence (level) | Competence development in this topic field |
| --- | --- |
| Understand (2) | explain the src layout, `pyproject.toml`, editable installs and imports. |
| Apply (2) | move code into modules and run it from the command line. |

**Tools:** uv, hatchling, `[project.scripts]`, ruff, mypy. **Possible contexts:** scheduling a training job; handing over a project.

### 12 Capstone

| Competence (level) | Competence development in this topic field |
| --- | --- |
| Design (2) | refactor the warm-up notebook into a package that passes the Core acceptance tests. |
| Design (3) | reach the Stretch and Challenge tests: configuration, error hierarchy, persistence, robustness to unseen data. |
| Communicate (3) | present one design decision and defend it (show and tell). |

**Tools:** everything above. **Possible contexts:** the first week of turning a prototype into a product.

### Self-study topic fields

- **X1 Versioning code, data and experiments** (Understand 2, Apply 2): git habits, DVC, MLflow.
- **X2 scikit-learn compatible estimators** (Apply 3-4, Understand 3): `BaseEstimator`, mixins, `check_estimator`.
- **X3 Design patterns in data science libraries** (Understand 3, Analyse and evaluate 3): strategy, template method, composite, factory and registry, adapter.

---

## 5. Embedded cross-cutting competences (Teil B)

| Teil B topic field | Where it is embedded | Level reached |
| --- | --- | --- |
| Error types and quality dimensions (Fehlerarten und Qualitätsdimensionen) | 00 (silent errors), 04 (re-fitting bug), 09 (fail loudly) | Understand 2, Analyse 2 |
| Evaluation metrics and methods (Evaluationsmetriken und -methoden) | 01 and 03 (confusion matrix, precision and recall, business cost metric), 05 (leaderboard) | Apply 2-3 |
| Monitoring and tracing landscape (Monitoring- & Tracing-Landschaft) | 09 (logging), X1 (experiment tracking) | Understand 2 |
| Testing as quality assurance | 10, 12 (acceptance tests) | Apply 2-3 |

---

## 6. Evidence of learning

- **Check cells** in every exercise give immediate feedback on Apply standards.
- **Check-your-understanding questions** (peer instruction) make Understand standards visible during the session.
- **Exit ticket** at the end of day 1 and the recap on day 2 show what is still unclear.
- **Capstone acceptance tests** map to levels: `test_1_core.py` corresponds to Apply/Design level 2, `test_2_stretch.py` and `test_3_challenge.py` to level 3.
- **Show and tell** gives evidence for Communicate level 2-3.

---

## Scope (Abgrenzung)

Not part of this subject part, and where it belongs instead:

- A systematic catalogue of design patterns: only introduced in X3; a separate advanced workshop.
- Concurrency, async and performance optimisation: separate topic.
- Serving models through web APIs (FastAPI), containers and deployment: Teil C "LLM Engineering & Operations" or an MLOps workshop.
- Data engineering (orchestration, warehouses, streaming): separate topic.
- Deep learning frameworks and their module systems (PyTorch `nn.Module`): only mentioned as an example of `__call__`.
- The AI techniques themselves (RAG, agents, fine-tuning): Teil C subject parts, which build on this one.
