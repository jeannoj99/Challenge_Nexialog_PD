# contient toutes les fonctions callbacks utilisées
from dash import Dash, html, dcc,Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.utils import show_risk_stability_graph, show_volume_stability_overtime
from utils.preprocessing import data_for_binary, data_for_lc
from utils.preprocessing import low_category_non_stable_vars

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