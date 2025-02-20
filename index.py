from dash import html, dcc
from dash.dependencies import Input, Output
from home import create_page_home
from page_2 import create_page_2
from page_3 import create_page_3
from page_4 import create_page_4
from page_5 import create_page_5
from app import app

server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/artists':
        return create_page_2()
    if pathname == '/listen':
        return create_page_3()
    if pathname == '/stats':
        return create_page_5()

    else:
        return create_page_home()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(host='0.0.0.0', port=port, debug=False)