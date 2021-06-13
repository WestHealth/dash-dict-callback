# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_dict_callback import DashDictCallbackPlugin

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, plugins=[DashDictCallbackPlugin])

app.layout = html.Div([
    dcc.Input(id='input-1-state', type='text', value='Montréal'),
    dcc.Input(id='input-2-state', type='text', value='Canada'),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    html.Div(id='output-state')
])


@app.dict_callback(Output('output-state', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'),
              State('input-2-state', 'value'))
def update_output(inputs, states):
    n_clicks=inputs['submit-button-state.n_clicks']
    input1 = states['input-1-state.value']
    input2 = states['input-2-state.value']
    return {
        'output-state.children': 
          u'''
          The Button has been pressed {} times,
          Input 1 is "{}",
          and Input 2 is "{}"
          '''.format(n_clicks, input1, input2)
        }


if __name__ == '__main__':
    app.run_server(debug=True)
