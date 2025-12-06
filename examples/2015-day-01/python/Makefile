.PHONY: test run build benchmark fmt
test:
	python -m unittest

run:
	python main.py

fmt:
	ruff format

benchmark:
	hyperfine -N "python main.py"
