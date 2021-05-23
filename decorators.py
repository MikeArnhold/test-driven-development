"""Decorator implementations"""
from functools import partial
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


template = partial(view_format, render_template)
