# Documentation

This directory contains the Sphinx documentation for the Quality of Prague project.

## Building the Documentation

To build the HTML documentation, run:

```bash
make docs
```

Or from the root directory:

```bash
cd docs && make html
```

## Viewing the Documentation

After building, open the documentation in your browser:

```bash
open build/html/index.html
```

Or from the root directory:

```bash
open docs/build/html/index.html
```

Or use the convenient command:

```bash
make docs-open
```

## Creating PDF Documentation

### On Mac (No LaTeX Required)

Generate a print-friendly HTML and convert to PDF using your browser:

```bash
make docs-pdf
```

This will:
1. Create a single-page HTML with all documentation
2. Open it in your default browser
3. Show instructions for saving as PDF

**To create the PDF:**
1. Press `Cmd+P` (or File → Print)
2. Click the "PDF" dropdown in the bottom-left corner
3. Select "Save as PDF"
4. Choose a location and save

The PDF will include all documentation with proper formatting and page breaks.

## Cleaning the Documentation

To remove all built documentation files:

```bash
make docs-clean
```

Or from the docs directory:

```bash
cd docs && make clean
```

## Documentation Structure

- `source/` - Source files for the documentation
  - `conf.py` - Sphinx configuration
  - `index.rst` - Main documentation index
  - `modules/` - API reference documentation
- `build/` - Generated documentation (not tracked in git)
  - `html/` - HTML output

## Writing Documentation

The documentation uses:
- **reStructuredText** (.rst) format for documentation files
- **Google-style docstrings** in Python code
- **Sphinx autodoc** to automatically generate API documentation from docstrings
- **Read the Docs theme** for styling

### Adding Documentation for New Modules

1. Create a new `.rst` file in `source/modules/`
2. Add the module reference using autodoc directives
3. Include the new file in the appropriate toctree

Example:

```rst
My New Module
=============

.. automodule:: src.my_module
   :members:
   :undoc-members:
   :show-inheritance:
```

