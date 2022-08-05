from pathlib import Path
from plone_code_analysis.cmd import run_command
from plone_code_analysis.cmd import run_zpretty
from plone_code_analysis.logger import logger
from plone_code_analysis.settings import formatters_from_settings


FORMATTERS = {
    "isort": [
        run_command,
        [
            "isort",
            [],
        ],
    ],
    "black": [
        run_command,
        [
            "black",
            [],
        ],
    ],
    "zpretty": [
        run_zpretty,
        [
            "zpretty",
            [],
        ],
    ],
}


def run_formatter(tool: str, paths: list[Path]) -> int:
    """Run one formatter."""
    formatter = FORMATTERS.get(tool)
    if not formatter:
        logger.error(f"Please provide a valid formatter. Received {tool}")
        return 1
    elif not paths:
        logger.error("Please provide a valid path.")
        return 1
    func, args = formatter
    return func(*args, paths=paths)


def run_formatters(settings: dict, tool: str = "", paths: list[Path] = None) -> int:
    """Run one or more formatters."""
    status = 0
    all_formatters = formatters_from_settings(settings)
    if tool and paths:
        formatters = {tool: paths}
    elif tool:
        formatters = {tool: all_formatters[tool]}
    else:
        formatters = all_formatters
    for formatter, paths in formatters.items():
        logger.info(f"Running formatter: {formatter}", header=2)
        status = run_formatter(formatter, paths) or status
    return status
