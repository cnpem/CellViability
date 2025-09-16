# Developer Guide

This document provides guidelines for developers who want to contribute to the **CellViability** package. It explains how to set up the development environment, run tests, maintain code quality, build the package, and manage documentationusing the provided `Makefile`.

## Development Environment

To set up a development environment for the **CellViability** package, you need to install the [uv](https://docs.astral.sh/uv/), our project management tool.

1. Clone the repository:

```bash
git clone https://github.com/cnpem/CellViability.git
cd CellViability
```

2. Install the required dependencies:

```bash
make install
```

**Note:** This will create a virtual environment in the .venv directory, install the cellviability package along with development (dev) and documentation (docs) dependencies, and configure pre-commit hooks.

## Code Quality

To maintain consistent code quality, run the following:

```bash
make check
```

**Note:** This executes lock file consistency checks, pre-commit hooks, and static type checking with mypy.

## Testing

To run the test suite, use:

```bash
make test
```

**Note:** All tests in the tests/ directory will be executed using pytest, including coverage reporting.

## Build

To build the package, run:

```bash
make build
```

**Note:** Builds will create a source distribution and a wheel file in the dist/ directory.

To remove previous builds, use:

```bash
make clean-build
```

## Documentation

To verify that the documentation builds correctly, run:

```bash
make docs-test
```

To serve the documentation locally, use:

```bash
make docs
```

**Note:** This allows you to preview the documentation in a web browser. You can view the documentation at `http://localhost:8000/CellViability` in your web browser.

## Clean up untracked files

To remove untracked files from the repository, run:

```bash
make clean
```

**Note:** This will delete all untracked files and directories, except the virtual environment `.venv` and `data` directories.

---

Thank you for contributing to the **CellViability** package!
