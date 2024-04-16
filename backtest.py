import warnings
warnings.filterwarnings("ignore")
import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
from models.callable import DecisionExpertSystem, Dataset, binomial_test

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

features_by_contract = {
    'Cash loans': ["OCCUPATION_TYPE", "NAME_EDUCATION_TYPE"  , "AMT_CREDIT_NORM" , "BORROWER_AGE" , "BORROWER_SENIORITY" , "CB_NB_CREDIT_CLOSED", "CB_DAYS_CREDIT","Segment"],
    'Revolving loans': ["AMT_GOODS_PRICE", "OCCUPATION_TYPE", "NAME_EDUCATION_TYPE" , "DAYS_LAST_PHONE_CHANGE" , "BORROWER_SENIORITY" , "CB_NB_CREDIT_CLOSED", "CB_DAYS_CREDIT","Segment"]
}

all_features=list(set(features_by_contract['Cash loans']+features_by_contract['Revolving loans'])) + ["Note","TARGET"]

import plotly.graph_objects as go

def create_distribution_graph(reference_data, backtest_data):
    # Création d'une figure
    fig = go.Figure()

    # Ajouter la courbe KDE pour les données de référence
    fig.add_trace(go.Histogram(
        x=reference_data,
        histnorm='probability density',  # Normalise l'histogramme pour obtenir une estimation de la densité
        name='Reference',
        opacity=0,
        marker_color='blue'
    ))

    # Ajouter la courbe KDE pour les données de backtest
    fig.add_trace(go.Histogram(
        x=backtest_data,
        histnorm='probability density',  # Normalise l'histogramme pour obtenir une estimation de la densité
        name='Backtesting',
        opacity=0,
        marker_color='red'
    ))

    # Mise à jour des paramètres du layout
    fig.update_layout(
        title_text='Distribution Comparison',
        xaxis_title_text='Note',
        yaxis_title_text='Density',
        barmode='overlay'  # Les histogrammes sont superposés
    )

    return fig

# Exemple d'utilisation



app.layout = html.Div([
    html.H3('BACKTESTING', style={'text-align': 'center', 'margin-bottom': '20px'}),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Label('Select Contract Type:', style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='backtesting-contract-type-dropdown',
                    options=[{'label': k, 'value': k} for k in features_by_contract.keys()],
                    value='Cash loans',
                    clearable=False
                ),
                html.Label('Select Variables:', style={'font-weight': 'bold', 'margin-top': '20px'}),
                dcc.Dropdown(
                    id='backtesting-feature-dropdown',
                    clearable=False
                ),
            ], width=6)
        ], justify='center', style={'margin-bottom': '20px'}),
        dbc.Row([
            dbc.Col([
                html.H5("Variables stability tests"),
                html.Div(id='stability-test-output')
            ], style={'margin-bottom': '20px'})
        ], justify='center'),
        dbc.Row([
            dbc.Col([
                html.Div(id='system-stability-index-output')
            ], style={'margin-bottom': '20px'})
        ], justify='center'),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='contract-type-graph'),
                html.Div(id='kolmogorov-smirnov-result')
            ], style={'margin-bottom': '20px'})
        ], justify='center'),
        dbc.Row([
            dbc.Col([
                html.H5('PD Goodness-of-fit Test on CHRs'),
                html.Div(id='second-table-output')
            ], style={'margin-bottom': '20px'})
        ], justify='center')
    ], fluid=True, style={'padding': '0 15%'})
], style={'max-width': '1200px', 'margin': 'auto'})


@app.callback(
    Output('backtesting-feature-dropdown', 'options'),
    Input('backtesting-contract-type-dropdown', 'value')
)
def update_backtesting_features_dropdown(selected_contract):
    return [{'label': feature, 'value': feature} for feature in features_by_contract[selected_contract]]

data=pd.read_csv("data/application_train_vf.csv",parse_dates=["date_mensuelle"], index_col=0)
credit_bureau_data=pd.read_csv("data/cb_findings.csv", index_col=0)
data=data.merge(credit_bureau_data, left_on="SK_ID_CURR", right_on="CB_SK_ID_CURR")

data["date_annee"]=data["date_mensuelle"].dt.year
data_reference = data[data["date_annee"] < 2020]
data_backtest = data[data["date_annee"] == 2020]

# CASH LOANS DATA
dataset_backtest_cash = Dataset(data_backtest, "Cash loans")
dataset_backtest_cash.transform_columns()
dataset_backtest_cash.get_chr()

dataset_reference_cash = Dataset(data_reference, "Cash loans")
dataset_reference_cash.transform_columns()
dataset_reference_cash.get_chr()

# REVOLVING DATA
dataset_reference_revolving = Dataset(data_reference, "Revolving loans")
dataset_reference_revolving.transform_columns()
dataset_reference_revolving.get_chr()

dataset_backtest_revolving = Dataset(data_backtest, "Revolving loans")
dataset_backtest_revolving.transform_columns()
dataset_backtest_revolving.get_chr()

datas_backtesting={
    "Cash loans":{
        "reference":dataset_reference_cash,
        "backtest":dataset_backtest_cash
    },
    "Revolving loans":{
        "reference":dataset_reference_revolving,
        "backtest":dataset_backtest_revolving
    }
        
}

gof_summary_table = {}
import pickle
with open("web_app/utils/Cash/summary_pd_gof.pkl","rb") as f:
    gof_summary_table['Cash loans']=pickle.load(f)

with open("web_app/utils/Revolving/summary_pd_gof.pkl","rb") as f:
    gof_summary_table['Revolving loans']=pickle.load(f)

def calculate_contribution_to_is(x):
    return (x["proportion_reference"] - x["proportion_backtest"])*np.log(x["proportion_reference"] / x["proportion_backtest"])

def system_stability_index(reference,backtest, variable):
    dist_ref = (reference[variable].astype(str)).value_counts(normalize=True).reset_index()
    dist_back = (backtest[variable].astype(str)).value_counts(normalize=True).reset_index()
    dist_all = dist_ref.merge(dist_back, how="outer", on=variable, suffixes=("_reference","_backtest"))
    dist_all["contribution"]=dist_all.apply(calculate_contribution_to_is, axis=1)
    
    float_cols = dist_all.select_dtypes(include=['float64']).columns
    dist_all[float_cols] = dist_all[float_cols].round(6)
    return dist_all, dist_all["contribution"].sum()


@app.callback(
    [Output('stability-test-output', 'children'),
     Output('system-stability-index-output', 'children'),
     Output('second-table-output', 'children')],
    [Input('backtesting-contract-type-dropdown', 'value'),
     Input('backtesting-feature-dropdown', 'value')]
)
def update_tables_and_tests(selected_contract, selected_feature):
    if selected_feature not in features_by_contract[selected_contract]:
        return dash.no_update

    sol = system_stability_index((datas_backtesting[selected_contract]["reference"]).data,
                                 (datas_backtesting[selected_contract]["backtest"]).data, selected_feature) if selected_feature else (pd.DataFrame(), None)
    df = sol[0]
    ssi = sol[1]
    stability_table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={'height': 'auto', 'minWidth': '180px', 'width': '180px', 'maxWidth': '180px', 'whiteSpace': 'normal'}
    )

    gof_table = dash_table.DataTable(
        data=gof_summary_table[selected_contract].to_dict('records'),
        columns=[{'name': i, 'id': i} for i in gof_summary_table[selected_contract].columns],
        style_table={'overflowX': 'auto'},
        style_cell={'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'}
    )

    return stability_table, ssi, gof_table


@app.callback(
    [Output('contract-type-graph', 'figure'),
     Output('kolmogorov-smirnov-result', 'children')],
    Input('backtesting-contract-type-dropdown', 'value'),
)
def update_graph_kolmogorov_smirnov(selected_contract):
    # Utilisation de l'alternative Plotly Graph Objects pour le graphique
    fig = ff.create_distplot([(datas_backtesting[selected_contract]["reference"]).data['Note'],
     (datas_backtesting[selected_contract]["backtest"]).data['Note']],
    group_labels=['Reference', 'Backtesting'],
         colors=['blue', 'red'], 
         show_hist=False,
         show_rug=False
     )
    ks_result = ks_2samp((datas_backtesting[selected_contract]["reference"]).data['Note'],
                         (datas_backtesting[selected_contract]["backtest"]).data['Note'], alternative='two-sided')
    ks_text = f"KS-test result: p-value={ks_result.pvalue:.3f}, statistic={ks_result.statistic:.3f}"

    return fig, ks_text


if __name__ == '__main__':
    app.run_server(debug=True)
