from dash import Dash, html, dcc,Input, Output, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import plotly.express as px
from utils.callbacks import  binary_risk_stability_graph, binary_volume_stability_graph, binary_risk_info
from utils.callbacks import hc_risk_stability_graph, hc_volume_stability_graph
from utils.preprocessing import binary_vars_for_app, lc_vars_for_app, hc_vars_for_app_nd
from utils.callbacks import hc_iv, hc_mann_whitney,hc_cramers_v, hc_chi_stat,hc_stability_info

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

        # variables binaires

        dmc.Container(
            [   
                    # dmc.Title("TEST", order=1)

                    html.Div(
            [
                dmc.Title('Binary Variables', order = 3, style={'textAlign': 'center'}),
                html.Br(),
                dmc.Select(
                    data=binary_vars_for_app,
                    value='FLAG_MOBIL',
                    id='binary_col',
                    style={"width": 400, "margin": "0 auto", "marginBottom": 10, 'textAlign': 'center'}
                ),
                html.Br(),
            ],
            style={'padding': '1%'}
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='b_graph_risk_stability_overtime'),
                                html.Div(id = "binary_risk_info")
                    ],
                    style={'flex': '1', 'margin-right': '10px', 'width': '45vw'}  # Utilisez 30% de la largeur de la fenêtre
                ),
                html.Div(
                    [
                        dcc.Graph(id='b_graph_volume_stability_overtime'),
                                html.Div(id = "binary_vol_info"),
                    ],
                    style={'flex': '1', 'margin-right': '10px', 'width': '45vw'}  # Utilisez 30% de la largeur de la fenêtre
                )
            ],
            style={'display': 'flex', 'flexDirection': 'row', 'width': '100%'}  
        ),

        html.Br(),

            ],
            style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}, size="100"
        ),


 
# A partir de là variables catégorielles (lc)
        html.Div(
            [
                html.Div(
                    [
                        dmc.Title('Categorical Variables', order = 3, style={'textAlign': 'center'}),
                        html.Br(),
                        dmc.Select(
                            data=lc_vars_for_app,
                            value='NAME_CONTRACT_TYPE',
                            id='lc_col',
                            style={"width": 400, "margin": "0 auto", "marginBottom": 10, 'textAlign': 'center'}
                        ),
                        html.Br(),
                    ],
                    style={'padding': '1%'}
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='lc_graph_risk_stability_overtime'),
                            ],
                            style={'flex': '1', 'margin-right': '10px', 'width': '45vw'}  # Utilisez 30% de la largeur de la fenêtre
                        ),
                        html.Div(
                            [
                                dcc.Graph(id='lc_graph_volume_stability_overtime'),
                            ],
                            style={'flex': '1', 'margin-right': '10px', 'width': '45vw'}  # Utilisez 30% de la largeur de la fenêtre
                        ),

                    ],
                    style={'display': 'flex', 'flexDirection': 'row', 'width': '100%'}  
                ),

                html.Div(id="lc_stability_info"), 
               
            ],
            style={'display': 'flex', 'flexDirection': 'column'}
        ),  


# A partir de là variable catégo (hc)
        html.Div(
            [ 
            #     html.H3(children='Variables catégorielles à grand nombre de modalités',
            # style={'margin-bottom': '15px','textAlign': 'left'}),

            dmc.Title('Variables catégorielles à grand nombre de modalités', order = 3, style={'textAlign': 'center'}),

            dmc.Checkbox(label="Variables discrétisées", id="checkbox_discretized_choice", style={"width": 400, "margin": "0 auto", "marginBottom": 10, 'textAlign': 'center'}),

            dcc.Dropdown(id="dropdown_var_choice",options=[{'label': i, 'value': i} for i in hc_vars_for_app_nd],value='NAME_EDUCATION_TYPE', style={"width": 400, "margin": "0 auto", "marginBottom": 10, 'textAlign': 'center'}),
             
             html.Div([
            
            # dmc.Checkbox(label="Variables discrétisées", id="checkbox_discretized_choice"),
            
            # dcc.Dropdown(id="dropdown_var_choice",options=[{'label': i, 'value': i} for i in hc_vars_for_app_nd],value='NAME_EDUCATION_TYPE'),
            
            html.Br(),
            
            html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='hc_graph_risk_stability_overtime'),
                            ],
                            style={'flex': '1', 'margin-right': '10px', 'width': '45vw'}  # Utilisez 30% de la largeur de la fenêtre
                        ),
                        html.Div(
                            [
                                dcc.Graph(id='hc_graph_volume_stability_overtime'),
                            ],
                            style={'flex': '1', 'margin-right': '10px', 'width': '45vw'}  # Utilisez 30% de la largeur de la fenêtre
                        ),
                    ],
                    style={'display': 'flex', 'flexDirection': 'row', 'width': '100%'}  
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H4("Informations supplémentaires"),
                                        dmc.List(
                                            [
# TODO REGARDEZ CE QUE VOUS VOULEZ FAIRE AVEC LES ARRONDIS (check utils.utils)
                                                dmc.ListItem(id='hc_stability_info'),
                                                dmc.ListItem(id='hc_chi_stat_info'),
                                                dmc.ListItem(id='hc_cramers_v_info'),
# TODO QUOI FAIRE AVEC MANNWHITEENYE                                                
                                                dmc.ListItem(id='hc_mann_whitney_info'), 
                                                dmc.ListItem(id='hc_iv_info'),
                                                
                                            ]
                                        ),
                                    ],
                                    style={'padding': '1%', 'backgroundColor': '#00ffff', 'border': '2px solid #000', 'borderRadius': '10px', 'width': '100%', 'height': 'auto'}
                                )
                            ],
                            style={'flex': '1', 'width': '100%'} 
                        )
                    ],
                    style={'display': 'flex', 'flexDirection': 'row', 'width': '100%', 'marginTop': '20px'}  
                )
            ],
            style={'display': 'flex', 'flexDirection': 'column'}
        )
        
])
    ]
)