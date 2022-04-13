# kitconcept Code Quality tool

## Usage

First, go to the repository you want to check.

Check **src** directory and **setup.py** file with **black**
```bash
docker run --rm -v "${PWD}":/github/workspace kitconcept/code-quality:latest check black src setup.py
```

Check **src** directory and **setup.py** file with **flake8**
```bash
docker run --rm -v "${PWD}":/github/workspace kitconcept/code-quality:latest check flake8 src setup.py
```

Check **src** directory and **setup.py** file with **isort**
```bash
docker run --rm -v "${PWD}":/github/workspace kitconcept/code-quality:latest check isort src setup.py
```

Check **src** directory with **zpretty**
```bash
docker run --rm -v "${PWD}":/github/workspace kitconcept/code-quality:latest check zpretty src
```

## Configuration

To configure black, flake8 (via flakeheaven) and isort, make sure you have a pyproject.toml in the root of the directory you are mounting.
