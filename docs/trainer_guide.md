# Trainer guide

How to run the two days. Written for whoever teaches the workshop, including a colleague who has never seen it before.

---

## The design in one page

- **Audience:** career changers into data science, many with a PhD, very mixed programming experience. It's very difficult to predict the level of a batch, so the material is built for all levels at once.
- **Goal:** everybody can write their own classes and understand the code they meet. Experienced participants are challenged, not bored.
- **One story:** a telecom churn model, real data (`data/raw/telco_churn.csv`). Notebook 00 is a working but fragile notebook with a hidden bug: it re-fits its encoder on each new batch, so a customer's score depends on who else is in the file. Day 1 builds the tools to fix it; day 2 turns the result into a tested package (capstone). The finished version is `src/churn`.
- **Rhythm:** no input block longer than about 20 minutes. Every concept is followed by a hands-on exercise or a check-your-understanding question within 20 to 30 minutes.
- **Differentiation:** every exercise exists at three levels (Core, Stretch, Challenge). The `X` notebooks are a challenge track. The capstone has three test files, one per level.
- **Hands-on, then talk:** every exercise is done at the computer and ends with a **Discuss** question. The coding builds the skill; the discussion is where design judgement grows.
- **Flexible format:** every exercise works alone or in pairs, on site or online. You decide on the day (see the next section).
- **Timing:** 09:30 to 17:30, coffee 11:00 to 11:15 and 15:45 to 16:00, lunch 13:00 to 14:00. That is 6.5 hours of teaching per day, 13 hours in total. The live path through each notebook fits this; everything under "Going further" is self-study.

---

## Choosing the format on the day

You will not always know in advance whether the group is in the room or online, and whether pairing will work for this batch. The material does not force a choice: every exercise is written so one person can do it alone at their computer, and every exercise ends with a **Discuss** question that works for a pair, a breakout room or the whole group.

**Solo or pairs**

| | Solo | Pairs |
| --- | --- | --- |
| Coding | Everyone types in their own notebook. | Driver types, navigator reviews and thinks ahead; swap at every exercise. Both keep the solution in their own notebook afterwards (copy it over). |
| Discuss question | Write a two-sentence answer in a markdown cell, then compare in the debrief. | Talk it through before moving on; agree on an answer or note the disagreement. |
| Good for | Very mixed levels, people who need to type everything themselves, short exercises. | Long exercises, the capstone, groups where beginners need support. |

A practical default: solo for the short Core exercises, pairs for Stretch/Challenge and the capstone. Switch whenever the room's energy asks for it.

**On site or online**

| Activity | On site | Online |
| --- | --- | --- |
| Pair work | Two people at one laptop, or side by side | Breakout rooms of two; the driver shares their screen, or both use VS Code Live Share |
| Quick votes (check your understanding) | Raised fingers (1 to 4) | Poll or reactions in the video tool, or answers typed in the chat |
| Collecting ideas (warm-up problems, KWL, retrospective) | Whiteboard or flip chart | A shared board or document (Miro, a shared doc, the chat) prepared in advance |
| Looking at other people's work (diagrams, solutions) | Laptops open, people walk around | Paste the Mermaid code or a screenshot into the shared board; two or three people share their screen |
| Helping stuck people | Walk around | Visit breakout rooms in turn; ask people to post "stuck on exercise 4.1" in the chat |

**Debriefing the Discuss questions.** After each exercise block, take 3 to 5 minutes for one or two Discuss questions in plenary. Ask for two different answers rather than one right one. Online, ask everyone to type a one-line answer in the chat first, then pick two to discuss: it keeps quiet participants in the conversation.

---

## Before the workshop

**Two weeks before**
- Send the setup instructions from the README and ask everyone to run `uv run python scripts/check_setup.py` and reply with a screenshot or the error.
- Send a short self-assessment (5 minutes, anonymous is fine): "I have written a class before" (never / once or twice / regularly), "I have used git", "I have written a test", "I have built a Python package". Use it to plan pairs (if you pair) and to guess how much Stretch and Challenge material you will need.
- Point people with little Python experience to `notebooks/P0_python_refresher.ipynb` (flipped classroom).

**The day before**
- Pull the repo, run `uv sync`, `uv run pytest` (64 tests green) and `CAPSTONE_PACKAGE=churn uv run pytest tests_capstone` (20 green).
- Open every notebook you will teach and run the demo cells once, so the kernel and data are cached.
- Prepare a visible timer and a place to collect things: a whiteboard or flip chart on site, a shared board or document online (prepare both if you are unsure). On it: three columns for the KWL chart (Know, Want, Learned) and a parking lot for questions that do not fit the moment.
- Online: test breakout rooms and screen sharing, and make sure everyone can install the VS Code Live Share extension if you plan to pair.
- Optional: a polling tool for check-your-understanding votes. Raised fingers or the chat work just as well.

**If you work in pairs.** Pair people across experience levels on day 1: beginners get a guide, experienced participants consolidate by explaining. For the capstone on day 2, pair people of similar level, so both partners type and experienced pairs can go for the Challenge tests. If pairing does not work for a group (or online fatigue sets in), switch to solo work plus plenary debriefs; the exercises do not change.

---

## Day 1: OOP foundations

### 09:30 to 09:50 · Opening (20 min)

| | |
| --- | --- |
| Goal | Arrive, know the plan, working setup, decide solo or pairs |
| Methods | One-word check-in, advance organizer, KWL chart (first two columns) |
| Trainer | Show the agenda (README) as the advance organizer and keep it visible both days. Explain the churn story in two sentences. Explain Core / Stretch / Challenge and that check cells fail until solved. |
| Participants | One word each (aloud or in the chat): "How do you feel about writing classes?" Add one note for "I know" and one for "I want to learn" to the KWL board. Run `scripts/check_setup.py`. |
| If setup fails | Pair the person with a neighbour's screen (online: a breakout room with screen sharing) for the morning and fix it at the coffee break. Do not debug installations in front of the group. |

### 09:50 to 10:20 · 00 Warm-up: what's wrong with this code? (30 min)

| | |
| --- | --- |
| Goal | Feel the pain the next two days will remove. Find problems, not solutions. |
| Methods | Mystery opener, think-pair-share |
| Flow | 3 min: run the notebook top to bottom, it works and the report looks fine. 12 min alone or in pairs: the hands-on investigation tasks in the notebook, notes in the notes cell. 10 min plenary: collect problems on the shared board, cluster them. 5 min: show the "next month's customers" cell and the mystery. Do not explain the cause. |
| Key moment | The same customer gets a different prediction depending on the batch. Leave it open: "By this afternoon you will be able to explain and fix this." Write it on the parking lot. |
| Differentiation | Experienced participants usually spot the bug. Ask them not to reveal it, and to write down how they would design the fix instead. |

### 10:20 to 11:00 and 11:15 to 12:00 · 01 Classes and objects (85 min, coffee in between)

| | |
| --- | --- |
| Goal | Write a class with `__init__`, attributes, methods, a property and a class method. |
| Methods | Live coding with think-aloud, peer instruction, then pair programming (driver and navigator swap every 15 min) |
| Before the break (40 min) | 10 min why classes (loose variables problem). 20 min live coding of the `ConfusionMatrix` class, deliberately making and fixing a typical mistake (forgetting `self`). 10 min check-your-understanding on class vs instance attributes: everyone predicts and votes, discuss with someone who voted differently (pair or breakout room), vote again, then run the prediction cell. |
| After the break (45 min) | 10 min properties and `@classmethod` (`from_predictions`; show that scikit-learn uses the same name). 30 min exercise `ChurnDataset` (Core), Stretch and Challenge for those who finish. 5 min: one person or pair shares their screen and solution; debrief one Discuss question. |
| Watch for | Beginners mixing up the class and the instance (`ConfusionMatrix.precision` vs `cm.precision`). Ask "which customer table? which matrix?" rather than correcting. |

### 12:00 to 13:00 · 02 Inheritance (60 min)

| | |
| --- | --- |
| Goal | Build a small class family that shares code; know when not to inherit. |
| Methods | Demonstration, pair programming, short discussion |
| Flow | 15 min demo: `BaselineModel` with inherited `evaluate`, `MajorityClassModel` (great accuracy, zero recall: discuss why accuracy misleads at 27% churn), `ContractRuleModel`. 10 min `super()` and overriding. 25 min exercise `TenureRuleModel` (Core) and learning the threshold in `fit` (Stretch). 10 min plenary: the "is-a" test, and a teaser that day 2 prefers composition. |
| Challenge track | The `CombinedRuleModel` exercise is a design discussion in disguise. Ask someone who did it to present it after lunch in 3 minutes. |

### 14:00 to 14:45 · 03 Special methods (45 min)

| | |
| --- | --- |
| Goal | Make objects work with Python syntax where it is meaningful. |
| Methods | Peer instruction ("what does this print?"), live coding, code kata |
| Flow | 5 min after-lunch activation: two "what does this print?" questions. 15 min `__repr__`, `__len__`, `__iter__` (unpacking like scikit-learn's `ravel()`), `__eq__`. 10 min `__add__` for pooling folds and `__call__` for the `RetentionCost` metric. 15 min exercise `CVResult` (Core) or pooling with `__radd__` (Stretch, Challenge). |
| Message to repeat | Only overload an operator when its meaning is obvious. `cm1 + cm2` is obvious; `model_a < model_b` is not. |

### 14:45 to 15:45 · 04 Encapsulation and abstraction (60 min)

| | |
| --- | --- |
| Goal | Solve the morning's mystery. Learned state, internal vs public, abstract base classes. |
| Methods | Socratic dialogue to resolve the mystery, live coding, pair programming |
| Flow | 10 min: back to the parking lot. Ask questions until the group finds the cause (the encoder learns from whatever batch it sees). 15 min: build `OneHotEncoder` with `fit`/`transform` and show the bug is gone. 10 min: `_internal` names (a convention, not a lock), returning copies, a validating property. 5 min: `Transformer` ABC, an incomplete subclass fails at creation. 20 min: exercise `MedianImputer` (Core), unseen categories (Stretch), `TransformerChain` (Challenge). |
| Watch for | The claim "underscore makes it private". It does not; it tells colleagues what they may rely on. |

### 16:00 to 16:50 · 05 Polymorphism, duck typing and protocols (50 min)

| | |
| --- | --- |
| Goal | One function for many kinds of objects; describe interfaces with `Protocol`. |
| Methods | Live coding, pair programming, decision table discussion |
| Flow | 15 min: the leaderboard function evaluating rule baselines and scikit-learn models together. 10 min: duck typing, and why `cross_val_score` still rejects our rule models (it clones, so it needs `get_params`; this is the hook for X2). 10 min: `Protocol` vs ABC, decision table. 15 min: exercise (add `GradientBoostingClassifier` without touching the function; Stretch and Challenge on probabilities and cost-optimal thresholds). |
| Energy | This is the low point of the afternoon. Keep the input short and let people type. |

### 16:50 to 17:20 · 06 Code safari: reading real code (30 min)

| | |
| --- | --- |
| Goal | Recognise the day's concepts in real library code. This directly trains "understand code you see". |
| Methods | Jigsaw (one station per person or pair), short report back |
| Flow | 2 min: assign one station per person or pair (online: one breakout room per station). 15 min: work through the station at the computer, answers in a markdown cell. 10 min: each station reports in one minute ("we found a mixin, here is what it does"). 3 min: the reading checklist at the end of the notebook. Solo alternative: everyone does stations 1 to 3 and debriefs together. |
| Differentiation | Give the most experienced participants the `BaseEstimator.get_params` challenge. |

### 17:20 to 17:30 · Exit ticket (10 min)

KWL third column ("what I learned", one note each on the board) and a muddiest point: "What is still unclear?" On site on a card, online in an anonymous form or a private chat message to you. Collect them. Read them in the evening and pick the two or three most frequent themes for tomorrow's recap.

---

## Day 2: Software engineering and architecture

### 09:30 to 09:45 · Recap (15 min)

Answer the most common muddiest points from the exit tickets, with code, briefly. Then three peer-instruction questions mixing day 1 topics (one each on instance state, inheritance, a special method). Vote, discuss, vote again.

### 09:45 to 11:00 · 07 Type hints, docstrings and dataclasses (75 min)

| | |
| --- | --- |
| Goal | Write code that explains itself; replace config dicts by validated dataclasses. |
| Methods | Demonstration, code kata, pair programming |
| Flow | 5 min hook: the config dict with a typo that silently does nothing. 15 min type hints essentials and a mypy run (show it in the terminal). 10 min Google-style docstrings, `help()`. 10 min Core exercise: annotate and document. 15 min dataclasses: generated methods, `field(default_factory=...)`, `__post_init__` validation, `frozen=True`, `from_json`. 15 min Core exercise: the experiment config dataclass. 5 min: Pydantic in one slide, "validate at the boundary". |
| Challenge track | The Pydantic exercise and the question "where should validation live?" |

### 11:15 to 12:15 · 08 Design and architecture (60 min)

| | |
| --- | --- |
| Goal | Single responsibility, composition, layers, dependency injection, reading and drawing UML. |
| Methods | Code review of a "god class", diagramming in Mermaid, gallery walk (in the room or on a shared board) |
| Flow | 10 min: show the god class, ask "how would you test this without the CSV file?" 15 min: concepts with the refactored version (composition, layers, dependency injection). 15 min: alone or in pairs, write the class diagram of the refactored warm-up in Mermaid in the notebook. 10 min: gallery walk: on site, laptops open and people walk around; online, everyone pastes their Mermaid code or a screenshot on the shared board. Each person leaves one comment ("I like", "I wonder") on two other diagrams. 10 min: Core coding exercise (inject the loader) or Stretch (SQLite loader). |
| Challenge track | The design review exercise with four design problems, ending in a refactored code skeleton. Experienced participants can do this instead of the diagram. |

### 12:15 to 13:00 · 09 Exceptions and logging (45 min)

| | |
| --- | --- |
| Goal | Fail loudly with useful errors; log like an application, not like a script. |
| Methods | Debugging exercise, live coding |
| Flow | 5 min: a function that returns `None` on bad data and the silent damage it causes downstream. 15 min: raising the right exception, the project hierarchy, `raise ... from`, catching at the boundary. 10 min: module loggers, levels, why libraries never call `basicConfig` (show `src/churn/__main__.py`). 15 min: exercise `validate_batch` (Core), wrapping and logging (Stretch), `ExceptionGroup` (Challenge). |

### 14:00 to 15:00 · 10 Testing with pytest (60 min)

| | |
| --- | --- |
| Goal | Write and run tests; know what to test in data science code. |
| Methods | Live coding in the terminal, code kata, test-first bug fix |
| Flow | 15 min: run `uv run pytest` on the repo, open `tests/test_features.py` and read two tests together (Arrange, Act, Assert). 15 min: asserts, `pytest.approx`, `pytest.raises`, fixtures, parametrize, demonstrated in the notebook. 25 min: participants write tests in `playground/` (Core: ConfusionMatrix tests; Stretch: parametrize and fixtures; Challenge: reproduce the warm-up bug as a failing test, then fix it). 5 min: what not to test. |
| Watch for | People calling fixtures directly. pytest injects them by argument name. |

### 15:00 to 15:25 · 11 From notebook to package (25 min)

| | |
| --- | --- |
| Goal | Understand the project layout well enough to start the capstone. |
| Methods | Guided walkthrough with checkpoints |
| Flow | Tour of the repository tree, `pyproject.toml` section by section, what `uv sync` did, `import churn` from anywhere, `python -m churn`, `uv run churn-train`. Checkpoint: everyone runs `uv run pytest tests_capstone` and sees red tests. That red is the starting point of the capstone. |

### 15:25 to 15:45 and 16:00 to 17:00 · 12 Capstone (80 min, coffee in between)

| | |
| --- | --- |
| Goal | Refactor the warm-up notebook into the `churn_capstone` package until the acceptance tests pass. |
| Methods | Pair programming (driver and navigator, swap every 15 minutes) or solo work, hackathon light. Online: one breakout room per pair, or solo with a shared "help" channel |
| Levels | Core tests: everyone aims for these. Stretch tests: configuration, error hierarchy, a useful model. Challenge tests: robustness and persistence, then the extension menu in the notebook. |
| Trainer | Walk around (online: visit breakout rooms in turn). When someone is stuck, ask what the failing test expects before looking at their code. Keep a visible tally of passing tests if the group likes a bit of competition; skip it if it creates pressure. At 16:50 announce ten minutes left and ask everyone to prepare their show and tell. |

### 17:00 to 17:30 · Closing (30 min)

| | |
| --- | --- |
| Show and tell (15 min) | Five or six people or pairs, 2 minutes each with screen sharing: one design decision they are proud of, one they are unsure about. The trainer links each to `src/churn`. |
| Retrospective (10 min) | Start, stop, continue: one note per column per person on the shared board, about the workshop and about their own way of coding. |
| Transfer (5 min) | Each person writes down one notebook from their own work they will apply the capstone recipe to in the next two weeks, and the first step they will take (transfer task). Finish the KWL board. |

---

## Differentiation toolbox

- **Three exercise levels** in every notebook. Tell the group explicitly that nobody is expected to finish Challenge exercises, and that skipping Stretch is fine.
- **Challenge track notebooks** X2 and X3 for participants who finish everything early. X2 (scikit-learn compatible estimators) connects directly to notebook 05 and 06.
- **Reciprocal teaching:** an experienced participant who is done may explain their solution to someone who is stuck (online: in a breakout room). Offer, do not impose: they also came to learn.
- **Parking lot** for deep questions (metaclasses, descriptors, async). Answer them during breaks or point to "Going further" sections.
- **Discuss questions** scale too: beginners answer them about their Core solution, experienced participants about the Challenge design.
- **If you pair: mixed pairs on day 1, similar-level pairs in the capstone.**

## If you run late (cutting plan)

Cut in this order; each item is covered in writing in the notebook, so nothing is lost for later self-study:

1. 03: context managers and `__radd__` (keep `__repr__`, `__iter__`, `__add__`, `__call__`).
2. 05: mixins; shorten the ABC vs Protocol discussion to the decision table.
3. 06: run three stations instead of five.
4. 07: Pydantic.
5. 08: replace the gallery walk by two diagrams shared on screen and discussed in plenary.
6. 09: `try/except/else/finally` details and warnings.
7. 11: shrink to the checkpoint (`uv run pytest tests_capstone`).

Never cut the capstone below 60 minutes or the exit ticket and the recap: they carry the learning of the whole workshop.

## If the group is fast

- Give more time to Challenge exercises and ask people to present them.
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
