<p align="center">
  <a href="https://hub.docker.com/r/plone/code-quality">
    <img alt="Plone Code Quality tool" width="200px" src="https://raw.githubusercontent.com/plone/code-quality/main/docs/icon.png">
  </a>
</p>

<h1 align="center">
  Plone Code Quality tool
</h1>

<div align="center">

[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/plone/code-quality)](https://hub.docker.com/r/plone/code-quality)
![GitHub Repo stars](https://img.shields.io/github/stars/plone/code-quality?style=flat-square)
[![license badge](https://img.shields.io/github/license/plone/code-quality)](./LICENSE)

</div>

## Configuration

This tool looks for configuration in a `pyproject.toml`file in the root of the codebase being analysed.

The default configuration values are:

```toml
[tool.plone-code-analysis]
checkers = ["black", "flake8", "isort", "pyroma", "zpretty"]
formatters = ["black", "isort", "zpretty"]
paths = "."
paths_pyroma = "."
paths_black = "."
paths_flake8 = "."
paths_isort = "."
paths_pyroma = "."
paths_zpretty = "."
```

If you want to change only the `paths`, you should add to your `pyproject.toml` the following settings:

```toml
[tool.plone-code-analysis]
paths = "src/ setup.py"
```
Also, it is possible to change the paths used for individual tools:

```toml
[tool.plone-code-analysis]
paths_black = "src/ tests/ setup.py"
paths_flake8 = "src/ setup.py"
```

Or explicitly set `checkers` or `formatters` to be used:


```toml
[tool.plone-code-analysis]
checkers = ["black", "flake8", "isort", "pyroma", ]
formatters = ["black", "isort",]
```

### Tools configuration

To configure black, flake8 (via flakeheaven) and isort, also use the `pyproject.toml` file in the root of the directory you are mounting.

An example configuration, used by this image, follows:

```toml
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'

[tool.isort]
profile = "black"
force_alphabetical_sort = true
force_single_line = true
lines_after_imports = 2
line_length = 120

[tool.flakeheaven]
format="grouped"
max_line_length=88
show_source=true
max-complexity=25

[tool.flakeheaven.plugins]
pycodestyle = ["+*"]
pyflakes = ["+*"]
"flake8-*" = ["+*"]

[tool.plone-code-analysis]
paths = "docker-entrypoint.py src/setup.py src/plone_code_analysis tests/fixtures/packages/ok tests/package tests/conftest.py"
paths_pyroma = "src/ tests/fixtures/packages/ok"
```

## Usage

First, go to the repository you want to check or format.

### Checks / Linter

#### Run all Checks

Using the configuration available in `pyproject.toml`, run:

```bash
docker run --rm -v "${PWD}":/github/workspace plone/code-quality:latest check
```

#### Check with [black](https://black.readthedocs.io/en/stable/)

Check with `pyproject.toml` settings:

```bash
docker run --rm -v "${PWD}":/github/workspace plone/code-quality:latest check black
```

Explicitly check **src** directory and **setup.py** file.

```bash
docker run --rm -v "${PWD}":/github/workspace plone/code-quality:latest check black src setup.py
```

#### Check with [flake8](https://flake8.pycqa.org/en/stable/)

Flake8 checks, using [flakeheaven](https://pypi.org/project/flakeheaven/) configuration format.

Current plugins in use:

* [flake8-blind-except](https://pypi.org/project/flake8-blind-except/)
* [flake8-debugger](https://pypi.org/project/flake8-debugger/)
* [flake8-print](https://pypi.org/project/flake8-print/)

Check with `pyproject.toml` settings:

```bash
docker run --rm -v "${PWD}":/github/workspace plone/code-quality:latest check flake8
```

Explicitly check **src** directory and **setup.py** file.

```bash
docker run --rm -v "${PWD}":/github/workspace plone/code-quality:latest check flake8 src setup.py
```

#### Check with [isort](https://pycqa.github.io/isort/)

Check with `pyproject.toml` settings:

```bash
docker run --rm -v "${PWD}":/github/workspace plone/code-quality:latest check isort
```

Explicitly check **src** directory and **setup.py** file.

```bash
docker run --rm -v "${PWD}":/github/workspace plone/code-quality:latest check isort src setup.py
```


#### Check with [pyroma](https://pycqa.github.io/pyroma/)

Check with `pyproject.toml` settings:

```bash
docker run --rm -v "${PWD}":/github/workspace plone/code-quality:latest check pyroma
```

Explicitly check **src/mypackage** directory .

```bash
docker run --rm -v "${PWD}":/github/workspace plone/code-quality:latest check pyroma src/mypackage
```

#### Check with [zpretty](https://pypi.org/project/zpretty/)

Check with `pyproject.toml` settings:

```bash
docker run --rm -v "${PWD}":/github/workspace plone/code-quality:latest check zpretty
```

Explicitly check **src** directory .

```bash
docker run --rm -v "${PWD}":/github/workspace plone/code-quality:latest check zpretty src

```

### Formatter

To avoid rewriting the owner and group information of the formatted files, we need to pass the correct `--user` option to the `docker run` command.

In all examples bellow we use the `"$(id -u $(whoami)):$(getent group $(whoami)|cut -d: -f3)"` snippet to set the `--user` option to the current user running the formatter.

#### Run all formatters

Using the configuration available in `pyproject.toml`, run:

```bash
docker run --user="$(id -u $(whoami)):$(getent group $(whoami)|cut -d: -f3)" --rm -v "${PWD}":/github/workspace plone/code-quality:latest format
```

#### Format with [black](https://black.readthedocs.io/en/stable/)

Format with `pyproject.toml` settings:

```bash
docker run --user="$(id -u $(whoami)):$(getent group $(whoami)|cut -d: -f3)" --rm -v "${PWD}":/github/workspace plone/code-quality:latest format black
```

Explicitly format **src** directory and **setup.py** file.

```bash
docker run --user="$(id -u $(whoami)):$(getent group $(whoami)|cut -d: -f3)" --rm -v "${PWD}":/github/workspace plone/code-quality:latest format src setup.py
```

#### Format with [isort](https://pycqa.github.io/isort/)

Format with `pyproject.toml` settings:

```bash
docker run --user="$(id -u $(whoami)):$(getent group $(whoami)|cut -d: -f3)" --rm -v "${PWD}":/github/workspace plone/code-quality:latest format isort
```

Explicitly format **src** directory and **setup.py** file.

```bash
docker run --user="$(id -u $(whoami)):$(getent group $(whoami)|cut -d: -f3)" --rm -v "${PWD}":/github/workspace plone/code-quality:latest format src setup.py
```

#### Format with [zpretty](https://pypi.org/project/zpretty/)

Format with `pyproject.toml` settings:

```bash
docker run --user="$(id -u $(whoami)):$(getent group $(whoami)|cut -d: -f3)" --rm -v "${PWD}":/github/workspace plone/code-quality:latest format zpretty
```

Explicitly format the **src** directory .

```bash
docker run --user="$(id -u $(whoami)):$(getent group $(whoami)|cut -d: -f3)" --rm -v "${PWD}":/github/workspace plone/code-quality:latest format src

```

## Contribute

- [Issue Tracker](https://github.com/plone/code-quality/issues)
- [Source Code](https://github.com/plone/code-quality/)
- [Documentation](https://github.com/plone/code-quality/)

Please **DO NOT** commit to version branches directly. Even for the smallest and most trivial fix.

**ALWAYS** open a pull request and ask somebody else to merge your code. **NEVER** merge it yourself.


### Running linters on this codebase

Use this tool to lint its own codebase:

```shell
make lint-all
```

You can also increase the verbosity with:

```shell
LOG_LEVEL=DEBUG make lint-all
```
### Running formatters on this codebase

Use this tool to format its own codebase:

```shell
make format
```

You can also increase the verbosity with:

```shell
LOG_LEVEL=DEBUG make format
```


### Running local tests

Tests are implemented with `pytest` and can be run with:

```shell
make test
```

## Credits

Based on a solution originally developed by [kitconcept GmbH](https://kitconcept.com).

[![Plone Foundation](https://raw.githubusercontent.com/plone/.github/main/plone-foundation.png)](https://plone.org/)

## License

The project is licensed under the GPLv2.
