import sys

import nox


@nox.session(venv_backend="none")
def lint(session: nox.Session) -> None:
    session.run(sys.executable, "-m", "mypy", ".")
    session.run(sys.executable, "-m", "ruff", "check", ".")


@nox.session(venv_backend="none")
def test(session: nox.Session) -> None:
    session.run(sys.executable, "-m", "pytest")
