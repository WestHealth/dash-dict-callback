import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash_dict_callback import DashDictCallbackPlugin

app = dash.Dash(__name__, suppress_callback_exceptions=True, plugins=[DashDictCallbackPlugin])

app.layout = html.Div([
    html.Button("Add Filter", id="dynamic-add-filter", n_clicks=0),
    html.Div(id='dynamic-dropdown-container', children=[]),
])

@app.dict_callback(
    Output('dynamic-dropdown-container', 'children'),
    Input('dynamic-add-filter', 'n_clicks'),
    State('dynamic-dropdown-container', 'children'))
def display_dropdowns(inputs, states):
    new_element = html.Div([
        dcc.Dropdown(
            id={
                'type': 'dynamic-dropdown',
                'index': inputs['dynamic-add-filter.n_clicks']
            },
            options=[{'label': i, 'value': i} for i in ['NYC', 'MTL', 'LA', 'TOKYO']]
        ),
        html.Div(
            id={
                'type': 'dynamic-output',
                'index': inputs['dynamic-add-filter.n_clicks']
            }
        )
    ])
    states['dynamic-dropdown-container.children'].append(new_element)
    return states


@app.dict_callback(
    Output({'type': 'dynamic-output', 'index': MATCH}, 'children'),
    Input({'type': 'dynamic-dropdown', 'index': MATCH}, 'value'),allow_missing=False
)
def display_output(inputs, states):
    id_, _ = inputs.pkeys()[0]
    output=dash.Dash.callback_dict()

    div = html.Div('Dropdown {} = {}'.format(id_['index'], inputs.pget(id_,'value')))
    output.pset(type='dynamic-output', index=id_['index'], property='children', value=div)
    return output


if __name__ == '__main__':
    app.run_server(debug=True)
