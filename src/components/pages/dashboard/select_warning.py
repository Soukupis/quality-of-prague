"""Warning message component for dashboard page.

This module provides a friendly warning message displayed when users haven't
selected both required options (districts and dataset) on the dashboard.
"""
from dash import html

def select_warning():
    """Create a warning message prompting users to make selections.

    Displays a centered, styled message box with an info icon asking users
    to select both a district and a dataset to view the comparison chart.
    Text is in Czech.

    Returns:
        html.Div: Styled warning message component with icon and text.

    Examples:
        >>> warning = select_warning()
        >>> # Displays: "Vyberte prosím obě možnosti"
        >>> # (Please select both options)
    """
    return html.Div([
            html.Div([
                html.I(className="fas fa-info-circle", style={'fontSize': '48px', 'color': '#3b82f6', 'marginBottom': '20px'}),
                html.H3("Vyberte prosím obě možnosti", style={'color': '#1e293b', 'marginBottom': '10px'}),
                html.P("Pro zobrazení grafu je potřeba vybrat městskou část i datovou sadu.",
                       style={'color': '#64748b', 'fontSize': '16px'})
            ], style={
                'textAlign': 'center',
                'padding': '40px',
                'backgroundColor': '#f8fafc',
                'borderRadius': '12px',
                'border': '2px dashed #cbd5e1',
                'margin': '20px'
            })
        ])