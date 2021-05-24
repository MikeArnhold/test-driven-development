"""Type anotations"""

from typing import Any, Callable, Text

TRender = Callable[[Text, Any], Text]

TView = Callable[..., Any]
TViewDecorator = Callable[[TView], TView]
