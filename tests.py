"""Test implementations"""
from typing import Callable
from unittest import TestCase

from flask import Response, render_template_string

from decorators import endpoint, parameters, rest, view_format
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

        def route(view):
            nonlocal passed
            passed = view

        def dec_a(view):
            def wrapper():
                return ["a"] + view()

            return wrapper

        def dec_b(view):
            def wrapper():
                return ["b"] + view()

            return wrapper

        @endpoint(route, dec_a, dec_b)
        def view():
            return ["v"]

        self.assertListEqual(["a", "b", "v"], passed())

    def test_multiple_enpoints(self) -> None:
        """multiple endpoints don't break app"""

        def dec(view):
            def wrapper():
                return view()

            return wrapper

        @endpoint(app.route("/a"), dec)
        def view_a() -> dict:
            return {}

        try:

            @endpoint(app.route("/b"), dec)
            def view_b() -> dict:
                return {}

        except AssertionError:
            self.fail()


class RestTests(TestCase):
    """rest tests"""

    def test_jsonify(self) -> None:
        """Data are jsonified"""

        @rest
        def view() -> dict:
            return dict()

        with app.app_context():
            self.assertTrue(isinstance(view(), Response))

    def test_data_integrity(self) -> None:
        """Data are preserved"""
        data = {"hello": "world"}

        @rest
        def view() -> dict:
            return data

        with app.app_context():
            # pylint: disable=no-member
            self.assertEqual(data, view().json)

    def test_data_params(self) -> None:
        """Params are parsed to view"""
        got_args = ()
        got_kwargs = {}

        @rest
        def view(*args, **kwargs) -> dict:
            nonlocal got_args, got_kwargs
            got_args = args
            got_kwargs = kwargs
            return dict()

        with app.app_context():
            # pylint: disable=no-member
            view(42, foo="bar")
            self.assertEqual(((42,), {"foo": "bar"}), (got_args, got_kwargs))


class ParametersTests(TestCase):
    """parameter tests"""

    def test_pass_arg(self) -> None:
        """pass positional arguments"""
        got = -1

        @parameters(42)
        def view(value):
            nonlocal got
            got = value

        view()  # pylint: disable=no-value-for-parameter

        self.assertEqual(42, got)

    def test_pass_kwarg(self) -> None:
        """pass keyword arguments"""
        got = -1

        @parameters(value=42)
        def view(value=-1):
            nonlocal got
            got = value

        view()  # pylint: disable=no-value-for-parameter

        self.assertEqual(42, got)

    def test_arg(self) -> None:
        """call positional arguments"""
        got = (-1, -1)

        @parameters(42)
        def view(value_a, value_b):
            nonlocal got
            got = (value_a, value_b)

        view(33)  # pylint: disable=no-value-for-parameter

        self.assertEqual((42, 33), got)

    def test_kwarg(self) -> None:
        """call keyword arguments"""
        got = (-1, -1)

        @parameters(value_a=42)
        def view(value_a=-1, value_b=-1):
            nonlocal got
            got = (value_a, value_b)

        view(value_b=33)  # pylint: disable=no-value-for-parameter

        self.assertEqual((42, 33), got)
