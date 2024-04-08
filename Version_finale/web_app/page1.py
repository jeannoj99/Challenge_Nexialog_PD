# page1.py

# Importez les modules nécessaires depuis dash
from dash import dcc, html

# Layout
def layout(app):  # Ajoutez l'argument app ici
    return html.Div([
        dcc.Dropdown(
            id='contract-type-dropdown',
            options=[
                {'label': 'Cash loans', 'value': 'Cash loans'},
                {'label': 'Revolving loans', 'value': 'Revolving loans'},
                {'label': 'Tous les contrats', 'value': 'All contracts'}
            ],
            value='All contracts',
            clearable=False,
            style={'width': '50%'}
        ),
        html.Br(),
        html.Div(id='image-container', children=[]),
    ])

# Callback pour afficher les images correspondant à la sélection
def update_images(selected_contract):
    if selected_contract == 'Cash loans':
        return [
            html.Img(src="/assets/page3/defaut_par_CHR.png", style={'width': '30%'}),
            html.Img(src='/assets/page3/hypothèsesCHRtest.jpg', style={'width': '30%'})
        ]
    elif selected_contract == 'Revolving loans':
        return [
            html.Img(src='/assets/page3/hypothèsesCHRtest.jpg', style={'width': '30%'})
        ]
    else:  # Tous les contrats
         return [
            html.Div([
                html.Div([
                    html.Img(src='/assets/page3/hypothèsesCHRtest.jpg', style={'width': '100%'})
                ], className='col-lg-6'),  # Première image à gauche pour les grands écrans
                html.Div([
                    html.Img(src='/assets/page3/defaut_par_CHR.png', style={'width': '100%'})
                ], className='col-lg-6'),  # Deuxième image à droite pour les grands écrans
            ], className='row'),  # Première ligne avec deux images
            html.Div([
                html.Div([
                    html.Img(src='/assets/page3/PD_par_seg.png', style={'width': '100%'})
                ], className='col-lg-6 mx-auto'),  # Troisième image centrée pour les grands écrans
            ], className='row mt-3')  # Marge supérieure pour séparer du contenu précédent
        ]