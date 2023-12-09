# List out available commands
default:
	@just --list

# Execute installation
setup:
	@echo "Setting up project."
	pip3 install --upgrade setuptools
	@echo "Installing testing dependencies."
	pip3 install -r requirements-test.txt
	@echo "Setting up project requirements."
	pip3 install -r requirements.txt
	@echo "Project setup complete!"

# Run pep8, black, mypy linters
lint:
	python -m pylint api/
	python -m flake8 api/
	python -m black -l 80 --check api/
	python -m mypy --ignore-missing-imports api/

# Clean unused files
clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build
	@rm -rf .venv
	@echo "Cleaned out unused files and directories!"

# Run PyTest unit tests
test:
	@echo "Running unittest suite..."
	pytest -vv -rA
