# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_dict_callback import DashDictCallbackPlugin

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, plugins=[DashDictCallbackPlugin])

all_options = {
    'America': ['New York City', 'San Francisco', 'Cincinnati'],
    'Canada': [u'Montréal', 'Toronto', 'Ottawa']
}
app.layout = html.Div([
    dcc.RadioItems(
        id='countries-radio',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='America'
    ),

    html.Hr(),

    dcc.RadioItems(id='cities-radio'),

    html.Hr(),

    html.Div(id='display-selected-values')
])


@app.dict_callback(
    Output('cities-radio', 'options'),
    Input('countries-radio', 'value'))
def set_cities_options(inputs, states):
    selected_country=inputs['countries-radio.value']
    output = {'cities-radio.options': [{'label': i, 'value': i} for i in all_options[selected_country]]}
    return output

@app.dict_callback(
    Output('cities-radio', 'value'),
    Input('cities-radio', 'options'))
def set_cities_value(inputs, states):
    available_options = inputs['cities-radio.options']
    return {'cities-radio.value': available_options[0]['value']}


@app.dict_callback(
    Output('display-selected-values', 'children'),
    Input('countries-radio', 'value'),
    Input('cities-radio', 'value'))
def set_display_children(inputs, states):
    selected_country =inputs['countries-radio.value']
    selected_city = inputs['cities-radio.value']
    out = u'{} is a city in {}'.format(
        selected_city, selected_country,
    )
    return {'display-selected-values.children': out}


if __name__ == '__main__':
    app.run_server(debug=True)
