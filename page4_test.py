import dash
import pandas as pd
from dash import Input, Output, State, html, dcc, dash_table, MATCH, ALL, ctx
import dash_mantine_components as dmc
from models.callable import DecisionExpertSystem
# from src.preprocessing import DecisionTreeDiscretizer
# from models.callable import Dataset, ExpertSystem

df=pd.read_csv("data/application_train_vf.csv",parse_dates=["date_mensuelle"], index_col=0)

# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Liste des champs pour l'interface utilisateur
fields = ["NAME_CONTRACT_TYPE","OCCUPATION_TYPE", "NAME_EDUCATION_TYPE" , "CB_NB_CREDIT_CLOSED", "CB_DAYS_CREDIT", "AMT_CREDIT",
          "CB_AMT_CREDIT_SUM", "AMT_INCOME_TOTAL", "AMT_GOODS_PRICE", "DAYS_BIRTH", "DAYS_EMPLOYED", "DAYS_REGISTRATION"]

# Liste des variables catégorielles et numériques
categorical_vars = ["NAME_CONTRACT_TYPE", "OCCUPATION_TYPE", "NAME_EDUCATION_TYPE"]
numeric_vars = ["CB_NB_CREDIT_CLOSED", "CB_DAYS_CREDIT", "AMT_CREDIT",
                "CB_AMT_CREDIT_SUM", "AMT_INCOME_TOTAL", "AMT_GOODS_PRICE", "DAYS_BIRTH", "DAYS_EMPLOYED", "DAYS_REGISTRATION"]

# Fonction pour créer un dropdown pour les variables catégorielles
def create_categorical_dropdown(id, label):
    return dmc.Select(
        id=id,
        label=label,
        data=[{'value': i, 'label': i} for i in df[label].unique().tolist()],
        value=df[label].unique()[0]
    )

# Fonction pour créer un champ de saisie numérique pour les variables numériques
def create_numeric_input(id, label):
    return dmc.NumberInput(
        id=id,
        label=label,
        value=1
    )

# Définition du layout de l'application
app.layout = html.Div(
    children=[
        html.Div(
            dmc.Title(children='CREDIT RISK PLATFORM', order=3, style={'font-family': 'IntegralCF-ExtraBold', 'text-align': 'center', 'color': 'slategray'}),
            style={'margin': '20px auto'}  # Marges sur les côtés et centrage horizontal
        ),
        html.Div(
            dmc.SimpleGrid( 
                cols=4, 
                children=[
                    html.Div([create_categorical_dropdown(f"dropdown-{field}", field) if field in categorical_vars else create_numeric_input(f"input-{field}", field) for field in fields[0:3]], className='row'),
                    html.Div([create_categorical_dropdown(f"dropdown-{field}", field) if field in categorical_vars else create_numeric_input(f"input-{field}", field) for field in fields[3:6]], className='row'),
                    html.Div([create_categorical_dropdown(f"dropdown-{field}", field) if field in categorical_vars else create_numeric_input(f"input-{field}", field) for field in fields[6:9]], className='row'),
                    html.Div([create_categorical_dropdown(f"dropdown-{field}", field) if field in categorical_vars else create_numeric_input(f"input-{field}", field) for field in fields[9:12]], className='row')
                ],
                id='fields-container',
                style={'margin': '0 auto 20px'}  # Marge en bas et centrage horizontal
            )
        ),
        html.Div(
            html.Button('Submit request', id='submit-button', n_clicks=0, style={'background-color': 'blue', 'padding': '10px 20px', 'font-size': '16px'}),
            style={'text-align': 'center', 'margin': '0 auto 20px'}  # Centrage horizontal et marge en bas
        ),
        html.Div([
    dmc.Container(
        [
            # Zone de texte pour la décision, stylisée et centrée dans un Paper
            dmc.Paper(
                html.Div("Votre décision de crédit s'affichera ici", id="decision", style={'textAlign': 'center', 'padding': '20px'}),
                withBorder=True,
                radius="md",
                shadow="xs",
                p="md",
                style={'maxWidth': '600px', 'margin': '40px auto', 'backgroundColor': '#f0f0f0'}
            ),
            # Ajoutez ici d'autres composants de votre application...
        ],
        style={'padding': '20px'}
    )
], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#eaeaea'}),
        html.Div(
            dmc.Progress(id='probability', value=55, className='progressbar', color='green', label='55%', size='xl'),
            style={'margin': '0 auto 20px'}  # Marge en bas et centrage horizontal
        ),
        html.Div(id='output-container')  # Placeholder pour afficher les résultats de la soumission
    ],
    style={'max-width': '800px', 'margin': 'auto'}  # Centrage horizontal
)



# Callback pour traiter la soumission des données et afficher les résultats
@app.callback(
        Output('decision', 'children'),
        Output('decision','style'),
        Output('dropdown-NAME_CONTRACT_TYPE', 'value'),
        Output('dropdown-OCCUPATION_TYPE', 'value'),
        Output('dropdown-NAME_EDUCATION_TYPE', 'value'),
        Output('input-CB_NB_CREDIT_CLOSED', 'value'),
        Output('input-CB_DAYS_CREDIT', 'value'),
        Output('input-AMT_CREDIT', 'value'),
        Output('input-CB_AMT_CREDIT_SUM', 'value'),
        Output('input-AMT_INCOME_TOTAL', 'value'),
        Output('input-AMT_GOODS_PRICE', 'value'),
        Output('input-DAYS_BIRTH', 'value'),
        Output('input-DAYS_EMPLOYED', 'value'),
        Output('input-DAYS_REGISTRATION', 'value'),
        
        Input('submit-button', 'n_clicks'),
        
        State('dropdown-NAME_CONTRACT_TYPE', 'value'),
        State('dropdown-OCCUPATION_TYPE', 'value'),
        State('dropdown-NAME_EDUCATION_TYPE', 'value'),
        State('input-CB_NB_CREDIT_CLOSED', 'value'),
        State('input-CB_DAYS_CREDIT', 'value'),
        State('input-AMT_CREDIT', 'value'),
        State('input-CB_AMT_CREDIT_SUM', 'value'),
        State('input-AMT_INCOME_TOTAL', 'value'),
        State('input-AMT_GOODS_PRICE', 'value'),
        State('input-DAYS_BIRTH', 'value'),
        State('input-DAYS_EMPLOYED', 'value'),
        State('input-DAYS_REGISTRATION', 'value'),
        prevent_initial_call=True
)
def update_output(n_clicks, *values):
    if ctx.triggered_id == 'submit-button':
        field_values = {}
        # Ajout des valeurs des dropdowns pour les variables catégorielles
        for i, field in enumerate(categorical_vars):
            field_values[field] = values[i]

        # Ajout des valeurs des champs de saisie numérique pour les variables numériques
        for i, field in enumerate(numeric_vars):
            field_values[field] = values[i + len(categorical_vars)]
        
        data = DecisionExpertSystem(field_values)
        data.transform_columns()
        data.score()
        decision, decision_color = data.get_decision()
        
        # Mise à jour du style de l'élément 'decision' avec la couleur obtenue
        decision_style = {'textAlign': 'center', 'padding': '20px', 'backgroundColor': decision_color}
        
        return decision, decision_style, *values

if __name__ == '__main__':
    app.run_server(debug=True)
