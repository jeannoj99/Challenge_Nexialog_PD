import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
from jenkspy import JenksNaturalBreaks
import plotly.express as px
from dash import dash_table


data_test = pd.read_csv("../data/data_seg_test.csv")
data_train = pd.read_csv("../data/data_seg_train.csv")

data_test_cash= pd.read_csv("../data/data_seg_test_cash.csv")
data_train_cash= pd.read_csv("../data/data_seg_train_cash.csv")

data_test_revolving= pd.read_csv("../data/data_seg_test_revolving.csv")
data_train_revolving= pd.read_csv("../data/data_seg_train_revolving.csv")

def subplot_segment_default_rate(data):
    mean_target_by_segment = data.groupby('Segment')['TARGET'].mean().reset_index()
    observation_count_by_segment = data['Segment'].value_counts(normalize=True).reset_index()
    observation_count_by_segment.columns = ['Segment', 'Observation Rate']

    # Barplot
    fig_bar = px.bar(observation_count_by_segment, x='Segment', y='Observation Rate', color='Segment',
                     labels={'Observation Rate': 'Taux d\'observation par segment'})

    # Line plot
    fig_line = px.line(mean_target_by_segment, x='Segment', y='TARGET', markers=True, line_shape='linear',
                       labels={'TARGET': 'Taux de défaut'}, title='Taux de défaut ')
    

    #les deux
    fig_combined = fig_bar.update_traces(marker=dict(color='navy'), selector=dict(type='bar'))
    fig_combined.add_traces(fig_line.data)
    return fig_combined

def show_risk_stability_overtime(data: pd.DataFrame, colname: str):
    result = data.groupby([colname, "date_annee"])['TARGET'].value_counts(normalize=True).unstack().fillna(0)[1]
    fig = px.line(result, x=result.index.get_level_values("date_annee"),
                  y=result.values, color=result.index.get_level_values(f"{colname}"), markers=True)
    fig.update_layout(xaxis_title="date_annee", yaxis_title="taux de défaut")
    return fig

#tableau
PD = [
    [0, 0.186826, 0.003031, 0.007340, 0.197197],
    [1, 0.126575, 0.001476, 0.003896, 0.131947],
    [2, 0.086883, 0.001023, 0.002799, 0.090705],
    [3, 0.064165, 0.000915, 0.002260, 0.067341],
    [4, 0.044405, 0.000757, 0.002021, 0.047184],
    [5, 0.033370, 0.000793, 0.002392, 0.036554],
    [6, 0.025495, 0.001377, 0.003908, 0.030779]
]
df_PD = pd.DataFrame(PD, columns=["Segment", "LRA", "MOC A", "MOC C", "PD"])

PD_revolving = [
    [0, 0.137796, 0.006492, 0.016257, 0.160544],
    [1, 0.079234, 0.004214, 0.009393, 0.092841],
    [2, 0.050962, 0.002467, 0.007147, 0.060576],
    [3, 0.037172, 0.002358, 0.006413, 0.045944],
    [4, 0.025781, 0.002861, 0.006084, 0.034725],
    [5, 0.016404, 0.001508, 0.004510, 0.022422],
    [6, 0.009841, 0.001370, 0.008375, 0.019586]
]
df_PD_revolving = pd.DataFrame(PD_revolving, columns=["Segment", "LRA", "MOC A", "MOC C", "PD"])

PD_cash = [
    [0, 0.190468, 0.002764, 0.007218, 0.200450],
    [1, 0.131752, 0.001596, 0.004045, 0.137392],
    [2, 0.091733, 0.001236, 0.003037, 0.096006],
    [3, 0.062877, 0.000947, 0.002581, 0.066405],
    [4, 0.046966, 0.000924, 0.002250, 0.050140],
    [5, 0.031889, 0.000800, 0.002214, 0.034903],
    [6, 0.026482, 0.001616, 0.004423, 0.032521]
]
df_PD_cash = pd.DataFrame(PD_cash, columns=["Segment", "LRA", "MOC A", "MOC C", "PD"])

layout = html.Div([
    dcc.Dropdown(
        id='contract-type-dropdown',
        options=[
            {'label': 'All contracts', 'value': 'all_contracts'},
            {'label': 'Revolving loans', 'value': 'revolving_loans'},
            {'label': 'Cash loans', 'value': 'cash_loans'}
        ],
        value='all_contracts'
    ),

    html.Div([
        html.H2(children='Graphiques de répartition et de taux de défaut par CHR', style={'textAlign': 'center'}),
        dcc.Graph(figure=subplot_segment_default_rate(data_train), id='subplot_graph', style={'width': '50%', 'display': 'inline-block', 'backgroundColor': 'lightgrey'}),
        dcc.Graph(figure=subplot_segment_default_rate(data_test), id='subplot_graph2', style={'width': '50%', 'display': 'inline-block', 'backgroundColor': 'lightgrey'}),
    ], style={'textAlign': 'center', 'margin-bottom': '20px'}),  


    html.Div([
        html.H2(children='Graphiques de stabilité du risque au fil du temps', style={'textAlign': 'center'}),
        dcc.Graph(figure=show_risk_stability_overtime(data_train, "Segment"), id='second_graph', style={'width': '50%', 'display': 'inline-block', 'backgroundColor': 'lightgrey'}),
        dcc.Graph(figure=show_risk_stability_overtime(data_test, "Segment"), id='second_graph2', style={'width': '50%', 'display': 'inline-block', 'backgroundColor': 'lightgrey'}),
    ], style={'textAlign': 'center', 'margin-bottom': '20px'}), 


    html.Div([
        html.H2(children='Probabilité de défaut', style={'textAlign': 'center'}),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_PD.columns],
            data=df_PD.to_dict('records'),
            style_table={'width': '80%', 'margin': 'auto'}
        )
    ], style={'textAlign': 'center'})
], style={'padding': 10})

@callback(
    [Output('subplot_graph', 'figure'),
     Output('subplot_graph2', 'figure'),
     Output('second_graph', 'figure'),
     Output('second_graph2', 'figure'),
     Output('table', 'data')],
    [Input('contract-type-dropdown', 'value')]
)
def update_graph(selected_contract_type):
    if selected_contract_type == 'all_contracts':
        subplot_fig = subplot_segment_default_rate(data_train)
        subplot_fig2 = subplot_segment_default_rate(data_test)
        risk_fig = show_risk_stability_overtime(data_test, "Segment")
        risk_fig2 = show_risk_stability_overtime(data_train, "Segment")
        return subplot_fig, subplot_fig2, risk_fig, risk_fig2, df_PD.to_dict('records')
    elif selected_contract_type == 'revolving_loans':
        subplot_fig = subplot_segment_default_rate(data_train_revolving)
        subplot_fig2 = subplot_segment_default_rate(data_test_revolving)
        risk_fig = show_risk_stability_overtime(data_test_revolving, "Segment")
        risk_fig2 = show_risk_stability_overtime(data_train_revolving, "Segment")
        return subplot_fig, subplot_fig2, risk_fig, risk_fig2, df_PD_revolving.to_dict('records')  
    elif selected_contract_type == 'cash_loans':
        subplot_fig = subplot_segment_default_rate(data_train_cash)
        subplot_fig2 = subplot_segment_default_rate(data_test_cash)
        risk_fig = show_risk_stability_overtime(data_test_cash, "Segment")
        risk_fig2 = show_risk_stability_overtime(data_train_cash, "Segment")
        return subplot_fig, subplot_fig2, risk_fig, risk_fig2, df_PD_cash.to_dict('records')  
    else:
        return [html.P("Sélectionnez un type de contrat")]