import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash_dict_callback import DashDictCallbackPlugin

app = dash.Dash(__name__, suppress_callback_exceptions=True, plugins=[DashDictCallbackPlugin])

app.layout = html.Div([
    html.Button("Add Filter", id="add-filter", n_clicks=0),
    html.Div(id='dropdown-container', children=[]),
    html.Div(id='dropdown-container-output')
])

@app.dict_callback(
    Output('dropdown-container', 'children'),
    Input('add-filter', 'n_clicks'),
    State('dropdown-container', 'children'))
def display_dropdowns(inputs, states):
    
    new_dropdown = dcc.Dropdown(
        id={
            'type': 'filter-dropdown',
            'index': inputs['add-filter.n_clicks']
        },
        options=[{'label': i, 'value': i} for i in ['NYC', 'MTL', 'LA', 'TOKYO']]
    )
    states['dropdown-container.children'].append(new_dropdown)
    return states

def flatten_list(lst):
    out = []
    for each in lst:
        if isinstance(each, list):
            out.extend(each)
        else:
            out.append(each)
    return out
@app.dict_callback(
    Output('dropdown-container-output', 'children'),
    Input({'type': 'filter-dropdown', 'index': ALL}, 'value')
)
def display_output(inputs, states):
    ctx=dash.callback_context
    divs=[]
    for id_, property in inputs.pkeys():
        if id_.get('type')=='filter-dropdown':
            divs.append(html.Div('Dropdown {} = {}'.format(id_['index'], inputs.pget(property='value', **id_))))

    return {'dropdown-container-output.children': html.Div(divs)}


if __name__ == '__main__':
    app.run_server(debug=True)
