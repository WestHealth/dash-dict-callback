import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_dict_callback import DashDictCallbackPlugin

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, plugins=[DashDictCallbackPlugin])

app.layout = html.Div([
    html.P('Enter a composite number to see its prime factors'),
    dcc.Input(id='num', type='number', debounce=True, min=1, step=1),
    html.P(id='err', style={'color': 'red'}),
    html.P(id='out')
])

@app.dict_callback(
    Output('out', 'children'),
    Output('err', 'children'),
    Input('num', 'value')
)
def show_factors(inputs, states):
    num = inputs['num.value']
    if num is None:
        # PreventUpdate prevents ALL outputs updating
        raise dash.exceptions.PreventUpdate

    factors = prime_factors(num)
    if len(factors) == 1:
        # dash.no_update prevents any single output updating
        # (note: it's OK to use for a single-output callback too)
        return {'err.children': '{} is prime!'.format(num)}

    return {'out.children': '{} is {}'.format(num, ' * '.join(str(n) for n in factors)),
            'err.children': ''}

def prime_factors(num):
    n, i, out = num, 2, []
    while i * i <= n:
        if n % i == 0:
            n = int(n / i)
            out.append(i)
        else:
            i += 1 if i == 2 else 2
    out.append(n)
    return out

if __name__ == '__main__':
    app.run_server(debug=True)
