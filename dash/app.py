import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Initialiser l'application Dash
app = dash.Dash(__name__,suppress_callback_exceptions=True)

# Générateur de menu déroulant pour les filières
def generate_filiere_dropdown():
    # Liste des formations
    filieres = [
        'Mécanique et Interactions (MI)',
        'Microélectronique Et Automatique (MEA)',
        'Matériaux (MAT)',
        'Génie Biologique et Agroalimentaires (GBA)',
        'Mécanique Structures Industrielles (MSI - apprentissage)',
        'Eau et Génie Civil (EGC - apprentissage)',
        'Sciences et Technologies de l\'Eau (STE)',
        'Informatique et Gestion (IG)',
        'Systèmes Embarqués (SE - apprentissage)',
        'Global'
    ]
    return dcc.Dropdown(
        id='filiere-dropdown',
        options=[{'label': filiere, 'value': filiere} for filiere in filieres],
        value=filieres[0]  # La valeur par défaut peut être la première filière de la liste
    )

# La structure de l'application avec des onglets pour chaque type de résultat
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Avis sur les UE', value='tab-1'),
        dcc.Tab(label="Conseils pour l'insertion pro", value='tab-2'),
        dcc.Tab(label="Difficultés pour la recherche d'emploi", value='tab-3'),
        dcc.Tab(label="Motivations pour la poursuite d'étude", value='tab-4'),
        dcc.Tab(label="Projets d'évolution de carrière", value='tab-5'),
        dcc.Tab(label='Taux de satisfaction insertion', value='tab-6')
    ]),
    html.Div(id='tabs-content'),
    dcc.RadioItems(
                id='graph-type-selector-employment-difficulty',
                options=[
                    {'label': '2D Graph', 'value': '2DGraph'},
                    {'label': 'Bar Chart', 'value': 'BarChart'}
                ],
                value='2DGraph'
            ),
    dcc.RadioItems(
                id='graph-type-selector-motivations-poursuite-etude',
                options=[
                    {'label': '2D Graph', 'value': '2DGraph'},
                    {'label': 'Bar Chart', 'value': 'BarChart'}
                ],
                value='2DGraph'
            ),
    generate_filiere_dropdown()
])



# Le callback pour mettre à jour le contenu des onglets
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])  # Ajout de l'Input pour le sélecteur de filière
def render_content(tab):
    if tab == 'tab-1':
        # Intégrer ici le résultat du script avisUE.py
        return html.Div([
            html.H3('Avis sur les UE'),
            # Ajouter ici le graphique ou le tableau pertinent
        ])
    elif tab == 'tab-2':
        # Intégrer ici le résultat du script conseilsInsertion.py
        return html.Div([
            html.H3("Conseils pour l'insertion pro"),
            # Ajouter ici le graphique ou le tableau pertinent
        ])
    elif tab == 'tab-3':
        # Difficultés pour la recherche d'emploi
        return html.Div([
            html.H3("Difficultés pour la recherche d'emploi"),
            html.Div(id='employment-difficulty-graph')
        ])
    elif tab == 'tab-4':
        # Intégrer ici le résultat du script motivationsPoursuiteEtude.py
        return html.Div([
            html.H3("Motivations pour la poursuite d'étude"),
            html.Div(id='motivations-poursuite-etude-graph')
            # Ajouter ici le graphique ou le tableau pertinent
        ])
    elif tab == 'tab-5':
        # Intégrer ici le résultat du script projetsEvolution.py
        return html.Div([
            html.H3("Projets d'évolution de carrière"),
            # Ajouter ici le graphique ou le tableau pertinent
        ])
    elif tab == 'tab-6':
        # Intégrer ici le résultat du script tauxSatisfactionInsertion.py
        return html.Div([
            html.H3('Taux de satisfaction insertion')
            # Ajouter ici le graphique ou le tableau pertinent
        ])



# Callback pour l'onglet "Difficultés pour la recherche d'emploi"
@app.callback(
    Output('employment-difficulty-graph', 'children'),
    [Input('graph-type-selector-employment-difficulty', 'value')])
def update_graph(graph_type):
    if graph_type == '2DGraph':
        return html.Iframe(
            src='assets/diffEmploi/difficultésEmploiTopics.html',
            style={"height": "600px", "width": "100%"}
        )
    elif graph_type == 'BarChart':
        return html.Iframe(
            src='assets/diffEmploi/difficultésEmploiBarchart.html',
            style={"height": "600px", "width": "100%"}
        )

# Callback pour l'onglet "motivations pour la poursuite d'étude"
@app.callback(
    Output('motivations-poursuite-etude-graph', 'children'),
    [Input('graph-type-selector-motivations-poursuite-etude', 'value')])
def update_graph(graph_type):
    if graph_type == '2DGraph':
        return html.Iframe(
            src='assets/motiv/topicsPoursuiteEtude.html',
            style={"height": "600px", "width": "100%"}
        )
    elif graph_type == 'BarChart':
        return html.Iframe(
            src='assets/motiv/barchartPoursuiteEtude.html',
            style={"height": "600px", "width": "100%"}
        )



# Notez que nous devons maintenant définir des callbacks séparés pour chaque graphique
# qui dépend du sélecteur de filière. Voici un exemple de callback pour l'onglet 'Avis sur les UE':
#@app.callback(
#    Output('avis-ue-graph', 'figure'),
#    [Input('filiere-dropdown', 'value')]
#)
#def update_avis_ue_graph(selected_filiere):
    # Ici, vous filtreriez vos données en fonction de la filière sélectionnée et
    # génèreriez le graphique correspondant. Voici un exemple générique:
#    df = pd.DataFrame()  # Remplacez par le chargement de vos données réelles
#    filtered_df = df[df['Filière'] == selected_filiere]
#    fig = px.line(filtered_df, x='Année', y='Valeur')  # Remplacez par vos axes réels
#    return fig



@app.callback(
    Output('filiere-dropdown', 'style'),
    [Input('tabs', 'value')]
)
def show_hide_filiere_dropdown(tab):
    if tab in ['tab-1', 'tab-2', 'tab-5', 'tab-6']:
        return {'display': 'block'}
    else:
        return {'display': 'none'}
    
@app.callback(
    Output('graph-type-selector-employment-difficulty', 'style'),
    [Input('tabs', 'value')]
)
def show_hide_employment_selector(tab):
    if tab in ['tab-3']:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('graph-type-selector-motivations-poursuite-etude', 'style'),
    [Input('tabs', 'value')]
)
def show_hide_motiv_selector(tab):
    if tab in ['tab-4']:
        return {'display': 'block'}
    else:
        return {'display': 'none'}
    
    
if __name__ == '__main__':
    app.run_server(debug=True)
