import dash
from dash.dependencies import Input, Output
import dash_html_components as html
from dash_dict_callback import DashDictCallbackPlugin
from datetime import datetime
import time

app = dash.Dash(plugins=[DashDictCallbackPlugin])

app.layout = html.Div(
    [
        html.Button("execute callbacks", id="button_2"),
        html.Div(children="callback not executed", id="first_output_2"),
        html.Div(children="callback not executed", id="second_output_2"),
        html.Div(children="callback not executed", id="third_output_2"),
        html.Div(children="callback not executed", id="fourth_output_2"),
    ]
)


@app.dict_callback(
    Output("first_output_2", "children"),
    Output("second_output_2", "children"),
    Input("button_2", "n_clicks"), prevent_initial_call=True)
def first_callback(i,s):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return {'first_output_2.children': "in the first callback it is " + current_time,
            'second_output_2.children': "in the first callback it is " + current_time}


@app.dict_callback(
    Output("third_output_2", "children"), Input("second_output_2", "children"), prevent_initial_call=True)
def second_callback(i,s):
    time.sleep(2)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return {'third_output_2.children': "in the second callback it is " + current_time}


@app.dict_callback(
    Output("fourth_output_2", "children"),
    Input("first_output_2", "children"),
    Input("third_output_2", "children"), prevent_initial_call=True)
def third_output(i, s):
    time.sleep(2)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return {'fourth_output_2.children': "in the third callback it is " + current_time}


if __name__ == '__main__':
    app.run_server(debug=True)
