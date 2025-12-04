.PHONY: install
install: ## Install the virtual environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using uv"
	@uv sync
	@uv pip install .[dev,docs]
	@echo "🔧 Installing pre-commit hooks"
	@uv run pre-commit install

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking lock file consistency with 'pyproject.toml'"
	@uv lock --locked
	@echo "🚀 Linting code: Running pre-commit"
	@uv run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@uv run mypy

.PHONY: tests
tests: ## Test the code
	@echo "🚀 Testing package from tests/integration/fixtures"
	@(cd tests/integration/fixtures && \
		uv run CellViability --config config.json --instances --npy --verbose)

.PHONY: experiments
experiments: install ## Run experiments
	@echo "🚀 Configuring environments for experiments"

	@echo "> Cellpose 3.1.1.2"
	@uv -q venv tests/experiments/.venv/cellpose3 --python 3.13
	@( \
		export VIRTUAL_ENV=tests/experiments/.venv/cellpose3/; \
		uv pip -q install cellpose==3.1.1.2; \
		uv pip -q install -e . ; \
		tests/experiments/.venv/cellpose3/bin/python tests/experiments/runcellpose3.py; \
	)
	@echo "==============================="

	@echo "> Cellpose 4.0.7"
	@uv -q venv tests/experiments/.venv/cellpose4 --python 3.13
	@( \
		export VIRTUAL_ENV=tests/experiments/.venv/cellpose4/; \
		uv pip -q install cellpose==4.0.7; \
		uv pip -q install -e . ; \
		tests/experiments/.venv/cellpose4/bin/python tests/experiments/runcellpose4.py; \
	)
	@echo "==============================="

	@echo "> StarDist 0.9.1"
	@uv -q venv tests/experiments/.venv/stardist --python 3.13
	@( \
		export VIRTUAL_ENV=tests/experiments/.venv/stardist/; \
		uv pip -q install stardist==0.9.1; \
		uv pip -q install -e . ; \
		tests/experiments/.venv/stardist/bin/python tests/experiments/runstardist.py; \
	)
	@echo "==============================="

# 	@echo "🚀 Running experiments from tests/experiments/fixtures"
# 	@(cd tests/experiments/fixtures && \
# 		uv run CellViability --config config.json --instances)

.PHONY: build
build: build ## Build wheel file
	@echo "🚀 Creating wheel file"
	@uvx --from build pyproject-build --installer uv

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	@uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

.PHONY: clean
clean: ## Remove all untracked files (except .venv and data/)
	@echo "🚀 Removing untracked files"
	@git clean -fdx -e .venv -e data/ -e results/ .

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@uv run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@uv run mkdocs serve

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help
