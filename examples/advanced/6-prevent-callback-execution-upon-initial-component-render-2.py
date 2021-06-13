import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_dict_callback import DashDictCallbackPlugin


import urllib
app = dash.Dash(__name__, suppress_callback_exceptions=True, plugins=[DashDictCallbackPlugin])
server = app.server
app.layout = html.Div([
    dcc.Location(id='url'),
    html.Div(id='layout-div'),
    html.Div(id='content')
])

@app.dict_callback(Output('content', 'children'), Input('url', 'pathname'))
def display_page(i,s):
    return {'content.children': html.Div([
        dcc.Input(id='input', value='hello world'),
        html.Div(id='output')
    ])}

@app.dict_callback(Output('output', 'children'), Input('input', 'value'), prevent_initial_call=True)
def update_output(inputs, states):
    print('>>> update_output')
    return {'output.children': inputs['input.value']}

@app.dict_callback(Output('layout-div', 'children'), Input('input', 'value'), prevent_initial_call=True)
def update_layout_div(inputs, states):
    print('>>> update_layout_div')
    return {'layout-div.children': inputs['input.value']}


if __name__ == '__main__':
    app.run_server(debug=True)
