import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


app.layout = html.Div(
    children=[
        dcc.Location(id="url", refresh=False),
        html.H1("Projet Data Science", className="display-4"),
        html.P("Application dash pour la visualisation des résultats des analyses", className="lead"),
        html.Div(
            children=[
                html.Button("Analyse des avis sur les UE", className="btn btn-primary mr-2", id="btn-avis"),
                html.Button("Analyse de la satisfaction", className="btn btn-primary", id="btn-satisfaction"),
                html.Button("Analyse des projets d'évolution de carrière", className="btn btn-primary", id="btn-projets-evolution")
            ],
            className="mb-4"
        ),
        html.Div(id="page-content")
    ],
    className="container mt-4"
)

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/page1":
        return html.H2("Contenu de la page 1")
    elif pathname == "/page2":
        return html.H2("Contenu de la page 2")
    else:
        return html.H2("Page non trouvée")

if __name__ == "__main__":
    app.run_server(debug=True)
