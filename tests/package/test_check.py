"""Test plone_code_analysis.settings."""
from pathlib import Path
from plone_code_analysis import check
from plone_code_analysis import settings

import os
import pytest


PCK_OK = Path("tests/fixtures/packages/ok").resolve()
PCK_NOK = Path("tests/fixtures/packages/not_ok").resolve()


@pytest.fixture
def package_ok(cwd) -> Path:
    """package folder."""
    os.chdir(PCK_OK)
    yield PCK_OK
    os.chdir(cwd)


@pytest.fixture
def package_nok(cwd) -> Path:
    """package folder."""
    os.chdir(PCK_NOK)
    yield PCK_NOK
    os.chdir(cwd)


@pytest.mark.parametrize(
    "tool,paths,expected",
    [
        [
            "black",
            [
                PCK_OK / "setup.py",
            ],
            0,
        ],
        [
            "flake8",
            [
                PCK_OK / "setup.py",
            ],
            0,
        ],
        [
            "isort",
            [
                PCK_OK / "setup.py",
            ],
            0,
        ],
        [
            "pyroma",
            [
                PCK_OK,
            ],
            0,
        ],
        [
            "zpretty",
            [
                PCK_OK / "foo",
            ],
            0,
        ],
        [
            "black",
            [
                PCK_NOK / "setup.py",
            ],
            1,
        ],
        [
            "flake8",
            [
                PCK_NOK / "setup.py",
            ],
            1,
        ],
        [
            "isort",
            [
                PCK_NOK / "setup.py",
            ],
            1,
        ],
        [
            "pyroma",
            [
                PCK_NOK,
            ],
            2,
        ],
        [
            "zpretty",
            [
                PCK_NOK / "bar",
            ],
            1,
        ],
    ],
)
def test_run_check(tool, paths, expected):
    """Check check.run_check."""
    assert check.run_check(tool, paths) == expected


def test_run_checks_pass(package_ok):
    """Check check.run_checks."""
    config = settings.read_settings_from_file(package_ok / "pyproject.toml")
    assert check.run_checks(config) == 0


def test_run_checks_fail(package_nok):
    """Check check.run_checks."""
    config = settings.read_settings_from_file(package_nok / "pyproject.toml")
    assert check.run_checks(config) == 1
