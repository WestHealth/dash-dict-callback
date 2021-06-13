# A Dictionary Based Callback for Dash

## Introduction

Working with `Dash`callbacks can get to be confusing or difficult to maintain when callbacks get large. Generally good programming practices advocate small modular units that are easier to understand, maintain and test. Unfortunately large and possibly complex callbacks are unavoidable due to the constraints on callbacks in particular that any `Output`can belong to only one callback.

`Dash` callbacks operate on the premise that a callback receives lists or tuples of `Input`, `State` and produce a list or tuple of `Output`. Quite often as the callbacks get larger, tracking which index belongs to which `Input` `State` or `Output` can be come difficult.

A more pythonic method method of writing callbacks is to present the callback with `Input` and `State` in a dictionary and return a dictionary for the `Output`

## Getting Started

The `dict_callback` is implemented as a `Dash` plugin.  The plugin is available by cloning this repo and placing the `dash_dict_callback` directory in your `PYTHONPATH` or (if not yet soon)  to be available on PyPi. You can install via pip

```
pip install dash_dict_callback
```

## Usage

The dictionary based callback decorator `@app.dict_callback` operates similarly to the normal `@app.callback` decorator. With two additional options `strict` and `allow_missing`. The invocation of the decorator is virtually identical. The `prevent_initial_call` parameter is also supported.

In order to use it, you must pass the plugin to the `Dash` constructor.

```
from dash_dict_callback import DashDictCallbackPlugin

app = dash.Dash(__name__, plugins=[DashDictCallbackPlugin])
```

The parameters to the `@app.dict_callback` decorator are the same as with the `@app.callback` operator which takes `Output` `Input` and `State` or list of them. However, since the callback now operate on dictionaries the wrapped callback doesn't need to know what order the `Input`, `State` or `Output` are presented in the parameter list. Because of this, the `@app.dict_callback` is more liberal with the parameters. You may specify any combination of `Input`, `State`and `Output` or nested list of them. The decorator will flatten the parameters and separate the different dependency types. The only caveat is that now `prevent_initial_call` (as well as the new `strict` and `allow_missing) parameters if used **must be a named parameter**.

The callback itself receives two parameters `inputs` and `states`as dictionaries. The keys to the dictionaries are of the form `id.property`. Pattern matching (i.e. `ids` that are dictionaries) are supported but a little more involved and is described below.

A few basic examples are taken from the dash documentation and are ported to use the dictionary callback.

### Basic Example with State

This example is the same basic example given in the documentation
except using `dict_callback`.

```
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_dict_callback import DashDictCallbackPlugin

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, plugins=[DashDictCallbackPlugin], 	
				external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='dcinp-1-state', type='text', value='Montréal'),
    dcc.Input(id='dcinp-2-state', type='text', value='Canada'),
    html.Button(id='dc-submit-button', n_clicks=0, children='Submit'),
    html.Div(id='dc-output')
])


@app.dict_callback(Output('dc-output', 'children'),
                   Input('dc-submit-button', 'n_clicks'),
                   State('dcinp-1-state', 'value'),
                   State('dcinp-2-state', 'value'))
def update_output(inputs, states):
    return {'dc-output.children': u'''
        The Button has been pressed {} times,
        Input 1 is "{}",
        and Input 2 is "{}"
    '''.format(inputs['dc-submit-button.n_clicks'],
               states['dcinp-1-state.value'],
               states['dcinp-2-state.value'])}
```

### The `strict` and `allow_missing` options

For performance reasons, the `dict_callback` decorated callback doesn't by default check to make sure all keys in the output dictionary correspond to actual output ids and output properties declared in the invocation. The `strict` option enforces that. If the output contains a key not corresponding to a declared output `id` and `property` a `KeyError` is thrown. A good practice is to set `strict` to try while developing and debugging to catch possible errors. The `allow_missing` option is set to `True` by default. This options
allows for an incomplete output dictionary. All missing properties are unchanged. This is particularly useful for a complex callback where helper functions may be responsible for some outputs and not all outputs need to be updated.

In the following example, a `KeyError` is thrown since `output-2-children` is missing from the dictionary but if `allow_missing` were set to `True` it would be allowed. This pattern is very useful. Due to the constraints on outputs belonging to a single callback, you can easily be forced to conglomerate a bunch of callbacks into one. This pattern allows you to subdivide the callback into separate functions and one only needs to merge the dictionaries at the end.

```
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Input(id="input1", value="initial value"),
    dcc.Input(id="input2", value="state"),
    html.Div([html.Div(id="output-1"), html.Div(id="output-2")])
])

@app.dict_callback([Output("output-1", "children"), Output("output-2", "children")],
                   [Input("input1", "value")],
                   [State("input2", "value")], allow_missing=False)
def update_output(inputs, states):
    output = {"output-1.children": inputs['input1.value']
    }
    return output
```

In this example, `strict` is set. This will throw a `KeyError` as there is no output called `output-3.children`. While this is usually a good thing, it requires a separate check so could impact performance.

```
app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Input(id="input1", value="initial value"),
        dcc.Input(id="input2", value="state"),
        html.Div([html.Div(id="output-1"), html.Div(id="output-2")])
    ]
)

@app.dict_callback([Output("output-1", "children"), Output("output-2", "children")],
                   [Input("input1", "value")],
                   [State("input2", "value")], strict=True)
def update_output(inputs, states):
    output = {"output-1.children": inputs['input1.value'],
              "output-2.children": states['input2.value'],
              "output-3.children": "Another Value",
    }
    return output
```

### Pattern Matching Support

Finally, the `dict_callback` decorator works with pattern matching as in this Pattern Matching Example (taken from the documentation). Note that `dict_callback` works with a `callback_dict` which is a subclass of `dict` that provides `pset` and `pget` that allows access to the dictionary using pattern matching keys without having to worry about the underlying hashing or the order.

```
app = dash.Dash(__name__)

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
```

### Useful pattern if only one state or one input is given

For simpler callbacks, the typing out of dictionary keys might be cumbersome. You can access a single input or single state using the following pattern

```
def callback(inputs, states):
	single_input = next(iter(inputs.values()))
	single_state = next(iter(states.values()))
```

But please note this only works if there is only one input or one state. If this is a useful feature, I can add a method.

## Unlocking Modular Programming Patterns

TBD WORK IN PROGRESS

The callback structure introduces many constraints. Fortunately, `Dash` has resolved one of them by supporting circular callbacks (see [here](https://dash.plotly.com/advanced-callbacks)). However, one of the biggest limitation to writing modular code is that it is currently not possible for a single output to belong to multiple outputs.

The example above shows two filter sets applied to two graphical units. In the ideal, you would want four callbacks with distinct

## Guide to Examples

See the README file in the Examples directory