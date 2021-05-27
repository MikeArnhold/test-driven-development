"""Decorator implementations"""
from functools import partial, reduce
from typing import Any, Callable, List, Text, Tuple

from flask import jsonify, render_template
from flask.wrappers import Response
from werkzeug.wrappers.response import Response as WerkzeugResponse

from app_types import TRender, TView, TViewDecorator


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


def dict_format(
    format_fn: TRender,
    format_str: Text,
    format_non_dict: List[Tuple[type, Callable[[Any], Any]]] = None,
) -> TViewDecorator:
    """Decorator factory to render view data via format_fn"""

    def decorator(view: TView) -> TView:
        def wrapper(*args: Any, **kwargs: Any):
            context = view(*args, **kwargs)
            if format_non_dict is not None:
                for ctx_type, format_fallback in format_non_dict:
                    if isinstance(context, ctx_type):
                        return format_fallback(context)
            return format_fn(format_str, **context)

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
    dict_format,
    render_template,
    format_non_dict=[(WerkzeugResponse, lambda d: d)],
)
