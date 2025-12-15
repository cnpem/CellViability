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

.PHONY: build
build: build ## Build wheel file
	@echo "🚀 Creating wheel file"
	@uvx --from build pyproject-build --installer uv

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	@uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

.PHONY: tests
tests: install ## Test the code
	@echo "🚀 Testing package from tests/integration/fixtures"
	@(cd tests/integration/fixtures && \
		uv run CellViability --config config.json --instances --npy --verbose)

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

.PHONY: setup-envs
setup-envs: install ## Setup virtual environments for tests (CP3, CP4, StarDist)
	@echo "🚀 Configuring environments for performance tests"

	@echo "[==> Creating env: cellpose3"
	@uv -q venv tests/.venv/cellpose3 --python 3.10
	@( \
		export VIRTUAL_ENV=tests/.venv/cellpose3/; \
		uv pip -q install cellpose==3.1.1.2; \
		uv pip -q install . ; \
		uv pip -q install -U "numpy<2"; \
		uv pip -q install nvidia-ml-py3; \
	)
	@echo "==============================="

	@echo "[==> Creating env: cellpose4"
	@uv -q venv tests/.venv/cellpose4 --python 3.10
	@( \
		export VIRTUAL_ENV=tests/.venv/cellpose4/; \
		uv pip -q install cellpose==4.0.7; \
		uv pip -q install . ; \
		uv pip -q install -U "numpy<2"; \
		uv pip -q install nvidia-ml-py3; \
	)
	@echo "==============================="

	@echo "[==> Creating env: stardist"
	@uv -q venv tests/.venv/stardist --python 3.10
	@( \
		export VIRTUAL_ENV=tests/.venv/stardist/; \
		uv pip -q install stardist==0.9.1; \
		uv pip -q install . ; \
		uv pip -q install -U "numpy<2"; \
		uv pip -q install nvidia-ml-py3; \
	)
	@echo "==============================="

.PHONY: benchmark
benchmark: ## Run performance tests (CP3, CP4, StarDist)
	@echo "🚀 Running benchmarking "

	@echo "[==> Cellpose 3.1.1.2"
	@( \
		export VIRTUAL_ENV=tests/.venv/cellpose3/; \
		tests/.venv/cellpose3/bin/python tests/benchmark/runcellpose3.py; \
	)
	@echo "==============================="

	@echo "[==> Cellpose 4.0.7"
	@( \
		export VIRTUAL_ENV=tests/.venv/cellpose4/; \
		tests/.venv/cellpose4/bin/python tests/benchmark/runcellpose4.py; \
	)
	@echo "==============================="

	@echo "[==> StarDist 0.9.1"
	@( \
		export VIRTUAL_ENV=tests/.venv/stardist/; \
		tests/.venv/stardist/bin/python tests/benchmark/runstardist.py; \
	)
	@echo "==============================="

	@echo "[==> Analyzing benchmark"
	@( \
		export VIRTUAL_ENV=.venv/; \
		.venv/bin/python tests/benchmark/analyze.py; \
	)
	@echo "==============================="

.PHONY: gpu
gpu: ## Test memory usage on GPU (CP3, CP4, StarDist)
	@echo "🚀 Testing GPU memory usage for segmentation models"

	@echo "[==> Cellpose 3.1.1.2"
	@( \
		export VIRTUAL_ENV=tests/.venv/cellpose3/; \
		tests/.venv/cellpose3/bin/python tests/gpu/runcellpose3.py; \
	)
	@echo "==============================="

	@echo "[==> Cellpose 4.0.7"
	@( \
		export VIRTUAL_ENV=tests/.venv/cellpose4/; \
		tests/.venv/cellpose4/bin/python tests/gpu/runcellpose4.py; \
	)
	@echo "==============================="

	@echo "[==> StarDist 0.9.1"
	@( \
		export VIRTUAL_ENV=tests/.venv/stardist/; \
		tests/.venv/stardist/bin/python tests/gpu/runstardist.py; \
	)
	@echo "==============================="

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help
