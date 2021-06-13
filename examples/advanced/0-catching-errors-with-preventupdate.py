import dash
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dash_dict_callback import DashDictCallbackPlugin

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, plugins=[DashDictCallbackPlugin])

app.layout = html.Div([
    html.Button('Click here to see the content', id='show-secret'),
    html.Div(id='body-div')
])

@app.dict_callback(
    Output(component_id='body-div', component_property='children'),
    Input(component_id='show-secret', component_property='n_clicks')
)
def update_output(inputs,states):
    n_clicks = inputs['show-secret.n_clicks']
    if n_clicks is None:
        raise PreventUpdate
    else:
        return {'body-div.children': "Elephants are the only animal that can't jump"}

if __name__ == '__main__':
    app.run_server(debug=True)
