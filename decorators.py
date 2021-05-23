"""Decorator implementations"""
from typing import Any, Callable, Dict, Text

TRender = Callable[[Text, Any], Text]

TView = Callable[..., Dict[str, Any]]
TViewDecorator = Callable[[TView], TView]


def template_render(render_fn: TRender, render_str: Text) -> TViewDecorator:
    """Decorator factory to render view data via template"""

    def decorator(view: TView) -> TView:
        def wrapper():
            return render_fn(render_str, **view())

        return wrapper

    return decorator
