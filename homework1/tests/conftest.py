"""Shared pytest fixtures for Homework 1.
 
Every task file does its work at the top level (no functions to import),
so tests run each script with runpy and inspect what it printed (capsys)
and the variables it left behind (the globals dict runpy returns).
"""

import builtins
import runpy
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src"
HOMEWORK_ROOT = SRC.parent 

@pytest.fixture 
def run_script(monkeypatch):
    """Return a helper that runs src/<name>.py with fake keyboard input.
 
    inputs: strings handed back, in order, each time the script calls input().
    Returns the script's global variables so tests can check its values.
    """
    def _run(name, inputs=()):
        answers = iter(inputs)
        monkeypatch.setattr(builtins, "input", lambda prompt="": next(answers))
        return runpy.run_path(str(SRC / f"{name}.py"))

    return _run