import dash
from dash.dependencies import Input, Output
import dash_html_components as html
from dash_dict_callback import DashDictCallbackPlugin

app = dash.Dash(plugins=[DashDictCallbackPlugin])
app.layout = html.Div(
    [
        html.Button("execute callback", id="button_1"),
        html.Div(children="callback not executed", id="first_output_1"),
        html.Div(children="callback not executed", id="second_output_1"),
    ]
)


@app.dict_callback(
    Output("first_output_1", "children"),
    Output("second_output_1", "children"),
    Input("button_1", "n_clicks")
)
def change_text(inputs, states):
    n_clicks = inputs['button_1.n_clicks']
    outstr = "n_clicks is " + str(n_clicks)
    return {'first_output_1.children': outstr,
            'second_output_1.children': outstr}

if __name__ == '__main__':
    app.run_server(debug=True)
