from pathlib import Path

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
    result = subprocess.run(all_args)
    return result.returncode


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
