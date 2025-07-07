import nox

@nox.session
def build(session):
  session.install("build")
  session.run("python3", "-m", "build")

import nox
import glob
import os

nox.options.sessions = ["build", "test_sdist"]

@nox.session
def build(session):
  """Build the sdist and wheel."""
  session.install("build")
  session.run("python", "-m", "build")

@nox.session
def test_sdist(session):
  """Install the .tar.gz sdist and run tests."""
  sdist_files = glob.glob("dist/*.tar.gz")
  if not sdist_files:
      session.error("No .tar.gz file found in dist/. Run `nox -s build` first.")

  sdist = sdist_files[0]

  session.log(f"Installing from: {sdist}")

  # Install the built sdist
  session.install(sdist)

def build_and_test(session):
  """Build and install the sdist"""
  pass

def editable_install(session):
  """Install in editable mode"""
  pass

def publish_package(session):
  """Publish package on pypi"""
  pass