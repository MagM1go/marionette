import sys

import nox

LINT_PATHS: tuple[str, ...] = ("src", "tests", "noxfile.py")


@nox.session(venv_backend="none")
def lint(session: nox.Session) -> None:
    session.run(sys.executable, "-m", "mypy", *LINT_PATHS)
    session.run(sys.executable, "-m", "ruff", "check", *LINT_PATHS)


@nox.session(venv_backend="none")
def test(session: nox.Session) -> None:
    session.run(sys.executable, "-m", "pytest")
