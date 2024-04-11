import dash
import pandas as pd
import sys
import os
from dash import Input, Output, State, html, dcc, dash_table, MATCH, ALL, ctx
import dash_mantine_components as dmc
path=os.getcwd()
sys.path.append(path+"/models")
print(f"current path is : {path}")
from models.callable import DecisionExpertSystem
# from src.preprocessing import DecisionTreeDiscretizer
# from models.callable import Dataset, ExpertSystem

df=pd.read_csv("../../data/application_train_vf.csv",parse_dates=["date_mensuelle"], index_col=0)

# Initialisation de l'application Dash
octroi = dash.Dash(__name__)

# Liste des champs pour l'interface utilisateur
fields = ["NAME_CONTRACT_TYPE","OCCUPATION_TYPE", "NAME_EDUCATION_TYPE" , "CB_NB_CREDIT_CLOSED", "CB_DAYS_CREDIT", "AMT_CREDIT",
          "CB_AMT_CREDIT_SUM", "AMT_INCOME_TOTAL", "AMT_GOODS_PRICE", "DAYS_BIRTH", "DAYS_EMPLOYED", "DAYS_REGISTRATION","DAYS_LAST_PHONE_CHANGE"]

# Liste des variables catégorielles et numériques
categorical_vars = ["NAME_CONTRACT_TYPE", "OCCUPATION_TYPE", "NAME_EDUCATION_TYPE"]
numeric_vars = ["CB_NB_CREDIT_CLOSED", "CB_DAYS_CREDIT", "AMT_CREDIT",
                "CB_AMT_CREDIT_SUM", "AMT_INCOME_TOTAL", "AMT_GOODS_PRICE", "DAYS_BIRTH", "DAYS_EMPLOYED", "DAYS_REGISTRATION","DAYS_LAST_PHONE_CHANGE"]

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
octroi.layout = html.Div(
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
        html.Div(
            dmc.Progress(id='probability', value=55, className='progressbar', color='green', label='55%', size='xl'),
            style={'margin': '0 auto 20px'}
        ),
        html.Div(id='output-container')
    ],
    style={'max-width': '800px', 'margin': 'auto'}
)



# Callback pour traiter la soumission des données et afficher les résultats
@octroi.callback(
        Output('decision', 'children'),
        Output('decision','style'),
        Output('dropdown-NAME_CONTRACT_TYPE', 'value'),
        Output('dropdown-OCCUPATION_TYPE', 'value'),
        Output('dropdown-NAME_EDUCATION_TYPE', 'value'),
        Output('input-CB_NB_CREDIT_CLOSED', 'value'),
        Output('input-CB_DAYS_CREDIT', 'value'),
        Output('input-AMT_CREDIT', 'value'),
        Output('input-CB_AMT_CREDIT_SUM', 'value'),
        Output('input-AMT_INCOME_TOTAL', 'value'),
        Output('input-AMT_GOODS_PRICE', 'value'),
        Output('input-DAYS_BIRTH', 'value'),
        Output('input-DAYS_EMPLOYED', 'value'),
        Output('input-DAYS_REGISTRATION', 'value'),
        Output('input-DAYS_LAST_PHONE_CHANGE', 'value'),
        Input('submit-button', 'n_clicks'),
        
        State('dropdown-NAME_CONTRACT_TYPE', 'value'),
        State('dropdown-OCCUPATION_TYPE', 'value'),
        State('dropdown-NAME_EDUCATION_TYPE', 'value'),
        State('input-CB_NB_CREDIT_CLOSED', 'value'),
        State('input-CB_DAYS_CREDIT', 'value'),
        State('input-AMT_CREDIT', 'value'),
        State('input-CB_AMT_CREDIT_SUM', 'value'),
        State('input-AMT_INCOME_TOTAL', 'value'),
        State('input-AMT_GOODS_PRICE', 'value'),
        State('input-DAYS_BIRTH', 'value'),
        State('input-DAYS_EMPLOYED', 'value'),
        State('input-DAYS_REGISTRATION', 'value'),
        State('input-DAYS_LAST_PHONE_CHANGE', 'value'),
        prevent_initial_call=True
)
def update_output(n_clicks, *values):
    if ctx.triggered_id == 'submit-button':
        field_values = {}
        # Ajout des valeurs des dropdowns pour les variables catégorielles
        for i, field in enumerate(categorical_vars):
            field_values[field] = values[i]

        # Ajout des valeurs des champs de saisie numérique pour les variables numériques
        for i, field in enumerate(numeric_vars):
            field_values[field] = values[i + len(categorical_vars)]
        
        data = DecisionExpertSystem(field_values)
        data.transform_columns()
        data.score()
        decision, decision_color = data.get_decision()
        
        # Mise à jour du style de l'élément 'decision' avec la couleur obtenue
        decision_style = {'textAlign': 'center', 'padding': '20px', 'backgroundColor': decision_color}
        
        return decision, decision_style, *values


