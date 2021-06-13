import dash
from functools import wraps, partial
from types import MethodType
from collections.abc import Iterable
from dash.dependencies import Output, Input, State

class _DashDictCallbackPlugin():
    class callback_dict(dict):
        """
        This class is a convenience class to work with dict_callback. It extends the
        builtin dict class by adding three methods that can be used to more easily
        interact with pattern matching component ids.

        The private method _property_key_key converts an id/property dict to
        our internal dict label. String id components have their property are
        mapped to 'id.property' while pattern matched id's are flattened using
        frozenset which guarantees the id dict will map to the same immutable object
        regardless of the order of the keys. We use the hashable tuple
        (frozenset, property) as the key. This mapping is centralize here.

        The method pget is intended to be used with pattern matched components
        but can be used with string id components. It can be accessed in two ways
        the id can be supplied with the property or as long as there isn't a name
        collision with the named parameters, the id components can be supplied by
        themselves. For example, input.pget({type: 'btn', index: 1}, 'n_clicks')
        or input.pget(type='btn', index=1, property='n_clicks') can be used.

        The method pset is also mainly a pattern matched component convenience.
        It sets a value in the dictionary. And has two modes of operation similar to pget.

<        Finally, pkeys unpacks all the pattern matched id/property into tuples of
        ids and properties. But only lists the pattern matched component ids.
        """

        @classmethod
        def _property_to_key(cls, prop):
            """Converts the property to our key format for dictionaries"""
            if type(prop['id']) == dict:
                return (frozenset(prop['id'].items()), prop['property'])
            else:
                return f"{prop['id']}.{prop['property']}"

        def pget(self, id_=None, property=None, **kwargs):
            if not id_:
                id_ = kwargs
            return self[self._property_to_key(dict(id=id_, property=property))]

        def pset(self, key=None, property=None, value=None, **kwargs):
            if not key:
                key = kwargs
            self[self._property_to_key(dict(id=key, property=property))] = value

        def pkeys(self):
            return [(dict(k[0]), k[1]) for k in self.keys() if isinstance(k, tuple)]

    def dict_callback(self, app, *_args, **_kwargs):
        """
        Normally used as a decorator, `@app.dict_callback` provides a server-side
        callback relating the values of one or more `Output` items to one or
        more `Input` items which will trigger the callback when they change,
        and optionally `State` items which provide additional information but
        do not trigger the callback directly.
        
        This differs from the standard callback because the callback function 
        receives as input an input and state dictionary and generates as output 
        an output dictionary. They keys in a dictionary are of the form "id.property"
        for standard Inputs, States, and Outputs and "type#index.property" for pattern
        matched Inputs and States.
        
        This decorator accepts any keyword arguments the standard callback method does 
        including the optional argument 'prevent_initial_call'. In addition, two
        additional optional callback arguments are added 'strict' and 'allow_missing'.

        The optional argument `prevent_initial_call` causes the callback
        not to fire when its outputs are first added to the page. Defaults to
        `False` unless `prevent_initial_callbacks=True` at the app level.

        The 'strict' argument causes the callback to raise a KeyError if the callback
        returns a key in the dictionary that is not expected as an Output. Defaults to 
        'False'.
        
        The 'allow_missing' argument returns a 'no_update'. For any keys missing when
        in the output returned by the callback. If 'False' a KeyError is raised if
        any keys are missing in the output dictionary. Defaults to 'True'.
        """

        # Pull new options out of the keyword arguments
        strict = _kwargs.pop('strict', False)
        allow_missing = _kwargs.pop('allow_missing', True)
        prevent_initial_call = _kwargs.pop('prevent_initial_call', None)
        _args=self.normalize(_args)
        
        return partial(self.decorator, app, allow_missing, strict, prevent_initial_call, _args, _kwargs)

    def decorator(self, app, allow_missing, strict, pic, _args, _kwargs, func):
        return app.callback(*_args, prevent_initial_call=pic, **_kwargs)(self.dictionaryize(allow_missing, strict, func))

    def dictionaryize(self, allow_missing, strict, func):

        #
        # Helper Functions
        #

        # property_to_key is defined in the callback_dict class. Rather than
        # making two copies we refer to the original for maintainablility
        property_to_key = self.callback_dict._property_to_key

        def to_dict(in_, prop_list, recurse=True):
            """
            Maps an values input list to a dict based on the list of properties.
            We allow one level of recursion since pattern matching allows for a list of lists.
            """
            if len(in_) != len(prop_list):
                raise ValueError("List must have the same number of elements as keys")
            out_dict = self.callback_dict()
            for prop, value in zip(prop_list, in_):
                if isinstance(prop, (list, tuple)) and recurse:
                    out_dict.update(to_dict(value, prop, recurse=False))
                else:
                    out_dict[property_to_key(prop)] = value
            return out_dict

        def get_keys_from_list(prop_list, recurse=True):
            """
            Converts a list of properties to a list of keys. This is for 'strict' validation.
            We allow one level of recurse for pattern matching.
            """
            out_list = []
            for prop in prop_list:
                if isinstance(prop, (list, tuple)) and recurse:
                    out_list += get_keys_from_list(prop_list, recurse=False)
                else:
                    out_list.append(property_to_key(prop))
            return out_list

        def from_dict(output_values, prop_list, recurse=True):
            """
            Maps output_values dict to a list based on the list of properties. 
            For symmetry sake, we allow one level of recursion, but pattern matching on outputs
            doesn't support any kind of list of list. 
            """
            # A single property may appear not as a so we make it a list for consistent processing.

            if not isinstance(prop_list, (list, tuple)):
                prop_list = [prop_list]

            out_list = []
            for prop in prop_list:
                if isinstance(prop, (list, tuple)) and recurse:
                    out_list.append(from_dict(output_values, prop, recurse=False))
                else:
                    if allow_missing:
                        out_list.append(output_values.get(property_to_key(prop), dash.no_update))
                    else:  # Throw Key error if value is missing
                        out_list.append(output_values[property_to_key(prop)])

            return out_list

        @wraps(func)
        def wrapped_func(*args, **kwargs):
                ctx = dash.callback_context
                inputs = to_dict(args[0:len(ctx.inputs_list)], ctx.inputs_list)
                state = to_dict(args[len(ctx.inputs_list):], ctx.states_list)
                output_dict = func(inputs, state, **kwargs)  # %% callback invoked %%
                # As with standard callback, we still support the returning of a single
                # no_update to prevent updating

                if output_dict == dash.no_update:
                    raise PreventUpdate

                output_value = from_dict(output_dict, ctx.outputs_list)
                if strict:
                    # Check to see if there are any excess keys in strict mode
                    excess_keys = set(output_dict.keys()) - set(get_keys_from_list(ctx.outputs_list))
                    if excess_keys:
                        raise KeyError(f'The following keys were note found {",".join(list(excess_keys))}')

                # If the expected output is not a list we need to unwrap it from our list

                if not isinstance(ctx.outputs_list, (list, tuple)):
                    output_value = output_value[0]

                return output_value

        return wrapped_func

    def plug(self, app):
        app.dict_callback = MethodType(self.dict_callback, app)
        app.__class__.callback_dict = self.callback_dict
    def normalize(*args):
        def flatten(l):
            """ taken from https://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists
            """
            for el in l:
                if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
                    yield from flatten(el)
                else:
                    yield el
        outputs=[]
        inputs =[]
        states = []
        for each in flatten(args):
            if isinstance(each, Output):
                outputs.append(each)
            if isinstance(each, Input):
                inputs.append(each)
            if isinstance(each, State):
                states.append(each)
        return outputs, inputs, states
        
def dictionary(args=None, strict=False, allow_missing=True):
    if callable(args):
        return DashCallbackPlugin().dictionaryize(allow_missing, strict, args)
    return partial(DashCallbackPlugin().dictionaryize, allow_missing, strict)

# Since we always use the instantiation. Let's instantiate it
DashDictCallbackPlugin = _DashDictCallbackPlugin()
