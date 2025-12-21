from pathlib import Path
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html

def get_data_readmes(data_dir=None):
    """Discover and load all README.md files from the data directory.

    Recursively searches the data directory and its subdirectories for
    README.md files, reads their content, and returns structured data with
    titles derived from folder names.

    Args:
        data_dir: Path to the data directory. Can be string or Path object.
            If None, uses the default '../../../data' relative to this file.

    Returns:
        list: List of dictionaries, each containing:
            - 'title' (str): Folder name converted to title case, or
              "Project Data Directory" for root README.
            - 'markdown' (str): Full content of the README.md file.

    Examples:
        >>> # Use default data directory
        >>> readmes = get_data_readmes()
        >>> for readme in readmes:
        ...     print(f"Title: {readme['title']}")
        ...     print(f"Length: {len(readme['markdown'])} chars")
        >>>
        >>> # Use custom directory
        >>> readmes = get_data_readmes("/path/to/custom/data")
    """
    if data_dir is None:
        data_dir = Path(__file__).parent.parent.parent / "data"
    else:
        data_dir = Path(data_dir)
    readme_files = list(data_dir.glob("**/README.md"))
    readmes = []
    for f in sorted(readme_files):
        with open(f, encoding="utf-8") as file:
            md_content = file.read()
            # Use folder name as title if not root README
            if f.parent == data_dir:
                title = "Project Data Directory"
            else:
                title = f.parent.name.replace('_', ' ').title()
            readmes.append({
                "title": title,
                "markdown": md_content
            })
    return readmes

def build_readme_cards(readmes, compact=True):
    """Build Dash card components from README data.

    Transforms a list of README dictionaries into styled Bootstrap card
    components with Markdown content rendering. Supports both compact and
    expanded layouts.

    Args:
        readmes: List of dictionaries, each containing 'title' (str) and
            'markdown' (str) keys with README content.
        compact: If True, uses compact styling with smaller fonts and padding.
            If False, uses expanded styling. Defaults to True.

    Returns:
        list: List of dbc.Card components, each containing a header with the
            title and a body with rendered Markdown content.

    Examples:
        >>> readmes = get_data_readmes()
        >>> cards = build_readme_cards(readmes, compact=True)
        >>> layout = html.Div(cards)
        >>>
        >>> # With expanded styling
        >>> cards_expanded = build_readme_cards(readmes, compact=False)
    """
    cards = []
    for readme in readmes:
        cards.append(
            dbc.Card([
                dbc.CardHeader(
                    html.H5(readme["title"], className="mb-0", style={"fontSize": "1.1rem", "fontWeight": 500, "padding": "0.5rem 1rem"})
                ),
                dbc.CardBody([
                    dcc.Markdown(
                        readme["markdown"],
                        className=("about-markdown compact-markdown" if compact else "about-markdown"),
                        style={
                            "background": "#f8f9fa",
                            "padding": "0.75rem 1rem" if compact else "1.5rem",
                            "borderRadius": "0.4rem" if compact else "0.5rem",
                            "textAlign": "left",
                            "fontSize": "0.97rem" if compact else "1.08rem",
                            "overflowX": "auto",
                            "lineHeight": "1.5" if compact else "1.7",
                            "margin": 0
                        }
                    )
                ], className="about-card-body", style={"padding": "0.5rem 0.5rem 0.7rem 0.5rem" if compact else "1rem 1.5rem"})
            ], className="mb-3 shadow-sm", style={"borderRadius": "0.7rem", "boxShadow": "0 2px 8px rgba(0,0,0,0.04)"})
        )
    return cards

