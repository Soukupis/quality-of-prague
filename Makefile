.PHONY: docs docs-clean docs-html docs-open docs-view docs-pdf

docs:
	cd docs && $(MAKE) html

docs-html:
	cd docs && $(MAKE) html

docs-clean:
	cd docs && $(MAKE) clean

docs-open: docs
	open docs/build/html/index.html

docs-view: docs-open

docs-pdf:
	@python3 make_pdf.py

# Legacy pdoc command (kept for reference)
docs-pdoc:
	pdoc src --docformat google --no-include-undocumented --output-dir docs_pdoc_backup
