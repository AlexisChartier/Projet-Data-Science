import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Ajoutez du CSS personnalisé ici
external_css = [
    "style/styles.css"  # Ajoutez le lien vers votre fichier CSS personnalisé ici
]

for css in external_css:
    app.css.append_css({"external_url": css})

app.layout = html.Div(
    children=[
        dcc.Location(id="url", refresh=False),
        html.H1("Projet Data Science", className="display-4"),
        html.P("Application dash pour la visualisation des résultats des analyses", className="lead"),
        html.Div(
            children=[
                html.Button("Page 1", className="btn btn-primary mr-2", id="btn-page1"),
                html.Button("Page 2", className="btn btn-primary", id="btn-page2")
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
