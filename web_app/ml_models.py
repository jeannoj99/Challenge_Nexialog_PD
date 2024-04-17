import dash
from dash import dcc, html, dash_table, Output, Input
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pickle
from utils.utils_from_cecile import subplot_segment_default_rate, show_risk_stability_overtime, plot_feature_importances

pd_summary_ml_cash = pd.DataFrame({'Segment': [0, 1, 2, 3, 4, 5, 6],
                                   'LRA': [0.200602, 0.133405, 0.095642, 0.07068, 0.049801, 0.032432, 0.018837],
                                   'MOC_A': [0.002566,0.001639,0.00125,0.001055,0.000976,0.000871,0.000889],
                                   'MOC_C': [0.006757,0.004361,0.003314,0.002846,0.002388,0.002244,0.002452],
                                   'PD': [0.209925, 0.139404, 0.100207, 0.074581, 0.053165, 0.035547, 0.022177]})

pd_summary_ml_revolving = pd.DataFrame({'Segment': [0, 1, 2, 3, 4, 5, 6],
                                        'LRA': [0.292775, 0.169922, 0.116582, 0.08708, 0.05132, 0.033209, 0.011151],
                                        'MOC_A': [0.022545,0.010349,0.00638,0.004107,0.002763,0.002175,0.001705],
                                        'MOC_C': [0.090857,0.027752,0.016639,0.011231,0.007735,0.005281,0.003862],
                                        'PD': [0.406178, 0.208023, 0.139601, 0.102417, 0.061817, 0.040665, 0.016718]})


pd_summaries_ml ={
    "Cash loans": pd_summary_ml_cash,
    "Revolving loans": pd_summary_ml_revolving
}

ginis_ml_models = {
    "Cash loans":0.3449805416329841,
    "Revolving loans": 0.38072400582710175
}

models_challenger = {}

with open("../models/challenger_model_cash_loans.pkl","rb") as f:
    models_challenger["Cash loans"] = pickle.load(f)

with open("../models/challenger_model_revolving_loans.pkl","rb") as f:
    models_challenger["Revolving loans"] = pickle.load(f)


datas_challenger = {
    "Cash loans":{
        "train":pd.read_csv("../data/synthetic_data_test_ml_models_cash.csv"),
        "test":pd.read_csv("../data/synthetic_data_test_ml_models_cash.csv")
    },
    "Revolving loans":{
        "train":pd.read_csv("../data/synthetic_data_test_ml_models_revolving.csv"),
        "test":pd.read_csv("../data/synthetic_data_test_ml_models_revolving.csv")
    }
}

shap_graphs_src = {
    "Cash loans" : "/assets/shap_summary_plot_cash.png",
    "Revolving loans": "/assets/shap_summary_plot_revolving.png"
}

def plot_feature_importances(model):
    
    # Obtenir les importances des features avec 'gain' comme mesure de l'importance
    importance = model.feature_importances_
    features_df = pd.DataFrame({
        'Feature': model.feature_names_in_,
        'Importance': importance
    }).sort_values(by='Importance', ascending=False)
    
    # Créer et retourner un graphique pour les features importances
    fig = px.bar(
        features_df, 
        x='Importance', 
        y='Feature', 
        orientation='h', 
        title='Représentation des Feature importances',
        labels={'Feature': 'Feature', 'Importance': 'Importance'},
        height=500,  # Hauteur du graphique
        width=700   # Largeur du graphique
    )
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        plot_bgcolor='white',
        xaxis_title='Importance Score',
        yaxis_title='Features'
    )
    return fig

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dmc.Title("Modèles de Machine Learning", order=1, style={'textAlign': 'center', 'marginBottom': '10px'}),
    dcc.Dropdown(
        id='model-choice',
        options=[
            {'label': 'Cash loans', 'value': 'Cash loans'},
            {'label': 'Revolving loans', 'value': 'Revolving loans'}
        ],
        value='Cash loans',  # Default value
        clearable=False
    ),

    html.Div([
        dmc.Title("Interprétation du modèles", order=3, style={'textAlign': 'center', 'marginBottom': '10px'}),
        html.Div([
            dcc.Graph(id='feature-importances'),
            html.Img(id='shap-image', src='/assets/shap_summary_plot_cash.png', style={'width': 'auto', 'height': '500'})
        ], style={'display': 'flex', 'justifyContent': 'space-around'})  # Graphs side by side
    ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '5px', 'margin': '20px'}),

    dbc.Card(
        [ dmc.Title("Evaluation du modèle sur le test", order=5, style={'textAlign': 'center', 'marginBottom': '10px'}),
            html.Div(
            id='gini-score-challenger', 
            style={'textAlign': 'center', 'fontWeight': 'bold'}  # Texte en gras
        )],
        body=True,
        style={'maxWidth': '200px', 'margin': '20px auto', 'padding': '10px','backgroundColor': 'skyblue'}
    ),
    html.Div([
        html.H2("Quantification du risque", style={'textAlign': 'center'}),
        html.Div([
            dcc.Graph(id="risk-stability-overtime"),
            dcc.Graph(id='density-plot-challenger')
        ], style={'display': 'flex', 'justifyContent': 'space-around'}),  # Two graphs side by side
        
        html.Div([
            dcc.Graph(id='segment-challenger')  # Third graph below and centered
        ], style={'width': '60%', 'margin': '0 auto'}),
        
    html.Div([
            dmc.Title("Tableau résumé de la PD", order=3 , style={'textAlign': 'center', 'marginBottom': '10px'}),
            dash_table.DataTable(
        id='pd-summary',
        style_table={'overflowX': 'auto'},
        style_cell={
            'minWidth': '50px',  # Réduire la largeur minimum pour s'adapter mieux au contenu
            'width': 'auto',     # Laisser la largeur s'ajuster automatiquement
            'maxWidth': 'auto', # Limite supérieure de la largeur
            'whiteSpace': 'normal'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
        ],
        style_as_list_view=True
)])
    ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '5px', 'margin': '20px'})
])




@app.callback(
    [Output('feature-importances', 'figure'),
     Output('shap-image', 'src'),
     Output('gini-score-challenger', 'children')],
      [Input('model-choice', 'value')]
)
def update_interpretable_ml(model_choice):
    
    # Generate figures
    fig_importances = plot_feature_importances(models_challenger[model_choice])
    
    shap_src = shap_graphs_src[model_choice]
    gini_display = f"Gini Score : {ginis_ml_models[model_choice]:.3f}"
    
    return fig_importances, shap_src, gini_display

# Callbacks to update graphs and table based on model choice
@app.callback(
    [Output('risk-stability-overtime', 'figure'),
     Output('density-plot-challenger', 'figure'),
     Output('segment-challenger', 'figure'),
     Output('pd-summary', 'data')],
    [Input('model-choice', 'value')]
)
def update_risk_quantification_ml(model_choice):
    # Example calculations (to replace with actual model methods)
    feature_importances = pd.DataFrame({
        'Feature': ['Feature1', 'Feature2', 'Feature3'],
        'Importance': np.random.rand(3)
    })
    shap_values = pd.DataFrame({
        'Feature': ['Feature1', 'Feature2', 'Feature3'],
        'SHAP': np.random.randn(3)
    })
   
    # # Generate figures
    # fig_importances = px.bar(feature_importances, x='Feature', y='Importance', title="Feature Importances")
    
    # fig_shap = px.bar(shap_values, x='Feature', y='SHAP', title="SHAP Values")
    
    data0 = datas_challenger[model_choice]["test"]['Note'][datas_challenger[model_choice]["test"]['TARGET'] == 0]
    data1 = datas_challenger[model_choice]["test"]['Note'][datas_challenger[model_choice]["test"]['TARGET'] == 1]
    fig_density = ff.create_distplot(
         [data0, data1],
         group_labels=['Target = 0', 'Target = 1'],
         colors=['blue', 'red'], 
         show_hist=False,
         show_rug=False
     )
    
    fig_density.update_layout(
         title=f'Distribution des notes suivant la cible sur {model_choice} (test)',
         xaxis_title='Note',
         yaxis_title='Fréquence',
         xaxis=dict(range=[min(data0.min(), data1.min()), max(data0.max(), data1.max())])
     )
    
    risk_fig = show_risk_stability_overtime(datas_challenger[model_choice]["test"], "Segment")
    
    risk_fig.update_layout(
        title = f"Stabilité en risque des segments dans le temps pour {model_choice} (test)"
    )
    
    segment_fig = subplot_segment_default_rate(datas_challenger[model_choice]["test"])
    
    segment_fig.update_layout(
        title = f"Répartition sur les segments et taux de défaut par segment pour {model_choice} (test)"
    )
    # Update PD summary table
    pd_summary_data = pd_summaries_ml[model_choice].to_dict('records')

    # Gini score display
    gini_display = f"Gini Score: {ginis_ml_models[model_choice]:.3f}"

    return  risk_fig, fig_density, segment_fig, pd_summary_data




if __name__ == '__main__':
    app.run_server(debug=True)
