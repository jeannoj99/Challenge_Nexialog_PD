import warnings
warnings.filterwarnings("ignore")
import sys
import os
from dash import Dash, html, dcc,Input, Output, State, callback, dash_table, MATCH, ALL, ctx, no_update
from dash.exceptions import PreventUpdate
import plotly.figure_factory as ff
sys.path.append(os.getcwd()+"/..")
from models.callable import DecisionExpertSystem, Dataset, binomial_test
import pandas as pd
import numpy as np
from datetime import datetime
from scipy.stats import ks_2samp


features_by_contract = {
    'Cash loans': ["OCCUPATION_TYPE", "NAME_EDUCATION_TYPE"  , "AMT_CREDIT_NORM" , "BORROWER_AGE" , "BORROWER_SENIORITY" , "CB_NB_CREDIT_CLOSED", "CB_DAYS_CREDIT","Segment"],
    'Revolving loans': ["AMT_GOODS_PRICE", "OCCUPATION_TYPE", "NAME_EDUCATION_TYPE" , "DAYS_LAST_PHONE_CHANGE" , "BORROWER_SENIORITY" , "CB_NB_CREDIT_CLOSED", "CB_DAYS_CREDIT","Segment"]
}

fields = ["NAME_CONTRACT_TYPE","OCCUPATION_TYPE", "NAME_EDUCATION_TYPE" ,"CODE_GENDER", "CB_NB_CREDIT_CLOSED", "CB_DAYS_CREDIT", "AMT_CREDIT",
          "CB_AMT_CREDIT_SUM", "AMT_INCOME_TOTAL", "AMT_GOODS_PRICE", "DAYS_BIRTH", "DAYS_EMPLOYED", "DAYS_REGISTRATION","DAYS_LAST_PHONE_CHANGE","NAME_FAMILY_STATUS"]

# Liste des variables catégorielles et numériques
categorical_vars = ["NAME_CONTRACT_TYPE", "OCCUPATION_TYPE", "NAME_EDUCATION_TYPE","CODE_GENDER","NAME_FAMILY_STATUS"]
numeric_vars = ["CNT_CHILDREN", "CB_NB_CREDIT_CLOSED", "AMT_CREDIT",
                "CB_AMT_CREDIT_SUM", "AMT_INCOME_TOTAL", "AMT_GOODS_PRICE", ]
date_vars = ["DAYS_BIRTH", "DAYS_EMPLOYED", "DAYS_REGISTRATION","CB_DAYS_CREDIT", "DAYS_LAST_PHONE_CHANGE"]

@callback(
        Output('decision-alert', 'children'),
        Output('decision-alert', 'color'),
        Output('decision-alert', 'style'),
        Output("decision-alert", "hide"),
        Output('dropdown-NAME_CONTRACT_TYPE', 'value'),
        Output('dropdown-OCCUPATION_TYPE', 'value'),
        Output('dropdown-NAME_EDUCATION_TYPE', 'value'),
        Output('dropdown-CODE_GENDER', 'value'),
        Output('dropdown-NAME_FAMILY_STATUS', 'value'),
        Output('input-CB_NB_CREDIT_CLOSED', 'value'),
        Output('input-CNT_CHILDREN', 'value'),
        Output('input-AMT_CREDIT', 'value'),
        Output('input-CB_AMT_CREDIT_SUM', 'value'),
        Output('input-AMT_INCOME_TOTAL', 'value'),
        Output('input-AMT_GOODS_PRICE', 'value'),
        Output('input-DAYS_BIRTH', 'value'),
        Output('input-DAYS_EMPLOYED', 'value'),
        Output('input-DAYS_REGISTRATION', 'value'),
        Output('input-CB_DAYS_CREDIT', 'value'),
        Output('input-DAYS_LAST_PHONE_CHANGE', 'value'),
        Input('submit-button', 'n_clicks'),
        
        State("decision-alert", "hide"),
        State('dropdown-NAME_CONTRACT_TYPE', 'value'),
        State('dropdown-OCCUPATION_TYPE', 'value'),
        State('dropdown-NAME_EDUCATION_TYPE', 'value'),
        State('dropdown-CODE_GENDER', 'value'),
        State('dropdown-NAME_FAMILY_STATUS', 'value'),
        State('input-CNT_CHILDREN', 'value'),
        State('input-CB_NB_CREDIT_CLOSED', 'value'),
        State('input-AMT_CREDIT', 'value'),
        State('input-CB_AMT_CREDIT_SUM', 'value'),
        State('input-AMT_INCOME_TOTAL', 'value'),
        State('input-AMT_GOODS_PRICE', 'value'),
        State('input-DAYS_BIRTH', 'value'),
        State('input-DAYS_EMPLOYED', 'value'),
        State('input-DAYS_REGISTRATION', 'value'),
        State('input-CB_DAYS_CREDIT', 'value'),
        State('input-DAYS_LAST_PHONE_CHANGE', 'value'),
        prevent_initial_call=True
)
def update_decision_output(n_clicks, hide, *values):
    if ctx.triggered_id == 'submit-button':
        field_values = {}
        # Ajout des valeurs des dropdowns pour les variables catégorielles
        for i, field in enumerate(categorical_vars):
            field_values[field] = values[i]

        # Ajout des valeurs des champs de saisie numérique pour les variables numériques
        for i, field in enumerate(numeric_vars):
            field_values[field] = values[i + len(categorical_vars)]
            
        for i, field in enumerate(date_vars):
            field_values[field] = (datetime.strptime(values[i + len(categorical_vars+numeric_vars)],"%Y-%m-%d").date() - datetime.now().date()).days
        
        data = DecisionExpertSystem(field_values)
        data.transform_columns()
        data.score()
        decision, decision_color = data.get_decision()
        
        # Mise à jour du style de l'élément 'decision' avec la couleur obtenue
        decision_style = {'display': 'block'}
        
        if hide == True :
            hide = False
            
        return  decision, decision_color, decision_style, hide, *values
    
#######################################################################################################################################
############################################################### BACKTESTING ###########################################################

data=pd.read_csv("../data/application_train_vf.csv",parse_dates=["date_mensuelle"], index_col=0)
credit_bureau_data=pd.read_csv("../data/cb_findings.csv", index_col=0)
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
with open("./utils/Cash/summary_pd_gof.pkl","rb") as f:
    gof_summary_table['Cash loans']=pickle.load(f)

with open("./utils/Revolving/summary_pd_gof.pkl","rb") as f:
    gof_summary_table['Revolving loans']=pickle.load(f)

def calculate_contribution_to_is(x):
    return (x["proportion_reference"] - x["proportion_backtest"])*np.log(x["proportion_reference"] / x["proportion_backtest"])

def system_stability_index(reference,backtest, variable):
    dist_ref = (reference[variable].astype(str)).value_counts(normalize=True).reset_index()
    dist_back = (backtest[variable].astype(str)).value_counts(normalize=True).reset_index()
    dist_all = dist_ref.merge(dist_back, how="outer", on=variable, suffixes=("_reference","_backtest"))
    dist_all["contribution"]=dist_all.apply(calculate_contribution_to_is, axis=1)
    return dist_all, dist_all["contribution"].sum()




# callbacks
@callback(
    Output('backtesting-feature-dropdown', 'options'),
    Input('backtesting-contract-type-dropdown', 'value')
)
def update_backtesting_features_dropdown(selected_contract):
    return [{'label': feature, 'value': feature} for feature in features_by_contract[selected_contract]]



@callback(
    [Output('stability-test-output', 'children'),
     Output('system-stability-index-output', 'children'),
     Output('second-table-output', 'children')],
    [Input('backtesting-contract-type-dropdown', 'value'),
     Input('backtesting-feature-dropdown', 'value')]
)
def update_tables_and_tests(selected_contract, selected_feature):
    if selected_feature not in features_by_contract[selected_contract]:
        return no_update

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
    style_table={
        'overflowX': 'auto'  # Permet le défilement horizontal si le tableau est trop large
    },
    style_cell={
        'minWidth': 'fit-content',  # Assure que la largeur minimale est celle du contenu
        'width': 'fit-content',  # Fixe la largeur de la cellule à celle de son contenu
        'maxWidth': 'fit-content',  # La largeur maximale est également celle du contenu
        'whiteSpace': 'normal'  # Permet aux cellules d'avoir un contenu sur plusieurs lignes
    },
    style_header={  # Styles optionnels pour l'en-tête pour le distinguer
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    }
)

    return stability_table, ssi, gof_table


@callback(
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
    
    fig.update_layout(
        title_text='Distribution des notes sur la période de référence et de backtesting',  # Titre du graphique
        xaxis_title='Notes',  # Titre de l'axe X
        yaxis_title='Densité',  # Titre de l'axe Y
        template='plotly_white',  # Utilisez un template de fond clair pour une meilleure lisibilité
        legend_title='Période',  # Titre pour la légende
        legend=dict(  # Personnalisation de la position et du style de la légende
            x=1,
            xanchor='auto',
            y=1,
            yanchor='auto'
        )
    )
    
    ks_result = ks_2samp((datas_backtesting[selected_contract]["reference"]).data['Note'],
                         (datas_backtesting[selected_contract]["backtest"]).data['Note'], alternative='two-sided')
    ks_text = f"KS-test result: p-value={ks_result.pvalue:.3f}, statistic={ks_result.statistic:.3f}"

    return fig, ks_text



