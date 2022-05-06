# Plone Code Quality tool

## Usage

First, go to the repository you want to check.

Check **src** directory and **setup.py** file with **black**
```bash
docker run --rm -v "${PWD}":/github/workspace plone/code-quality:latest check black src setup.py
```

Check **src** directory and **setup.py** file with **flake8**
```bash
docker run --rm -v "${PWD}":/github/workspace plone/code-quality:latest check flake8 src setup.py
```

Check **src** directory and **setup.py** file with **isort**
```bash
docker run --rm -v "${PWD}":/github/workspace plone/code-quality:latest check isort src setup.py
```

Check **src** directory with **zpretty**
```bash
docker run --rm -v "${PWD}":/github/workspace plone/code-quality:latest check zpretty src
```

## Configuration

To configure black, flake8 (via flakeheaven) and isort, make sure you have a pyproject.toml in the root of the directory you are mounting.

An example configuration, used by this image, follows:

```toml
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
exclude = '''
(
  /(
      \.eggs         # exclude a few common directories in the
    | \.git          # root of the project
    | \.hg
    | \.mypy_cache
    | \.tox
    | \.venv
    | _build
    | buck-out
    | build
    | dist
  )/
)
'''

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
```

## Contribute

- [Issue Tracker](https://github.com/plone/code-quality/issues)
- [Source Code](https://github.com/plone/code-quality/)
- [Documentation](https://github.com/plone/code-quality/)

Please **DO NOT** commit to version branches directly. Even for the smallest and most trivial fix.

**ALWAYS** open a pull request and ask somebody else to merge your code. **NEVER** merge it yourself.

## Credits

Based on a solution originally developed by [kitconcept GmbH](https://kitconcept.com).

![Plone Foundation](https://raw.githubusercontent.com/plone/.github/main/plone-foundation.png)

## License

The project is licensed under the GPLv2.
