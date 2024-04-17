# contient toutes les fonctions callbacks utilisées
from dash import Dash, html, dcc,Input, Output, callback, State , dash_table, MATCH, ALL, ctx, no_update
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.utils import show_risk_stability_graph, show_volume_stability_overtime
from utils.preprocessing import data_for_binary, data_for_lc, data_for_hc_nd, data_for_hc_d_train
from utils.preprocessing import low_category_non_stable_vars
from utils.preprocessing import hc_vars_for_app_nd, hc_vars_for_app_d
from utils.utils import cramers_v, mannwhitney_test, calculate_information_value, calculate_chi_stat

import plotly.figure_factory as ff
import numpy as np
from scipy.stats import ks_2samp
from models.callable import DecisionExpertSystem, Dataset, binomial_test

# variables binaires (b)
@callback(
    Output('b_graph_risk_stability_overtime', 'figure'),
    Input('binary_col', 'value')
)
def binary_risk_stability_graph(colname):
    return show_risk_stability_graph(data_for_binary, colname)

@callback(
    Output('b_graph_volume_stability_overtime', 'figure'),
    Input('binary_col', 'value')
)
def binary_volume_stability_graph(binary_col):
    fig = show_volume_stability_overtime(data_for_binary, binary_col)
    return fig

@callback(
    Output('binary_risk_info', 'children'),
    Input('binary_col', 'value')
)
def binary_risk_info(binary_col):
    summary = ""
    binary_risk_non_stable_vars=["FLAG_MOBIL", "FLAG_CONT_MOBILE", "FLAG_EMAIL", "REG_REGION_NOT_LIVE_REGION", "REG_REGION_NOT_WORK_REGION","LIVE_REGION_NOT_WORK_REGION"]
    if binary_col in binary_risk_non_stable_vars:
        summary+= f"{binary_col} est Non Stable en Risque !"
    else:
        summary+= f"{binary_col} est Stable en Risque !"
    return summary

@callback(
    Output('binary_vol_info', 'children'),
    Input('binary_col', 'value')
)
def binary_vol_info(binary_col): # toutes les binaires sont stables en volume
    return f"{binary_col} est stable en volume !"


# variables catégorielles faibles moda (lc)
@callback(
    Output('lc_graph_risk_stability_overtime', 'figure'),
    Input('lc_col', 'value')
)
def lc_risk_stability_graph(colname):
    return show_risk_stability_graph(data_for_lc, colname)

@callback(
    Output('lc_graph_volume_stability_overtime', 'figure'),
    Input('lc_col', 'value')
)
def lc_volume_stability_graph(colname):
    fig = show_volume_stability_overtime(data_for_lc, colname)
    return fig

@callback(
    Output('lc_stability_info', 'children'),
    Input('lc_col', 'value')
)
def lc_stability_info(lc_col):
    if lc_col in low_category_non_stable_vars:
        return f"{lc_col} est Non Stable en Risque/Volume !"
    else:
        return f"{lc_col} est Stable en Risque/Volume !"
    
# variables catégo a haute modalité (hc)

@callback(
    Output("dropdown_var_choice", "options"),
    [Input("checkbox_discretized_choice", "checked")]
)
def update_dropdown_options(checked):
    if checked:
        return [{'label': i, 'value': i} for i in hc_vars_for_app_d]
    else:
        return [{'label': i, 'value': i} for i in hc_vars_for_app_nd]
    
@callback(
    Output("hc_graph_risk_stability_overtime", "figure"),
    [Input("dropdown_var_choice", "value"), Input("checkbox_discretized_choice", "checked")]
)
def hc_risk_stability_graph(selected_variable, checked):
    if checked:
        return show_risk_stability_graph(data_for_hc_d_train, selected_variable)
    else:
        return show_risk_stability_graph(data_for_hc_nd, selected_variable)
    
@callback(
    Output("hc_graph_volume_stability_overtime", "figure"),
    [Input("dropdown_var_choice", "value"), Input("checkbox_discretized_choice", "checked")]
)
def hc_volume_stability_graph(selected_variable, checked):
    if checked:
        return show_volume_stability_overtime(data_for_hc_d_train, selected_variable)
    else:
        return show_volume_stability_overtime(data_for_hc_nd, selected_variable)

@callback(
    Output("hc_stability_info", "children"),
    [Input("dropdown_var_choice", "value"), Input("checkbox_discretized_choice", "checked")]
)
def hc_stability_info(selected_variable, checked):
    if checked:
        return " faudra écrire une décision là. Est-ce stable en volume/risque ?"
    else:
        return "faudra écrire une décision ici. Est-ce stable en volume/risque ?"


@callback(
    Output("hc_chi_stat_info", "children"),
    [Input("dropdown_var_choice", "value"), Input("checkbox_discretized_choice", "checked")]
)
def hc_chi_stat(colname,checked):
    if checked:
        return calculate_chi_stat(data_for_hc_d_train, colname)
    else:
        return calculate_chi_stat(data_for_hc_nd, colname)

@callback(
    Output("hc_cramers_v_info", "children"),
    [Input("dropdown_var_choice", "value"), Input("checkbox_discretized_choice", "checked")]
)
def hc_cramers_v(colname,checked):
    if checked:
        return cramers_v(data_for_hc_d_train, colname)
    else:
        return cramers_v(data_for_hc_nd, colname)

@callback(
    Output("hc_mann_whitney_info", "children"),
    [Input("dropdown_var_choice", "value"), Input("checkbox_discretized_choice", "checked")]
)
def hc_mann_whitney(colname,checked):
    if checked:
        return mannwhitney_test(data_for_hc_d_train, colname)
    else:
        return mannwhitney_test(data_for_hc_nd, colname)

@callback(
    Output("hc_iv_info", "children"),
    [Input("dropdown_var_choice", "value"), Input("checkbox_discretized_choice", "checked")]
)
def hc_iv(colname,checked):
    if checked:
        return calculate_information_value(data_for_hc_d_train, colname)
    else:
        return calculate_information_value(data_for_hc_nd, colname) 
    
