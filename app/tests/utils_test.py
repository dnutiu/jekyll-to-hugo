import pytest

from app.utils import key_error_silence, guard_against_none_or_empty_str


def test_key_error_silence():
    # Test that the context manager silences the exception
    with key_error_silence():
        raise KeyError
    # Test that the context manager does not silence other exceptions
    with pytest.raises(ValueError):
        with key_error_silence():
            raise ValueError


@pytest.mark.parametrize(
    "input_data",
    [
        (""),
        (None),
        (1),
        (True),
        (False),
        ({}),
        ([]),
        ({"a": 1}),
    ],
)
def test_guard_against_none_or_empty_str(input_data):
    with pytest.raises(ValueError):
        guard_against_none_or_empty_str(input_data, "test")


def test_guard_against_none_or_empty_str_happy():
    guard_against_none_or_empty_str("a", "test")
