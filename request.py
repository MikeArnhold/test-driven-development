"""Request implementations"""
from abc import ABC, abstractproperty
from typing import Any, Dict


class BaseFormRequest(ABC):
    """Base request"""

    @abstractproperty
    def method(self) -> str:
        """request method"""

    @abstractproperty
    def form(self) -> Dict[str, Any]:
        """request form"""
