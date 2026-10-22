# Trainer guide

How to run the two days. Written for whoever teaches the workshop, including a colleague who has never seen it before. Methods are named as in the "Methodenkoffer für AI-Workshops" so they can be looked up there.

---

## The design in one page

- **Audience:** career changers into data science, many with a PhD, very mixed programming experience. You cannot predict the level of a batch, so the material is built for all levels at once.
- **Goal:** everybody can write their own classes and understand the code they meet. Experienced participants are challenged, not bored. See `docs/curriculum.md` for the competence targets.
- **One story:** a telecom churn model, real data (`data/raw/telco_churn.csv`). Notebook 00 is a working but fragile notebook with a hidden bug: it re-fits its encoder on each new batch, so a customer's score depends on who else is in the file. Day 1 builds the tools to fix it; day 2 turns the result into a tested package (capstone). The finished version is `src/churn`.
- **Rhythm:** no input block longer than about 20 minutes. Every concept is followed by a hands-on exercise or a check-your-understanding question within 20 to 30 minutes.
- **Differentiation:** every exercise exists at three levels (Core, Stretch, Challenge). The `X` notebooks are a challenge track. The capstone has three test files, one per level.
- **Timing:** 09:00 to 17:00, coffee 10:30 to 10:45 and 15:15 to 15:30, lunch 12:30 to 13:30. That is 6.5 hours of teaching per day, 13 hours in total. The live path through each notebook fits this; everything under "Going further" is self-study.

---

## Before the workshop

**Two weeks before**
- Send the setup instructions from the README and ask everyone to run `uv run python scripts/check_setup.py` and reply with a screenshot or the error.
- Send a short self-assessment (5 minutes, anonymous is fine): "I have written a class before" (never / once or twice / regularly), "I have used git", "I have written a test", "I have built a Python package". Use it to plan buddy pairs and to guess how much Stretch and Challenge material you will need.
- Point people with little Python experience to `notebooks/P0_python_refresher.ipynb` (flipped classroom).

**The day before**
- Pull the repo, run `uv sync`, `uv run pytest` (64 tests green) and `CAPSTONE_PACKAGE=churn uv run pytest tests_capstone` (20 green).
- Open every notebook you will teach and run the demo cells once, so the kernel and data are cached.
- Prepare: a timer visible to everyone, sticky notes and pens, a whiteboard or flip chart with three columns for the KWL chart (Know, Want, Learned), a parking lot area for questions that do not fit the moment.
- Optional: Mentimeter or similar for check-your-understanding votes. Raised fingers (1 to 4) work just as well in a room.

**Buddy pairs.** Pair people across experience levels on day 1 (buddy system): beginners get a guide, experienced participants consolidate by explaining (reciprocal teaching). For the capstone on day 2, pair people of similar level, so both partners type and experienced pairs can go for the Challenge tests.

---

## Day 1: OOP foundations

### 09:00 to 09:20 · Opening (20 min)

| | |
| --- | --- |
| Goal | Arrive, know the plan, working setup, buddy pairs formed |
| Methods | One-word check-in (Ein-Wort-Check-in), advance organizer, KWL chart (first two columns) |
| Trainer | Show the agenda (README) as the advance organizer and keep it visible both days. Explain the churn story in two sentences. Explain Core / Stretch / Challenge and that check cells fail until solved. |
| Participants | One word each: "How do you feel about writing classes?" Write one sticky for "I know" and one for "I want to learn" on the KWL board. Run `scripts/check_setup.py` with their buddy. |
| If setup fails | Pair the person with their buddy's screen for the morning and fix it at the coffee break. Do not debug installations in front of the group. |

### 09:20 to 09:50 · 00 Warm-up: what's wrong with this code? (30 min)

| | |
| --- | --- |
| Goal | Feel the pain the next two days will remove. Find problems, not solutions. |
| Methods | Mystery entry (Mystery-Einstieg), think-pair-share |
| Flow | 3 min: run the notebook top to bottom, it works and the report looks fine. 2 min alone: "Where would this hurt you?" 10 min in pairs with the prompts in the notebook. 10 min plenary: collect problems on the whiteboard, cluster them (affinity mapping light). 5 min: show the "next month's customers" cell and the mystery. Do not explain the cause. |
| Key moment | The same customer gets a different prediction depending on the batch. Leave it open: "By this afternoon you will be able to explain and fix this." Write it on the parking lot. |
| Differentiation | Experienced participants usually spot the bug. Ask them not to reveal it, and to write down how they would design the fix instead. |

### 09:50 to 10:30 and 10:45 to 11:30 · 01 Classes and objects (85 min, coffee in between)

| | |
| --- | --- |
| Goal | Write a class with `__init__`, attributes, methods, a property and a class method. |
| Methods | Live coding with think-aloud, peer instruction, then pair programming (driver and navigator swap every 15 min) |
| Before the break (40 min) | 10 min why classes (loose variables problem). 20 min live coding of the `ConfusionMatrix` class, deliberately making and fixing a typical mistake (forgetting `self`). 10 min check-your-understanding on class vs instance attributes: vote, discuss with someone who voted differently, vote again. |
| After the break (45 min) | 10 min properties and `@classmethod` (`from_predictions`; show that scikit-learn uses the same name). 30 min exercise `ChurnDataset` (Core), Stretch and Challenge for those who finish. 5 min: one pair shows its solution. |
| Watch for | Beginners mixing up the class and the instance (`ConfusionMatrix.precision` vs `cm.precision`). Ask "which customer table? which matrix?" rather than correcting. |

### 11:30 to 12:30 · 02 Inheritance (60 min)

| | |
| --- | --- |
| Goal | Build a small class family that shares code; know when not to inherit. |
| Methods | Demonstration, pair programming, short discussion |
| Flow | 15 min demo: `BaselineModel` with inherited `evaluate`, `MajorityClassModel` (great accuracy, zero recall: discuss why accuracy misleads at 27% churn), `ContractRuleModel`. 10 min `super()` and overriding. 25 min exercise `TenureRuleModel` (Core) and learning the threshold in `fit` (Stretch). 10 min plenary: the "is-a" test, and a teaser that day 2 prefers composition. |
| Challenge track | The `CombinedRuleModel` exercise is a design discussion in disguise. Ask an experienced pair to present it after lunch in 3 minutes. |

### 13:30 to 14:15 · 03 Special methods (45 min)

| | |
| --- | --- |
| Goal | Make objects work with Python syntax where it is meaningful. |
| Methods | Peer instruction ("what does this print?"), live coding, code kata |
| Flow | 5 min after-lunch activation: two "what does this print?" questions. 15 min `__repr__`, `__len__`, `__iter__` (unpacking like scikit-learn's `ravel()`), `__eq__`. 10 min `__add__` for pooling folds and `__call__` for the `RetentionCost` metric. 15 min exercise `CVResult` (Core) or pooling with `__radd__` (Stretch, Challenge). |
| Message to repeat | Only overload an operator when its meaning is obvious. `cm1 + cm2` is obvious; `model_a < model_b` is not. |

### 14:15 to 15:15 · 04 Encapsulation and abstraction (60 min)

| | |
| --- | --- |
| Goal | Solve the morning's mystery. Learned state, internal vs public, abstract base classes. |
| Methods | Socratic dialogue to resolve the mystery, live coding, pair programming |
| Flow | 10 min: back to the parking lot. Ask questions until the group finds the cause (the encoder learns from whatever batch it sees). 15 min: build `OneHotEncoder` with `fit`/`transform` and show the bug is gone. 10 min: `_internal` names (a convention, not a lock), returning copies, a validating property. 5 min: `Transformer` ABC, an incomplete subclass fails at creation. 20 min: exercise `MedianImputer` (Core), unseen categories (Stretch), `TransformerChain` (Challenge). |
| Watch for | The claim "underscore makes it private". It does not; it tells colleagues what they may rely on. |

### 15:30 to 16:20 · 05 Polymorphism, duck typing and protocols (50 min)

| | |
| --- | --- |
| Goal | One function for many kinds of objects; describe interfaces with `Protocol`. |
| Methods | Live coding, pair programming, decision table discussion |
| Flow | 15 min: the leaderboard function evaluating rule baselines and scikit-learn models together. 10 min: duck typing, and why `cross_val_score` still rejects our rule models (it clones, so it needs `get_params`; this is the hook for X2). 10 min: `Protocol` vs ABC, decision table. 15 min: exercise (add `GradientBoostingClassifier` without touching the function; Stretch and Challenge on probabilities and cost-optimal thresholds). |
| Energy | This is the low point of the afternoon. Keep the input short and let people type. |

### 16:20 to 16:50 · 06 Code safari: reading real code (30 min)

| | |
| --- | --- |
| Goal | Recognise the day's concepts in real library code. This directly trains "understand code you see". |
| Methods | Jigsaw (expert groups per station), short report back |
| Flow | 2 min: assign one station per pair. 15 min: pairs work through their station's questions. 10 min: each pair explains its finding in one minute ("we found a mixin, here is what it does"). 3 min: the reading checklist at the end of the notebook. |
| Differentiation | Give the most experienced pair the `BaseEstimator.get_params` challenge. |

### 16:50 to 17:00 · Exit ticket (10 min)

KWL third column ("what I learned", one sticky each) and a muddiest-point card: "What is still unclear?" Collect the cards. Read them in the evening and pick the two or three most frequent themes for tomorrow's recap.

---

## Day 2: Software engineering and architecture

### 09:00 to 09:15 · Recap (15 min)

Answer the most common muddiest points from the exit tickets, with code, briefly. Then three peer-instruction questions mixing day 1 topics (one each on instance state, inheritance, a special method). Vote, discuss, vote again.

### 09:15 to 10:30 · 07 Type hints, docstrings and dataclasses (75 min)

| | |
| --- | --- |
| Goal | Write code that explains itself; replace config dicts by validated dataclasses. |
| Methods | Demonstration, code kata, pair programming |
| Flow | 5 min hook: the config dict with a typo that silently does nothing. 15 min type hints essentials and a mypy run (show it in the terminal). 10 min Google-style docstrings, `help()`. 10 min Core exercise: annotate and document. 15 min dataclasses: generated methods, `field(default_factory=...)`, `__post_init__` validation, `frozen=True`, `from_json`. 15 min Core exercise: the experiment config dataclass. 5 min: Pydantic in one slide, "validate at the boundary". |
| Challenge track | The Pydantic exercise and the question "where should validation live?" |

### 10:45 to 11:45 · 08 Design and architecture (60 min)

| | |
| --- | --- |
| Goal | Single responsibility, composition, layers, dependency injection, reading and drawing UML. |
| Methods | Code review of a "god class", sketching in pairs, gallery walk |
| Flow | 10 min: show the god class, ask "how would you test this without the CSV file?" 15 min: concepts with the refactored version (composition, layers, dependency injection). 15 min: pairs sketch the class diagram of the refactored warm-up on paper or in Mermaid. 10 min: gallery walk, everyone leaves one sticky ("I like", "I wonder") on two other diagrams. 10 min: Core coding exercise (inject the loader) or Stretch (SQLite loader). |
| Challenge track | The code review exercise with four design problems. Experienced participants can do this instead of the sketch. |

### 11:45 to 12:30 · 09 Exceptions and logging (45 min)

| | |
| --- | --- |
| Goal | Fail loudly with useful errors; log like an application, not like a script. |
| Methods | Debugging exercise, live coding |
| Flow | 5 min: a function that returns `None` on bad data and the silent damage it causes downstream. 15 min: raising the right exception, the project hierarchy, `raise ... from`, catching at the boundary. 10 min: module loggers, levels, why libraries never call `basicConfig` (show `src/churn/__main__.py`). 15 min: exercise `validate_batch` (Core), wrapping and logging (Stretch), `ExceptionGroup` (Challenge). |

### 13:30 to 14:30 · 10 Testing with pytest (60 min)

| | |
| --- | --- |
| Goal | Write and run tests; know what to test in data science code. |
| Methods | Live coding in the terminal, code kata, test-first bug fix |
| Flow | 15 min: run `uv run pytest` on the repo, open `tests/test_features.py` and read two tests together (Arrange, Act, Assert). 15 min: asserts, `pytest.approx`, `pytest.raises`, fixtures, parametrize, demonstrated in the notebook. 25 min: participants write tests in `playground/` (Core: ConfusionMatrix tests; Stretch: parametrize and fixtures; Challenge: reproduce the warm-up bug as a failing test, then fix it). 5 min: what not to test. |
| Watch for | People calling fixtures directly. pytest injects them by argument name. |

### 14:30 to 14:55 · 11 From notebook to package (25 min)

| | |
| --- | --- |
| Goal | Understand the project layout well enough to start the capstone. |
| Methods | Guided walkthrough with checkpoints |
| Flow | Tour of the repository tree, `pyproject.toml` section by section, what `uv sync` did, `import churn` from anywhere, `python -m churn`, `uv run churn-train`. Checkpoint: everyone runs `uv run pytest tests_capstone` and sees red tests. That red is the starting point of the capstone. |

### 14:55 to 15:15 and 15:30 to 16:30 · 12 Capstone (80 min, coffee in between)

| | |
| --- | --- |
| Goal | Refactor the warm-up notebook into the `churn_capstone` package until the acceptance tests pass. |
| Methods | Pair programming (driver and navigator, swap every 15 minutes), hackathon light |
| Levels | Core tests: everyone aims for these. Stretch tests: configuration, error hierarchy, a useful model. Challenge tests: robustness and persistence, then the extension menu in the notebook. |
| Trainer | Walk around. When a pair is stuck, ask what the failing test expects before looking at their code. Keep a visible tally of passing tests per pair if the group likes a bit of competition; skip it if it creates pressure. At 16:20 announce ten minutes left and ask pairs to prepare their show and tell. |

### 16:30 to 17:00 · Closing (30 min)

| | |
| --- | --- |
| Show and tell (15 min) | Five or six pairs, 2 minutes each: one design decision they are proud of, one they are unsure about. The trainer links each to `src/churn`. |
| Retrospective (10 min) | Start, stop, continue: one sticky per column per person, about the workshop and about their own way of coding. |
| Transfer (5 min) | Each person writes down one notebook from their own work they will apply the capstone recipe to in the next two weeks, and the first step they will take (transfer task). Finish the KWL board. |

---

## Differentiation toolbox

- **Three exercise levels** in every notebook. Tell the group explicitly that nobody is expected to finish Challenge exercises, and that skipping Stretch is fine.
- **Challenge track notebooks** X2 and X3 for participants who finish everything early. X2 (scikit-learn compatible estimators) connects directly to notebook 05 and 06.
- **Reciprocal teaching:** an experienced participant who is done may explain their solution to a pair that is stuck. Offer, do not impose: they also came to learn.
- **Parking lot** for deep questions (metaclasses, descriptors, async). Answer them during breaks or point to "Going further" sections.
- **Mixed pairs on day 1, similar-level pairs in the capstone.**

## If you run late (cutting plan)

Cut in this order; each item is covered in writing in the notebook, so nothing is lost for later self-study:

1. 03: context managers and `__radd__` (keep `__repr__`, `__iter__`, `__add__`, `__call__`).
2. 05: mixins; shorten the ABC vs Protocol discussion to the decision table.
3. 06: run three stations instead of five.
4. 07: Pydantic.
5. 08: replace the gallery walk by two diagrams discussed in plenary.
6. 09: `try/except/else/finally` details and warnings.
7. 11: shrink to the checkpoint (`uv run pytest tests_capstone`).

Never cut the capstone below 60 minutes or the exit ticket and the recap: they carry the learning of the whole workshop.

## If the group is fast

- Give more time to Challenge exercises and ask pairs to present them.
- Start X2 after notebook 06 (end of day 1) or X3 after notebook 08.
- In the capstone, add the extension menu items as requirements: CLI entry point, experiment tracking from X1, cost-optimal threshold.

## Common stumbling blocks

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `FileNotFoundError: ../data/raw/telco_churn.csv` | Notebook started from another working directory | Open the notebook from the `notebooks/` folder in VS Code, or check the kernel's cwd with `import os; os.getcwd()` |
| `ModuleNotFoundError: churn` | Kernel is not the project `.venv`, or `uv sync` was not run | Select `.venv` in the kernel picker; run `uv sync` |
| `TypeError: ... missing 1 required positional argument: 'self'` | Calling a method on the class instead of an instance | Create the object first |
| Changes in `src/` not visible in the notebook | Module already imported | Restart the kernel (or use `%load_ext autoreload` and `%autoreload 2`) |
| Capstone tests show "Create the module ..." | Expected at the start | Create the file the message names |
