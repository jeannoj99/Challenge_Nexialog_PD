from dash import Dash, html, dcc,Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import dash_mantine_components as dmc
from dash_iconify import DashIconify

layout = html.Div(
    [
    dmc.Title("Curieux de tester de l'application ?"),

    html.Br(),

html.Div([
    # À gauche : dmc.Center
    dmc.Center([
        dmc.Image(
            src="/assets/qr_code.jpg",
            alt="qr_code",
            width=610,
            radius="md"
        )
    ], style={'float': 'left', 'width': '50%'}),  # Utilise 50% de la largeur de la div parente

    # À droite : dmc.Title
    dmc.Title("Pour nous contacter : ", order=2, style={'float': 'right', 'width': '50%', 'textAlign': 'center'}),

    html.Br(), html.Br(),

    html.Div([
    html.Div([
        html.A(
            dmc.Tooltip(
                dmc.Avatar(
                    src="https://media.licdn.com/dms/image/D4E03AQEnsX3GCq2m-Q/profile-displayphoto-shrink_800_800/0/1695562539243?e=1718236800&v=beta&t=5vKndKk0rwOoIY11teaMh0Ef1NO3bXdEtEfe8gnJnqc",
                    size=150,
                    radius="xl",
                ),
                label="Cécile HUANG",
                # position="bottom",
            ),
            href="https://www.linkedin.com/in/cecile-huang/",
            target="_blank",
            style={'textAlign': 'center'}
        ),
    ], style={'display': 'inline-block', 'margin-left' : '300', 'margin-right': '30px'}),

    html.Div([
        html.A(
            dmc.Tooltip(
                dmc.Avatar(
                    src="https://media.licdn.com/dms/image/D4E03AQG9ya945acRxw/profile-displayphoto-shrink_800_800/0/1700774257624?e=1718236800&v=beta&t=mAckE_Vxw0RrqBG56T6rJ1EkQrpEYrGqNWXphf0F_lg",
                    size=150,
                    radius="xl",
                ),
                label="Yoan JSEM",
                # position="bottom",
            ),
            href="https://www.linkedin.com/in/yoan-jsem/",
            target="_blank",
            style={'textAlign': 'center'}
        ),
    ], style={'display': 'inline-block', 'margin-left' : '0px','margin-right': '30px'}),
    html.Div([
        html.A(
            dmc.Tooltip(
                dmc.Avatar(
                    src="https://media.licdn.com/dms/image/D5603AQE_h5V9DB5Dag/profile-displayphoto-shrink_800_800/0/1694464803267?e=1718841600&v=beta&t=vnr3Nf-CrDcer-rERwUmETYH9s0PiT5bTN0H9LFXtcc",
                    size=150,
                    radius="xl",
                ),
                label="Jynaldo JEANNOT  ",
                # position="bottom",
            ),
            href="https://www.linkedin.com/in/jynaldo-jeannot99/",
            target="_blank",
            style={'textAlign': 'center'}
        ),
    ], style={'display': 'inline-block', 'margin-left' : '0px', 'margin-right': '30px'}),
    html.Div([
        html.A(
            dmc.Tooltip(
                dmc.Avatar(
                    src="https://media.licdn.com/dms/image/D4E03AQHtWufhFZkwlQ/profile-displayphoto-shrink_800_800/0/1665177569585?e=1718841600&v=beta&t=ZrcTU9iwhyJMtikbsfPly-RBhLrF_cL97QZyTQKZUZo",
                    size=150,
                    radius="xl",
                ),
                label="Alice LIU",
                # position="bottom",
            ),
            href="https://www.linkedin.com/in/alice-liu1/",
            target="_blank",
            style={'textAlign': 'center'}
        ),
    ], style={'display': 'inline-block', 'margin-left' : '0px', 'margin-right': '30px', 'textAlign': 'center'}),
]) ,

html.Br(style={'height': '2000px'}),

dmc.Timeline(
    active=6,
    bulletSize=20,
    lineWidth=2,
    style={"marginLeft": "60%", "marginTop": "50px"},
    # align = "right",
    children=[
        dmc.TimelineItem(
            title=dmc.Title("Analyse des variables", order=4),
            children=[
                dmc.Text(
                    [
                        "Revoir les ",
                        dmc.Anchor("analyses", href="/analyse-des-variables", size="sm"),
                        
                    ],
                    color="dimmed",
                    size="sm",
                ),
            ],
        ),
        dmc.TimelineItem(
            title=dmc.Title("Modélisation", order=4),
            children=[
                dmc.Text(
                    [
                        "Comparer les ",
                        dmc.Anchor("modèles", href="/modelisation", size="sm"),
                    ],
                    color="dimmed",
                    size="sm",
                ),
            ],
        ),
        dmc.TimelineItem(
            title=dmc.Title("Quantification des résultats",order=4),
            children=[
                dmc.Text(
                    [
                        "Revoir les ",
                        dmc.Anchor(
                            "résultats",
                            href="/quantification",
                            size="sm",
                        ),
                    ],
                    color="dimmed",
                    size="sm",
                ),
            ],
        ),
        dmc.TimelineItem(
            title=dmc.Title("Credit Risk Platform",order=4),
            children=[
                dmc.Text(
                    [
                        "Accéder à la  ",
                        dmc.Anchor("plateforme", href="/modelisation", size="sm"),
                        " d'octroi"
                    ],
                    color="dimmed",
                    size="sm",
                ),
            ],
        ),
        dmc.TimelineItem(
            title=dmc.Title("Backtesting",order=4),
            children=[
                dmc.Text(
                    [
                        "Revoir le ",
                        dmc.Anchor(
                            "backtesting",
                            href="#",
                            size="sm",
                        ),
                    ],
                    color="dimmed",
                    size="sm",
                ),
            ],
        ),
        dmc.TimelineItem(
            title=dmc.Title("Modèles de Machine Learning",order=4),
            children=[
                dmc.Text(
                    [
                        "Revoir le ",
                        dmc.Anchor(
                            "modèle challenger",
                            href="#",
                            size="sm",
                        ),
                    ],
                    color="dimmed",
                    size="sm",
                ),
            ],
        ),
        dmc.TimelineItem(
            [ 
                dmc.Text(
                    [
                        dmc.Anchor(
                            href="#",
                            size="sm",
                        ),
                        "Vous êtes bien arrivés à destination !",
                    ],
                    color="dimmed",
                    size="sm",
                ),
            ],
            title=dmc.Title("Merci !",order=4),
            lineVariant="dashed"
        ),
    ],
)



], 


style={'overflow': 'hidden'})  # Assure que le contenu ne dépasse pas la taille de la div parente



    ]


)