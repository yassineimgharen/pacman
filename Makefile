install:
	@python3 -m pip install -r requirements.txt

run:
	@python3 pac-man.py config.json

debug:
	@python3 -m pdb pac-man.py config.json

clean:
	@find . -type d -name "__pycache__" -not -path "./venv/*" -exec rm -rf {} + 2>/dev/null; \
	rm -rf .mypy_cache .pytest_cache build dist || True

lint:
	@flake8 .
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
