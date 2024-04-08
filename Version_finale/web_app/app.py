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
import page1 
from page1 import layout as page1_layout, update_images

# juste des notes

#BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css"
# app = dash.Dash(external_stylesheets=[BS]) mettre un lien bootstrap en particulier

# link fontawesome to get the chevron icons
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME] 
  
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
                    [html.Img(src="/assets/methodologie.png", height="20px", style={"margin-right": "5px"}), "Méthodologie"],
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
            dbc.NavLink("Analyse des variables", href="/page-1/1"),
            dbc.NavLink("Modèle et grille de score", href="/page-1/2"),
            dbc.NavLink("Quantification des résultats", href="/page-1/3"),
        ],
        id="submenu-1-collapse",
    ),
]

submenu_2 = [
    html.Li(
        dbc.Row(
            [
                dbc.Col(
                    [html.Img(src="/assets/croissance.png", height="20px", style={"margin-right": "5px"}), "Utilité Métier"],
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
        [
            dbc.NavLink("Page 2.1", href="/page-2/1"),
            dbc.NavLink("Page 2.2", href="/page-2/2"),
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

        #html.H4("NEXIALOG x MoSEF", className="display-6"),
        html.Hr(),
        dbc.Nav(submenu_1 + submenu_2, vertical=True),
    ],
    style=SIDEBAR_STYLE,
    id="sidebar",
)

# Layout for the home page
home_page_content = html.Div(
    [
        html.H1("Modélisation de la PD bâloise"),
        html.P("Cécile Huang, Jynaldo Jeannot, Yoan Jsem, Alice Liu"),
    ],
    style=CONTENT_STYLE
)

content = html.Div(id="page-content", style=CONTENT_STYLE, children=[
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

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

page1_content = page1_layout(app)

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
    if pathname in ["/", "/page-1/1"]:
        return page1_content
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
    
@app.callback(
    Output('image-container', 'children'),
    [Input('contract-type-dropdown', 'value')]
)
def update_images_callback(selected_contract):
    return update_images(selected_contract)
    

    
if __name__ == '__main__':
    app.run_server(debug=True, port=8087)
