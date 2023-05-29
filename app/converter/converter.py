import os
from pathlib import Path

from app import utils
from app.converter.wordpress_markdown import WordpressMarkdownConverter


class Converter:
    """
    Convert Jekyll posts to Hugo posts
    """

    def __init__(self, jekyll_posts_path: str, hugo_posts_path: str):
        """
        Initializes the converter

        Parameters
        ----------
        jekyll_posts_path : str
            The path to the Jekyll posts
        hugo_posts_path : str
            The path to the Hugo posts
        """
        utils.guard_against_none_or_empty_str(jekyll_posts_path, "jekyll_posts_path")
        utils.guard_against_none_or_empty_str(hugo_posts_path, "hugo_posts_path")

        self._jekyll_posts_path = jekyll_posts_path
        self._hugo_posts_path = hugo_posts_path

        # The converter that converts the markdown
        self.markdown_converter = WordpressMarkdownConverter()

    def convert(self):
        """
        Converts the Jekyll posts to Hugo posts
        """
        source_path = self._jekyll_posts_path
        output_path = Path(self._hugo_posts_path)
        _, _, files = next(os.walk(source_path))
        for file in files:
            source_abs_path = source_path / Path(file)
            self.markdown_converter.convert_jekyll_to_hugo(
                source_abs_path,
                output_path,
            )
