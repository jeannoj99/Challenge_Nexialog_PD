import dash
import pandas as pd
import sys
import os
from datetime import datetime
from dash import Input, Output, State, html, dcc, dash_table, MATCH, ALL, ctx, callback
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
sys.path.append(os.getcwd()+"/..")
from models.callable import DecisionExpertSystem
from utils.callbacks_j import update_decision_output, fields, categorical_vars, numeric_vars, features_by_contract

border_color = "#8C8C8C"

style = {
    #"height": 100,
    "border": f"1px solid {border_color}",
    "marginTop": 20,
    #"marginBottom": 20,
    "borderRadius": 10,  # Arrondir les bordures
    "backgroundColor": "white",  # Fond blanc
    
}



layout = html.Div([
    dmc.Title('Backtesting', order=1, style={'text-align': 'center', 'margin-bottom': '20px'}),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Label('Sélectionner le type de contrat :', style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='backtesting-contract-type-dropdown',
                    options=[{'label': k, 'value': k} for k in features_by_contract.keys()],
                    value='Cash loans',
                    clearable=False
                ),
                html.Label('Sélectionner la variable :', style={'font-weight': 'bold', 'margin-top': '20px'}),
                dcc.Dropdown(
                    id='backtesting-feature-dropdown',
                    clearable=False
                ),
            ], width=6)
        ], justify='center', style={'margin-bottom': '20px'}),

        dmc.Container(
            [
                dbc.Row([
            dbc.Col([
                dmc.Title("Tests de stabilité des variables", order=3, style={'text-align': 'center', 'margin-bottom': '20px'}),
                html.Div(id='stability-test-output')
            ], style={'margin-bottom': '20px'})
        ], justify='center'),
        dbc.Row([
            dbc.Col([
                html.Div(id='system-stability-index-output')
            ], style={'margin-bottom': '20px'})
        ], justify='center'),

            ], 
        style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}
        ),


        dmc.Container(
            [
                dbc.Row([
            dbc.Col([
                dcc.Graph(id='contract-type-graph'),
                html.Div(id='kolmogorov-smirnov-result')
            ], style={'margin-bottom': '20px'})
        ], justify='center')

            ],
            style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}
        ),

        dmc.Container(
            [
                dbc.Row([
                    dbc.Col([
                        dmc.Title('Test d’adéquation de la PD sur les CHRs', order = 3, style={'text-align': 'center', 'margin-bottom': '20px'}),
                        html.Div(id='second-table-output')
                    ], style={'margin-bottom': '20px'})
                ], justify='center')
            ] ,
            style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}
        ),


    ], fluid=True, style={'padding': '0 15%'})
], style={'max-width': '1200px', 'margin': 'auto'})