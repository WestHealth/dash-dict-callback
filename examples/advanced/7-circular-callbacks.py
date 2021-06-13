import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from dash_dict_callback import DashDictCallbackPlugin

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, plugins=[DashDictCallbackPlugin])

app.layout = html.Div(
    [
        dcc.Slider(
            id="slider-circular", min=0, max=20, 
            marks={i: str(i) for i in range(21)}, 
            value=3
        ),
        dcc.Input(
            id="input-circular", type="number", min=0, max=20, value=3
        ),
    ]
)
@app.dict_callback(
    Output("input-circular", "value"),
    Output("slider-circular", "value"),
    Input("input-circular", "value"),
    Input("slider-circular", "value"),
)
def callback(inputs, states):
    ctx = dash.callback_context
    if not ctx.triggered:
        return {}
    trigger_prop = ctx.triggered[0]["prop_id"]
    value = inputs[trigger_prop]
    return {'input-circular.value': value,
            'slider-circular.value': value}

if __name__ == '__main__':
    app.run_server(debug=True)
