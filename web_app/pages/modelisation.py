from dash import Dash, html, dcc,Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# layout = html.P("zae!")

data=pd.read_csv("../data/application_train_vf.csv",parse_dates=["date_mensuelle"], index_col=0)
data["date_annee"]=data["date_mensuelle"].dt.year

grid_score = pd.read_excel("../data/grille_de_score.xlsx",index_col=0)

data_test = pd.read_csv("../../data/data_test_all.csv",sep=',')
data_test = pd.read_csv("../../data/data_test_all.csv",sep=',')

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

df_logit_results = pd.DataFrame(logit_results, columns=["Variable", "Modalités", "Coefficient", "std err", "z", "P>|z|", "[0.025, 0.975]"])

layout = html.Div(
    [
        html.Div(
            html.H1(children='Modélisation', style={'textAlign': 'center'}),
            style={'margin-bottom': '20px'}
        ),

        html.Div(
            [
                html.Label('Choix du modèle'),
                dcc.Dropdown(
                    options=[
                        {'label': 'Loans', 'value': 'FLAG_MOBIL'},
                        {'label': 'Revolving', 'value': 'FLAG_EMP_PHONE'},
                        {'label': 'Les deux', 'value': 'Les deux'},
                    ],
                    value='Loans',id='dropdown-logit'
                ),

            ],
            style={'padding': 10, 'flex': 1}
        ),
      
      html.Div(id='logit-results'),

      html.Div(
            html.H3(children='Grille de score', style={'textAlign': 'center'}),
            style={'margin-bottom': '20px'}
        ),

        html.Br(),

        html.Div(
            [
                html.Label('Choix de la variable'),
                dcc.Dropdown(
                    options=[
                        {'label': 'AMT_CREDIT_NORM', 'value': 'AMT_CREDIT_NORM'},
                        {'label': 'BORROWER_AGE', 'value': 'BORROWER_AGE'},
                        {'label': 'BORROWER_SENIORITY', 'value': 'BORROWER_SENIORITY'},
                    ],
                    value='AMT_CREDIT_NORM',id='dropdown-grid-score'
                ),

            ],
            style={'padding': 10, 'flex': 1}
        ),

        dcc.Graph(id='effectif-modalites'),

        html.Div(
            html.H3(children='Répartition des notes en fonction de la target', style={'textAlign': 'center'}),
            style={'margin-bottom': '20px'}
        ),

    ],
    style={'display': 'flex', 'flexDirection': 'column'}
)

# Callback pour mettre à jour l'affichage du DataFrame en fonction de la sélection du dropdown
@callback(
    Output('logit-results', 'children'),
    [Input('dropdown-logit', 'value')]
)
def update_results(selected_model):
    if selected_model == 'Les deux':
        # Afficher df_logit_results
        return html.Table(
            [
                html.Thead(  # En-tête de la table
                    html.Tr([html.Th(col) for col in df_logit_results.columns])
                ),
                html.Tbody(  # Corps de la table
                    [html.Tr([html.Td(df_logit_results.iloc[i][col]) for col in df_logit_results.columns]) for i in
                     range(len(df_logit_results))]
                )
            ],
            className='table table-sm' # table pour CSS et table-sm pour small
        )
    else:
        return html.Div()


@callback(
    Output('effectif-modalites', 'figure'),
    [Input('dropdown-grid-score', 'value')]
)
def update_score_grid_graph(selected_variable):
    if selected_variable == "AMT_CREDIT_NORM":
        # Filtrer les données de la grille de score pour la variable sélectionnée
        variable_data = grid_score[grid_score["Variable"] == "AMT_CREDIT_NORM"]


        # Créer le premier histogramme pour les effectifs
        # fig1 = px.bar(variable_data, 
        #               x="Modalités", 
        #               y='effectif'
        #               )
        
        fig1 = px.pie(variable_data, 
                      names="Modalités", 
                      values='effectif'
                      )
        #fig.add_trace(fig1,row=1,col=1)
        # fig1.update_layout(title='Effectif/Modalités', xaxis_title="Modalités", template='plotly_dark')  # Utilisation du template 'plotly_dark'
        # fig1.update_xaxes(title_text='Modalités', categoryorder='total ascending', showgrid=False)  # Désactivation de la grille
        # fig1.update_yaxes(title_text='Effectif', showgrid=False)  # Désactivation de la grille

        # Créer le deuxième histogramme horizontal pour les notes
        fig2 = px.bar(variable_data, y="Modalités", x='Note', orientation='h')

        # fig2.update_layout(title='Modalités/Notes', template='plotly_dark')  # Utilisation du template 'plotly_dark'
        # fig2.update_yaxes(title_text='Modalités', categoryorder='total ascending', showgrid=False)  # Désactivation de la grille
        # fig2.update_xaxes(title_text='Notes', showgrid=False)  # Désactivation de la grille

        fig3 = px.line(variable_data, x="Modalités",y="tx_defaut")

        fig4 =  go.Table(
        header=dict(
            values=["Modalités","Coefficient","p-value"],
            font=dict(size=10),
            align="left"
        ),
        cells=dict(
            values=[variable_data[k].tolist() for k in variable_data.columns[1:4]],
            align = "left")
    )

        # Créer une figure avec deux sous-traces
        fig = make_subplots(rows=2, cols=2, subplot_titles=('Effectif/Modalités', 'Modalités/Notes', "Modalités/Taux Défaut","Table"), 
                            specs=[[{"type": "pie"}, {"type": "bar"}],
                                    [{"type": "scatter"}, {"type": "pie"}]]
                            )
                
        
        # Ajouter les deux graphiques aux sous-traces
        for trace in fig1.data:
            fig.add_trace(trace, row=1, col=1)
        for trace in fig2.data:
            fig.add_trace(trace, row=1, col=2)
        for trace in fig3.data:
            fig.add_trace(trace, row=2, col=1)
        #for trace in fig4:
        fig.add_trace(fig4, row=2, col=2)
        
        # Mettre à jour la disposition de la figure
        fig.update_layout(title_text='Title')

        return fig.to_dict()
    else:
        return {}
