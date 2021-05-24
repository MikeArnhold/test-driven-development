"""Request implementations"""
from abc import ABC, abstractproperty
from typing import Any, Dict

from flask import request


class BaseFormRequest(ABC):
    """Base request"""

    @abstractproperty
    def method(self) -> str:
        """request method"""

    @abstractproperty
    def form(self) -> Dict[str, Any]:
        """request form"""


class CompleteRequest(BaseFormRequest):
    """Complete request wrapping flaks request"""

    @property
    def method(self) -> str:
        return request.method

    @property
    def form(self) -> Dict[str, Any]:
        return request.form
