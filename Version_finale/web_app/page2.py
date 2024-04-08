from dash import html

def page2_layout(pathname):
    if pathname == "/page-2/1":
        return html.P("This is the content of page 2.1!")
    elif pathname == "/page-2/2":
        return html.P("This is the content of page 2.2. Yay!")
    elif pathname == "/page-2/3":
        return html.P("This is the content of page 2.3. Yay!")
