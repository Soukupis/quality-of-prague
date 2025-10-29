from pathlib import Path
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html

def get_data_readmes(data_dir=None):
    """
    Discover all README.md files in the data directory and subfolders.
    Returns a list of dicts with 'title' and 'markdown'.
    """
    if data_dir is None:
        data_dir = Path(__file__).parent.parent / "data"
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
    """
    Build a list of Dash cards from a list of readme dicts.
    If compact=True, use compact-markdown class for smaller cards.
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

