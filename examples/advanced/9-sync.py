import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash_dict_callback import DashDictCallbackPlugin

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, plugins=[DashDictCallbackPlugin])

options = [
    {"label": "New York City", "value": "NYC"},
    {"label": "Montréal", "value": "MTL"},
    {"label": "San Francisco", "value": "SF"},
]
all_cities = [option["value"] for option in options]

app.layout = html.Div(
    [
        dcc.Checklist(
            id="all-checklist",
            options=[{"label": "All", "value": "All"}],
            value=[],
            labelStyle={"display": "inline-block"},
        ),
        dcc.Checklist(
            id="city-checklist",
            options=options,
            value=[],
            labelStyle={"display": "inline-block"},
        ),
    ]
)
@app.dict_callback(
    Output("city-checklist", "value"),
    Output("all-checklist", "value"),
    Input("city-checklist", "value"),
    Input("all-checklist", "value"),
)
def sync_checklists(inputs, states):
    cities_selected=inputs['city-checklist.value']
    all_selected=inputs['all-checklist.value']
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "city-checklist":
        all_selected = ["All"] if set(cities_selected) == set(all_cities) else []
    else:
        cities_selected = all_cities if all_selected else []
    outputs={}
    outputs['city-checklist.value'] = cities_selected
    outputs['all-checklist.value'] = all_selected
    return outputs

if __name__ == "__main__":
    app.run_server(debug=True)
