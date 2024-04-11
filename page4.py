import dash
from dash import Input, Output, State, html, dcc, dash_table, MATCH, ALL, ctx
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, time, timedelta
import time as time_pck
import os
import dash_daq as daq
import pickle
import random

df=pd.read_csv("/Challenge_Nexialog_PD/data/application_train_vf.csv",parse_dates=["date_mensuelle"], index_col=0)

from app import app

def create_dropdown(id,label, options_list):
    return dmc.Select(
        id = id,
        label = label,
        data = [{'value':i, 'label': i} for i in options_list],
        value = options_list[0]
    )

# Liste des champs spécifiés
fields = ["NAME_CONTRACT_TYPE","OCCUPATION_TYPE", "NAME_EDUCATION_TYPE" , "CB_NB_CREDIT_CLOSED",
          "CB_DAYS_CREDIT", "AMT_CREDIT","CB_AMT_CREDIT_SUM","AMT_INCOME_TOTAL",
          "AMT_GOODS_PRICE","DAYS_BIRTH", "DAYS_EMPLOYED", "DAYS_REGISTRATION" ]

layout = html.Div(
    children=[
        dmc.Title(children = 'Credit Grantings', order = 3, style = {'font-family':'IntegralCF-ExtraBold', 'text-align':'center', 'color' :'slategray'}),
        dmc.Modal(
            id = 'info-ml',
            size = '75%',
            overflow="inside",
            title = [dmc.Title('Model Info', order = 3)],
            children = [
                dmc.Divider(label = 'AUC Curves and Model Performance', labelPosition = 'center'),
                dmc.SimpleGrid(
                    cols = 2,
                    children = [
                        dmc.Title('AUC - Original Data', order = 4, style = {'text-align':'center'}),
                        dmc.Title('AUC- Balanced Data', order = 4, style = {'text-align':'center'}),
                        html.Img(
                            src = app.get_asset_url('chr_train.png'),
                            style = {'width':'25vw','justify-self':'center'}, 
                        ),
                        html.Img(
                            src = app.get_asset_url('chr_train.png'),
                            style = {'width':'25vw','justify-self':'center'}
                        ),
                        dmc.Text('We had a Yes-No ratio of approx. 4:1. This was the model generated with that data.', style= {'justify-self':'center'}),
                        dmc.Text('I balanced the Yes-No ratio to 1:1 with SMOTE. This is the new model. It performs better', style= {'justify-self':'center'}),
                    ]
                ),
                dmc.Divider(label = 'Confusion Matrix', labelPosition='center'),
                dmc.Stack(
                    align = 'center',
                    children = [
                        dmc.Title('Random Forest Confusion Matrix', order = 4, style = {'text-align':'center'}),
                        html.Img(
                            src = app.get_asset_url('chr_train.png'),
                            style = {'width':'25vw','justify-self':'center'}, 
                        ),
                        dmc.Text('I choose the random forest classifier model from above. This is the confusion matrix for said model.', style = {'justify-self':'center'})
                    ]
                )
            ]
        ),
        dmc.Paper(
            m = 'sm',
            pb = 'sm',
            shadow = 'md',
            withBorder = True,
            radius = 'md',
            children = [
                dmc.Stack(
                    align = 'center',
                    children = [
                        dmc.Divider(label = 'Based off Random Forest Classifier', labelPosition='center'),
                        dmc.Title('Create a customer below', order = 4, style = {'text-align':'center'}),
                        dmc.Button( id = 'randomize', children = 'Randomize a Customer', size = 'sm'),
                        dmc.SimpleGrid(
                            cols = 4,
                            children = [
                                *[create_dropdown(f'select-{field.lower().replace(" ", "-")}', field, df[field].unique()) for field in fields],
                                dmc.NumberInput(id = 'monthly-charges', label = 'Monthly Charges ($)', value = 50),
                                dmc.NumberInput(id = 'total-charges', label = 'Total Charges ($ Tenure x Monthly Charges)', value = 0, disabled=True)
                            ]
                        ),
                        dmc.Button(id = 'submit-customer', children = 'Submit'),
                        dmc.Group(spacing = 'sm', children = [dmc.Title('Predicted Churn Probability', order = 3),dmc.ActionIcon(id = 'more-info', color = 'blue', size = 'lg', children = [DashIconify(icon = 'material-symbols:info', width = 24)])]),
                        dmc.Text(size = 'xs', color = 'dimmed', children = 'We want low % of churn!'),
                        dmc.Progress(id = 'probability', value=37.8, class_name = 'progressbar', color = 'green', label = '37.8%', size = 'xl')
                    ]
                )
            ]
        )
    ]
)

@app.callback(Output('total-charges', 'value'),
                Input('input-tenure','value'),
                Input('monthly-charges', 'value'))
def update_test(tenure, mc):
    return tenure * mc


@app.callback(Output('probability', 'label'),
                Output('probability', 'value'),
                Output('probability', 'color'),
                Output({f'select-{field.lower().replace(" ", "-")}' for field in fields}, 'value'),
                Input('submit-customer', 'n_clicks'),
                Input('randomize', 'n_clicks'),
                State({f'select-{field.lower().replace(" ", "-")}' for field in fields}, 'value'),
                State('monthly-charges', 'value'),
                State('total-charges', 'value'),
                prevent_inital_update = True)
def update_prob(n, randomize, field_values, monthlycharges, totalcharges):
    if ctx.triggered_id == 'submit-customer' or ctx.triggered_id is None:
        input_data = [[*field_values, monthlycharges, totalcharges]]
        input_df = pd.DataFrame(data=input_data, columns=[*fields, 'MonthlyCharges', 'TotalCharges'])

        # Supprimer les colonnes non nécessaires et prétraiter les données
        custs = input_df.drop(columns=['Churn', 'customerID'])
        custs['TotalCharges'] = custs['TotalCharges'].replace(' ', 0).astype(float)

        # Charger le modèle
        with open('rf_model.pickle', 'rb') as f:
            rf = pickle.load(f)

        # Prédictions
        vals = rf.predict_proba(custs.tail(1))[0][1] * 100
        if vals > 50:
            color = 'red'
        elif vals < 50:
            color = 'green'
        else:
            color = 'yellow'

        probby = '{:,.1f}%'.format(vals)

        return probby, vals, color, dash.no_update
    elif ctx.triggered_id == 'randomize':
        # Générer des valeurs aléatoires pour les champs spécifiés
        field_values = []
        for field in fields:
            choose_from = df[field].unique()
            length_of_choose = len(choose_from)
            rng_value = random.randint(0, length_of_choose - 1)
            field_values.append(choose_from[rng_value])

        # Calculer le total des charges
        tenure = random.randint(1, 60)
        monthlycharges = random.randint(20, 200)
        totalcharges = tenure * monthlycharges

        return '', 0, '', field_values, monthlycharges, totalcharges


@app.callback(Output('info-ml', 'opened'),
                Input('more-info', 'n_clicks'),
                State('info-ml', 'opened'))
def open_modal(n, opened):
    if ctx.triggered_id is not None:
        return not opened
    else:
        return False

