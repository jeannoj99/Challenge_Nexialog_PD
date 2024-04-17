from dash import Dash, html, dcc,Input, Output, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import plotly.express as px
# from utils.callbacks import  binary_risk_stability_graph, binary_volume_stability_graph, binary_risk_info
# from utils.callbacks import hc_risk_stability_graph, hc_volume_stability_graph
from utils.preprocessing import binary_vars_for_app, lc_vars_for_app, catego_a_utiliser
# from utils.callbacks import hc_iv, hc_mann_whitney,hc_cramers_v, hc_chi_stat,hc_stability_info
from utils.callbacks import display_switch_var_discr, risk_stability_graph, volume_stability_graph
from utils.callbacks import recup_var_1, recup_var_2
from utils.callbacks import choix_var_2_ou_target, choix_var_1, compute_stats

border_color = "#8C8C8C"

style = {
    #"height": 100,
    "border": f"1px solid {border_color}",
    "marginTop": 20,
    #"marginBottom": 20,
    "borderRadius": 10,  # Arrondir les bordures
    "backgroundColor": "white",  # Fond blanc
    
}

layout = html.Div(
    [
        html.Div(
            dmc.Title('Analyse des variables', order=1, style={'textAlign': 'center'}),
            style={'margin-bottom': '20px'}
        ),

# graphique variable unique (toutes confondues)

        dmc.Container([
            html.Div(
                [
                    dmc.Title('Choose your variable', order=3, style={'textAlign': 'center'}),
                    html.Br(),
                    dmc.Select(
                        data=[{'label': i, 'value': i} for i in sorted(list(set(binary_vars_for_app + lc_vars_for_app + catego_a_utiliser)))],
                        value='FLAG_EMP_PHONE',
                        id='col_for_graphs',
                        style={"width": 400, "margin": "0 auto", "marginBottom": 10, 'textAlign': 'center'}
                    ),
                    html.Div(id='switch_var_d_nd'),
                    html.Div(id='switch'), # pour éviter l'erreur
                    html.Br(),
                ],
                style={'padding': '1%'}
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(id='graph_risk_stability_overtime'),
                        ],
                        style={'flex': '1', 'margin-right': '10px', 'width': '45vw'}  # Utilisez 30% de la largeur de la fenêtre
                    ),
                    html.Div(
                        [
                            dcc.Graph(id='graph_volume_stability_overtime'),
                        ],
                        style={'flex': '1', 'margin-right': '10px', 'width': '45vw'}  # Utilisez 30% de la largeur de la fenêtre
                    )
                ],
                style={'display': 'flex', 'flexDirection': 'row', 'width': '100%'}
            )
        ]),

# Ici la partie gestion des variables

        dmc.Container([
            
            html.Div([
                dmc.SegmentedControl(
                    id="catego_ou_numerique",
                    value="numerical",
                    data=[
                        {"value": "numerical", "label": "Numerical Variables"},
                        {"value": "categorical", "label": "Categorical Variables"}
                    ],
                    mt=10,
        ),
                dmc.Checkbox(id='target_selected_checkbox', label='Compare with Target'),
                html.Div(id='choice_var_1'),
                html.Div(id='choice_var_2'),
                html.Div(id='var_1_compare'),
                html.Div(id='var_2_compare'),

                html.Div(
    [
        # dmc.Checkbox(id="checkbox-simple", label="Valider", mb=10),
        dmc.Button('Cliquer pour valider votre choix', id='submit-var-explo', n_clicks=0, style={'background-color': 'skyblue', 'padding': '5px 15px', 'font-size': '16px'}),
        dmc.Text(id="checkbox-output"),
    ]
),

                html.Div(id='stats_display'),
                html.Div(id='valeur_var_1', style={'display':'none'}),
                html.Div(id='valeur_var_2', style={'display':'none'}),
    
            ])
            ]),

        html.Br(),

    ],
    style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}
)