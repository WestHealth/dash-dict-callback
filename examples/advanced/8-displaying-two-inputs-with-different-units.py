import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash_dict_callback import DashDictCallbackPlugin

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, plugins=[DashDictCallbackPlugin])

app.layout = html.Div([
    html.Div('Convert Temperature'),
    'Celsius',
    dcc.Input(
        id="celsius",
        value=0.0,
        type="number"
    ),
    ' = Fahrenheit',
    dcc.Input(
        id="fahrenheit",
        value=32.0,
        type="number",
    ),
])

@app.dict_callback(
    Output("celsius", "value"),
    Output("fahrenheit", "value"),
    Input("celsius", "value"),
    Input("fahrenheit", "value"),
)
def sync_input(inputs, states):
    celsius=inputs['celsius.value']
    fahrenheit=inputs['fahrenheit.value']
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "celsius":
        inputs['fahrenheit.value'] = None if celsius is None else (float(celsius) * 9/5) + 32
    else:
        inputs['celsius.value'] = None if fahrenheit is None else (float(fahrenheit) - 32) * 5/9
    return inputs

if __name__ == "__main__":
    app.run_server(debug=True)
