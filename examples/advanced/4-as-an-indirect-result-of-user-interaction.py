import dash
from dash.dependencies import Input, Output
import dash_html_components as html
from dash_dict_callback import DashDictCallbackPlugin
from datetime import datetime
import time

app = dash.Dash(plugins=[DashDictCallbackPlugin])
app.layout = html.Div(
    [
        html.Button("execute fast callback", id="button_3"),
        html.Button("execute slow callback", id="button_4"),
        html.Div(children="callback not executed", id="first_output_3"),
        html.Div(children="callback not executed", id="second_output_3"),
        html.Div(children="callback not executed", id="third_output_3"),
    ]
)


@app.dict_callback(
    Output("first_output_3", "children"),
    Input("button_3", "n_clicks"))
def first_callback(inputs, states):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return {'first_output_3.children': "in the fast callback it is " + current_time}


@app.dict_callback(
    Output("second_output_3", "children"), Input("button_4", "n_clicks"))
def second_callback(inputs, states):
    time.sleep(5)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return {'second_output_3.children': "in the slow callback it is " + current_time}


@app.dict_callback(
    Output("third_output_3", "children"),
    Input("first_output_3", "children"),
    Input("second_output_3", "children"))
def third_callback(inputs, states):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return {'third_output_3.children': "in the third callback it is " + current_time}


if __name__ == '__main__':
    app.run_server(debug=True)
