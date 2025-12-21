Dependencies and Packages
==========================

This document lists all the packages and dependencies used in the Quality of Prague project.

Core Framework
--------------

Dash
~~~~
**Version:** Latest
**Purpose:** Main web application framework for building interactive dashboards
**Website:** https://dash.plotly.com/

The application is built on Dash, a Python framework for building analytical web applications.
Dash provides the component system, callback mechanism, and routing functionality.

**Key Features Used:**

* Multi-page apps with ``dash.register_page()``
* Callbacks for interactivity
* Component layout system
* Client-side callbacks for performance

Dash Bootstrap Components
~~~~~~~~~~~~~~~~~~~~~~~~~~
**Package:** ``dash-bootstrap-components``
**Purpose:** Bootstrap 5 UI components for Dash
**Website:** https://dash-bootstrap-components.opensource.faculty.ai/

Provides professional UI components like Cards, Navbar, Containers, Rows, and Columns.

**Components Used:**

* ``dbc.Container`` - Page layout containers
* ``dbc.Row`` / ``dbc.Col`` - Grid system
* ``dbc.Card`` - Information cards
* ``dbc.Navbar`` - Navigation bar
* ``dbc.Button`` - Interactive buttons
* ``dbc.Accordion`` - Collapsible content

Data Processing
---------------

Pandas
~~~~~~
**Package:** ``pandas``
**Purpose:** Data manipulation and analysis
**Website:** https://pandas.pydata.org/

Used for working with tabular data, filtering, aggregation, and data transformations.

**Use Cases:**

* Loading and processing CSV/JSON data
* Data filtering and aggregation
* Creating DataFrames for visualization
* Statistical calculations

GeoPandas
~~~~~~~~~
**Package:** ``geopandas``
**Purpose:** Geographic data operations
**Website:** https://geopandas.org/

Extends Pandas with geographic data types and spatial operations.

**Use Cases:**

* Loading GeoJSON files
* Spatial filtering (points within polygons)
* Coordinate system transformations
* Computing centroids
* Geographic data visualization

NumPy
~~~~~
**Package:** ``numpy``
**Purpose:** Numerical computing
**Website:** https://numpy.org/

Fundamental package for numerical operations and array computations.

Visualization
-------------

Plotly
~~~~~~
**Package:** ``plotly``
**Purpose:** Interactive graphing library
**Website:** https://plotly.com/python/

Creates all interactive maps and charts in the application.

**Chart Types Used:**

* ``go.Choroplethmap`` - District boundary maps
* ``go.Scattermap`` - Point markers (stations, meters, etc.)
* ``go.Bar`` - Comparison bar charts

**Features Used:**

* Interactive hover information
* Click events for navigation
* Custom styling and theming
* Legends and annotations

Geospatial
----------

Shapely
~~~~~~~
**Package:** ``shapely``
**Purpose:** Geometric operations
**Website:** https://shapely.readthedocs.io/

Manipulation and analysis of planar geometric objects.

**Use Cases:**

* Creating and manipulating polygons
* Point-in-polygon tests
* Geometry validation (buffer operations)
* Extracting coordinates from geometries

Caching
-------

Flask-Caching
~~~~~~~~~~~~~
**Package:** ``flask-caching``
**Purpose:** Server-side caching
**Website:** https://flask-caching.readthedocs.io/

Provides caching mechanisms to improve application performance.

**Configuration:**

* Simple cache backend
* Memoization for expensive computations
* Configurable timeout values

Development Tools
-----------------

Sphinx
~~~~~~
**Package:** ``sphinx``
**Purpose:** Documentation generation
**Website:** https://www.sphinx-doc.org/

Used to generate this documentation from Python docstrings.

**Extensions Used:**

* ``sphinx.ext.autodoc`` - Auto-documentation from docstrings
* ``sphinx.ext.napoleon`` - Google-style docstring support
* ``sphinx.ext.viewcode`` - Source code linking
* ``sphinx.ext.intersphinx`` - Cross-project references

sphinx-rtd-theme
~~~~~~~~~~~~~~~~
**Package:** ``sphinx-rtd-theme``
**Purpose:** Read the Docs theme for Sphinx

Provides the professional theme used for this documentation.

Optional Development
--------------------

These packages are used during development but not required for running the application:

* **pdoc** - Alternative documentation generator (legacy)
* **pytest** - Testing framework (if tests are added)
* **black** - Code formatting
* **flake8** - Code linting

Installation
------------

This project uses ``pyproject.toml`` for dependency management.

Install the package and all dependencies::

    pip install -e .

Or install directly from pyproject.toml::

    pip install .

For development with additional tools::

    pip install -e ".[dev]"

Package Versions
----------------

All package versions and dependencies are defined in:

* ``pyproject.toml`` - Project configuration and dependencies

The ``pyproject.toml`` file follows the modern Python packaging standards (PEP 517/518)
and contains all package metadata, dependencies, and build configuration.

Python Version
--------------

**Minimum Required:** Python 3.9+

The application is developed and tested with Python 3.9 and later versions.

Summary
-------

**Total Core Dependencies:** ~10 packages

**Categories:**

* Web Framework: Dash, Dash Bootstrap Components
* Data: Pandas, GeoPandas, NumPy
* Visualization: Plotly
* Geospatial: Shapely
* Performance: Flask-Caching
* Documentation: Sphinx, sphinx-rtd-theme

All packages are open-source and actively maintained.

