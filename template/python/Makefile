.PHONY: test run build benchmark fmt
test:
	python -m unittest

run:
	python main.py

fmt:
	ruff format

benchmark:
	hyperfine --warmup 3 -N "python main.py"
