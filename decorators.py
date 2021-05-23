"""Decorator implementations"""
from typing import Text

from app_types import TRender, TView, TViewDecorator


def view_format(format_fn: TRender, format_str: Text) -> TViewDecorator:
    """Decorator factory to render view data via template"""

    def decorator(view: TView) -> TView:
        def wrapper():
            return "<div>42</div>"

        return wrapper

    return decorator
