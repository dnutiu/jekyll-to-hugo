# Formats the code
format:
	black . && isort -r .
# Run tests
test:
	pytest .