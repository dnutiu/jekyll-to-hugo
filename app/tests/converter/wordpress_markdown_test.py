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
