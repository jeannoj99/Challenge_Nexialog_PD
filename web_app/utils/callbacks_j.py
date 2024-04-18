import warnings
warnings.filterwarnings("ignore")
import sys
import os
from dash import Dash, html, dcc,Input, Output, State, callback, dash_table, MATCH, ALL, ctx, no_update
from dash.exceptions import PreventUpdate
import plotly.figure_factory as ff
sys.path.append(os.getcwd()+"//app")
from models.callable import DecisionExpertSystem, Dataset, binomial_test
from utils.utils_from_cecile import subplot_segment_default_rate, show_risk_stability_overtime, plot_feature_importances
import pandas as pd
import numpy as np
from datetime import datetime
from scipy.stats import ks_2samp
import dash_mantine_components as dmc


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
        Output('decision-alert', 'title'),
        Output('decision-alert', 'color'),
        Output('decision-alert', 'message'),
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
        decision_message = "zzzz"
        # Mise à jour du style de l'élément 'decision' avec la couleur obtenue
        decision_style = {'display': 'block'}
        
        if hide == True :
            hide = False
            
        return  decision, decision_color, decision_message, decision_style, hide, *values
    
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

    return stability_table, dmc.Alert(f"{ssi}", title="Indice de stabilité", color="green"), gof_table


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
    ks_text = f"p-value={ks_result.pvalue:.3f}, statistic={ks_result.statistic:.3f}"

    return fig, dmc.Alert(f"{ks_text}",title="Résultat du test de Kolmogorov Smirnov", color="blue")


######################################################################################################################################
##################################################         MACHINE LEARNING           ################################################
######################################################################################################################################


# variables

pd_summary_ml_cash = pd.DataFrame({'Segment': [0, 1, 2, 3, 4, 5, 6],
                                   'LRA': [0.200602, 0.133405, 0.095642, 0.07068, 0.049801, 0.032432, 0.018837],
                                   'MOC_A': [0.002566,0.001639,0.00125,0.001055,0.000976,0.000871,0.000889],
                                   'MOC_C': [0.006757,0.004361,0.003314,0.002846,0.002388,0.002244,0.002452],
                                   'PD': [0.209925, 0.139404, 0.100207, 0.074581, 0.053165, 0.035547, 0.022177]})

pd_summary_ml_revolving = pd.DataFrame({'Segment': [0, 1, 2, 3, 4, 5, 6],
                                        'LRA': [0.292775, 0.169922, 0.116582, 0.08708, 0.05132, 0.033209, 0.011151],
                                        'MOC_A': [0.022545,0.010349,0.00638,0.004107,0.002763,0.002175,0.001705],
                                        'MOC_C': [0.090857,0.027752,0.016639,0.011231,0.007735,0.005281,0.003862],
                                        'PD': [0.406178, 0.208023, 0.139601, 0.102417, 0.061817, 0.040665, 0.016718]})


pd_summaries_ml ={
    "Cash loans": pd_summary_ml_cash,
    "Revolving loans": pd_summary_ml_revolving
}

ginis_ml_models = {
    "Cash loans":0.3449805416329841,
    "Revolving loans": 0.38072400582710175
}

models_challenger = {}

with open("../models/challenger_model_cash_loans.pkl","rb") as f:
    models_challenger["Cash loans"] = pickle.load(f)

with open("../models/challenger_model_revolving_loans.pkl","rb") as f:
    models_challenger["Revolving loans"] = pickle.load(f)


datas_challenger = {
    "Cash loans":{
        "train":pd.read_csv("../data/synthetic_data_test_ml_models_cash.csv"),
        "test":pd.read_csv("../data/synthetic_data_test_ml_models_cash.csv")
    },
    "Revolving loans":{
        "train":pd.read_csv("../data/synthetic_data_test_ml_models_revolving.csv"),
        "test":pd.read_csv("../data/synthetic_data_test_ml_models_revolving.csv")
    }
}

shap_graphs_src = {
    "Cash loans" : "/assets/shap_summary_plot_cash.png",
    "Revolving loans": "/assets/shap_summary_plot_revolving.png"
}




# callbacks
@callback(
    [Output('feature-importances', 'figure'),
     Output('shap-image', 'src'),
     Output('gini-score-challenger', 'children')],
      [Input('model-choice', 'value')]
)
def update_interpretable_ml(model_choice):
    
    # Generate figures
    fig_importances = plot_feature_importances(models_challenger[model_choice])
    
    shap_src = shap_graphs_src[model_choice]
    gini_display = f"Gini Score : {ginis_ml_models[model_choice]:.3f}"
    
    return fig_importances, shap_src, gini_display

# Callbacks to update graphs and table based on model choice
@callback(
    [Output('risk-stability-overtime', 'figure'),
     Output('density-plot-challenger', 'figure'),
     Output('segment-challenger', 'figure'),
     Output('pd-summary', 'data')],
    [Input('model-choice', 'value')]
)
def update_risk_quantification_ml(model_choice):
    # Example calculations (to replace with actual model methods)
    feature_importances = pd.DataFrame({
        'Feature': ['Feature1', 'Feature2', 'Feature3'],
        'Importance': np.random.rand(3)
    })
    shap_values = pd.DataFrame({
        'Feature': ['Feature1', 'Feature2', 'Feature3'],
        'SHAP': np.random.randn(3)
    })
   
    
    
    data0 = datas_challenger[model_choice]["test"]['Note'][datas_challenger[model_choice]["test"]['TARGET'] == 0]
    data1 = datas_challenger[model_choice]["test"]['Note'][datas_challenger[model_choice]["test"]['TARGET'] == 1]
    fig_density = ff.create_distplot(
         [data0, 
          data1],
         group_labels=['Target = 0', 'Target = 1'],
         colors=['blue', 'red'], 
         show_hist=False,
         show_rug=False
     )
    
    fig_density.update_layout(
         title=f'Distribution de TARGET en fonction de la Note sur {model_choice}',
         xaxis_title='Note',
         yaxis_title='Fréquence',
         xaxis=dict(range=[min(data0.min(), data1.min()), max(data0.max(), data1.max())])
     )
    
    risk_fig = show_risk_stability_overtime(datas_challenger[model_choice]["test"], "Segment")
    segment_fig = subplot_segment_default_rate(datas_challenger[model_choice]["test"])
    
    # Update PD summary table
    pd_summary_data = pd_summaries_ml[model_choice].to_dict('records')

    # Gini score display
    gini_display = f"Gini Score: {ginis_ml_models[model_choice]:.3f}"

    return  risk_fig, fig_density, segment_fig, pd_summary_data


@callback(
    Output("modal-centered", "opened"),
    Input("modal-centered-button", "n_clicks"),
    State("modal-centered", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    return not opened

@callback(
    Output("output-modal", "children"),  # Modifier le contenu du modal
    Input("model-choice", "value"),  # Valeur sélectionnée dans le dropdown
    prevent_initial_call=False
)
def update_modal_content(selected_value):
    # Vous pouvez définir différentes chaînes de texte ou tout autre contenu selon les valeurs sélectionnées
    if selected_value == 'Cash loans':
        text = """
Type : Extreme Gradient Boosting (XGBOOST) \n
OverSampling : Oui \n
params={"objective" : "binary:logistic", \n
"n_estimators": 1919, \n
    "max_depth": 3,
    "learning_rate": 0.0859629599254648,
    "subsample": 0.5551507002697985,
    "colsample_bytree": 0.5259021305964645,
    "gamma": 4.73594274760292,
    "reg_alpha": 2.0479518991587744,
    "reg_lambda": 1.6104339752926782,
    "min_child_weight": 9.552310062227694}
                """
        modal_content = dmc.Text(f"{text}")
    elif selected_value == 'Revolving loans':
        text = """ Type : Extreme Gradient Boosting (XGBOOST)
OverSampling : Non
params={ 'objective' : 'binary:logistic',
'n_estimators': 3346,
 'max_depth': 14,
 'learning_rate': 0.09682173875579893,
 'subsample': 0.9925031110142413,
 'colsample_bytree': 0.5203989753044218,
 'gamma': 1.6414640218829,
 'reg_alpha': 0.6325232901507183,
 'reg_lambda': 0.28657378226912456,
 'min_child_weight': 19.655206808761505,
 'random_state': 7607}
"""
        modal_content = dmc.Text(f"{text}")
    else:
        modal_content = dmc.Text("Aucun contenu spécifique sélectionné.")
    
    return modal_content  # Retourne le contenu du modal en tant que liste
