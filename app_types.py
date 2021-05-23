"""Type anotations"""

from typing import Any, Callable, Dict

TRender = Callable[..., str]
TView = Callable[..., Dict[str, Any]]
TViewDecorator = Callable[[TView], TView]
