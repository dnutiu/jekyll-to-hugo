# Formats the code
format:
	autoflake --exclude venv -ri . && black . && isort -r .
# Run tests
test:
	pytest .