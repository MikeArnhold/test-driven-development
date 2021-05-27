"""Decorator implementations"""
from functools import partial, reduce
from typing import Any, Callable, Tuple

from flask import jsonify, render_template
from flask.wrappers import Response

from app_types import TView, TViewDecorator


def endpoint(
    route: TViewDecorator, *decorators: TViewDecorator
) -> TViewDecorator:
    """Endpoint factory for views, that return data only

    Arguments:
        route: Intended to be app.route(...)
        decorators: Used in reverse order. Decorator stack is fed into route.

    Returns:
        Decorator that will return unwrapped target function.
    """

    def wrap(func, decorator):
        return decorator(func)

    def decorator(view: TView) -> TView:
        wrapper = reduce(wrap, reversed(decorators), view)
        wrapper.__name__ = f"endpoint_{view.__name__}"
        route(wrapper)
        return view

    return decorator


def rest(view: TView) -> Callable[..., Response]:
    """Decorate view to jsonify data"""

    def wrapper(*args: Any, **kwargs: Any):
        return jsonify(view(*args, **kwargs))

    return wrapper


def convert(
    *converters: Tuple[type, Callable[[Any, dict], Any]],
    **kwargs: Any,
) -> TViewDecorator:
    """Decorator factory to render view data via format_fn"""

    def decorator(view: TView) -> TView:
        def wrapper(*w_args: Any, **w_kwargs: Any):
            context = view(*w_args, **w_kwargs)
            for c_type, converter in converters or ():
                if isinstance(context, c_type):
                    return converter(context, kwargs)
            return context

        return wrapper

    return decorator


def parameters(*args, **kwargs) -> TViewDecorator:
    """Decorator factory to parse default arguments"""

    def decorator(view: TView) -> TView:
        def wrapper(*w_args, **w_kwargs):
            return view(*args, *w_args, **kwargs, **w_kwargs)

        return wrapper

    return decorator


template = partial(
    convert,
    (dict, lambda d, kwargs: render_template(kwargs["name"], **d)),
)
