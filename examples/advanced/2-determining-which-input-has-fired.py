import json

import dash
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_dict_callback import DashDictCallbackPlugin

app = dash.Dash(__name__, plugins=[DashDictCallbackPlugin])

app.layout = html.Div([
    html.Button('Button 1', id='btn-1'),
    html.Button('Button 2', id='btn-2'),
    html.Button('Button 3', id='btn-3'),
    html.Div(id='container')
])


@app.dict_callback(Output('container', 'children'),
              Input('btn-1', 'n_clicks'),
              Input('btn-2', 'n_clicks'),
              Input('btn-3', 'n_clicks'))
def display(inputs,states):
    btn1 = inputs['btn-1.n_clicks']
    btn2 = inputs['btn-2.n_clicks']
    btn3 = inputs['btn-3.n_clicks']
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)

    return {'container.children':
            html.Div([
                html.Table([
                    html.Tr([html.Th('Button 1'),
                             html.Th('Button 2'),
                             html.Th('Button 3'),
                             html.Th('Most Recent Click')]),
                    html.Tr([html.Td(btn1 or 0),
                             html.Td(btn2 or 0),
                             html.Td(btn3 or 0),
                             html.Td(button_id)])
                ]),
                html.Pre(ctx_msg)
            ])
            }


if __name__ == '__main__':
    app.run_server(debug=True)
