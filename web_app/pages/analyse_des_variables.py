from dash import Dash, html, dcc,Input, Output, callback
import pandas as pd
import plotly.express as px

data=pd.read_csv("../data/application_train_vf.csv",parse_dates=["date_mensuelle"], index_col=0)
data["date_annee"]=data["date_mensuelle"].dt.year

layout = html.Div(
    [
        html.Div(
            html.H1(children='Analyse des variables', style={'textAlign': 'center'}),
            style={'margin-bottom': '20px'}
        ),

        html.Div(
            [
                html.Label('Stability over Time'),
                dcc.Dropdown(
                    options=[
                        {'label': 'FLAG_MOBIL', 'value': 'FLAG_MOBIL'},
                        {'label': 'FLAG_EMP_PHONE', 'value': 'FLAG_EMP_PHONE'},
                        {'label': 'FLAG_WORK_PHONE', 'value': 'FLAG_WORK_PHONE'},
                        {'label': 'FLAG_EMAIL', 'value': 'FLAG_EMAIL'}
                    ],
                    value='FLAG_WORK_PHONE',id='col_for_risk_stab'
                ),

                html.Br(),

                dcc.Graph(id='graph_risk_stab_time'),

                html.Br(),
                html.Label('Multi-Select Dropdown'),
                dcc.Dropdown(
                    options=[
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': 'Montréal', 'value': 'MTL'},
                        {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value=['MTL', 'SF'],
                    multi=True
                ),

                html.Br(),

                html.Label('Radio Items'),
                dcc.RadioItems(
                    options=[
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': 'Montréal', 'value': 'MTL'},
                        {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value='MTL'
                ),
            ],
            style={'padding': 10, 'flex': 1}
        ),

        html.Div(
            [
                html.Label('Checkboxes'),
                dcc.Checklist(
                    options=[
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': 'Montréal', 'value': 'MTL'},
                        {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value=['MTL', 'SF']
                ),

                html.Br(),

                html.Label('Text Input'),
                dcc.Input(value='MTL', type='text'),

                html.Br(),

                html.Label('Slider'),
                dcc.Slider(
                    min=0,
                    max=9,
                    marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 6)},
                    value=5,
                ),
            ],
            style={'padding': 10, 'flex': 1}
        )
    ],
    style={'display': 'flex', 'flexDirection': 'column'}
)

@callback(
        Output('graph_risk_stab_time','figure'),
        Input('col_for_risk_stab','value'))
def show_risk_stability_overtime(colname:str):
    print(colname)
    result = data.groupby([colname, "date_annee"])['TARGET'].value_counts(normalize=True).unstack().fillna(0)[1]
    fig = px.line(result, x=result.index.get_level_values("date_annee"),
                   y=result.values, color=result.index.get_level_values(f"{colname}"),markers=True)
    return fig
