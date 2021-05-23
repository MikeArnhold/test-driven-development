"""Test implementations"""
from typing import Callable
from unittest import TestCase

from flask import render_template_string

from decorators import endpoint, view_format
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

    def test_render_p_bar_33(self) -> None:
        """render bar=33 within p"""

        @view_format(render_template_string, r"<p>{{ bar }}</p>")
        def view():
            return dict(bar=33)

        with app.app_context():
            self.assertEqual("<p>33</p>", view())

    def test_render_span_parameters(self) -> None:
        """render view parameters within span"""

        @view_format(render_template_string, r"<span>{{ smurf }}</span>")
        def view(key, value="papa"):
            ret = {}
            ret[key] = value
            return ret

        with app.app_context():
            self.assertEqual("<span>mama</span>", view("smurf", "mama"))


class EnpointTests(TestCase):
    """endpoint tests"""

    def test_wrapped_unchanged(self) -> None:
        """leaves decorated function unchanged"""

        def route(_):
            pass

        def view():
            pass

        self.assertEqual(view, endpoint(route)(view))

    def test_wrapped_to_route(self) -> None:
        """decorated function passed to route"""
        passed = None

        def route(view):
            nonlocal passed
            passed = view

        @endpoint(route)
        def view():
            pass

        self.assertEqual(view, passed)

    def test_wrapper_to_route(self) -> None:
        """decorated function passed to route with decorators"""
        passed: Callable[[], None]
        called = []

        def route(view):
            nonlocal passed
            passed = view

        def dec_a(view):
            def wrapper():
                called.append("a")
                return view()

            return wrapper

        def dec_b(view):
            def wrapper():
                called.append("b")
                return view()

            return wrapper

        @endpoint(route, dec_a, dec_b)
        def view():
            called.append("v")

        passed()
        self.assertListEqual(["a", "b", "v"], called)
