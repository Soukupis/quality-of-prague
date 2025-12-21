# Quick Docstring Reference Guide

## Google-Style Docstring Template

```python
def function_name(param1: str, param2: int = 10, param3: list = None) -> dict:
    """One-line summary starting with a verb (50-80 chars max).
    
    More detailed description explaining what the function does,
    how it works, and any important implementation details.
    Can span multiple paragraphs if needed.
    
    Args:
        param1: Description of param1. Be specific about what it
            represents and any constraints or valid values.
        param2: Description of param2. Defaults to 10.
        param3: Description of optional parameter. Defaults to None,
            which is treated as an empty list.
    
    Returns:
        dict: Description of return value, including structure and
            special cases (None, empty, etc.). Example:
            {'key': 'value', 'count': 42}
    
    Raises:
        ValueError: When param1 is empty or invalid.
        KeyError: When required dict key is missing.
    
    Examples:
        >>> # Basic usage
        >>> result = function_name("test", 20)
        >>> print(result['count'])
        42
        >>> 
        >>> # With optional parameter
        >>> result = function_name("demo", param3=['a', 'b'])
    """
    if param3 is None:
        param3 = []
    return {'key': param1, 'count': param2}
```

## Common Patterns

### Simple Function

```python
def calculate_total(values: list) -> float:
    """Calculate the sum of all values in a list.
    
    Args:
        values: List of numeric values to sum.
    
    Returns:
        float: The total sum of all values.
    
    Examples:
        >>> calculate_total([1, 2, 3])
        6.0
    """
    return sum(values)
```

### Function with Optional Parameters

```python
def create_chart(data: pd.DataFrame, title: str = "Chart", 
                 show_legend: bool = True) -> go.Figure:
    """Create a Plotly chart from DataFrame data.
    
    Generates an interactive chart with customizable title and
    optional legend display.
    
    Args:
        data: DataFrame containing the data to plot.
        title: Chart title text. Defaults to "Chart".
        show_legend: Whether to display the legend. Defaults to True.
    
    Returns:
        go.Figure: Plotly Figure object ready for display.
    
    Examples:
        >>> df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        >>> fig = create_chart(df, "My Chart", show_legend=False)
    """
    # Implementation
    pass
```

### Function with Error Handling

```python
def load_config(filepath: str) -> dict:
    """Load configuration from a JSON file.
    
    Reads and parses a JSON configuration file, validating
    that required keys are present.
    
    Args:
        filepath: Path to the JSON configuration file.
    
    Returns:
        dict: Parsed configuration dictionary.
    
    Raises:
        FileNotFoundError: If the config file doesn't exist.
        json.JSONDecodeError: If the file is not valid JSON.
        KeyError: If required configuration keys are missing.
    
    Examples:
        >>> config = load_config("/path/to/config.json")
        >>> print(config['app_name'])
        'My Application'
    """
    # Implementation
    pass
```

### Generator Function

```python
def read_large_file(filepath: str, chunk_size: int = 1024):
    """Read a large file in chunks to save memory.
    
    Yields file contents in manageable chunks, useful for
    processing large files without loading everything into memory.
    
    Args:
        filepath: Path to the file to read.
        chunk_size: Number of bytes per chunk. Defaults to 1024.
    
    Yields:
        str: The next chunk of file content.
    
    Examples:
        >>> for chunk in read_large_file("large.txt", 512):
        ...     process(chunk)
    """
    # Implementation
    pass
```

### Class Method

```python
class DataProcessor:
    """Process and analyze data from various sources.
    
    This class provides methods for loading, cleaning, and
    analyzing data from CSV, JSON, and database sources.
    
    Attributes:
        data: Loaded DataFrame containing the current dataset.
        config: Configuration dictionary for processing options.
    
    Examples:
        >>> processor = DataProcessor(config={'clean': True})
        >>> processor.load_csv("data.csv")
        >>> result = processor.analyze()
    """
    
    def __init__(self, config: dict = None):
        """Initialize the DataProcessor.
        
        Args:
            config: Optional configuration dictionary. Defaults to None.
        
        Examples:
            >>> processor = DataProcessor({'clean': True})
        """
        self.config = config or {}
        self.data = None
    
    def load_csv(self, filepath: str) -> pd.DataFrame:
        """Load data from a CSV file.
        
        Reads a CSV file and stores it in the data attribute.
        Applies cleaning if configured.
        
        Args:
            filepath: Path to the CSV file.
        
        Returns:
            pd.DataFrame: The loaded and optionally cleaned data.
        
        Raises:
            FileNotFoundError: If the CSV file doesn't exist.
        
        Examples:
            >>> processor = DataProcessor()
            >>> df = processor.load_csv("data.csv")
            >>> print(len(df))
            100
        """
        # Implementation
        pass
```

### Callback Function (Dash)

```python
@callback(
    Output('output-div', 'children'),
    Input('input-dropdown', 'value'),
    State('state-store', 'data')
)
def update_display(selected_value: str, stored_data: dict):
    """Update the display based on dropdown selection.
    
    Dash callback that processes the selected value and stored
    state to generate updated content for the output div.
    
    Args:
        selected_value: Value selected from the dropdown component.
        stored_data: Dictionary of data stored in the dcc.Store
            component.
    
    Returns:
        Dash component or list of components to display in the
        output div.
    
    Examples:
        This is a Dash callback - it's triggered automatically:
        >>> # User selects "option1" from dropdown
        >>> # Callback executes: update_display("option1", {...})
        >>> # Returns: html.Div("You selected: option1")
    """
    # Implementation
    pass
```

## Quick Tips

### DO ✅

- Start with a verb in the summary ("Calculate...", "Load...", "Create...")
- Keep summary to one line (50-80 characters)
- Describe what the function does, not how
- Include type hints in function signature
- Provide realistic examples
- Document edge cases and special return values
- Use consistent formatting

### DON'T ❌

- Start with "This function..." (redundant)
- Repeat the function name in the description
- Write overly technical implementation details
- Forget to document optional parameters
- Leave out the Returns section
- Skip examples for complex functions
- Use inconsistent terminology

## Section Guidelines

### Args

- One parameter per line
- Include default values
- Explain constraints (e.g., "Must be > 0")
- Note if None is acceptable

### Returns

- Include the type
- Describe the structure (for dicts, lists)
- Note special cases (None, empty results)

### Raises

- List all exceptions that might be raised
- Explain when each exception occurs

### Examples

- Show realistic use cases
- Include expected output
- Show both simple and complex usage
- Use >>> for doctest compatibility

## Validation

Check your docstring:

```bash
# In Python console
>>> import my_module
>>> help(my_module.my_function)

# Should show formatted docstring
```

## VSCode/PyCharm

Trigger docstring template:
- Place cursor after `def function_name():`
- Type `"""`
- Press Enter
- IDE auto-generates template

## Building Docs

After adding docstrings:

```bash
# Rebuild documentation
make docs-clean
make docs

# View results
make docs-open
```

---

**Remember**: Good docstrings make your code self-documenting and save time for everyone (including future you)! 📝

