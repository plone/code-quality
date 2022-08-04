from copy import deepcopy
from pathlib import Path
from plone_code_analysis.logger import logger
from typing import Any

import tomli


SECTION = "tool.plone-code-analysis"


CHECKERS = ["black", "flake8", "isort", "pyroma", "zpretty"]
FORMATTERS = ["black", "isort", "zpretty"]


DEFAULT_SETTINGS = {
    "checkers": CHECKERS,
    "formatters": FORMATTERS,
    "paths": ".",
    "paths_pyroma": ".",
}


def read_settings_from_file(path: Path) -> dict[str, Any]:
    """Read settings from toml file.

    :param path: Path to the toml file with settings.
    :returns: Dictionary with settings..
    """
    settings = deepcopy(DEFAULT_SETTINGS)
    if not path.exists():
        logger.info("File not found: pyproject.toml")
        return {}
    config = tomli.loads(path.read_text())
    for key in SECTION.split("."):
        config = config.get(key, {})
    settings.update(config)
    # Parse paths into a list of paths
    path_keys = [key for key in settings.keys() if key.startswith("paths")]
    for key in path_keys:
        value = settings.get(key, "")
        settings[key] = value if isinstance(value, list) else parse_paths(value)
    return settings


def parse_paths(value: str) -> list[Path]:
    """Parse path information.

    :param value: String with path information.
    :returns: List of valid paths.
    """
    separator = "\n" if "\n" in value else " "
    possible_paths = [Path(path) for path in value.split(separator)]
    valid_paths = {path.resolve() for path in possible_paths if path.exists()}
    return list(valid_paths)


def checks_from_settings(settings: dict) -> dict:
    """Extract check information from settings.

    :param settings: Dictionary with settings information.
    :returns: Dictionary with checks and paths.
    """
    all_checks = settings.get("checkers", CHECKERS)
    default_path = settings.get("paths", [])
    checks = {
        check: settings.get(f"paths_{check}", default_path) for check in all_checks
    }
    return checks


def formatters_from_settings(settings: dict) -> dict:
    """Extract formatter information from settings.

    :param settings: Dictionary with settings information.
    :returns: Dictionary with formatters and paths.
    """
    all_formatters = settings.get("formatters", FORMATTERS)
    default_path = settings.get("paths", [])
    formatters = {
        formatter: settings.get(f"paths_{formatter}", default_path)
        for formatter in all_formatters
    }
    return formatters
