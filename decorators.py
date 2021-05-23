"""Decorator implementations"""
from functools import partial
from typing import Any, Callable, Dict, Text

from flask import render_template

TRender = Callable[[Text, Any], Text]

TView = Callable[..., Dict[str, Any]]
TViewDecorator = Callable[[TView], TView]


def template_render(render_fn: TRender, render_str: Text) -> TViewDecorator:
    """Decorator factory to render view data via template"""

    def decorator(view: TView) -> TView:
        def wrapper(*args: Any, **kwargs: Any):
            return render_fn(render_str, **view(*args, **kwargs))

        return wrapper

    return decorator


template = partial(template_render, render_template)
