from dash import Dash, html, dcc,Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import dash_mantine_components as dmc

grid_score = pd.read_excel("../data/grille_de_score.xlsx",index_col=0)
grid_score = grid_score.sort_values(by=['Variable', 'tx_defaut'], ascending=[True, False])

grid_score_cash = pd.read_excel("../data/grille_de_score_cash.xlsx",index_col=0)
grid_score_cash = grid_score_cash.sort_values(by=['Variable', 'tx_defaut'], ascending=[True, False])

grid_score_revolving = pd.read_excel("../data/grille_de_score_revolving.xlsx",index_col=0)
grid_score_revolving = grid_score_revolving.sort_values(by=['Variable', 'tx_defaut'], ascending=[True, False])

data_train = pd.read_csv("../data/data_train_all.csv",sep=',')
data_test = pd.read_csv("../data/data_test_all.csv",sep=',')

data_train_cash = pd.read_csv("../data/data_train_notes_target_cash.csv",sep=',')
data_test_cash = pd.read_csv("../data/data_test_notes_target_cash.csv",sep=',')

data_train_revolving = pd.read_csv("../data/data_train_notes_target_revolving.csv",sep=',')
data_test_revolving = pd.read_csv("../data/data_test_notes_target_revolving.csv",sep=',')

logit_results = [
    ["OCCUPATION_TYPE", "Treatment(reference=0)[0]", -0.9269, 0.059, -15.723, 0.000, "-1.042, -0.811"],
    ["OCCUPATION_TYPE", "Treatment(reference=0)[1]", -0.7332, 0.046, -15.868, 0.000, "-0.824, -0.643"],
    ["OCCUPATION_TYPE", "Treatment(reference=0)[2]", -0.5365, 0.045, -11.963, 0.000, "-0.624, -0.449"],
    ["OCCUPATION_TYPE", "Treatment(reference=0)[3]", -0.3485, 0.051, -6.806, 0.000, "-0.449, -0.248"],
    ["NAME_EDUCATION_TYPE", "Treatment(reference='Non graduated')[T.Graduated]", -0.4997, 0.025, -20.222, 0.000, "-0.548, -0.451"],
    ["AMT_CREDIT_NORM", "Treatment(reference=3)[Interval(-inf, 1.158, closed='right')]", -0.6339, 0.026, -24.132, 0.000, "-0.685, -0.582"],
    ["AMT_CREDIT_NORM", "Treatment(reference=3)[Interval(1.158, 1.211, closed='right')]", -0.3376, 0.032, -10.608, 0.000, "-0.400, -0.275"],
    ["AMT_CREDIT_NORM", "Treatment(reference=3)[Interval(1.211, 1.317, closed='right')]", -0.1996, 0.033, -6.083, 0.000, "-0.264, -0.135"],
    ["BORROWER_AGE", "Treatment(reference=0)[Interval(30.5, 38.5, closed='right')]", -0.0779, 0.026, -3.020, 0.003, "-0.129, -0.027"],
    ["BORROWER_AGE", "Treatment(reference=0)[Interval(38.5, 52.5, closed='right')]", -0.2929, 0.025, -11.748, 0.000, "-0.342, -0.244"],
    ["BORROWER_AGE", "Treatment(reference=0)[Interval(52.5, inf, closed='right')]", -0.4591, 0.033, -14.102, 0.000, "-0.523, -0.395"],
    ["BORROWER_SENIORITY", "Treatment(reference=0)[Interval(2.5, 4.5, closed='right')]", -0.1048, 0.025, -4.163, 0.000, "-0.154, -0.055"],
    ["BORROWER_SENIORITY", "Treatment(reference=0)[Interval(4.5, 10.5, closed='right')]", -0.3358, 0.024, -13.854, 0.000, "-0.383, -0.288"],
    ["BORROWER_SENIORITY", "Treatment(reference=0)[Interval(10.5, inf, closed='right')]", -0.4539, 0.029, -15.664, 0.000, "-0.511, -0.397"],
    ["CB_NB_CREDIT_CLOSED", "Treatment(reference=0)[Interval(0.5, 1.5, closed='right')]", -0.2592, 0.026, -9.857, 0.000, "-0.311, -0.208"],
    ["CB_NB_CREDIT_CLOSED", "Treatment(reference=0)[Interval(1.5, inf, closed='right')]", -0.4585, 0.022, -20.916, 0.000, "-0.502, -0.416"],
    ["CB_DAYS_CREDIT", "Treatment(reference=3)[Interval(-inf, -2921.5, closed='right')]", -0.7503, 0.036, -20.567, 0.000, "-0.822, -0.679"],
    ["CB_DAYS_CREDIT", "Treatment(reference=3)[Interval(-2921.5, -254.5, closed='right')]", -0.7457, 0.036, -21.003, 0.000, "-0.815, -0.676"],
    ["CB_DAYS_CREDIT", "Treatment(reference=3)[Interval(-254.5, -47.5, closed='right')]", -0.3522, 0.035, -10.117, 0.000, "-0.420, -0.284"]
]

logit_results_cash = [
    ["OCCUPATION_TYPE", "Treatment(reference=0)[0]", -1.0071, 0.059, -16.996, 0.000, "-1.123, -0.891"],
    ["OCCUPATION_TYPE", "Treatment(reference=0)[1]", -0.7837, 0.045, -17.375, 0.000, "-0.872, -0.695"],
    ["OCCUPATION_TYPE", "Treatment(reference=0)[2]", -0.5928, 0.044, -13.616, 0.000, "-0.678, -0.507"],
    ["OCCUPATION_TYPE", "Treatment(reference=0)[3]", -0.4061, 0.050, -8.077, 0.000, "-0.505, -0.308"],
    ["NAME_EDUCATION_TYPE", "Treatment(reference='Non graduated')[T.Graduated]", -0.4841, 0.026, -18.791, 0.000, "-0.535, -0.434"],
    ["AMT_CREDIT_NORM", "Treatment(reference=3)[Interval(-inf, 1.158, closed='right')]", -0.5673, 0.027, -21.204, 0.000, "-0.620, -0.515"],
    ["AMT_CREDIT_NORM", "Treatment(reference=3)[Interval(1.158, 1.211, closed='right')]", -0.2965, 0.032, -9.267, 0.000, "-0.359, -0.234"],
    ["AMT_CREDIT_NORM", "Treatment(reference=3)[Interval(1.211, 1.317, closed='right')]", -0.1669, 0.032, -5.136, 0.000, "-0.231, -0.103"],
    ["BORROWER_AGE", "Treatment(reference=0)[Interval(30.5, 38.5, closed='right')]", -0.0607, 0.027, -2.260, 0.024, "-0.113, -0.008"],
    ["BORROWER_AGE", "Treatment(reference=0)[Interval(38.5, 52.5, closed='right')]", -0.3020, 0.026, -11.596, 0.000, "-0.353, -0.251"],
    ["BORROWER_AGE", "Treatment(reference=0)[Interval(52.5, inf, closed='right')]", -0.4754, 0.034, -14.048, 0.000, "-0.542, -0.409"],
    ["BORROWER_SENIORITY", "Treatment(reference=0)[Interval(2.5, 5.5, closed='right')]", -0.1371, 0.024, -5.691, 0.000, "-0.184, -0.090"],
    ["BORROWER_SENIORITY", "Treatment(reference=0)[Interval(5.5, 10.5, closed='right')]", -0.3501, 0.027, -12.761, 0.000, "-0.404, -0.296"],
    ["BORROWER_SENIORITY", "Treatment(reference=0)[Interval(10.5, inf, closed='right')]", -0.4504, 0.030, -15.058, 0.000, "-0.509, -0.392"],
    ["CB_NB_CREDIT_CLOSED", "Treatment(reference=0)[Interval(0.5, 1.5, closed='right')]", -0.2713, 0.027, -9.867, 0.000, "-0.325, -0.217"],
    ["CB_NB_CREDIT_CLOSED", "Treatment(reference=0)[Interval(1.5, inf, closed='right')]", -0.4552, 0.023, -20.003, 0.000, "-0.500, -0.411"],
    ["CB_DAYS_CREDIT", "Treatment(reference=3)[Interval(-inf, -2921.5, closed='right')]", -0.7206, 0.034, -20.935, 0.000, "-0.788, -0.653"],
    ["CB_DAYS_CREDIT", "Treatment(reference=3)[Interval(-2921.5, -254.5, closed='right')]", -0.7167, 0.033, -21.617, 0.000, "-0.782, -0.652"],
    ["CB_DAYS_CREDIT", "Treatment(reference=3)[Interval(-254.5, -59.5, closed='right')]", -0.3408, 0.033, -10.405, 0.000, "-0.405, -0.277"]
]

logit_results_revolving = [
    ["NAME_EDUCATION_TYPE", "Treatment(reference='Non graduated')[Graduated]", -1.7127, 0.158, -10.819, 0.000, "-2.023, -1.402"],
    ["NAME_EDUCATION_TYPE", "Treatment(reference='Non graduated')[Non graduated]", -1.2163, 0.131, -9.268, 0.000, "-1.474, -0.959"],
    ["AMT_GOODS_PRICE", "Treatment(reference=1)[Interval(-inf, 168750.0, closed='right')]", -0.0547, 0.117, -0.466, 0.641, "-0.284, 0.175"],
    ["AMT_GOODS_PRICE", "Treatment(reference=1)[Interval(191250.0, 517500.0, closed='right')]", -0.1914, 0.081, -2.363, 0.018, "-0.350, -0.033"],
    ["AMT_GOODS_PRICE", "Treatment(reference=1)[Interval(517500.0, inf, closed='right')]", -0.8978, 0.170, -5.278, 0.000, "-1.231, -0.564"],
    ["OCCUPATION_TYPE", "Treatment(reference=2)[T.0]", -0.4678, 0.096, -4.861, 0.000, "-0.656, -0.279"],
    ["OCCUPATION_TYPE", "Treatment(reference=2)[T.1]", -0.1214, 0.087, -1.402, 0.161, "-0.291, 0.048"],
    ["DAYS_LAST_PHONE_CHANGE", "Treatment(reference=3)[Interval(-inf, -1637.5, closed='right')]", -0.7690, 0.134, -5.738, 0.000, "-1.032, -0.506"],
    ["DAYS_LAST_PHONE_CHANGE", "Treatment(reference=3)[Interval(-1637.5, -817.5, closed='right')]", -0.5477, 0.107, -5.133, 0.000, "-0.757, -0.339"],
    ["DAYS_LAST_PHONE_CHANGE", "Treatment(reference=3)[Interval(-817.5, -226.5, closed='right')]", -0.2421, 0.081, -3.004, 0.003, "-0.400, -0.084"],
    ["BORROWER_SENIORITY", "Treatment(reference=0)[Interval(1.5, 4.5, closed='right')]", -0.1040, 0.084, -1.232, 0.218, "-0.269, 0.061"],
    ["BORROWER_SENIORITY", "Treatment(reference=0)[Interval(4.5, 8.5, closed='right')]", -0.3162, 0.111, -2.849, 0.004, "-0.534, -0.099"],
    ["BORROWER_SENIORITY", "Treatment(reference=0)[Interval(8.5, inf, closed='right')]", -0.5673, 0.109, -5.189, 0.000, "-0.782, -0.353"],
    ["CB_NB_CREDIT_CLOSED", "Treatment(reference=0)[Interval(0.5, 2.5, closed='right')]", -0.1769, 0.085, -2.092, 0.036, "-0.343, -0.011"],
    ["CB_NB_CREDIT_CLOSED", "Treatment(reference=0)[Interval(2.5, inf, closed='right')]", -0.3705, 0.093, -3.971, 0.000, "-0.553, -0.188"],
    ["CB_DAYS_CREDIT", "Treatment(reference=3)[Interval(-inf, -2921.5, closed='right')]", -0.7500, 0.116, -6.467, 0.000, "-0.977, -0.523"],
    ["CB_DAYS_CREDIT", "Treatment(reference=3)[Interval(-2921.5, -264.5, closed='right')]", -0.7781, 0.118, -6.616, 0.000, "-1.009, -0.548"],
    ["CB_DAYS_CREDIT", "Treatment(reference=3)[Interval(-264.5, -64.5, closed='right')]", -0.3239, 0.111, -2.927, 0.003, "-0.541, -0.107"]
]



df_logit_results = pd.DataFrame(logit_results, columns=["Variable", "Modalités", "Coefficient", "std err", "z", "P>|z|", "[0.025, 0.975]"])
df_logit_results_cash = pd.DataFrame(logit_results_cash, columns=["Variable", "Modalités", "Coefficient", "std err", "z", "P>|z|", "[0.025, 0.975]"])
df_logit_results_revo = pd.DataFrame(logit_results_revolving, columns=["Variable", "Modalités", "Coefficient", "std err", "z", "P>|z|", "[0.025, 0.975]"])

border_color = "#8C8C8C"

style = {
    #"height": 100,
    "border": f"1px solid {border_color}",
    "marginTop": 20,
    #"marginBottom": 20,
    "borderRadius": 10,  # Arrondir les bordures
    "backgroundColor": "white",  # Fond blanc
}

layout = html.Div(
    [
        
    html.Div(
    [
        dmc.Title("All Contracts Model", order=1, style={'textAlign': 'center'}), 
        html.Br(),
        
        dmc.Container(
            [   html.Br(),
                dmc.Text("Modèle par défaut", weight=600),
                html.Br(style={'margin-top': '11px'}),
                html.Div(id='logit-results-all', style={'maxHeight': '300px', 'overflowY': 'auto'}),
                html.Br(),
                dmc.Group([dmc.Badge("Gini (train) : 0.33"), dmc.Space(w=20), dmc.Badge("Gini (test) : 0.32")]),
                html.Br(),
            ],
            style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}
        ),

        html.Br(),

        dmc.Container(
            [   html.Br(),
                dmc.Title(f"Grille de score", order=3, style={'textAlign': 'center'}),
                html.Label('Choix de la variable'),
                dcc.Dropdown(id='dropdown-grid-score-all', value="AMT_CREDIT_NORM"),
                dcc.Graph(id='effectif-modalites-all', style={'height': '800px'}),
                html.Br(),
                dmc.Switch(id="switch-example-all", label="Afficher la grille de score", checked=False, onLabel="ON", offLabel="OFF"),
                dmc.Space(h=30),
                dmc.Text(id="switch-settings-all"),
                html.Br()
            ],
            style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}

        ),

        html.Br(),

        dmc.Container(
            [   html.Br(),
                dmc.Title(f"Répartition des notes en fonction de la target", order=3, style={'textAlign': 'center'}),
                html.Label('Set de données'),
                dcc.Dropdown(
                        options=[{'label': 'data_train', 'value': 'data_train'},
                             {'label': 'data_test', 'value': 'data_test'},],
                        value='data_train',
                        id='dropdown-repartition-all'
                        ),
                dcc.Graph(id='repartition-target-all'),
        ],
            style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}

        )
    ],
    style={'flex': '1', 'margin-right': '10px', 'borderRadius': 10, 
           #'backgroundColor': 'white'
           }
)


        ,

        # Deuxième partie
html.Div(
    [
        dmc.Title("Cash Loans/Revolving Loans", order=1, style={'textAlign': 'center'}), 
        html.Br(),
        
        dmc.Container(
            [   html.Br(),
                dmc.Text('Choix du modèle à comparer', weight=600),
                dcc.Dropdown(
                    options=[
                        {'label': 'Cash Loans', 'value': 'Cash Loans'},
                        {'label': 'Revolving Loans', 'value': 'Revolving Loans'},
                    ],
                    value='Cash Loans',
                    id='main-dropdown'
                ),
                html.Div(id='logit-results', style={'maxHeight': '300px', 'overflowY': 'auto'}),
                html.Br(),
                dmc.Group(id="badge-group"),
                html.Br(),
            ],
            style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}
        ),

        html.Br(),

        dmc.Container(
            [   html.Br(),
                dmc.Title(f"Grille de score", order=3, style={'textAlign': 'center'}),
                html.Label('Choix de la variable'),
                dcc.Dropdown(id='dropdown-grid-score', value = "AMT_CREDIT_NORM"),
                dcc.Graph(id='effectif-modalites', style={'height': '800px'}),
                html.Br(),
                dmc.Switch(id="switch-example", label="Afficher la grille de score", checked=False, onLabel="ON", offLabel="OFF"),
                dmc.Space(h=30),
                dmc.Text(id="switch-settings"),
                html.Br()
            ],
            style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}

        ),

        html.Br(),

        dmc.Container(
            [   html.Br(),
                dmc.Title(f"Répartition des notes en fonction de la target", order=3, style={'textAlign': 'center'}),
                html.Label('Set de données'),

                dcc.Dropdown(
                    options=[
                        {'label': 'data_train', 'value': 'data_train'},
                        {'label': 'data_test', 'value': 'data_test'},
                    ],
                    value='data_train',
                    id='dropdown-repartition'
                ),

                dcc.Graph(id='repartition-target'),
        ],
            style={**style, 'borderRadius': 10, 'backgroundColor': 'white'}

        )
    ],
    style={'flex': '1', 'margin-right': '10px', 'borderRadius': 10, 
           #'backgroundColor': 'white'
           }
),
    ],
    style={'display': 'flex', 'justifyContent': 'space-between'}  # Pour aligner les deux parties à l'extrémité gauche et droite
)

###########################################################################################################
########################################## CALLBACKS ######################################################
###########################################################################################################

##### PARTIE GAUCHE

#choix du modèle et affiche les bonnes variables pour la grille de score selon modèle
@callback(
    Output('dropdown-grid-score-all', 'options'),
    [Input('main-dropdown', 'value')]
)
def update_grid_score_options(value):
    return [
            {'label': 'AMT_CREDIT_NORM', 'value': 'AMT_CREDIT_NORM'},
            {'label': 'BORROWER_AGE', 'value': 'BORROWER_AGE'},
            {'label': 'BORROWER_SENIORITY', 'value': 'BORROWER_SENIORITY'},
            {'label': 'CB_DAYS_CREDIT', 'value': 'CB_DAYS_CREDIT'},
            {'label': 'CB_NB_CREDIT_CLOSED', 'value': 'CB_NB_CREDIT_CLOSED'},
            {'label': 'NAME_EDUCATION_TYPE', 'value': 'NAME_EDUCATION_TYPE'},
            {'label': 'OCCUPATION_TYPE', 'value': 'OCCUPATION_TYPE'} ]


# résultats du logit en fonction du modèle choisi
@callback(
    Output('logit-results-all', 'children'),
    [Input('main-dropdown', 'value')]
)
def update_results_all(value):
    columns, values = df_logit_results.columns, df_logit_results.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    return dmc.Table(children=table, striped=True, highlightOnHover=True, withBorder=True, withColumnBorders=True)


@callback(Output("switch-settings-all", "children"), 
          Input("switch-example-all", "checked"))

def settings(checked):
    columns, values = grid_score.columns, grid_score.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    if checked :
        return dmc.Table(children=table, striped=True, highlightOnHover=True, withBorder=True, withColumnBorders=True)
    else :
        return ""

# Grille de score en fonction de la variable sélectionnée
@callback(
    Output('effectif-modalites-all', 'figure'),
    [Input('dropdown-grid-score-all', 'value'),
     #Input('main-dropdown', 'value')
     ]
)

def update_score_grid_graph(selected_variable): 
    data_filtered = grid_score[grid_score["Variable"] == selected_variable]

    # effectif/modalités
    fig1 = px.pie(data_filtered, 
          names="Modalités", 
          values='effectif',
          height=800
          )

    # notes/modalités
    fig2 = px.bar(data_filtered, y="Modalités", x='Note', orientation='h', text_auto=True)

    # taux de défaut/modalités
    fig3 = px.line(data_filtered, x="Modalités",y="tx_defaut", markers=True, text="tx_defaut")
    fig3.update_traces(textposition="top right")

    # tableau
    fig4 =  go.Table(
    header=dict(
        values=["Modalités","Coefficient","p-value"],
        font=dict(size=15),
        align="center"
    ),
    cells=dict(
        values=[data_filtered[k].tolist() for k in data_filtered.columns[[1,2,4]]],
        align = "center")
    )

    # mettre plusieurs graphes côte à côte
    fig = make_subplots(rows=2, cols=2, subplot_titles=("Répartition de l'effectif de la modalité", 'Notes par modalité', "Taux de défaut en fonction de la modalité","Statistiques"), 
        specs=[[{"type": "pie"}, {"type": "bar"}],
        [{"type": "scatter"}, {"type": "pie"}]]
        )


    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)
    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)
    for trace in fig3.data:
        fig.add_trace(trace, row=2, col=1)
   
    fig.add_trace(fig4, row=2, col=2)

    # Update xaxis properties
    fig.update_xaxes(title_text="Notes", row=1, col=2)
    fig.update_xaxes(title_text="Modalités", row=2, col=1)

    # Update yaxis properties
    fig.update_yaxes(title_text="Modalités", row=1, col=2, side="right")
    fig.update_yaxes(title_text="Taux de défaut", row=2, col=1)
    

    # Mettre à jour la disposition de la figure
    fig.update_layout(
        title_text='Dashboard', 
        title_x=0.5,
        template='simple_white' , 
                      margin=dict(l=0, r=0, t=100, b=100), # agrandir les marges
                      legend=dict(orientation='h', x=0, y=0.5)  # placer la légende
                          )

    return fig.to_dict()


@callback(
    Output('repartition-target-all', 'figure'),
    [Input('dropdown-repartition-all', 'value'),
     #Input('main-dropdown', 'value')
     ]
)

def update_repartition(selected_data):
    data_repartition = pd.DataFrame()
    if selected_data == "data_train" :
        data_repartition = data_train
    else :
        data_repartition = data_test
    
   
     # Création du displot avec ff.displot
    fig = ff.create_distplot(
         [data_repartition['Note'][data_repartition['TARGET'] == 0], 
          data_repartition['Note'][data_repartition['TARGET'] == 1]],
         group_labels=['Target = 0', 'Target = 1'],
         colors=['blue', 'red'], 
         show_hist=False,
         show_rug=False
     )

     # Mise en forme du titre et des axes
    fig.update_layout(
         title=f'Distribution de TARGET en fonction de la Note sur {selected_data} pour "All Contracts"',
         xaxis_title='Note',
         yaxis_title='Fréquence',
         template="simple_white"
     )

    return fig



##### PARTIE DROITE

#choix du modèle et affiche les bonnes variables pour la grille de score selon modèle
@callback(
    Output('dropdown-grid-score', 'options'),
    [Input('main-dropdown', 'value')]
)
def update_grid_score_options(selected_model):
    if selected_model == "Cash Loans":
        return [
            {'label': 'AMT_CREDIT_NORM', 'value': 'AMT_CREDIT_NORM'},
            {'label': 'BORROWER_AGE', 'value': 'BORROWER_AGE'},
            {'label': 'BORROWER_SENIORITY', 'value': 'BORROWER_SENIORITY'},
            {'label': 'CB_DAYS_CREDIT', 'value': 'CB_DAYS_CREDIT'},
            {'label': 'CB_NB_CREDIT_CLOSED', 'value': 'CB_NB_CREDIT_CLOSED'},
            {'label': 'NAME_EDUCATION_TYPE', 'value': 'NAME_EDUCATION_TYPE'},
            {'label': 'OCCUPATION_TYPE', 'value': 'OCCUPATION_TYPE'},   
        ]
    elif selected_model == "Revolving Loans":
        return [
            {'label': 'AMT_GOODS_PRICE', 'value': 'AMT_GOODS_PRICE'},
            {'label': 'BORROWER_SENIORITY', 'value': 'BORROWER_SENIORITY'},
            {'label': 'CB_DAYS_CREDIT', 'value': 'CB_DAYS_CREDIT'},
            {'label': 'CB_NB_CREDIT_CLOSED', 'value': 'CB_NB_CREDIT_CLOSED'},
            {'label': 'DAYS_LAST_PHONE_CHANGE', 'value': 'DAYS_LAST_PHONE_CHANGE'},
            {'label': 'NAME_EDUCATION_TYPE', 'value': 'NAME_EDUCATION_TYPE'},
            {'label': 'OCCUPATION_TYPE', 'value': 'OCCUPATION_TYPE'},   
        ]
    else:
        return []



# résultats du logit en fonction du modèle choisi
@callback(
    Output('logit-results', 'children'),
    [Input('main-dropdown', 'value')]
)
def update_results(selected_model):
    if selected_model == "Cash Loans" :
        df = df_logit_results_cash
    elif selected_model == "Revolving Loans" :
        df = df_logit_results_revo
    
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    return dmc.Table(children=table, striped=True, highlightOnHover=True, withBorder=True, withColumnBorders=True)

@callback(
        Output("badge-group","children"),
        Input('main-dropdown', 'value')
)

def evaluate_model(selected_model):
    if selected_model == "Cash Loans" :
        return dmc.Group([dmc.Badge("Gini (train) : 0.32"), dmc.Space(w=20), dmc.Badge("Gini (test) : 0.32")])
    elif selected_model == "Revolving Loans" :
        return dmc.Group([dmc.Badge("Gini (train) : 0.37"), dmc.Space(w=20), dmc.Badge("Gini (test) : 0.36")])

@callback(Output("switch-settings", "children"), 
          [Input("switch-example", "checked"),
           Input('main-dropdown', 'value')])

def settings(checked, selected_model):

    if selected_model == "Cash Loans" :
        df = grid_score_cash
    elif selected_model == "Revolving Loans" :
        df = grid_score_revolving

    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    if checked :
        return dmc.Table(children=table, striped=True, highlightOnHover=True, withBorder=True, withColumnBorders=True)
    else :
        return ""

# Grille de score en fonction de la variable sélectionnée
@callback(
    Output('effectif-modalites', 'figure'),
    [Input('dropdown-grid-score', 'value'),
     Input('main-dropdown', 'value')]
)

def update_score_grid_graph(selected_variable, selected_model):
    if selected_model == "Cash Loans" :
        data_filtered = grid_score_cash[grid_score_cash["Variable"] == selected_variable]
    elif selected_model == "Revolving Loans" :
        data_filtered = grid_score_revolving[grid_score_revolving["Variable"] == selected_variable]
        
    # effectif/modalités
    fig1 = px.pie(data_filtered, 
          names="Modalités", 
          values='effectif',
          height=800
          )

    # notes/modalités
    fig2 = px.bar(data_filtered, y="Modalités", x='Note', orientation='h', text_auto=True)

    # taux de défaut/modalités
    fig3 = px.line(data_filtered, x="Modalités",y="tx_defaut", markers=True, text="tx_defaut")
    fig3.update_traces(textposition="top right")

    # tableau
    fig4 =  go.Table(
    header=dict(
        values=["Modalités","Coefficient","p-value"],
        font=dict(size=15),
        align="center"
    ),
    cells=dict(
        values=[data_filtered[k].tolist() for k in data_filtered.columns[[1,2,4]]],
        align = "center")
    )

    # mettre plusieurs graphes côte à côte
    fig = make_subplots(rows=2, cols=2, subplot_titles=("Répartition de l'effectif de la modalité", 'Notes par modalité', "Taux de défaut en fonction de la modalité","Statistiques"), 
        specs=[[{"type": "pie"}, {"type": "bar"}],
        [{"type": "scatter"}, {"type": "pie"}]]
        )


    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)
    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)
    for trace in fig3.data:
        fig.add_trace(trace, row=2, col=1)
   
    fig.add_trace(fig4, row=2, col=2)

    # Update xaxis properties
    fig.update_xaxes(title_text="Notes", row=1, col=2)
    fig.update_xaxes(title_text="Modalités", row=2, col=1)

    # Update yaxis properties
    fig.update_yaxes(title_text="Modalités", row=1, col=2, side="right")
    fig.update_yaxes(title_text="Taux de défaut", row=2, col=1)
    

    # Mettre à jour la disposition de la figure
    fig.update_layout(title_text='Dashboard', 
        title_x=0.5, template='simple_white' , 
                      margin=dict(l=0, r=0, t=100, b=100),
                      legend=dict(orientation='h', x=0, y=0.5)
                          )
   
    return fig.to_dict()


@callback(
    Output('repartition-target', 'figure'),
    [Input('dropdown-repartition', 'value'),
     Input('main-dropdown', 'value')]
)

def update_repartition(selected_data,selected_model):
    data_repartition = pd.DataFrame()
    if selected_model == 'Cash Loans':
        if selected_data == "data_train" :
            data_repartition = data_train_cash
        else :
            data_repartition = data_test_cash
    elif selected_model == 'Revolving Loans':
        if selected_data == "data_train" :
            data_repartition = data_train_revolving
        else :
            data_repartition = data_test_revolving
   
     # Création du displot avec ff.displot
    fig = ff.create_distplot(
         [data_repartition['Note'][data_repartition['TARGET'] == 0], 
          data_repartition['Note'][data_repartition['TARGET'] == 1]],
         group_labels=['Target = 0', 'Target = 1'],
         colors=['blue', 'red'], 
         show_hist=False,
         show_rug=False
     )

     # Mise en forme du titre et des axes
    fig.update_layout(
         title=f'Distribution de TARGET en fonction de la Note sur {selected_data} pour {selected_model}',
         xaxis_title='Note',
         yaxis_title='Fréquence',
         template = "simple_white"
     )

    return fig
