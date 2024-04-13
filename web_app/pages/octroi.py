import dash
import pandas as pd
import sys
import os
from dash import Input, Output, State, html, dcc, dash_table, MATCH, ALL, ctx
import dash_mantine_components as dmc
from models.callable import DecisionExpertSystem
from utils.callbacks import update_decision_output, fields, categorical_vars, numeric_vars


df=pd.read_csv("../data/application_train_vf.csv",parse_dates=["date_mensuelle"], index_col=0)


# Fonction pour créer un dropdown pour les variables catégorielles
def create_categorical_dropdown(id, label):
    return dmc.Select(
        id=id,
        label=label,
        data=[{'value': i, 'label': i} for i in df[label].unique().tolist()],
        value=df[label].unique()[0]
    )

# Fonction pour créer un champ de saisie numérique pour les variables numériques
def create_numeric_input(id, label):
    return dmc.NumberInput(
        id=id,
        label=label,
        value=1
    )

# Définition du layout de l'application
layout = html.Div(
    children=[
        html.Div(
            dmc.Title(children='CREDIT RISK PLATFORM', order=3, style={'font-family': 'IntegralCF-ExtraBold', 'text-align': 'center', 'color': 'slategray'}),
            style={'margin': '20px auto'}
        ),
        dmc.SimpleGrid(
            cols=4,
            children=[
                create_categorical_dropdown("dropdown-NAME_CONTRACT_TYPE", "NAME_CONTRACT_TYPE"),
                create_categorical_dropdown("dropdown-OCCUPATION_TYPE", "OCCUPATION_TYPE"),
                create_categorical_dropdown("dropdown-NAME_EDUCATION_TYPE", "NAME_EDUCATION_TYPE"),
                create_categorical_dropdown("dropdown-CODE_GENDER", "CODE_GENDER"),
                create_numeric_input("input-CB_NB_CREDIT_CLOSED", "CB_NB_CREDIT_CLOSED"),
                create_numeric_input("input-CB_DAYS_CREDIT", "CB_DAYS_CREDIT"),
                create_numeric_input("input-AMT_CREDIT", "AMT_CREDIT"),
                create_numeric_input("input-CB_AMT_CREDIT_SUM", "CB_AMT_CREDIT_SUM"),
                create_numeric_input("input-AMT_INCOME_TOTAL", "AMT_INCOME_TOTAL"),
                create_numeric_input("input-AMT_GOODS_PRICE", "AMT_GOODS_PRICE"),
                create_numeric_input("input-DAYS_BIRTH", "DAYS_BIRTH"),
                create_numeric_input("input-DAYS_EMPLOYED", "DAYS_EMPLOYED"),
                create_numeric_input("input-DAYS_REGISTRATION", "DAYS_REGISTRATION"),
                create_numeric_input("input-DAYS_LAST_PHONE_CHANGE", "DAYS_LAST_PHONE_CHANGE")
            ],
            id='fields-container',
            style={'margin': '0 auto 20px'}
        ),
        html.Div(
            html.Button('Submit request', id='submit-button', n_clicks=0, style={'background-color': 'blue', 'padding': '10px 20px', 'font-size': '16px'}),
            style={'text-align': 'center', 'margin': '0 auto 20px'}
        ),
        dmc.Container(
            dmc.Paper(
                html.Div("Credit decision will be displayed here", id="decision", style={'textAlign': 'center', 'padding': '20px'}),
                withBorder=True,
                radius="md",
                shadow="xs",
                p="md",
                style={'maxWidth': '600px', 'margin': '40px auto', 'backgroundColor': '#f0f0f0'}
            ),
            style={'padding': '20px'}
        ),
        # html.Div(
        #     dmc.Progress(id='probability', value=55, className='progressbar', color='green', label='55%', size='xl'),
        #     style={'margin': '0 auto 20px'}
        # ),
        html.Div(id='output-container')
    ],
    style={'max-width': '800px', 'margin': 'auto'}
)

