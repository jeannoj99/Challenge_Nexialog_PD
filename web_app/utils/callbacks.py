# contient toutes les fonctions callbacks utilisées
from dash import Dash, html, dcc,Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.utils import show_risk_stability_graph, show_volume_stability_overtime


data = pd.read_csv("../data/application_train_vf.csv", parse_dates=["date_mensuelle"], index_col=0)
data["date_annee"] = data["date_mensuelle"].dt.year

@callback(
    Output('graph_risk_stability_overtime', 'figure'),
    Input('binary_col', 'value')
)
def binary_risk_stability_graph(colname):
    return show_risk_stability_graph(data, colname)

@callback(
    Output('graph_volume_stability_overtime', 'figure'),
    Input('binary_col', 'value')
)
def binary_volume_stability_graph(binary_col):
    fig = show_volume_stability_overtime(data, binary_col)
    return fig

@callback(
    Output('binary_info', 'children'),
    Input('binary_col', 'value')
)
def binary_summary(binary_col):
    summary = f"A Propos de {binary_col}: "
    binary_risk_non_stable_vars=["FLAG_MOBIL", "FLAG_CONT_MOBILE", "FLAG_EMAIL", "REG_REGION_NOT_LIVE_REGION", "REG_REGION_NOT_WORK_REGION","LIVE_REGION_NOT_WORK_REGION"]
    if binary_col in binary_risk_non_stable_vars:
        summary+= f" Non Stable en Risque !"
    else:
        summary+= f" Stable en Risque !"
    return summary