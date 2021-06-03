import json
from multiprocessing import Lock, Value
import pytest
import time

import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash
from dash_dict_callback import DashCallbackPlugin
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate
from dash.testing import wait


@pytest.mark.parametrize("strict,allow_missing", [(True, True), (True, False), (False, True), (False, False)])
def test_cdcb001_simple_callback(strict, allow_missing, dash_duo):
    """ Basic usage of dict callback. Run through the 4 combinations of new flags """
    lock = Lock()

    app = dash.Dash(__name__, plugins=[DashCallbackPlugin()])
    app.layout = html.Div(
        [
            dcc.Input(id="input1", value="initial value"),
            dcc.Input(id="input2", value="state"),
            html.Div([html.Div(id="output-1"), html.Div(id="output-2")])
        ]
    )

    call_count = Value("i", 0)

    @app.dict_callback([Output("output-1", "children"), Output("output-2", "children")],
                       [Input("input1", "value")],
                       [State("input2", "value")], strict=strict, allow_missing=allow_missing)
    def update_output(inputs, states):
        output = {"output-1.children": inputs['input1.value'],
                  "output-2.children": states['input2.value'],
                  }
        call_count.value = call_count.value + 1
        return output

    dash_duo.start_server(app)

    assert dash_duo.find_element("#output-1").text == "initial value"

    input_ = dash_duo.find_element("#input1")
    dash_duo.clear_input(input_)

    for key in "hello world":
        with lock:
            input_.send_keys(key)

    wait.until(lambda: dash_duo.find_element("#output-1").text == "hello world", 2)
    assert dash_duo.find_element("#output-2").text == "state"
    assert call_count.value == 2 + len("hello world"), "initial count + each key stroke"

    assert not dash_duo.redux_state_is_loading

    assert dash_duo.get_logs() == []


def test_cdcb002_dict_callback_strict_false(dash_duo):
    """ Test if strict is False we permit extra output keys in output dictionary """
    lock = Lock()

    app = dash.Dash(__name__, plugins=[DashCallbackPlugin()])
    app.layout = html.Div(
        [
            dcc.Input(id="input1", value="initial value"),
            dcc.Input(id="input2", value="state"),
            html.Div([html.Div(id="output-1"), html.Div(id="output-2")])
        ]
    )

    call_count = Value("i", 0)

    @app.dict_callback([Output("output-1", "children"), Output("output-2", "children")],
                       [Input("input1", "value")],
                       [State("input2", "value")])
    def update_output(inputs, states):
        output = {"output-1.children": inputs['input1.value'],
                  "output-2.children": states['input2.value'],
                  "output-3.children": "Another Value",
                  }
        call_count.value = call_count.value + 1
        return output

    dash_duo.start_server(app)

    assert dash_duo.find_element("#output-1").text == "initial value"

    input_ = dash_duo.find_element("#input1")
    dash_duo.clear_input(input_)

    for key in "hello world":
        with lock:
            input_.send_keys(key)

    wait.until(lambda: dash_duo.find_element("#output-1").text == "hello world", 2)
    assert dash_duo.find_element("#output-2").text == "state"
    assert call_count.value == 2 + len("hello world"), "initial count + each key stroke"

    assert not dash_duo.redux_state_is_loading

    assert dash_duo.get_logs() == []


@pytest.mark.skipif(True, reason="Don't know how to assert on an exception inside a callback")
def test_cdcb003_dict_callback_strict_true(dash_duo):
    """ Test if strict is True an extra output keys in output dictionary causes a KeyError
    At this point I don't know how to write an assertion for this
    """
    lock = Lock()

    app = dash.Dash(__name__, plugins=[DashCallbackPlugin()])
    app.layout = html.Div(
        [
            dcc.Input(id="input1", value="initial value"),
            dcc.Input(id="input2", value="state"),
            html.Div([html.Div(id="output-1"), html.Div(id="output-2")])
        ]
    )

    call_count = Value("i", 0)

    @app.dict_callback([Output("output-1", "children"), Output("output-2", "children")],
                       [Input("input1", "value")],
                       [State("input2", "value")], strict=True)
    def update_output(inputs, states):
        output = {"output-1.children": inputs['input1.value'],
                  "output-2.children": states['input2.value'],
                  "output-3.children": "Another Value",
                  }
        call_count.value = call_count.value + 1
        return output

    dash_duo.start_server(app)

    assert dash_duo.find_element("#output-1").text == "initial value"

    input_ = dash_duo.find_element("#input1")
    dash_duo.clear_input(input_)

    for key in "hello world":
        with lock:
            input_.send_keys(key)

    wait.until(lambda: dash_duo.find_element("#output-1").text == "hello world", 2)
    assert dash_duo.find_element("#output-2").text == "state"
    assert call_count.value == 2 + len("hello world"), "initial count + each key stroke"

    assert not dash_duo.redux_state_is_loading

    assert dash_duo.get_logs() == []


@pytest.mark.skipif(True, reason="Don't know how to assert on an exception inside a callback")
def test_cdcb004_dict_callback_allow_missing_false(dash_duo):
    """ Test if allow_missing is False a missing output keys in output dictionary causes a KeyError
    At this point I don't know how to write an assertion for this
    """
    lock = Lock()

    app = dash.Dash(__name__, plugins=[DashCallbackPlugin()])
    app.layout = html.Div(
        [
            dcc.Input(id="input1", value="initial value"),
            dcc.Input(id="input2", value="state"),
            html.Div([html.Div(id="output-1"), html.Div(id="output-2")])
        ]
    )

    call_count = Value("i", 0)

    @app.dict_callback([Output("output-1", "children"), Output("output-2", "children")],
                       [Input("input1", "value")],
                       [State("input2", "value")], allow_missing=False)
    def update_output(inputs, states):
        output = {"output-1.children": inputs['input1.value']
                  }
        call_count.value = call_count.value + 1
        return output

    dash_duo.start_server(app)

    assert dash_duo.find_element("#output-1").text == "initial value"

    input_ = dash_duo.find_element("#input1")
    dash_duo.clear_input(input_)

    for key in "hello world":
        with lock:
            input_.send_keys(key)

    wait.until(lambda: dash_duo.find_element("#output-1").text == "hello world", 2)
    assert dash_duo.find_element("#output-2").text == ""
    assert call_count.value == 2 + len("hello world"), "initial count + each key stroke"

    assert not dash_duo.redux_state_is_loading

    assert dash_duo.get_logs() == []


def test_cdcb005_dict_callback_allow_missing_true(dash_duo):
    """ Test that if allow_missing is True (default) a missing output key is the same as a
    dash.noupdate for that output
    """
    lock = Lock()

    app = dash.Dash(__name__, plugins=[DashCallbackPlugin()])
    app.layout = html.Div(
        [
            dcc.Input(id="input1", value="initial value"),
            dcc.Input(id="input2", value="state"),
            html.Div([html.Div(id="output-1"), html.Div(id="output-2")])
        ]
    )

    call_count = Value("i", 0)

    @app.dict_callback([Output("output-1", "children"), Output("output-2", "children")],
                       [Input("input1", "value")],
                       [State("input2", "value")], strict=True)
    def update_output(inputs, states):
        output = {"output-1.children": inputs['input1.value']
                  }
        call_count.value = call_count.value + 1
        return output

    dash_duo.start_server(app)

    assert dash_duo.find_element("#output-1").text == "initial value"

    input_ = dash_duo.find_element("#input1")
    dash_duo.clear_input(input_)

    for key in "hello world":
        with lock:
            input_.send_keys(key)

    wait.until(lambda: dash_duo.find_element("#output-1").text == "hello world", 2)
    assert dash_duo.find_element("#output-2").text == ""
    assert call_count.value == 2 + len("hello world"), "initial count + each key stroke"

    assert not dash_duo.redux_state_is_loading

    assert dash_duo.get_logs() == []


def test_cdcb007_dict_callback_pattern_matching(dash_duo):
    """ Basic test to check that dict_callback works with pattern matching"""
    app = dash.Dash(__name__, plugins=[DashCallbackPlugin()])
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
        Input({'type': 'dynamic-dropdown', 'index': MATCH}, 'value'), allow_missing=False
    )
    def display_output(inputs, states):
        id_, _ = inputs.pkeys()[0]
        output = dash.Dash.callback_dict()

        div = html.Div('Dropdown {} = {}'.format(id_['index'], inputs.pget(id_, 'value')))
        output.pset(type='dynamic-output', index=id_['index'], property='children', value=div)
        return output

    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal("#dynamic-add-filter", "Add Filter")
    dash_duo.select_dcc_dropdown(
        '#\\{\\"index\\"\\:0\\,\\"type\\"\\:\\"dynamic-dropdown\\"\\}', "LA"
    )
    dash_duo.wait_for_text_to_equal(
        '#\\{\\"index\\"\\:0\\,\\"type\\"\\:\\"dynamic-output\\"\\}', "Dropdown 0 = LA"
    )
    dash_duo.find_element("#dynamic-add-filter").click()
    dash_duo.select_dcc_dropdown(
        '#\\{\\"index\\"\\:1\\,\\"type\\"\\:\\"dynamic-dropdown\\"\\}', "MTL"
    )
    dash_duo.wait_for_text_to_equal(
        '#\\{\\"index\\"\\:1\\,\\"type\\"\\:\\"dynamic-output\\"\\}', "Dropdown 1 = MTL"
    )
    dash_duo.wait_for_text_to_equal(
        '#\\{\\"index\\"\\:0\\,\\"type\\"\\:\\"dynamic-output\\"\\}', "Dropdown 0 = LA"
    )
    dash_duo.wait_for_no_elements(dash_duo.devtools_error_count_locator)
