import dash
import pandas as pd
import sys
import os
from datetime import datetime
from dash import Input, Output, State, html, dcc, dash_table, MATCH, ALL, ctx, callback
import dash_mantine_components as dmc
sys.path.append(os.getcwd())
from models.callable import DecisionExpertSystem
from utils.callbacks import update_decision_output, fields, categorical_vars, numeric_vars
# from src.preprocessing import DecisionTreeDiscretizer
# from models.callable import Dataset, ExpertSystem

df=pd.read_csv("../data/application_train_vf.csv",parse_dates=["date_mensuelle"], index_col=0)

# Initialisation de l'application Dash
octroi = dash.Dash(__name__)

displayed_label={
    "NAME_CONTRACT_TYPE": "TYPE OF CONTRACT",
    "OCCUPATION_TYPE": "OCCUPATION TYPE",
    "NAME_EDUCATION_TYPE" : "EDUCATION LEVEL",
    "CODE_GENDER" : "GENDER",
    "NAME_FAMILY_STATUS" : "MARITAL STATUS",
    
    "CNT_CHILDREN":"NUMBER OF DEPENDENT CHILDREN",
    "CB_NB_CREDIT_CLOSED": "NUMBER OF CLOSED CREDITS",
    "AMT_CREDIT": "CREDIT REQUEST AMOUNT",
    "CB_AMT_CREDIT_SUM": "TOTAL CREDIT AMOUNT FROM CB",
    "AMT_INCOME_TOTAL": "TOTAL ANNUAL INCOME",
    "AMT_GOODS_PRICE" : "GOODS PRICE AMOUNT",

    "CB_DAYS_CREDIT": "PREVIOUS CREDIT DATE",
    "DAYS_BIRTH": "DATE OF BIRTH",
    "DAYS_EMPLOYED" : "ACTUAL JOB EMPLOYMENT DATE",
    "DAYS_REGISTRATION" : "BANK ACCOUNT REGISTRATION DATE",
    "DAYS_LAST_PHONE_CHANGE": "LAST PHONE CHANGE DATE"
}


# Fonction pour créer un dropdown pour les variables catégorielles
def create_categorical_dropdown(id, label):
    return dmc.Select(
        id=id,
        label=dmc.Badge(f"{displayed_label[label]}", variant="outline"),
        data=[{'value': i, 'label': i} for i in df[label].unique().tolist()],
        value=df[label].unique()[0],
        style={"width": 250, "height": 60}
    )

# Fonction pour créer un champ de saisie numérique pour les variables numériques
def create_numeric_input(id, label):
    return dmc.NumberInput(
        id=id,
        label=dmc.Badge(f"{displayed_label[label]}", variant="outline"),
        value=1,
        style={"width": 250, "height": 60}
    )
    
    
def create_date_input(id,label):
    return dmc.DatePicker(
        id=id,
            label=dmc.Badge(f"{displayed_label[label]}", variant="outline"),
            # description="You can also provide a description",
            # minDate=date(2020, 8, 5),
            value=datetime.now().date(),
            maxDate=datetime.now().date(),
            inputFormat="DD-MM-YYYY",
            style={"width": 250, "height": 60},
            
        )

border_color = "#8C8C8C"

style = {
    #"height": 100,
    "border": f"1px solid {border_color}",
    "marginTop": 20,
    #"marginBottom": 20,
    "borderRadius": 10,  # Arrondir les bordures
    "backgroundColor": "white",  # Fond blanc
    
}
    

# Définition du layout de l'application
layout = html.Div(
    children=[
        html.Div(
            dmc.Title(children='CREDIT RISK PLATFORM', order=1, style={'text-align': 'center', 'color': 'slategray'}),
            style={'margin': '20px auto'}
        ),

        dmc.Container (
            [
        dmc.SimpleGrid(
            cols=3,
            spacing="lg",
            children=[
                create_categorical_dropdown("dropdown-NAME_CONTRACT_TYPE", "NAME_CONTRACT_TYPE"),
                create_categorical_dropdown("dropdown-OCCUPATION_TYPE", "OCCUPATION_TYPE"),
                create_categorical_dropdown("dropdown-NAME_EDUCATION_TYPE", "NAME_EDUCATION_TYPE"),
                create_categorical_dropdown("dropdown-CODE_GENDER", "CODE_GENDER"),
                create_categorical_dropdown("dropdown-NAME_FAMILY_STATUS", "NAME_FAMILY_STATUS"),
                
                create_numeric_input("input-CNT_CHILDREN", "CNT_CHILDREN"),
                create_numeric_input("input-CB_NB_CREDIT_CLOSED", "CB_NB_CREDIT_CLOSED"),
                # create_numeric_input("input-CB_DAYS_CREDIT", "CB_DAYS_CREDIT"),
                create_numeric_input("input-AMT_CREDIT", "AMT_CREDIT"),
                create_numeric_input("input-CB_AMT_CREDIT_SUM", "CB_AMT_CREDIT_SUM"),
                create_numeric_input("input-AMT_INCOME_TOTAL", "AMT_INCOME_TOTAL"),
                create_numeric_input("input-AMT_GOODS_PRICE", "AMT_GOODS_PRICE"),
                # create_numeric_input("input-DAYS_BIRTH", "DAYS_BIRTH"),
                # create_numeric_input("input-DAYS_EMPLOYED", "DAYS_EMPLOYED"),
                # create_numeric_input("input-DAYS_REGISTRATION", "DAYS_REGISTRATION"),
                # create_numeric_input("input-DAYS_LAST_PHONE_CHANGE", "DAYS_LAST_PHONE_CHANGE")
                create_date_input("input-CB_DAYS_CREDIT", "CB_DAYS_CREDIT"),
                create_date_input("input-DAYS_BIRTH", "DAYS_BIRTH"),
                create_date_input("input-DAYS_EMPLOYED", "DAYS_EMPLOYED"),
                create_date_input("input-DAYS_REGISTRATION", "DAYS_REGISTRATION"),
                create_date_input("input-DAYS_LAST_PHONE_CHANGE", "DAYS_LAST_PHONE_CHANGE")
            ],
            id='fields-container',
            style={'margin': '0 auto 20px'}
        ), 

        html.Div(
            dmc.Button('Submit request', id='submit-button', n_clicks=0, style={'background-color': 'skyblue', 'padding': '5px 15px', 'font-size': '16px'}),
            style={'text-align': 'center', 'margin': '0 auto 20px'}
        ),

            ]

            ,

            style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}, #size à régler?
        ) ,


        
        
        dmc.Container(
            dmc.Paper(
                dmc.Alert("Credit decision will be displayed here", id="decision-alert", color="gray", withCloseButton=True, style={'display': 'none'}),
                withBorder=True,
                radius="md",
                shadow="xs",
                p="md",
                style={'maxWidth': '600px', 'margin': '40px auto', 'backgroundColor': '#f0f0f0'}
            ),
            style={'padding': '10px'}
        ),
        dcc.Store(id='alert-visible', data={'visible': True}),  # Stockage de l'état de visibilité
        # html.Div(id='output-container')
    ],
    style={'max-width': '800px', 'margin': 'auto'}
)



# Callback pour traiter la soumission des données et afficher les résultats
# @callback(
#         Output('decision-alert', 'children'),
#         Output('decision-alert', 'color'),
#         Output('decision-alert', 'style'),
#         Output('dropdown-NAME_CONTRACT_TYPE', 'value'),
#         Output('dropdown-OCCUPATION_TYPE', 'value'),
#         Output('dropdown-NAME_EDUCATION_TYPE', 'value'),
#         Output('dropdown-CODE_GENDER', 'value'),
#         Output('input-CB_NB_CREDIT_CLOSED', 'value'),
#         Output('input-CB_DAYS_CREDIT', 'value'),
#         Output('input-AMT_CREDIT', 'value'),
#         Output('input-CB_AMT_CREDIT_SUM', 'value'),
#         Output('input-AMT_INCOME_TOTAL', 'value'),
#         Output('input-AMT_GOODS_PRICE', 'value'),
#         Output('input-DAYS_BIRTH', 'value'),
#         Output('input-DAYS_EMPLOYED', 'value'),
#         Output('input-DAYS_REGISTRATION', 'value'),
#         Output('input-DAYS_LAST_PHONE_CHANGE', 'value'),
#         Input('submit-button', 'n_clicks'),
        
#         State('dropdown-NAME_CONTRACT_TYPE', 'value'),
#         State('dropdown-OCCUPATION_TYPE', 'value'),
#         State('dropdown-NAME_EDUCATION_TYPE', 'value'),
#         State('dropdown-CODE_GENDER', 'value'),
#         State('input-CB_NB_CREDIT_CLOSED', 'value'),
#         State('input-CB_DAYS_CREDIT', 'value'),
#         State('input-AMT_CREDIT', 'value'),
#         State('input-CB_AMT_CREDIT_SUM', 'value'),
#         State('input-AMT_INCOME_TOTAL', 'value'),
#         State('input-AMT_GOODS_PRICE', 'value'),
#         State('input-DAYS_BIRTH', 'value'),
#         State('input-DAYS_EMPLOYED', 'value'),
#         State('input-DAYS_REGISTRATION', 'value'),
#         State('input-DAYS_LAST_PHONE_CHANGE', 'value'),
#         prevent_initial_call=True
# )
# def update_decision_output(n_clicks, *values):
#     if ctx.triggered_id == 'submit-button':
#         field_values = {}
#         # Ajout des valeurs des dropdowns pour les variables catégorielles
#         for i, field in enumerate(categorical_vars):
#             field_values[field] = values[i]

#         # Ajout des valeurs des champs de saisie numérique pour les variables numériques
#         for i, field in enumerate(numeric_vars):
#             field_values[field] = values[i + len(categorical_vars)]
        
#         data = DecisionExpertSystem(field_values)
#         data.transform_columns()
#         data.score()
#         decision, decision_color = data.get_decision()
        
#         # Mise à jour du style de l'élément 'decision' avec la couleur obtenue
#         decision_style = {'display': 'block'}
        
#         return decision, decision_color, decision_style, *values