from dash import Dash, html, dcc,Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import dash_mantine_components as dmc

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
    dmc.Title("Contact", order=3, style={'float': 'right', 'width': '50%', 'textAlign': 'center'}),


# dmc.Badge(
#         "Cécile HUANG",
#         leftSection=dmc.Avatar(
#             src="https://media.licdn.com/dms/image/D4E03AQEnsX3GCq2m-Q/profile-displayphoto-shrink_800_800/0/1695562539243?e=1718236800&v=beta&t=5vKndKk0rwOoIY11teaMh0Ef1NO3bXdEtEfe8gnJnqc",
#             size="lg",
#             radius="xl",
#             mr=1,
#         ),
#         sx={"paddingLeft": 0},
#         size="xl",
#         radius="xl",
#         color="teal",
#         # href = "https://community.plotly.com/t/dash-mantine-components/58414"
#     ),

#     dmc.Anchor(
#     "Dash Mantine Components Announcement",
#     href="https://community.plotly.com/t/dash-mantine-components/58414",
# ),

#     html.Br(),html.Br(),html.Br(),

#     dmc.Badge("Jynaldo JEANNOT",leftSection=dmc.Avatar(src="https://media.licdn.com/dms/image/D5603AQE_h5V9DB5Dag/profile-displayphoto-shrink_200_200/0/1694464803267?e=1718236800&v=beta&t=W0hcOtpbiewCGVQeNn6hPe5bCgovBbRdkMg6kRXv-_o",    size="lg",    radius="xl",    mr=1,),sx={"paddingLeft": 0},size="xl",radius="xl",color="blue"),

#     html.Br(),
#     dmc.Badge("Yoan JSEM",leftSection=dmc.Avatar( src="https://media.licdn.com/dms/image/D4E03AQG9ya945acRxw/profile-displayphoto-shrink_800_800/0/1700774257624?e=1718236800&v=beta&t=mAckE_Vxw0RrqBG56T6rJ1EkQrpEYrGqNWXphf0F_lg", size="lg", radius="xl", mr=1,),sx={"paddingLeft": 0},size="xl",radius="xl",color="violet"), 

#     html.Br(),
#     dmc.Badge("Alice LIU",leftSection=dmc.Avatar( src="https://media.licdn.com/dms/image/D4E03AQHtWufhFZkwlQ/profile-displayphoto-shrink_200_200/0/1665177569585?e=1718236800&v=beta&t=sMpohGzkNcK_Jt8eseqkxfbSzgjKat5GhYVOWkI1_PY", size="lg", radius="xl", mr=1,),sx={"paddingLeft": 0},size="xl",radius="xl",color="yellow"), 

    html.Div([
    html.Div([
        html.A(
            dmc.Tooltip(
                dmc.Avatar(
                    src="https://media.licdn.com/dms/image/D4E03AQEnsX3GCq2m-Q/profile-displayphoto-shrink_800_800/0/1695562539243?e=1718236800&v=beta&t=5vKndKk0rwOoIY11teaMh0Ef1NO3bXdEtEfe8gnJnqc",
                    size="lg",
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
                    size="lg",
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
                    size="lg",
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
                    size="lg",
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
])



], 


style={'overflow': 'hidden'})  # Assure que le contenu ne dépasse pas la taille de la div parente



    ]


)