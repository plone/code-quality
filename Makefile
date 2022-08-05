IMAGE_NAME=plone/code-quality
DOCKERFILE=Dockerfile
ifndef LOG_LEVEL
	LOG_LEVEL=INFO
endif
CURRENT_USER=$$(whoami)
USER_INFO=$$(id -u ${CURRENT_USER}):$$(getent group ${CURRENT_USER}|cut -d: -f3)
CODEBASE=docker-entrypoint.py src/setup.py src/plone_code_analysis tests/fixtures/packages/ok tests/package tests/conftest.py
LINT=docker run -e LOG_LEVEL="${LOG_LEVEL}" --rm -v "${PWD}":/github/workspace "${IMAGE_NAME}:latest" check
FORMAT=docker run --user="${USER_INFO}" -e LOG_LEVEL="${LOG_LEVEL}" --rm -v "${PWD}":/github/workspace "${IMAGE_NAME}:latest" format


# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

bin/pip:
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	python3 -m venv .
	bin/pip install -r requirements.txt

bin/pytest:
	bin/pip install -r tests/requirements.txt

.PHONY: clean
clean: ## remove virtual environment
	rm -fr bin include lib lib64

.PHONY: setup
setup: bin/pytest ## Create virtualenv and run pip install

.PHONY: test
test: bin/pytest ## Create virtualenv and run pip install
	@echo "$(GREEN)==> Run tests $(RESET)"
	bin/python -m pytest tests

.PHONY: build-image
build-image:  ## Build Docker Image
	@echo "Building $(IMAGE_NAME):latest"
	@docker build . -t $(IMAGE_NAME):latest -f ${DOCKERFILE}

.PHONY: lint
lint:  build-image ## Lint code with existing image
	@echo "Linting ${CODEBASE} $(IMAGE_NAME):latest"
	$(LINT) black "${CODEBASE}"
	$(LINT) flake8 "${CODEBASE}"
	$(LINT) isort "${CODEBASE}"

.PHONY: lint-all
lint-all:  build-image ## Lint code with existing image using configurations from pyproject.toml
	@echo "Linting ${CODEBASE} $(IMAGE_NAME):latest"
	$(LINT)

.PHONY: format
format:  build-image ## Format code with existing image
	@echo "Formatting ${CODEBASE} $(IMAGE_NAME):latest"
	$(FORMAT)
