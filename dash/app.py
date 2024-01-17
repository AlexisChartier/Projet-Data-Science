import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Initialiser l'application Dash
app = dash.Dash(__name__,suppress_callback_exceptions=True)
# Ajouter du CSS pour rendre la navigation plus ergonomique et centrer le contenu
app.css.append_css({
    'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css'
})
app.css.append_css({
    'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css'
})
app.css.append_css({
    'external_url': 'https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i'
})
app.css.append_css({
    'external_url': 'https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i'
})
app.css.append_css({
    'external_url': 'https://cdn.jsdelivr.net/npm/dash-bootstrap-components@0.3.0/dist/dash-bootstrap-components.min.css'
})

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
        value=filieres[0],  # La valeur par défaut peut être la première filière de la liste
        style={'width': '300px'}
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
    ], style={'font-family': 'Raleway', 'font-weight': 'bold'}),
    html.Div(id='tabs-content', style={'margin-top': '20px'}),
    dcc.RadioItems(
        id='graph-type-selector-employment-difficulty',
        options=[
            {'label': '2D Graph', 'value': '2DGraph'},
            {'label': 'Bar Chart', 'value': 'BarChart'}
        ],
        value='2DGraph',
        style={'margin-top': '20px'}
    ),
    dcc.RadioItems(
        id='graph-selector-avis-ue',
        options=[
            {'label': 'UEs utiles pour l\'insertion professionnelle', 'value': 'utileinsertion'},
            {'label': 'UEs qui aurait méritées d\'être approfondies', 'value': 'meriteapprondis'},
            {'label': 'UEs absentes qui aurait été utiles', 'value': 'auraitutile'},
            {'label': 'UEs inutiles', 'value': 'inutile'}
        ],
        value='utileinsertion',
        style={'margin-top': '20px'}
    ),
    dcc.RadioItems(
        id='graph-type-selector-motivations-poursuite-etude',
        options=[
            {'label': '2D Graph', 'value': '2DGraph'},
            {'label': 'Bar Chart', 'value': 'BarChart'}
        ],
        value='2DGraph',
        style={'margin-top': '20px'}
    ),
    generate_filiere_dropdown()
], style={'text-align': 'center', 'font-family': 'Product Sans'})

# Le callback pour mettre à jour le contenu des onglets
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value'),
               Input('filiere-dropdown','value')])  # Ajout de l'Input pour le sélecteur de filière
def render_content(tab, selected_filiere):
    if tab == 'tab-1':
        # Intégrer ici le résultat du script avisUE.py
        return html.Div([
            html.H3('Avis sur les UE'),
            html.Img(id='avis-ue-image')
            # Ajouter ici le graphique ou le tableau pertinent
        ])
    elif tab == 'tab-2':
        # Intégrer ici le résultat du script conseilsInsertion.py
        return html.Div([
            html.H3("Conseils pour l'insertion pro"),
            html.Img(id='conseils-insertion-image')

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
            html.Img(id='projets-evolution-image')
            # Ajouter ici le graphique ou le tableau pertinent
        ])
    elif tab == 'tab-6':
        # Intégrer ici le résultat du script tauxSatisfactionInsertion.py
        return html.Div([
            html.H3('Taux de satisfaction insertion'),
            html.Div(id='taux-satisfaction-insertion-graph')
        ])


@app.callback(
    Output('avis-ue-image', 'src'),
    [Input('graph-selector-avis-ue', 'value'),
     Input('filiere-dropdown', 'value')])
def update_avis_ue_image(selected_avis_ue, selected_filiere):
    # Replace with actual logic to select the appropriate image based on the "filiere"
    return f'assets/avis/avisUE_{selected_filiere}_{selected_avis_ue}.png'

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
@app.callback(
    Output('taux-satisfaction-insertion-graph', 'children'),
    [Input('tabs', 'value')]
)
def show_graphSatisfaction(tab):
    if tab in ['tab-6']:
        return html.Img(src='assets/satisfaction/tauxSatisfactionInsertionFiliere.png', style={"height": "800px", "width": "100%"})



@app.callback(
    Output('filiere-dropdown', 'style'),
    [Input('tabs', 'value')]
)
def show_hide_filiere_dropdown(tab):
    if tab in ['tab-1', 'tab-2', 'tab-5']:
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
    

@app.callback(
    Output('graph-selector-avis-ue', 'style'),
    [Input('tabs', 'value')]
)
def show_hide_avis_ue_selector(tab):
    if tab in ['tab-1']:
        return {'display': 'block'}
    else:
        return {'display': 'none'}
    

# Callback for "Conseils pour l'insertion pro" image display based on selected "filiere"
@app.callback(
    Output('conseils-insertion-image', 'src'),
    [Input('filiere-dropdown', 'value')])
def update_conseils_insertion_image(selected_filiere):
    # Replace with actual logic to select the appropriate image based on the "filiere"
    return f'assets/conseils/{selected_filiere}.png'

# Callback for "Projets d'évolution de carrière" image display based on selected "filiere"
@app.callback(
    Output('projets-evolution-image', 'src'),
    [Input('filiere-dropdown', 'value')])
def update_projets_evolution_image(selected_filiere):
    # Replace with actual logic to select the appropriate image based on the "filiere"
    return f'assets/projets/{selected_filiere}.png'

    
if __name__ == '__main__':
    app.run_server(debug=True)
