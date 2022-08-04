#!/usr/bin/env python3
from pathlib import Path
from plone_code_analysis.check import run_checks
from plone_code_analysis.format import run_formatters
from plone_code_analysis.logger import logger
from plone_code_analysis.settings import FORMATTERS
from plone_code_analysis.settings import parse_paths
from plone_code_analysis.settings import read_settings_from_file

import os
import sys


ACTIONS = {
    "check": run_checks,
    "format": run_formatters,
}


def change_working_dir(sub_dir: str):
    """Change the working directory.

    :param sub_dir: Path to the subdiretory to use as working dir.
    """
    current_path = Path(".").resolve()
    new_dir = current_path / sub_dir
    if new_dir.exists() and new_dir.is_dir():
        os.chdir(new_dir)


if __name__ == "__main__":
    """Run code-quality."""
    # Change working directory, if needed
    base_dir = os.environ.get("BASE_DIR", "")
    if base_dir and not (base_dir.startswith(".") or base_dir.startswith("/")):
        change_working_dir(base_dir)

    settings = read_settings_from_file(Path("pyproject.toml"))

    # Remove filename from arguments
    all_args = sys.argv[1:]

    # Get the action to run: check or format
    action = all_args[0]
    if action not in ACTIONS:
        logger.error("Please provide a valid action")
        sys.exit(1)
    if len(all_args) == 1:
        # We run all checks/formatters
        tool = ""
        paths = ""
    elif len(all_args) == 2:
        if action == "format" and all_args[1] not in FORMATTERS:
            tool = "all"
            paths = all_args[1]
        else:
            tool = all_args[1]
            paths = ""
    elif len(all_args) >= 3:
        # Tool and many paths
        tool = all_args[1]
        paths = " ".join(all_args[2:])
    paths = parse_paths(paths)
    status = ACTIONS[action](settings, tool, paths)
    if status:
        sys.exit(1)
