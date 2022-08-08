"""Test plone_code_analysis.settings."""
from pathlib import Path
from plone_code_analysis import settings

import pytest


CONFIGS_PATH = Path("tests/fixtures/configs").resolve()


@pytest.mark.parametrize(
    "value,elements",
    [
        ["", 1],
        ["  ", 1],
        [".", 1],
        ["setup.py foo", 2],
        ["setup.py 404", 1],
        ["404", 0],
        ["setup.py foo setup.py foo", 2],
    ],
)
def test_parse_paths(configs_folder, value, elements):
    result = settings.parse_paths(value)
    assert len(result) == elements
    if elements:
        assert isinstance(result, list)
        assert isinstance(result[0], Path)


@pytest.mark.parametrize(
    "filename,key,expected",
    [
        [
            "check_path",
            "paths_isort",
            [
                CONFIGS_PATH / "setup.py",
            ],
        ],
        [
            "check_path",
            "paths_pyroma",
            [
                CONFIGS_PATH,
            ],
        ],
        [
            "check_path",
            "paths",
            [
                CONFIGS_PATH / "foo",
            ],
        ],
        ["check_path", "checkers", settings.CHECKERS],
        ["check_path", "formatters", settings.FORMATTERS],
        [
            "checkers",
            "checkers",
            [
                "black",
            ],
        ],
        [
            "checkers",
            "formatters",
            [
                "black",
            ],
        ],
        ["default", "paths_isort", None],
        [
            "default",
            "paths_pyroma",
            [
                CONFIGS_PATH,
            ],
        ],
        [
            "default",
            "paths",
            [
                CONFIGS_PATH,
            ],
        ],
        ["default", "checkers", settings.CHECKERS],
        ["default", "formatters", settings.FORMATTERS],
    ],
)
def test_default_settings(configs_folder, filename, key, expected):
    """Check with default values"""
    config = settings.read_settings_from_file(Path(f"{filename}.toml"))
    assert config.get(key) == expected


@pytest.mark.parametrize(
    "filename,check,paths",
    [
        [
            "check_path",
            "black",
            [
                CONFIGS_PATH / "foo",
            ],
        ],
        [
            "check_path",
            "isort",
            [
                CONFIGS_PATH / "setup.py",
            ],
        ],
        [
            "check_path",
            "pyroma",
            [
                CONFIGS_PATH,
            ],
        ],
        [
            "check_path",
            "zpretty",
            [
                CONFIGS_PATH / "foo",
            ],
        ],
        [
            "checkers",
            "black",
            [
                CONFIGS_PATH,
            ],
        ],
        [
            "default",
            "black",
            [
                CONFIGS_PATH,
            ],
        ],
        [
            "default",
            "isort",
            [
                CONFIGS_PATH,
            ],
        ],
        [
            "default",
            "pyroma",
            [
                CONFIGS_PATH,
            ],
        ],
        [
            "default",
            "zpretty",
            [
                CONFIGS_PATH,
            ],
        ],
    ],
)
def test_checks_from_settings(configs_folder, filename, check, paths):
    """Check with default values"""
    config = settings.read_settings_from_file(Path(f"{filename}.toml"))
    checks = settings.checks_from_settings(config)
    assert checks[check] == paths


@pytest.mark.parametrize(
    "filename,formatter,paths",
    [
        [
            "check_path",
            "black",
            [
                CONFIGS_PATH / "foo",
            ],
        ],
        [
            "check_path",
            "isort",
            [
                CONFIGS_PATH / "setup.py",
            ],
        ],
        [
            "check_path",
            "zpretty",
            [
                CONFIGS_PATH / "foo",
            ],
        ],
        [
            "checkers",
            "black",
            [
                CONFIGS_PATH,
            ],
        ],
        [
            "default",
            "black",
            [
                CONFIGS_PATH,
            ],
        ],
        [
            "default",
            "isort",
            [
                CONFIGS_PATH,
            ],
        ],
        [
            "default",
            "zpretty",
            [
                CONFIGS_PATH,
            ],
        ],
    ],
)
def test_formatters_from_settings(configs_folder, filename, formatter, paths):
    """Check with default values"""
    config = settings.read_settings_from_file(Path(f"{filename}.toml"))
    formatters = settings.formatters_from_settings(config)
    assert formatters[formatter] == paths
