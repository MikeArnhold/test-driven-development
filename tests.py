"""Test implementations"""
from typing import Any, Callable, Dict, List, Tuple
from unittest import TestCase

from flask import Response
from werkzeug.wrappers.response import Response as WerkzeugResponse

from decorators import convert, endpoint, parameters, rest
from main import app, index, service
from request import BaseFormRequest


class TestIndex(TestCase):
    """index tests"""

    def test_index(self):
        """Index returns greetind as data dict"""
        self.assertEqual({"greeting": "Hello, World!"}, index())


class DictFormatTests(TestCase):
    """view_format tests"""

    def test_palin(self) -> None:
        """return plain"""
        data = dict(foo=42)

        @convert()
        def view():
            return dict(foo=42)

        with app.app_context():
            self.assertEqual(data, view())

    def test_render_div_foo_42(self) -> None:
        """render foo=42 within div"""

        convert_dict = lambda d, fmt: fmt.format(**d)

        @convert((dict, convert_dict), fmt="__{foo}__")
        def view():
            return dict(foo=42)

        with app.app_context():
            self.assertEqual("__42__", view())

    def test_render_p_bar_33(self) -> None:
        """render bar=33 within p"""

        convert_dict = lambda d, fmt: fmt.format(**d)

        @convert((dict, convert_dict), fmt="~~{bar}~~")
        def view():
            return dict(bar=33)

        with app.app_context():
            self.assertEqual("~~33~~", view())

    def test_render_span_parameters(self) -> None:
        """render view parameters within span"""

        convert_dict = lambda d, fmt: fmt.format(**d)

        @convert((dict, convert_dict), fmt="--{smurf}--")
        def view(key, value="papa"):
            ret = {}
            ret[key] = value
            return ret

        with app.app_context():
            self.assertEqual("--mama--", view("smurf", "mama"))

    def test_return_pure_response(self) -> None:
        """Text data don't cause exception"""

        response = WerkzeugResponse("abc")

        convert_dict = lambda d, fmt: fmt.format(**d)
        return_plain = lambda d, **_: d

        @convert(
            (dict, convert_dict),
            (WerkzeugResponse, return_plain),
            fmt="--{smurf}--",
        )
        def view():
            return response

        with app.app_context():
            self.assertEqual(response, view())


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
        passed: Callable[[], List[str]]

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
        def view():
            return data

        with app.app_context():
            # pylint: disable=no-member
            self.assertEqual(data, view().json)

    def test_data_params(self) -> None:
        """Params are parsed to view"""
        got_args: Tuple[Any, ...] = ()
        got_kwargs = {}

        @rest
        def view(*args, **kwargs) -> dict:
            nonlocal got_args, got_kwargs
            got_args = args
            got_kwargs = kwargs
            return dict()

        with app.app_context():
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

    def test_return(self) -> None:
        """return wrapped return value"""

        @parameters()
        def view():
            return 42

        self.assertEqual(42, view())


class BaseMockRequest(BaseFormRequest):
    """lazy mock request"""

    @property
    def method(self):
        raise NotImplementedError()

    @property
    def form(self):
        raise NotImplementedError()


class SeriveTests(TestCase):
    """service tests"""

    def test_new_service(self) -> None:
        """Identify new serive"""

        class _MockRequest(BaseMockRequest):
            @property
            def method(self):
                return "GET"

        data = service(
            service_id=42,
            service_request=_MockRequest(),
            services={},
            success_redirect=lambda _: None,
        )
        self.assertTrue(data["new"])

    def test_service_not_new(self) -> None:
        """Identify existing serive"""

        class _MockRequest(BaseMockRequest):
            @property
            def method(self):
                return "GET"

        data = service(
            service_id=42,
            service_request=_MockRequest(),
            services={42: ""},
            success_redirect=lambda _: None,
        )
        self.assertFalse(data["new"])

    def test_create_new_service(self) -> None:
        """Identify new serive"""
        services: Dict[int, str] = {}

        class _MockRequest(BaseMockRequest):
            @property
            def method(self):
                return "POST"

            @property
            def form(self):
                return {"name": ""}

        service(
            service_id=11,
            service_request=_MockRequest(),
            services=services,
            success_redirect=lambda _: None,
        )
        self.assertTrue(11 in services.keys())

    def test_don_create_new_service_when_get(self) -> None:
        """Don't create new service on get"""
        services: Dict[int, str] = {}

        class _MockRequest(BaseMockRequest):
            @property
            def method(self):
                return "GET"

        service(
            service_id=11,
            service_request=_MockRequest(),
            services=services,
            success_redirect=lambda _: None,
        )
        self.assertTrue(11 not in services.keys())

    def test_create_new_service_with_name(self) -> None:
        """Create new posted service with name"""
        services: Dict[int, str] = {}

        class _MockRequest(BaseMockRequest):
            @property
            def method(self):
                return "POST"

            @property
            def form(self):
                return {"name": "foo"}

        service(
            service_id=3,
            service_request=_MockRequest(),
            services=services,
            success_redirect=lambda _: None,
        )
        self.assertEqual("foo", services[3])

    def test_service_id_and_anme(self) -> None:
        """Identify new serive"""

        class _MockRequest(BaseMockRequest):
            @property
            def method(self):
                return "GET"

        data = service(
            service_id=4,
            service_request=_MockRequest(),
            services={4: "bar"},
            success_redirect=lambda _: None,
        )
        self.assertEqual(
            (4, "bar"),
            (data.get("service_id"), data.get("service_name")),
        )

    def test_use_success_redirect(self) -> None:
        """POST success triggers redirect call"""

        class _MockRequest(BaseMockRequest):
            @property
            def method(self):
                return "POST"

            @property
            def form(self):
                return {"name": "foo"}

        def _redirect(service_id):
            return f"was redirected to service/{service_id}"

        data = service(
            service_id=4,
            service_request=_MockRequest(),
            services={4: "bar"},
            success_redirect=_redirect,
        )

        self.assertEqual("was redirected to service/4", data)
