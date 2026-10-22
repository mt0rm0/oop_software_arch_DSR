# Further reading

Where to go after the workshop, ordered as a learning path. Every notebook also ends with a **Sources and further reading** section listing the references for its own topic; this page collects the most useful ones in one place.

Each entry says what kind of resource it is and roughly what level it assumes. Everything marked *free* can be read online at no cost.

---

## Step 1: Solid Python foundations

Start here if some parts of day 1 felt fast.

- [The Python Tutorial](https://docs.python.org/3/tutorial/) (official, free, beginner). Chapter 9 covers classes; chapters 6 and 8 cover modules and exceptions.
- [Wes McKinney, *Python for Data Analysis*, 3rd edition](https://wesmckinney.com/book/) (book, free, beginner). pandas and NumPy from the author of pandas.
- [Real Python: Python Classes, the Power of Object-Oriented Programming](https://realpython.com/python-classes/) (article, beginner). A longer walk through notebook 01.
- [Real Python: Object-Oriented Programming learning path](https://realpython.com/learning-paths/object-oriented-programming-oop-python/) (course collection, beginner to intermediate; some content needs a subscription).
- [Raymond Hettinger, *Python's Class Development Toolkit*](https://www.youtube.com/watch?v=HTLu2DFOdTg) (talk, 45 min, beginner to intermediate). One class built feature by feature, with the reason for each one.

## Step 2: Understand Python's object model

When you want to know *why* Python classes work the way they do.

- Luciano Ramalho, *Fluent Python*, 2nd edition, O'Reilly 2022 ([book site](https://www.fluentpython.com/)) (book, intermediate to advanced). The best book on the Python data model: special methods (chapter 1), interfaces, protocols and ABCs (chapter 13), operator overloading (chapter 16).
- Brett Slatkin, *Effective Python* ([book site](https://effectivepython.com/)) (book, intermediate). Short, independent items of good practice.
- [Python Language Reference: Data model](https://docs.python.org/3/reference/datamodel.html) (official, advanced). The complete specification of every special method.
- [Raymond Hettinger, *Python's super() considered super!*](https://rhettinger.wordpress.com/2011/05/26/super-considered-super/) (blog post, advanced). Cooperative multiple inheritance explained by a core developer.
- [Real Python: Python Protocols](https://realpython.com/python-protocol/) and [Real Python: Duck Typing in Python](https://realpython.com/duck-typing-python/) (articles, intermediate).

## Step 3: Design and architecture

When your projects grow beyond one module.

- [Harry Percival and Bob Gregory, *Architecture Patterns with Python*](https://www.cosmicpython.com/) (book, free online, intermediate to advanced). Layers, dependency injection, repositories, testing. The natural continuation of notebook 08 and the capstone.
- [Brandon Rhodes, *Python Design Patterns*](https://python-patterns.guide/) (website, free, intermediate). Which classic patterns still matter in Python, and which the language makes unnecessary.
- [Refactoring Guru](https://refactoring.guru/) (website, free, beginner to intermediate). Illustrated catalogue of code smells, refactorings and design patterns.
- [Martin Fowler, *Inversion of Control Containers and the Dependency Injection pattern*](https://martinfowler.com/articles/injection.html) and [*Presentation Domain Data Layering*](https://martinfowler.com/bliki/PresentationDomainDataLayering.html) (articles, free, intermediate).
- [Martin Fowler, *Refactoring*, 2nd edition](https://martinfowler.com/books/refactoring.html) (book, intermediate). How to improve code in small, safe steps.
- [Peter Norvig, *Design Patterns in Dynamic Languages*](https://norvig.com/design-patterns/) (slides, free, advanced).
- David Thomas and Andrew Hunt, *The Pragmatic Programmer*, 20th anniversary edition ([publisher page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)) (book, all levels). Habits of effective programmers, language independent.

## Step 4: Code that plugs into the data science ecosystem

- [Buitinck et al. (2013), *API design for machine learning software: experiences from the scikit-learn project*](https://arxiv.org/abs/1309.0238) (paper, free, intermediate). Why scikit-learn's estimators, `fit`/`predict`/`transform` and pipelines look the way they do.
- [scikit-learn: Developing scikit-learn estimators](https://scikit-learn.org/stable/developers/develop.html) (official guide, advanced). The rules notebook X2 follows.
- [scikit-learn: Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html) (official guide, intermediate). Data leakage and inconsistent preprocessing, the bug from notebook 00.
- [scikit-learn glossary](https://scikit-learn.org/stable/glossary.html) (official reference). What estimator, fitted, clone and parameter mean precisely.

## Step 5: Testing, errors, logging

- [pytest documentation](https://docs.pytest.org/en/stable/getting-started.html) (official, free, beginner to advanced).
- [Real Python: pytest Tutorial, Effective Python Testing](https://realpython.com/pytest-python-testing/) (article, beginner to intermediate).
- [Brian Okken, *Python Testing with pytest*, 2nd edition](https://pragprog.com/titles/bopytest2/python-testing-with-pytest-second-edition/) (book, intermediate).
- [Jeremy Jordan, *Effective testing for machine learning systems*](https://www.jeremyjordan.me/testing-ml/) and [Eugene Yan, *How to Test Machine Learning Code and Systems*](https://eugeneyan.com/writing/testing-ml/) (blog posts, free, intermediate). What is worth testing in ML code.
- [Breck et al. (2017), *The ML Test Score*](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) (paper, free, intermediate). A checklist for production readiness.
- [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html) and [Real Python: Logging in Python](https://realpython.com/python-logging/) (official guide and article, beginner to intermediate).

## Step 6: From project to production

- [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/) and [uv documentation](https://docs.astral.sh/uv/guides/projects/) (official, free).
- [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/) (website, free, beginner). A project template with the reasoning behind each folder.
- [Made With ML](https://madewithml.com/) (course, free, intermediate to advanced). From notebook to production ML system, including testing and CI.
- [Scott Chacon and Ben Straub, *Pro Git*](https://git-scm.com/book/en/v2) (book, free) and [Learn Git Branching](https://learngitbranching.js.org/) (interactive, free, beginner).
- [Google: Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml) (guide, free, intermediate).

## Background reading for researchers

Many participants come from academia. These two papers translate the ideas of this workshop into the language of research software:

- [Wilson et al. (2017), *Good enough practices in scientific computing*](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510), PLOS Computational Biology (paper, free, beginner).
- [Wilson et al. (2014), *Best Practices for Scientific Computing*](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745), PLOS Biology (paper, free, beginner).
- [Sculley et al. (2015), *Hidden Technical Debt in Machine Learning Systems*](https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html), NeurIPS (paper, free, intermediate).
- [Joel Grus, *I don't like notebooks*](https://www.youtube.com/watch?v=7jiPeIFXb6U) (talk, JupyterCon 2018).
