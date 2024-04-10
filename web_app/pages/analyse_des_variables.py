from dash import Dash, html, dcc,Input, Output, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import plotly.express as px
from utils.callbacks import  binary_risk_stability_graph, binary_volume_stability_graph, binary_risk_info
from utils.preprocessing import binary_vars_for_app, lc_vars_for_app

layout = html.Div(
    [
        html.Div(
            html.H1(children='Analyse des variables', style={'textAlign': 'center'}),
            style={'margin-bottom': '20px'}
        ),
# variables binaires
        html.Div(
            [
                html.Label('Binary Variables'),
                dmc.Select(
                    data= binary_vars_for_app,
                    value='FLAG_MOBIL', id='binary_col',
                    style={"width": 400, "marginBottom": 10}
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
                    ],
                    style={'flex': '1', 'margin-right': '10px', 'width': '45vw'}  # Utilisez 30% de la largeur de la fenêtre
                ),
                html.Div(
                    [
                        dcc.Graph(id='b_graph_volume_stability_overtime'),
                    ],
                    style={'flex': '1', 'margin-right': '10px', 'width': '45vw'}  # Utilisez 30% de la largeur de la fenêtre
                )
                ,
            ],
            style={'display': 'flex', 'flexDirection': 'row', 'width': '100%'}  
        ),
        html.Div(
                    [
                        html.Div(
                            [   html.H2("Informations supplémentaires"),
                                dmc.List(
                                    [
                                        dmc.ListItem(id='binary_risk_info'),
                                        dmc.ListItem(id='binary_vol_info'),
                                    ]
                                ),
                                #html.P(),
                            ],
                            style={'padding': '1%', 'backgroundColor': '#00ffff', 'border': '2px solid #000', 'borderRadius': '10px', 'width': '20vw', 'height': 'auto'}
                        )
                    ],
                    style={'flex': '1', 'width': '30vw'} 
                ),
        
# A partir de là variables catégorielles
        html.Div(
            [
                html.Label('Categorical Variables'),
                dmc.Select(
                    data= lc_vars_for_app,
                    value='NAME_CONTRACT_TYPE', id='lc_col',
                    style={"width": 400, "marginBottom": 10}
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
                html.Div(
                    [
                        html.Div(
                            [   html.H2("Informations supplémentaires"),
                                dmc.List(
                                    [
                                        dmc.ListItem(id='lc_stability_info'),
                                    ]
                                ),
                                #html.P(),
                            ],
                            style={'padding': '1%', 'backgroundColor': '#00ffff', 'border': '2px solid #000', 'borderRadius': '10px', 'width': '20vw', 'height': 'auto'}
                        )
                    ],
                    style={'flex': '1', 'width': '30vw'} 
                )
            ],
            style={'display': 'flex', 'flexDirection': 'row', 'width': '100%'}  
        )
    ],
    
    style={'display': 'flex', 'flexDirection': 'column'}  
)


