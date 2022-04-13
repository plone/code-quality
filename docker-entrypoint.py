#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, args: list[str], paths: list[Path]) -> int:
    """Run command using subprocess.

    :param cmd: Command to run.
    :param args: Arguments to pass to the command.
    :param paths: List of paths to use.
    :returns: Status code.
    """
    cmd = [
        cmd,
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


FORMATTERS = {
    "black": [
        run_command,
        [
            "black",
            [],
        ],
    ],
    "isort": [
        run_command,
        [
            "isort",
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


def parse_paths(value: str) -> list[Path]:
    """Parse path information.

    :param value: String with path information.
    :returns: List of valid paths.
    """
    separator = "\n" if "\n" in value else " "
    paths = [path for path in value.split(separator)]
    return [Path(path) for path in paths if Path(path).exists()]


def main_check(tool: str, raw_paths: str) -> int:
    """Run checks."""
    check = CHECKS.get(tool)
    paths = parse_paths(raw_paths)
    if not check:
        print(f"Please provide a valid check. Received {check}")
        return 1
    elif not paths:
        print(f"Please provide a valid path. Parsed {raw_paths} to {paths}")
        return 1
    func, args = check
    return func(*args, paths=paths)


def main_format(raw_paths: str) -> int:
    """Run code formatting."""
    status = 0
    paths = parse_paths(raw_paths)
    if not (paths):
        print(f"Please provide a valid path. Parsed {raw_paths} to {paths}")
        return 1
    for value in FORMATTERS.values():
        func, raw_args = value
        cmd, args = raw_args
        status = func(cmd, args, paths) or status
    return status


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

    # Remove filename from arguments
    all_args = sys.argv[1:]
    # Get the action to run: check or format
    action = all_args[0]
    if action == "check":
        sys.exit(main_check(all_args[1], all_args[2]))
    elif action == "format":
        sys.exit(main_format(all_args[1]))
    else:
        print("Please provide a valid action")
        sys.exit(1)
