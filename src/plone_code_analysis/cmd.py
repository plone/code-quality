from pathlib import Path
from plone_code_analysis.logger import logger

import os
import subprocess


def _parse_cmd(cmd: str) -> str:
    if prefix := os.environ.get("PYTEST_BIN_DIR", ""):
        cmd = f"{prefix}/{cmd}"
    return cmd


def run_command(cmd: str, args: list[str], paths: list[Path]) -> int:
    """Run command using subprocess.

    :param cmd: Command to run.
    :param args: Arguments to pass to the command.
    :param paths: List of paths to use.
    :returns: Status code.
    """
    cmd = [
        _parse_cmd(cmd),
    ]
    all_args = cmd + args + paths
    logger.debug(f"Running command {all_args}")
    proc = subprocess.run(all_args, capture_output=True)
    code = proc.returncode
    if code:
        # Each tool behaves in a distinct way, so we
        # concatenate the stdout and stderr
        stdout = proc.stdout.decode()
        stderr = proc.stderr.decode()
        msg = f"{stdout}\n{stderr}".strip()
        logger.error(msg, fancy=False)
    else:
        logger.success("All good!")
    return code


def run_zpretty(cmd: str, args: list[str], paths: list[Path]) -> bool:
    """Run zpretty.

    :param paths: List of paths to format.
    :returns: Status code.
    """
    raw_paths = [path for path in paths if path.is_dir()]
    checks = {
        "xml": ["-x", "-i"] + args,
        "zcml": ["-z", "-i"] + args,
    }
    status = 0
    for ext, args in checks.items():
        for path in raw_paths:
            if paths := list(path.glob(f"**/*.{ext}")):
                result = run_command(cmd, args, paths)
                status = status or result
    return status
