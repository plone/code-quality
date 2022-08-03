IMAGE_NAME=plone/code-quality
DOCKERFILE=Dockerfile
CODEBASE=docker-entrypoint.py
LINT=docker run --rm -v "${PWD}":/github/workspace "${IMAGE_NAME}:latest" check
FORMAT=docker run --rm -v "${PWD}":/github/workspace "${IMAGE_NAME}:latest" format
CURRENT_USER=$$(whoami)

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

bin/pip:
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	python3 -m venv .
	bin/pip install -r requirements.txt

.PHONY: clean
clean: ## remove virtual environment
	rm -fr bin include lib lib64

.PHONY: setup
setup: bin/pip ## Create virtualenv and run pip install
	@echo "$(GREEN)==> Setup Dev Environment$(RESET)"
	bin/pip install -r tests/requirements.txt

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

.PHONY: format
format:  build-image ## Format code with existing image
	@echo "Formatting ${CODEBASE} $(IMAGE_NAME):latest"
	$(FORMAT) "${CODEBASE}"
	sudo chown -R ${CURRENT_USER}: *
