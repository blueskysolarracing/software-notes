# Blue Sky Solar Racing Python Coding Standards

1. All Python code must conform to [PEP 8](https://peps.python.org/pep-0008/) and pass style checks with [flake8](https://flake8.pycqa.org/en/latest/) prior to deployment.
2. All Python code must be completely typed as per [PEP 484](https://peps.python.org/pep-0484/) and pass strict static type checks with [mypy](https://mypy-lang.org/) prior to deployment.
3. All public classes, files, methods, and attributes must be documented as per [PEP 257](https://peps.python.org/pep-0257/) with [Sphinx](https://www.sphinx-doc.org/en/master/index.html) documentation format.
4. Documentations must be deployed using [Sphinx](https://www.sphinx-doc.org/en/master/index.html) via [ReadTheDocs](https://readthedocs.org/dashboard/).
5. Unit tests and doctests must cover a substantial portion of the code.
6. Logs should be used instead of printing to stdout whenever possible.
7. Libraries must never print anything to stdout unless explicitly stated in the documentation.
8. For software versioning, [PEP 440](https://peps.python.org/pep-0440/) must be followed.
    - Prototype versions (`0.0.A`): anything goes
    - Unstable versions For `0.A.B`: `A` is incremented if the change is breaking, `B` is incremented otherwise.
    - Stable versions `A.B.C`: `A` if incremented if the change is breaking, `B` is incremented if a new feature is introduced. `C` increments must be purely for maintenance (bug-fixing, documentation).
10. Use comments sparingly! (Don't spam them)
11. Most functions should be ~15 lines long!
