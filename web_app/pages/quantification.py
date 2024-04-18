import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
from jenkspy import JenksNaturalBreaks
import plotly.express as px
from dash import dash_table
import plotly.graph_objects as go
import dash_mantine_components as dmc


data_test = pd.read_csv("../data/data_seg_test.csv")
data_train = pd.read_csv("../data/data_seg_train.csv")

data_test_cash= pd.read_csv("../data/data_seg_test_cash.csv")
data_train_cash= pd.read_csv("../data/data_seg_train_cash.csv")

data_test_revolving= pd.read_csv("../data/data_seg_test_revolving.csv")
data_train_revolving= pd.read_csv("../data/data_seg_train_revolving.csv")

data_seg_2020= pd.read_csv("../data/data_seg_2020.csv")
data_seg_revolving_2020= pd.read_csv("../data/data_seg_revolving_2020.csv")
data_seg_cash_2020= pd.read_csv("../data/data_seg_cash_2020.csv")

border_color = "#8C8C8C"

style = {
    #"height": 100,
    "border": f"1px solid {border_color}",
    "marginTop": 20,
    #"marginBottom": 20,
    "borderRadius": 10,  # Arrondir les bordures
    "backgroundColor": "white",  # Fond blanc
}


def subplot_segment_default_rate(data):
    mean_target_by_segment = data.groupby('Segment')['TARGET'].mean().reset_index()
    
    color_scale = []

    for segment, default_rate in zip(mean_target_by_segment['Segment'], mean_target_by_segment['TARGET']):
        if default_rate < 0.03:
            color_scale.append('green') 
        elif default_rate < 0.1:
            color_scale.append('#F1F74B')  
        else:
            color_scale.append('#DA3232')   

    # Create a dictionary to map segment to color
    segment_color_map = dict(zip(mean_target_by_segment['Segment'], color_scale))

    # Map the colors to the segments in the original order
    bar_colors = [segment_color_map[segment] for segment in data['Segment'].value_counts(normalize=True).index]

    fig = go.Figure()

    fig.add_trace(go.Bar(x=data['Segment'].value_counts(normalize=True).index,
                         y=data['Segment'].value_counts(normalize=True),
                         marker=dict(color=bar_colors),
                         showlegend=False))
    fig.add_trace(go.Scatter(x=mean_target_by_segment['Segment'],
                             y=mean_target_by_segment['TARGET'],
                             mode='lines+markers',
                             line=dict(color='navy', width=2),
                             yaxis='y2',
                             showlegend=False))
    
    fig.update_layout(annotations=[
        dict(
            x=0.5,
            y=1.15,
            xref='paper',
            yref='paper',
            text="Taux de défaut",
            showarrow=False,
            font=dict(color="navy",size=14)
        ),
        dict(
            x=0.15,
            y=1.05,
            xref='paper',
            yref='paper',
            text="Élevé",
            showarrow=False,
            font=dict(color="#DA3232", size=12)
        ),
        dict(
            x=0.5,
            y=1.05,
            xref='paper',
            yref='paper',
            text="Modéré",
            showarrow=False,
            font=dict(color="#F1F74B", size=12)
        ),
        dict(
            x=0.85,
            y=1.05,
            xref='paper',
            yref='paper',
            text="Faible",
            showarrow=False,
            font=dict(color="green", size=12)
        )

    ])

    fig.update_layout(xaxis=dict(title='Segment',tickmode='array', tickvals=mean_target_by_segment['Segment']),
                      yaxis=dict(title='Répartition par segment'),
                      yaxis2=dict(title='Taux de défaut', color='navy', overlaying='y', side='right'))
    
    return fig



def show_risk_stability_overtime(data: pd.DataFrame, colname: str):
    result = data.groupby([colname, "date_annee"])['TARGET'].value_counts(normalize=True).unstack().fillna(0)[1]
    fig = px.line(result, x=result.index.get_level_values("date_annee"),
                  y=result.values, color=result.index.get_level_values(f"{colname}"), markers=True)
    fig.update_layout(xaxis=dict(title="date_annee", type='category'),
                      yaxis_title="taux de défaut",
                      legend_title="Segment")
    return fig


def show_risk_stability_overtime_2(data: pd.DataFrame, colname: str):
    result = data.groupby([colname, "date_annee"])['TARGET'].mean().reset_index()
    fig = px.bar(result, x="Segment", y="TARGET", color=colname, barmode='group')
    fig.update_layout(xaxis=dict(title="Taux de défaut par segment pour l'année 2020", type='category'),
                      yaxis_title="Taux de défaut moyen",
                      legend_title="Segment")
    

    return fig




#tableau
PD = [
    [0, 0.185832, 0.003705, 0.006443, 0.195980],
    [1, 0.125972, 0.001937, 0.003356, 0.131266],
    [2, 0.087642, 0.001534, 0.002675, 0.091851],
    [3, 0.061047, 0.001256, 0.002277, 0.064580],
    [4, 0.045436, 0.001090, 0.001938, 0.048465],
    [5, 0.030751, 0.001162, 0.002041, 0.033954],
    [6, 0.024824, 0.001946, 0.003842, 0.030611]
]
df_PD = pd.DataFrame(PD, columns=["Segment", "LRA", "MOC A", "MOC C", "PD"])

PD_revolving = [
    [0, 0.137796, 0.006229, 0.016712, 0.160738],
    [1, 0.079234, 0.004103, 0.009464, 0.092801],
    [2, 0.050962, 0.002460, 0.007324, 0.060746],
    [3, 0.037172, 0.002279, 0.006185, 0.045636],
    [4, 0.025781, 0.002801, 0.006111, 0.034693],
    [5, 0.016404, 0.001530, 0.004684, 0.022618],
    [6, 0.009841, 0.001391, 0.008398, 0.019630]
]
df_PD_revolving = pd.DataFrame(PD_revolving, columns=["Segment", "LRA", "MOC A", "MOC C", "PD"])

PD_cash = [
    [0, 0.190468, 0.003063, 0.007310, 0.200842],
    [1, 0.131752, 0.001502, 0.004198, 0.137451],
    [2, 0.091733, 0.001193, 0.003043, 0.095969],
    [3, 0.062877, 0.000923, 0.002378, 0.066178],
    [4, 0.046966, 0.000880, 0.002266, 0.050113],
    [5, 0.031889, 0.000802, 0.002303, 0.034994],
    [6, 0.026482, 0.001591, 0.004334, 0.032407]
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

        dmc.Container(

        [
            html.Div([
        dmc.Title('Graphiques de répartition et de taux de défaut par CHR', order = 1, style={'textAlign': 'center'}),
        html.Div([
            html.Div([
                html.H3("Les données d'entraînement", style={'fontSize': '16px'}),
                dcc.Graph(figure=subplot_segment_default_rate(data_train), id='subplot_graph', style={'width': '100%', 'backgroundColor': 'lightgrey'}, config={'displayModeBar': False}),
            ], style={'textAlign': 'center'}),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            html.Div([
                html.H3("Les données de test", style={'fontSize': '16px'}),
                dcc.Graph(figure=subplot_segment_default_rate(data_test), id='subplot_graph2', style={'width': '100%', 'backgroundColor': 'lightgrey'}, config={'displayModeBar': False}),
            ], style={'textAlign': 'center'}),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            html.H3("Les données de 2020", style={'fontSize': '16px'}),
            dcc.Graph(figure=subplot_segment_default_rate(data_seg_2020), id='subplot_graph3', style={'width': '100%', 'backgroundColor': 'lightgrey'}, config={'displayModeBar': False}),
        ], style={'width': '80%', 'display': 'inline-block'}),
    ], style={'textAlign': 'center', 'margin-bottom': '20px'}),
   
        ],
        
        style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}, size="100"

        ),
 
    dmc.Container(
        [

        html.Div([
        dmc.Title('Graphiques de stabilité du risque au fil du temps', order=1, style={'textAlign': 'center'}),
        html.Div([
            html.Div([
                html.H3("Les données d'entraînement", style={'fontSize': '16px'}),
                dcc.Graph(figure=show_risk_stability_overtime(data_train, "Segment"), id='second_graph', style={'width': '100%', 'backgroundColor': 'lightgrey'}, config={'displayModeBar': False}),
            ], style={'textAlign': 'center'}),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            html.Div([
                html.H3("Les données de test", style={'fontSize': '16px'}),
                dcc.Graph(figure=show_risk_stability_overtime(data_test, "Segment"), id='second_graph2', style={'width': '100%', 'backgroundColor': 'lightgrey'}, config={'displayModeBar': False}),
            ], style={'textAlign': 'center'}),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            html.Div([
                dcc.Graph(figure=show_risk_stability_overtime_2(data_seg_2020, "Segment"), id='second_graph3', style={'width': '100%', 'backgroundColor': 'lightgrey'}, config={'displayModeBar': False}),
            ], style={'textAlign': 'center'}),
        ], style={'width': '80%', 'display': 'inline-block'}),
    ], style={'textAlign': 'center', 'margin-bottom': '20px'}), 

        ],

        style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}, size="100"
    ),

    dmc.Container(

        [
            html.Div([
            dmc.Title('Probabilité de défaut', order = 2, style={'textAlign': 'center'}),
               html.Div([
    # Première moitié
    html.Div([
        dmc.HoverCard( withArrow=True, width=200, shadow="md",
            children=[ dmc.HoverCardTarget(dmc.Button("Objectifs des MOC")),
            dmc.HoverCardDropdown(
            dcc.Markdown(
                "La MOC C mesure l'erreur d'estimation réalisée par notre modèle.  \n"
                "La MOC A mesure les erreurs liées aux données.",
                style={"fontSize": "14px"}
            )
        ),
    ],
),

        html.Br() , html.Br(), html.Br(), html.Br(),

dmc.HoverCard( withArrow=True, width=800, shadow="md",
            children=[ dmc.HoverCardTarget(dmc.Button("Méthodologie des MOC")),
            dmc.HoverCardDropdown(
            dcc.Markdown(
                "La MOC C est calculée en prenant la différence entre le 90e centile et la moyenne des taux de défaut obtenus à partir de 5000 échantillons bootstrap. La MOC A est calculée en prenant la différence entre le 90e centile et la moyenne des ajustements, qui représente la différence entre la moyenne du taux de défaut pour les années avant 2019 et la moyenne totale du taux de défaut pour chaque segment.",
                style={"fontSize": "14px"}
            )
        ),
    ],
),
    ], style={'width': '10%', 'float': 'left'}),
    # Deuxième moitié
    html.Div([
       dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_PD.columns],
            data=df_PD.to_dict('records'),
            style_table={'width': '90%', 'margin': 'auto'}),
    ], style={'width': '80%', 'float': 'right'}),  # Définit la largeur à 80% et aligne à gauche
], style={'width': '100%', 'overflow': 'hidden'})  # Assure que la div parente englobe les deux moitiés

            ], style={'textAlign': 'center'}),

        html.Br(),

        ] ,

        style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}, size="100"

    ),



    
], style={'padding': 10})




@callback(
    [Output('subplot_graph', 'figure'),
     Output('subplot_graph2', 'figure'),
     Output('subplot_graph3', 'figure'),
     Output('second_graph', 'figure'),
     Output('second_graph2', 'figure'),
     Output('second_graph3', 'figure'),
     Output('table', 'data')],
    [Input('contract-type-dropdown', 'value')]
)
def update_graph(selected_contract_type):
    if selected_contract_type == 'all_contracts':
        subplot_fig = subplot_segment_default_rate(data_train)
        subplot_fig2 = subplot_segment_default_rate(data_test)
        subplot_fig3 = subplot_segment_default_rate(data_seg_2020)
        risk_fig = show_risk_stability_overtime(data_train, "Segment")
        risk_fig2 = show_risk_stability_overtime(data_test, "Segment")
        risk_fig3 = show_risk_stability_overtime_2(data_seg_2020, "Segment")
        return subplot_fig, subplot_fig2,subplot_fig3, risk_fig, risk_fig2,risk_fig3, df_PD.to_dict('records')
    elif selected_contract_type == 'revolving_loans':
        subplot_fig = subplot_segment_default_rate(data_train_revolving)
        subplot_fig2 = subplot_segment_default_rate(data_test_revolving)
        subplot_fig3 = subplot_segment_default_rate(data_seg_revolving_2020)
        risk_fig = show_risk_stability_overtime(data_train_revolving, "Segment")
        risk_fig2 = show_risk_stability_overtime(data_test_revolving, "Segment")
        risk_fig3 = show_risk_stability_overtime_2(data_seg_revolving_2020, "Segment")
        return subplot_fig, subplot_fig2,subplot_fig3, risk_fig, risk_fig2,risk_fig3, df_PD_revolving.to_dict('records')  
    elif selected_contract_type == 'cash_loans':
        subplot_fig = subplot_segment_default_rate(data_train_cash)
        subplot_fig2 = subplot_segment_default_rate(data_test_cash)
        subplot_fig3 = subplot_segment_default_rate(data_seg_cash_2020)
        risk_fig = show_risk_stability_overtime(data_train_cash, "Segment")
        risk_fig2 = show_risk_stability_overtime(data_test_cash, "Segment")
        risk_fig3 = show_risk_stability_overtime_2(data_seg_cash_2020, "Segment")
        return subplot_fig, subplot_fig2,subplot_fig3, risk_fig, risk_fig2,risk_fig3, df_PD_cash.to_dict('records')  
    else:
        return [html.P("Sélectionnez un type de contrat")]
