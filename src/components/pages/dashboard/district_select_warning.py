from dash import html

def district_select_warning():
    return html.Div([
            html.Div([
                html.I(className="fas fa-info-circle", style={'fontSize': '48px', 'color': '#3b82f6', 'marginBottom': '20px'}),
                html.H3("Vyberte prosím městkou část na grafu", style={'color': '#1e293b', 'marginBottom': '10px'}),
                html.P("Pro zobrazení mapy městské části je je potřeba vybrat městskou část na grafu.",
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