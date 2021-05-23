"""Decorator implementations"""
from functools import partial, reduce
from typing import Any, Callable, Text

from flask import jsonify, render_template
from flask.wrappers import Response

from app_types import TRender, TView, TViewDecorator


def endpoint(
    route: Callable[[TView], TView], *decorators: Callable[[TView], TView]
) -> TViewDecorator:
    """Endpoint factory for views, that return data only

    Target function will be decorated by decorators in reverse order.
    The resulting wrapper is fed into the route.
    """

    def wrap(func, decorator):
        return decorator(func)

    def decorator(view: TView) -> TView:
        wrapper = reduce(wrap, reversed(decorators), view)
        route(wrapper)
        return view

    return decorator


def rest(view: TView) -> Callable[..., Response]:
    """Decorate view to jsonify data"""

    def wrapper(*args: Any, **kwargs: Any):
        return jsonify(view(*args, **kwargs))

    return wrapper


def view_format(format_fn: TRender, format_str: Text) -> TViewDecorator:
    """Decorator factory to render view data via template"""

    def decorator(view: TView) -> TView:
        def wrapper(*args: Any, **kwargs: Any):
            return format_fn(format_str, **view(*args, **kwargs))

        return wrapper

    return decorator


template = partial(view_format, render_template)