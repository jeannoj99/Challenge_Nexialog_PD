from dash import Dash, html, dcc,Input, Output, callback
import pandas as pd
import plotly.express as px
from utils.callbacks import  binary_risk_stability_graph, binary_volume_stability_graph, binary_summary


layout = html.Div(
    [
        html.Div(
            html.H1(children='Analyse des variables', style={'textAlign': 'center'}),
            style={'margin-bottom': '20px'}
        ),

        html.Div(
            [
                html.Label('Binary Variables'),
                dcc.Dropdown(
                    options=[
                        {'label': 'FLAG_MOBIL', 'value': 'FLAG_MOBIL'},
                        {'label': 'FLAG_EMP_PHONE', 'value': 'FLAG_EMP_PHONE'},
                        {'label': 'FLAG_WORK_PHONE', 'value': 'FLAG_WORK_PHONE'},
                        {'label': 'FLAG_EMAIL', 'value': 'FLAG_EMAIL'}
                    ],
                    value='FLAG_WORK_PHONE', id='binary_col'
                ),

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
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2("Informations supplémentaires"),
                                html.P(id='binary_info'),
                            ],
                            style={'padding': '1%', 'backgroundColor': '#00ffff', 'border': '2px solid #000', 'borderRadius': '10px', 'width': '20vw'}  # Utilisez 40% de la largeur de la fenêtre
                        )
                    ],
                    style={'flex': '1', 'width': '30vw'}  # Utilisez 40% de la largeur de la fenêtre
                )
            ],
            style={'display': 'flex', 'flexDirection': 'row', 'width': '100%'}  # Utilisez 100% de la largeur de la fenêtre
        )
    ],
    style={'display': 'flex', 'flexDirection': 'column'}  
)


