#https://github.com/facultyai/dash-bootstrap-components/blob/main/examples/templates/multi-page-apps/sidebar-with-submenus/sidebar.py


"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location. There are three callbacks,
one uses the current location to render the appropriate page content, the other
two are used to toggle the collapsing sections in the sidebar. They control the
collapse component and the CSS that rotates the chevron icon respectively.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
import pages.analyse_des_variables as analyse_des_variables
import pages.modelisation as modelisation
import pages.quantification as quantification
import pages.octroi as octroi
import pages.derniere_page as derniere_page
import pages.backtesting as backtesting
import pages.ml_models as ml_models
from dash_bootstrap_templates import ThemeSwitchAIO
import dash_mantine_components as dmc
import os
from dash_iconify import DashIconify

# juste des notes

#BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css"
# app = dash.Dash(external_stylesheets=[BS]) mettre un lien bootstrap en particulier

# link fontawesome to get the chevron icons
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],suppress_callback_exceptions=True  
)





# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

submenu_1 = [
    html.Li(
        # use Row and Col components to position the chevrons
        dbc.Row(
            [
                dbc.Col(
                    [html.Img(src="/assets/methodologie.png", height="20px", style={"margin-right": "5px"}), 
                     html.Span("Méthodologie", style={"font-weight": "bold", "font-family": "Trebuchet MS, sans-serif"}), ],
                    width="auto",
                    style={"cursor": "pointer"}
                ),
                dbc.Col(
                    html.I(className="fas fa-chevron-right me-3"),
                    width="auto",
                ),
            ],
            className="my-1",
        ),
        style={"cursor": "pointer"},
        id="submenu-1",
    ),
    # we use the Collapse component to hide and reveal the navigation links
    dbc.Collapse(
        [
            dbc.NavLink("Analyse des variables", href="/analyse-des-variables", style={"font-family": "Trebuchet MS, sans-serif"}),
            dbc.NavLink("Modélisation", href="/modelisation", style={"font-family": "Trebuchet MS, sans-serif"}),
            dbc.NavLink("Quantification des résultats", href="/quantification", style={"font-family": "Trebuchet MS, sans-serif"}),
            dbc.NavLink("Modèle Challenger", href="/ml-model", style={"font-family": "Trebuchet MS, sans-serif"}),
            
        ],
        id="submenu-1-collapse",
    ),
]

submenu_2 = [
    html.Li(
        dbc.Row(
            [
                dbc.Col(
                    [html.Img(src="/assets/croissance.png", height="20px", style={"margin-right": "5px"}),
                     html.Span("Extensions", style={"font-weight": "bold", "font-family": "Trebuchet MS, sans-serif"})],
                    width="auto",
                    style={"cursor": "pointer"}
                ),
                dbc.Col(
                    html.I(className="fas fa-chevron-right me-3"),
                    width="auto",
                ),
            ],
            className="my-1",
        ),
        style={"cursor": "pointer"},
        id="submenu-2",
    ),
    dbc.Collapse(
        [   dbc.NavLink("Backtesting", href="/backtesting"),
            dbc.NavLink("Expert System Decision Tool", href="/octroi", style={"font-family": "Trebuchet MS, sans-serif"}),
            dbc.NavLink("En savoir plus", href="/en-savoir-plus", style={"font-family": "Trebuchet MS, sans-serif"})
        ],
        id="submenu-2-collapse",
    ),
]


sidebar = html.Div(
    [
       html.Div([
            html.Img(id="nexialog-logo", src="/assets/logo_nexialog.png", height="60px", style={"margin-right": "10px", "cursor": "pointer"}),
            html.Img(id="mosef-logo", src="/assets/logo_mosef.png", height="60px", style={"cursor": "pointer"}),
        ], style={"width": "60%", "margin": "auto", "text-align": "center"}),

        html.Hr(),
        dbc.Nav(submenu_1 + submenu_2, vertical=True),
    ],
    style=SIDEBAR_STYLE,
    id="sidebar",
)


home_page_content = dmc.Card(
    children=[
        dmc.CardSection(
            dmc.Image(
                src="/assets/page_accueil_nexialog2.PNG",
                height=705,
                #style={"objectFit": "contain"},
                #mt = "100px"
            ),
        ),
        dmc.Group(
            [
                dmc.Text("Composition de l'équipe", weight=500),
            ],
            position="center",
            mt="md",
            mb="xs",
        )
        ,
        dmc.Group([dmc.Badge("Cécile HUANG",leftSection=dmc.Avatar( src="https://media.licdn.com/dms/image/D4E03AQEnsX3GCq2m-Q/profile-displayphoto-shrink_800_800/0/1695562539243?e=1718236800&v=beta&t=5vKndKk0rwOoIY11teaMh0Ef1NO3bXdEtEfe8gnJnqc", size="md", radius="xl", mr=1,),sx={"paddingLeft": 0},size="xl",radius="xl",color="teal"), 
             dmc.Badge("Jynaldo JEANNOT",leftSection=dmc.Avatar(    src="https://media.licdn.com/dms/image/D5603AQE_h5V9DB5Dag/profile-displayphoto-shrink_200_200/0/1694464803267?e=1718236800&v=beta&t=W0hcOtpbiewCGVQeNn6hPe5bCgovBbRdkMg6kRXv-_o",    size="md",    radius="xl",    mr=1,),sx={"paddingLeft": 0},size="xl",radius="xl",color="blue"),
             dmc.Badge("Yoan JSEM",leftSection=dmc.Avatar( src="https://media.licdn.com/dms/image/D4E03AQG9ya945acRxw/profile-displayphoto-shrink_800_800/0/1700774257624?e=1718236800&v=beta&t=mAckE_Vxw0RrqBG56T6rJ1EkQrpEYrGqNWXphf0F_lg", size="md", radius="xl", mr=1,),sx={"paddingLeft": 0},size="xl",radius="xl",color="violet"), 
             dmc.Badge("Alice LIU",leftSection=dmc.Avatar( src="https://media.licdn.com/dms/image/D4E03AQHtWufhFZkwlQ/profile-displayphoto-shrink_200_200/0/1665177569585?e=1718236800&v=beta&t=sMpohGzkNcK_Jt8eseqkxfbSzgjKat5GhYVOWkI1_PY", size="md", radius="xl", mr=1,),sx={"paddingLeft": 0},size="xl",radius="xl",color="yellow"), 
                             ], 
        position="center"
        ),

        dmc.Button(
            "Bievenue dans CreditWise !",
            variant="light",
            color="blue",
            fullWidth=True,
            mt="md",
            radius="md",
        ),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"height": "100%"},
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"), 
    sidebar, 
    content,
    ], 
    style = {'background-color': '#F5F5F5'}
    )


# this function is used to toggle the is_open property of each Collapse
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# this function applies the "open" class to rotate the chevron
def set_navitem_class(is_open):
    if is_open:
        return "open"
    return ""


for i in [1, 2]:
    app.callback(
        Output(f"submenu-{i}-collapse", "is_open"),
        [Input(f"submenu-{i}", "n_clicks")],
        [State(f"submenu-{i}-collapse", "is_open")],
    )(toggle_collapse)

    app.callback(
        Output(f"submenu-{i}", "className"),
        [Input(f"submenu-{i}-collapse", "is_open")],
    )(set_navitem_class)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home_page_content
    if pathname in ["/", "/analyse-des-variables"]:
        return analyse_des_variables.layout
    elif pathname == "/modelisation":
        return modelisation.layout
    elif pathname == "/quantification":
        return quantification.layout
    elif pathname == "/octroi":
        return octroi.layout
    elif pathname == "/backtesting":
        return backtesting.layout
    elif pathname == "/en-savoir-plus":
        return derniere_page.layout
    elif pathname == "/ml-model":
        return ml_models.layout
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


# Define redirect to home page when clicking on logos
@app.callback(Output("url", "pathname"), [Input("nexialog-logo", "n_clicks"), Input("mosef-logo", "n_clicks")])
def redirect_to_home(n_clicks_nexialog, n_clicks_mosef):
    if n_clicks_nexialog is not None or n_clicks_mosef is not None:
        return "/"
    else:
        # If no clicks on logos, stay on current page
        return dash.no_update
    

    
if __name__ == "__main__":
    app.run_server(debug=True,host='0.0.0.0',port=5150)
