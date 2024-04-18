import dash
from dash import dcc, html, dash_table, Output, Input
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pickle
import sys
import os
sys.path.append(os.getcwd()+"/..")
from utils.utils_from_cecile import subplot_segment_default_rate, show_risk_stability_overtime, plot_feature_importances
from utils.callbacks_j import pd_summary_ml_cash, pd_summary_ml_revolving, pd_summaries_ml, ginis_ml_models, models_challenger, datas_challenger, shap_graphs_src, update_interpretable_ml, update_risk_quantification_ml, toggle_modal


border_color = "#8C8C8C"

style = {
    #"height": 100,
    "border": f"1px solid {border_color}",
    "marginTop": 20,
    #"marginBottom": 20,
    "borderRadius": 10,  # Arrondir les bordures
    "backgroundColor": "white",  # Fond blanc
    
}

# Define the layout of the app
layout = html.Div([
    dmc.Title("Modèles de Machine Learning", order=1, style={'textAlign': 'center', 'marginBottom': '10px'}),
    html.Br(),
    dcc.Dropdown(
        id='model-choice',
        options=[
            {'label': 'Cash loans', 'value': 'Cash loans'},
            {'label': 'Revolving loans', 'value': 'Revolving loans'}
        ],
        value='Cash loans',  # Default value
        clearable=False
    ),
    html.Br(),

    html.Div(
    [
        dmc.Modal(
            title="Type de modèle et paramètres utilisés",
            id="modal-centered",
            centered=True,
            zIndex=10000,
            children=[dmc.Text(id='output-modal')],
        ),
        dmc.Button("Détails", id="modal-centered-button"),
    ], style={'textAlign': 'center', 'marginBottom': '10px'}
),

    html.Div([

        html.Div([
        dmc.Title("Interprétation du modèle", order=2, style={'textAlign': 'center', 'marginBottom': '10px'}),
        html.Div([
            dcc.Graph(id='feature-importances'),
            html.Img(id='shap-image', src='/assets/shap_summary_plot_cash.png', style={'width': 'auto', 'height': '500'})
        ], style={'display': 'flex', 'justifyContent': 'space-around'})  # Graphs side by side
    ], style={'padding': '20px', 
            #   'border': '1px solid #ddd', 
              'borderRadius': '5px', 'margin': '20px'}),


    dbc.Card(
        [ dmc.Title("Evaluation du modèle sur le test", order=5, style={'textAlign': 'center', 'marginBottom': '10px'}),
            html.Div(
            id='gini-score-challenger', 
            style={'textAlign': 'center', 'fontWeight': 'bold'}  # Texte en gras
        )],
        body=True,
        style={'maxWidth': '200px', 'margin': '20px auto', 'padding': '10px', 'backgroundColor': 'skyblue'}
    )
 
    ] , style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}),


    html.Div([

           html.Div([
        dmc.Title("Quantification du risque", order=2, style={'textAlign': 'center', 'marginBottom': '10px'}),
        html.Div([
            dcc.Graph(id="risk-stability-overtime"),
            dcc.Graph(id='density-plot-challenger')
        ], style={'display': 'flex', 'justifyContent': 'space-around'}),  # Two graphs side by side
        
        html.Div([
            dcc.Graph(id='segment-challenger')  # Third graph below and centered
        ], style={'width': '60%', 'margin': '0 auto'}),
        
   
    ], style={'padding': '20px', 'borderRadius': '5px', 'margin': '20px'})
        

    ], style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}),

    html.Div([

         html.Div([
            dmc.Title("Tableau résumé de la PD", order=2 , style={'textAlign': 'center', 'marginBottom': '10px'}),
            dash_table.DataTable(
        id='pd-summary',
        style_table={'overflowX': 'auto'},
        style_cell={
            'minWidth': '50px',  # Réduire la largeur minimum pour s'adapter mieux au contenu
            'width': 'auto',     # Laisser la largeur s'ajuster automatiquement
            'maxWidth': 'auto', # Limite supérieure de la largeur
            'whiteSpace': 'normal'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
        ],
        style_as_list_view=True
)])

    ], style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}),


#     html.Div([
#         html.H2("Quantification du risque", style={'textAlign': 'center'}),
#         html.Div([
#             dcc.Graph(id="risk-stability-overtime"),
#             dcc.Graph(id='density-plot-challenger')
#         ], style={'display': 'flex', 'justifyContent': 'space-around'}),  # Two graphs side by side
        
#         html.Div([
#             dcc.Graph(id='segment-challenger')  # Third graph below and centered
#         ], style={'width': '60%', 'margin': '0 auto'}),
        
#     html.Div([
#             dmc.Title("Tableau résumé de la PD", order=3 , style={'textAlign': 'center', 'marginBottom': '10px'}),
#             dash_table.DataTable(
#         id='pd-summary',
#         style_table={'overflowX': 'auto'},
#         style_cell={
#             'minWidth': '50px',  # Réduire la largeur minimum pour s'adapter mieux au contenu
#             'width': 'auto',     # Laisser la largeur s'ajuster automatiquement
#             'maxWidth': 'auto', # Limite supérieure de la largeur
#             'whiteSpace': 'normal'
#         },
#         style_header={
#             'backgroundColor': 'rgb(230, 230, 230)',
#             'fontWeight': 'bold'
#         },
#         style_data_conditional=[
#             {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
#         ],
#         style_as_list_view=True
# )])
#     ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '5px', 'margin': '20px'})
])




