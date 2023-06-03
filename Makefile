# Formats the code
format:
	autoflake --exclude venv -ri . && black . && isort -r .
# Run tests
test:
	pytest .
# Build package
build:
	python -m build
# Upload package to PyPI
upload:
	hatch publish
release:
	hatch build && hatch publish