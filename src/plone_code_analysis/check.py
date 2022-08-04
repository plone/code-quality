from pathlib import Path
from plone_code_analysis.cmd import run_command
from plone_code_analysis.cmd import run_zpretty
from plone_code_analysis.logger import logger
from plone_code_analysis.settings import checks_from_settings


CHECKS = {
    "black": [
        run_command,
        [
            "black",
            ["--check", "--diff"],
        ],
    ],
    "flake8": [
        run_command,
        [
            "flakeheaven",
            ["lint"],
        ],
    ],
    "isort": [
        run_command,
        [
            "isort",
            ["--check-only"],
        ],
    ],
    "pyroma": [
        run_command,
        [
            "pyroma",
            ["-n", "10", "-d"],
        ],
    ],
    "zpretty": [
        run_zpretty,
        [
            "zpretty",
            [
                "--check",
            ],
        ],
    ],
}


def run_check(tool: str, paths: list[Path]) -> int:
    """Run individual check on provided paths."""
    check = CHECKS.get(tool)
    if not check:
        logger.error(f"Please provide a valid check. Received {check}")
        return 1
    elif not paths:
        logger.error("Please provide a valid path.")
        return 1
    func, args = check
    return func(*args, paths=paths)


def run_checks(settings: dict, tool: str = "", paths: list[Path] = None) -> int:
    """Run one or more checks."""
    status = 0
    all_checks = checks_from_settings(settings)
    if tool and paths:
        checks = {tool: paths}
    elif tool:
        checks = {tool: all_checks[tool]}
    else:
        checks = all_checks
    for check, paths in checks.items():
        status = status or run_check(check, paths)
    return status
