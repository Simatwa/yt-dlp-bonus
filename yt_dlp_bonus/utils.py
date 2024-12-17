"""Common and frequently required functions across the package"""


def assert_instance(obj, inst, name="Value"):
    """Asserts instanceship of an object"""
    assert isinstance(
        obj, inst
    ), f"{name} must be an instance of {inst} not {type(obj)}"
