# contient toutes les fonctions callbacks utilisées
from dash import Dash, html, dcc,Input, Output, callback, State , dash_table, MATCH, ALL, ctx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.utils import show_risk_stability_graph, show_volume_stability_overtime
from utils.preprocessing import data_for_binary, data_for_lc, data_for_hc_nd, data_for_hc_d_train, data_discret
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
    

@callback(Output("catego_ou_numerique-value", "children"), Input("catego_ou_numerique", "value"))
def select_value(value):
    return value


# Comparateur de variables

@callback(
    Output('choice_var_2', 'children'),
    [Input('target_selected_checkbox', 'checked'), 
     Input('catego_ou_numerique','value')]
)
def choix_var_2_ou_target(checked_target, cat_or_num):
    if checked_target:
        return dmc.Select(id='var_2_compare', data=[{'label': 'TARGET', 'value': 'TARGET'}],value='TARGET', disabled=True)
    elif cat_or_num== 'numerical':
        return dmc.Select(
            id='var_2_compare',
            data=[{'label': i, 'value': i} for i in sorted(list(set(discretised_cols+tested_numerical_variables)))] ,
            value=None,
            label='Select a 2nd variable'
        )
    elif cat_or_num=='categorical':
        return dmc.Select(
            id='var_2_compare',
            data=[{'label': i, 'value': i} for i in sorted(list(set(catego_a_utiliser + discretised_cols)))] ,
            value=None,
            label='Select a 2nd variable'
        )


@callback(
    Output('choice_var_1', 'children'),
    Input('catego_ou_numerique','value')
)
def choix_var_1(cat_or_num):
    if cat_or_num== 'numerical':
        return dmc.Select(
            id='var_1_compare',
            data=[{'label': i, 'value': i} for i in sorted(list(set(discretised_cols+tested_numerical_variables)))] ,
            value=None,
            label='Select a 1st variable'
        )
    elif cat_or_num=='categorical':
        return dmc.Select(
            id='var_1_compare',
            data=[{'label': i, 'value': i} for i in sorted(list(set(catego_a_utiliser + discretised_cols)))] ,
            value=None,
            label='Select a 1st variable')

@callback(Output('valeur_var_1','children'),
          Input('var_1_compare','value')
          )
def recup_var_1(choix):
    return choix

@callback(Output('valeur_var_2','children'),
          Input('var_2_compare','value'))
def recup_var_2(choix):
    return choix


@callback(
    Output("checkbox-output", "children"), 
    Input("submit-var-explo", "n_clicks")
)
def checkbox(n_clicks):
    if n_clicks is None:
        # Le bouton n'a pas encore été cliqué
        return False
    else:
        # Le bouton a été cliqué au moins une fois
        return True


@callback(
    Output('stats_display','children'),
    [
        Input('catego_ou_numerique','value'), 
        Input('target_selected_checkbox', 'checked'),
        Input("checkbox-output", "children")
    ],
    [
        State('valeur_var_1','children'),
        State('valeur_var_2','children')
    ], 

    prevent_initial_call=True
)
def compute_stats(cat_or_num, checked_target, booleen, vrai_var1, vrai_var2):
  
    if vrai_var1 is None or vrai_var2 is None:
        return "Veuillez sélectionner les variables à comparer."

    if checked_target == True and cat_or_num == 'categorical' and booleen == True: # chi2, Cramer, IV
        chi= calculate_chi_stat_target(data_for_hc_d_train, vrai_var1)
        iv = calculate_information_value(data_for_hc_d_train, vrai_var1)
        cramer= cramers_v_target(data_for_hc_d_train, vrai_var1)
        # print(chi)
        return [chi, iv, cramer]
    
    elif checked_target and cat_or_num =='numerical' and booleen == True : # Kruskal test
        return kruskal_wallis_test(data_discret,vrai_var1)
    
    elif cat_or_num =='numerical' and booleen == True: # Corr Pearson
        correlation = data_discret[[vrai_var1,vrai_var2]].corr().values[0,1]
        return f"Corrélation entre {vrai_var1} et {vrai_var2} est de : {correlation}"
    
    elif cat_or_num=='categorical': # Chi2, Cramer
        chi = calculate_chi_stat_cols(data_for_hc_d_train,vrai_var1,vrai_var2)
        cramer = cramers_v_cols(data_for_hc_d_train,vrai_var1,vrai_var2)
        return chi + cramer







    
# Jynaldo
from models.callable import DecisionExpertSystem
from datetime import datetime

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