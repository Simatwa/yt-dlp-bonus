"""Common and frequently required functions across the package"""

from typing import Sequence


def assert_instance(obj, inst, name="Value"):
    """Asserts instanceship of an object"""
    assert isinstance(
        obj, inst
    ), f"{name} must be an instance of {inst} not {type(obj)}"


def assert_type(obj, type_: object | Sequence[object], name: str = "Value"):
    """Aserts obj is of type type_"""
    if isinstance(type_, Sequence):
        assert (
            type(obj) in type_
        ), f"{name} must be one of types {type_} not {type(obj)}"
    else:
        assert type(obj) is type_, f"{name} must of type {type_} not {type(obj)}"
