"""Type anotations"""

from typing import Any, Callable, Dict, Text

TRender = Callable[[Text, Any], Text]

TView = Callable[..., Dict[str, Any]]
TViewDecorator = Callable[[TView], TView]
