"""Decorator implementations"""
from functools import partial, reduce
from typing import Any, Text

from flask import render_template

from app_types import TRender, TView, TViewDecorator


def view_format(format_fn: TRender, format_str: Text) -> TViewDecorator:
    """Decorator factory to render view data via template"""

    def decorator(view: TView) -> TView:
        def wrapper(*args: Any, **kwargs: Any):
            return format_fn(format_str, **view(*args, **kwargs))

        return wrapper

    return decorator


def endpoint(route, *decorators) -> TViewDecorator:
    """Endpoint factory for views, that return data only"""

    def wrap(func, decorator):
        return decorator(func)

    def decorator(view: TView) -> TView:
        wrapper = reduce(wrap, reversed(decorators), view)
        route(wrapper)
        return view

    return decorator


template = partial(view_format, render_template)
