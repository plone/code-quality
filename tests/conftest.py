"""Pytest configuration."""
from pathlib import Path

import os
import pytest
import sys


@pytest.fixture(autouse=True)
def setup_python():
    current_python = sys.executable
    os.environ["PYTEST_BIN_DIR"] = str(Path(current_python).parent)


@pytest.fixture(scope="session")
def cwd() -> Path:
    """Working directory."""
    return Path(os.curdir).resolve()


@pytest.fixture(scope="session")
def fixtures_folder() -> Path:
    """Fixtures folder."""
    return Path("tests/fixtures").resolve()


@pytest.fixture
def configs_folder(fixtures_folder, cwd) -> Path:
    """Fixtures folder."""
    path = (fixtures_folder / "configs").resolve()
    os.chdir(path)
    yield path
    os.chdir(cwd)
