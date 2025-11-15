.PHONY: docs

docs:
	pdoc src --docformat google --no-include-undocumented --output-dir docs
