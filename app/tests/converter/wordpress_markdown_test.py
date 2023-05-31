import pytest

from app.config import ConverterOptions
from app.converter import WordpressMarkdownConverter
from app.tests.utils import make_fake_configurator


@pytest.mark.parametrize(
    "author_rewrite, input_header, expected_header",
    [
        ("", {"author": "author"}, {"author": ""}),
        ("", {}, {"author": ""}),
        ("", {"a": 1}, {"a": 1, "author": ""}),
        ("NucuLabs.dev", {"author": "Denis"}, {"author": "NucuLabs.dev"}),
    ],
)
def test_fix_hugo_header_rewrite_author(author_rewrite, input_header, expected_header):
    configurator = make_fake_configurator(
        "wordpress_markdown_converter",
        ConverterOptions(
            author_rewrite=author_rewrite,
            links_rewrite=[],
            header_fields_drop=[],
        ),
    )
    converter = WordpressMarkdownConverter(configurator)
    assert converter.fix_hugo_header(input_header) == expected_header


@pytest.mark.parametrize(
    "header_fields_drop, input_header, expected_header",
    [
        ([], {}, {"author": ""}),
        (["a"], {"a": 1, "b": 2, "c": 3}, {"author": "", "b": 2, "c": 3}),
        (["a", "b"], {"a": 1, "b": 2, "c": 3}, {"author": "", "c": 3}),
        ([], {"a": 1, "b": 2, "c": 3}, {"author": "", "a": 1, "b": 2, "c": 3}),
    ],
)
def test_fix_hugo_header_fields_drop(header_fields_drop, input_header, expected_header):
    configurator = make_fake_configurator(
        "wordpress_markdown_converter",
        ConverterOptions(
            author_rewrite="",
            links_rewrite=[],
            header_fields_drop=header_fields_drop,
        ),
    )
    converter = WordpressMarkdownConverter(configurator)
    assert converter.fix_hugo_header(input_header) == expected_header
