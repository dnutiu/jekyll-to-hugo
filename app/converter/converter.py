import logging
import os
from pathlib import Path

from app import utils
from app.config import Configurator
from app.converter.wordpress_markdown import WordpressMarkdownConverter


class Converter:
    """
    Convert Jekyll posts to Hugo posts
    """

    def __init__(self, configurator: Configurator):
        """
        Initializes the converter

        Parameters
        ----------
        configurator : Configurator
            The configurator instance.
        """
        utils.guard_against_none(configurator, "configurator")

        self._logger = logging.getLogger(__name__)

        self._jekyll_posts_path = configurator.source_path
        self._hugo_posts_path = configurator.output_path

        self._logger.info(
            f"Using source: {self._jekyll_posts_path} output: {self._hugo_posts_path}"
        )

        # The converter that converts the markdown
        self.markdown_converter = WordpressMarkdownConverter(configurator)

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