"""Nox sessions for automated tasks"""

import os

import nox
from dotenv import load_dotenv

nox.options.sessions = ["lint", "type_check", "format"]


# Running ---------------------------------------------------------------------


@nox.session
def run_file(session):
    """
    Build current package and run selected file inside tests/

    To use it run: `nox -s run_file -- file_name`
    """
    # Install package in editable mode
    session.install("-e", ".")

    # Get the file name, if provided, else raise error
    file_name = session.posargs[0] if session.posargs else None
    if not file_name:
        session.error("Please provide a file name: `nox -s run_file -- my_script.py`")

    # Run the file
    session.run("python3", f"tests/{file_name}")


# Linting and Formatting ------------------------------------------------------


@nox.session
def lint(session):
    """Run ruff to check code quality."""
    session.install("ruff")
    session.run("ruff", "check", "src", "--fix")


@nox.session
def type_check(session):
    """Run mypy to check for type errors."""
    session.install("mypy")
    session.run("mypy", "--install-types", "--non-interactive")
    session.run("mypy", "src")


@nox.session
def format(session):
    """Format code using ruff."""
    session.install("ruff")
    session.log(f"Working dir: {os.getcwd()}")
    session.run("ruff", "format", "src")

@nox.session
def format_test(session):
    """Format code using ruff."""
    session.install("ruff")
    session.log(f"Working dir: {os.getcwd()}")
    session.run("ruff", "format", "test.py")


@nox.session
def check_formatting(session):
    """Check formatting using black and isort (non-destructive)."""
    session.install("black", "isort")
    session.run("isort", "--check", "--diff", "src", "tests", "noxfile.py")
    session.run(
        "black",
        "--check",
        "--diff",
        "--line-length=80",
        "src",
        "tests",
        "noxfile.py",
    )


# Building --------------------------------------------------------------------


@nox.session
def build(session):
    """Build the Project"""
    session.install("build")

    # Remove current dist/ folder
    session.run("rm", "-rf", "dist/", external=True)

    # Build
    session.run("python3", "-m", "build")


@nox.session
def publish(session):
    """Publish current build"""
    session.install("twine", "python-dotenv")

    # Getting Test Pypi API token
    load_dotenv()
    TESTPYPI_TOKEN = os.getenv("TESTPYPI_TOKEN")

    # Publishing
    session.run(
        "twine",
        "upload",
        "--repository",
        "testpypi",
        "--password",
        f"{TESTPYPI_TOKEN}",
        "dist/*",
    )


@nox.session
def build_and_publish(session):
    """Build The Project then publish"""
    session.install("build", "twine", "python-dotenv")

    # Remove current build
    session.run("rm", "-rf", "dist/", external=True)

    # Building
    session.run("python3", "-m", "build")

    # Getting Test Pypi API token
    load_dotenv()
    TESTPYPI_TOKEN = os.getenv("TESTPYPI_TOKEN")

    # Publishing
    session.run(
        "twine",
        "upload",
        "--repository",
        "testpypi",
        "--password",
        f"{TESTPYPI_TOKEN}",
        "dist/*",
    )


# Testing ---------------------------------------------------------------------


@nox.session
def run_tests(session):
    session.install("pytest")

    # Install Package in editable mode
    session.install("-e", ".")

    # Run pytest
    session.run("pytest")
