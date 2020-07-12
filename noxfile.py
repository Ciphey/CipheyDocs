import nox
from typing import Any
from nox.sessions import Session
import tempfile

locations = "docs/"
package = "ciphey"


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file.
    This function is a wrapper for nox.sessions.Session.install. It
    invokes pip to install packages inside of the session's virtualenv.
    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the
    packages as Poetry development dependencies.
    Arguments:
        session: The Session object.
        args: Command-line arguments for pip.
        kwargs: Additional keyword arguments for Session.install.
    """
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


# @nox.session(python=["3.8"])
# def xdoctest(session: Session) -> None:
#     """Run examples with xdoctest."""
#     args = session.posargs or ["all"]
#     session.run("poetry", "install", "--no-dev", external=True)
#     install_with_constraints(session, "xdoctest")
#     session.run("python", "-m", "xdoctest", package, *args)


# noxfile.py
@nox.session(python="3.8")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")
