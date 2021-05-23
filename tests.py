"""Test implementations"""
from unittest import TestCase

from flask import render_template_string

from decorators import view_format
from main import app, index


class TestIndex(TestCase):
    """index tests"""

    def test_index(self):
        """Index returns greetind as data dict"""
        self.assertEqual({"greeting": "Hello, World!"}, index())


class ViewFormatTests(TestCase):
    """view_format tests"""

    def test_render_div_foo_42(self) -> None:
        """render foo=42 within div"""

        @view_format(render_template_string, r"<div>{{ foo }}</div>")
        def view():
            return dict(foo=42)

        with app.app_context():
            self.assertEqual("<div>42</div>", view())
