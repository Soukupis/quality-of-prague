# Quality of Prague

A comprehensive web application built with Dash and Python for analyzing and presenting quality of life metrics for Prague, Czech Republic.

## Overview

Quality of Prague is a data visualization platform that provides insights into various quality of life indicators across the beautiful city of Prague. The application features interactive dashboards and analytics to help users understand what makes Prague a great place to live, work, and visit.

## Technology Stack

- **Backend**: Python, Dash
- **Frontend**: Dash Bootstrap Components (DBC)
- **Data Processing**: GeoPandas, Pandas
- **Visualization**: Plotly
- **Styling**: Bootstrap CSS, Custom CSS
- **Icons**: Bootstrap Icons

## Installation

### Prerequisites
- Python 3.9 or higher

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd quality-of-prague
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package and dependencies:
```bash
pip install -e .
```

This will install all required dependencies from the `pyproject.toml` file.

4. For development (includes Jupyter notebooks):
```bash
pip install -e ".[dev]"
```

### Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:8050` (or the port specified in your config).

