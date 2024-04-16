# contient toutes les fonctions callbacks utilisées
from dash import Dash, html, dcc,Input, Output, callback, State , dash_table, MATCH, ALL, ctx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.utils import show_risk_stability_graph, show_volume_stability_overtime
from utils.preprocessing import data_for_binary, data_for_lc, data_for_hc_nd, data_for_hc_d_train
from utils.preprocessing import low_category_non_stable_vars
from utils.preprocessing import binary_vars_for_app,lc_vars_for_app, hc_vars_for_app_nd, hc_vars_for_app_d
from utils.utils import cramers_v_target,cramers_v_cols, kruskal_wallis_test, calculate_information_value, calculate_chi_stat_target,calculate_chi_stat_cols
from utils.preprocessing import discretised_cols, catego_a_utiliser,tested_numerical_variables
import dash_mantine_components as dmc

# variables Tous types

@callback(
    Output('switch_var_d_nd', 'children'),
    [Input('col_for_graphs', 'value')]
)
def display_switch_var_discr(variable):
    if variable in ['NAME_EDUCATION_TYPE', 'OCCUPATION_TYPE']:
        return dmc.Switch(id='switch', checked=False, label='Afficher la version discrétisée')
    else:
        return dmc.Switch(id='switch', checked=False, label='Afficher la version discrétisée', disabled=True)

@callback(Output('listevide','value'),
        Input('switch','checked'))
def que_dalle(rien):
    return ""

@callback(
    Output('graph_risk_stability_overtime', 'figure'),
    [Input('col_for_graphs', 'value'),Input('switch','checked')]
)
def risk_stability_graph(colname,checked):
    if colname in binary_vars_for_app:
        return show_risk_stability_graph(data_for_binary, colname)
    elif colname in lc_vars_for_app:
        return show_risk_stability_graph(data_for_lc,colname)
    elif colname in ['NAME_EDUCATION_TYPE', 'OCCUPATION_TYPE']:
        if checked: 
            return show_risk_stability_graph(data_for_hc_d_train, colname)
        else: 
            return show_risk_stability_graph(data_for_hc_nd,colname)
    else: # colname in catego_a_utiliser
        return show_risk_stability_graph(data_for_hc_d_train,colname)


@callback(
    Output('graph_volume_stability_overtime', 'figure'),
    [Input('col_for_graphs', 'value'),Input('switch','checked')]
)
def volume_stability_graph(colname,checked):
    if colname in binary_vars_for_app:
        return show_volume_stability_overtime(data_for_binary, colname)
    elif colname in lc_vars_for_app:
        return show_volume_stability_overtime(data_for_lc,colname)
    elif colname in ['NAME_EDUCATION_TYPE', 'OCCUPATION_TYPE']:
        if checked: 
            return show_volume_stability_overtime(data_for_hc_d_train, colname)
        else: 
            return show_volume_stability_overtime(data_for_hc_nd,colname)
    else: # colname in catego_a_utiliser
        return show_volume_stability_overtime(data_for_hc_d_train,colname)

# Comparateur de variables

@callback(
    [Output('choice_var_1', 'children'),
     Output('choice_var_2', 'children')],
    [Input('catego_ou_numerique', 'value'),
     Input('target_selected_checkbox', 'checked')]
)
def update_variable_choices(cat_or_num, target_checked):
    options_numerical = [{'label': i, 'value': i} for i in sorted(list(set(discretised_cols + tested_numerical_variables)))]
    options_categorical = [{'label': i, 'value': i} for i in sorted(list(set(catego_a_utiliser + discretised_cols)))]

    select_1 = dmc.Select(
        id='var_1_compare',
        data=options_numerical if cat_or_num == 'numerical' else options_categorical,
        value=None,
        label='Select a 1st variable'
    )

    select_2 = dmc.Select(
        id='var_2_compare',
        data=options_numerical if cat_or_num == 'numerical' else options_categorical,
        value=None,
        label='Select a 2nd variable',
        disabled=target_checked
    )

    if target_checked:
        select_2 = dmc.Select(
            id='var_2_compare',
            data=[{'label': 'TARGET', 'value': 'TARGET'}],
            value='TARGET',
            disabled=True
        )
    
    return select_1, select_2


@callback(
    Output('stats_display', 'children'),
    [Input('var_1_compare', 'value'),
     Input('var_2_compare', 'value'),
     Input('catego_ou_numerique', 'value'),
     Input('target_selected_checkbox', 'checked')]
)
def compute_stats(var1, var2, cat_or_num, checked_target):
    if checked_target:
        if cat_or_num == 'categorical': # catego ~Y 
            chi = calculate_chi_stat_target(data_for_hc_nd, var1)
            iv = calculate_information_value(data_for_hc_d_train, var1)
            cramer = cramers_v_target(data_for_hc_d_train, var1)
            return html.Div([
                html.P(f"Chi-Square: {chi}"),
                html.P(f"Information Value: {iv}"),
                html.P(f"Cramer's V: {cramer}")
            ])
        elif cat_or_num == 'numerical': # numérique ~Y 
            kruskal_result = kruskal_wallis_test(data_for_hc_nd, var1)
            return html.P(f"Kruskal-Wallis Test Result: {kruskal_result}")
    else:
        if cat_or_num == 'numerical': # num ~num
            correlation = data_for_hc_nd[[var1, var2]].corr().iloc[0, 1]
            return html.P(f"Corrélation entre {var1} et {var2} est de : {correlation}")
        elif cat_or_num == 'categorical': # cat ~ cat
            chi = calculate_chi_stat_cols(data_for_hc_d_train, var1, var2)
            cramer = cramers_v_cols(data_for_hc_d_train, var1, var2)
            return html.Div([
                html.P(f"Chi-Square: {chi}"),
                html.P(f"Cramer's V: {cramer}")
            ])
























    
# Jynaldo
from models.callable import DecisionExpertSystem

fields = ["NAME_CONTRACT_TYPE","OCCUPATION_TYPE", "NAME_EDUCATION_TYPE" ,"CODE_GENDER", "CB_NB_CREDIT_CLOSED", "CB_DAYS_CREDIT", "AMT_CREDIT",
          "CB_AMT_CREDIT_SUM", "AMT_INCOME_TOTAL", "AMT_GOODS_PRICE", "DAYS_BIRTH", "DAYS_EMPLOYED", "DAYS_REGISTRATION","DAYS_LAST_PHONE_CHANGE"]

# Liste des variables catégorielles et numériques
categorical_vars = ["NAME_CONTRACT_TYPE", "OCCUPATION_TYPE", "NAME_EDUCATION_TYPE","CODE_GENDER"]
numeric_vars = ["CB_NB_CREDIT_CLOSED", "CB_DAYS_CREDIT", "AMT_CREDIT",
                "CB_AMT_CREDIT_SUM", "AMT_INCOME_TOTAL", "AMT_GOODS_PRICE", "DAYS_BIRTH", "DAYS_EMPLOYED", "DAYS_REGISTRATION","DAYS_LAST_PHONE_CHANGE"]


@callback(
        Output('decision', 'children'),
        Output('decision','style'),
        Output('dropdown-NAME_CONTRACT_TYPE', 'value'),
        Output('dropdown-OCCUPATION_TYPE', 'value'),
        Output('dropdown-NAME_EDUCATION_TYPE', 'value'),
        Output('dropdown-CODE_GENDER', 'value'),
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
        State('dropdown-CODE_GENDER', 'value'),
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
def update_decision_output(n_clicks, *values):
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