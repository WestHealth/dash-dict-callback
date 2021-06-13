import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_dict_callback import DashDictCallbackPlugin

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, plugins=[DashDictCallbackPlugin])

app.layout = html.Div([
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div(["Input: ",
              dcc.Input(id='my-input', value='initial value', type='text')]),
    html.Br(),
    html.Div(id='my-output'),

])


@app.dict_callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(inputs, states):
    input_value = inputs['my-input.value']
    return {'my-output.children': 'Output: {}'.format(input_value)}


if __name__ == '__main__':
    app.run_server(debug=True)
