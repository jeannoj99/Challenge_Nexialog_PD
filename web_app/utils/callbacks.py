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
            label='Sélectionner une 2ème variable'
        )
    elif cat_or_num=='categorical':
        return dmc.Select(
            id='var_2_compare',
            data=[{'label': i, 'value': i} for i in sorted(list(set(catego_a_utiliser + discretised_cols)))] ,
            value=None,
            label='Sélectionner une 2ème variable'
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
            label='Sélectionner la 1ère variable'
        )
    elif cat_or_num=='categorical':
        return dmc.Select(
            id='var_1_compare',
            data=[{'label': i, 'value': i} for i in sorted(list(set(catego_a_utiliser + discretised_cols)))] ,
            value=None,
            label='Sélectionner la 1ère variable')

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
        # return [chi, iv, cramer]
        return dmc.Alert(f"{chi}, {iv}, {cramer}", title="Résultats", color="green")
    
    elif checked_target and cat_or_num =='numerical' and booleen == True : # Kruskal test
        # return kruskal_wallis_test(data_discret,vrai_var1)
        return dmc.Alert(f"{kruskal_wallis_test(data_discret,vrai_var1)}", title="Résultats", color="green")
    
    elif cat_or_num =='numerical' and booleen == True: # Corr Pearson
        correlation = data_discret[[vrai_var1,vrai_var2]].corr().values[0,1]
        # return f"Corrélation entre {vrai_var1} et {vrai_var2} est de : {correlation}"
        return dmc.Alert(f"Corrélation entre {vrai_var1} et {vrai_var2} est de : {correlation}", title="Résultats", color="green")
    
    elif cat_or_num=='categorical': # Chi2, Cramer
        chi = calculate_chi_stat_cols(data_for_hc_d_train,vrai_var1,vrai_var2)
        cramer = cramers_v_cols(data_for_hc_d_train,vrai_var1,vrai_var2)
        # return chi + cramer
        return dmc.Alert(f"{chi}, {cramer}", title="Résultats", color="green")

    