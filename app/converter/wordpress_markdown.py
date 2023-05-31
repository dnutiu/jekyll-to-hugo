import yaml
from bs4 import BeautifulSoup, Tag

from app import utils
from app.config import Configurator
from app.io.reader import IoReader
from app.io.writer import IoWriter
from app.utils import key_error_silence


class WordpressMarkdownConverter:
    """
    Markdown converter that converts jekyll posts to hugo posts.
    """

    def __init__(self, configurator: Configurator):
        """
        Initializes the WordpressMarkdownConverter

        Parameters
        ----------
        configurator : Configurator
            The configurator instance.
        """
        utils.guard_against_none(configurator, "configurator")
        self.configurator = configurator

    def fix_hugo_header(self, header: dict) -> dict:
        """
        Fix the Hugo header

        Parameters
        ----------
        header : dict
            The header to fix

        Returns
        -------
        dict
            The fixed header
        """
        for field in self.configurator.converter_options.header_fields_drop:
            with key_error_silence():
                del header[field]
        # rewrite header fields
        header["guid"] = header["guid"].replace("http://localhost", "")
        header["author"] = self.configurator.converter_options.author_rewrite
        return header

    def remove_html_tags(self, post_lines):
        fixed_lines = []
        for line in post_lines:
            if line == "":
                fixed_lines.append("\n")
                continue
            soup = BeautifulSoup(line)
            for content in soup.contents:
                if isinstance(content, Tag):
                    # Check if it is a youtube video and add it as a shortcode.
                    if "is-provider-youtube" in content.attrs.get("class", []):
                        video_link = content.findNext("iframe").attrs["src"]
                        video_id_part = video_link.rsplit("/")
                        video_id = video_id_part[-1].split("?")[0]
                        fixed_lines.append(f"{{{{< youtube {video_id} >}}}}\n")
                    # Fix unknown tags.
                    else:
                        tags = list(map(str, content.contents))
                        if tags:
                            fixed_tags = self.remove_html_tags(tags)
                            if fixed_tags:
                                fixed_lines.extend(fixed_tags)
                else:
                    # Add the content as is.
                    fixed_lines.append(str(content))
        return fixed_lines

    def convert_post_content(self, post_content: str) -> str:
        """
        Converts the post content

        Parameters
        ----------
        post_content : str
            The post content

        Returns
        -------
        str
            The converted post content
        """
        # fix  link
        for task in self.configurator.converter_options.links_rewrite:
            source_link = task.get("source")
            target_link = task.get("target")
            if not source_link or not target_link:
                continue
            post_content = post_content.replace(source_link, target_link)

        # fix unknown tags
        post_lines = post_content.split("\n")
        fixed_lines = self.remove_html_tags(post_lines)

        return "\n".join(fixed_lines)

    def read_jekyll_post(self, reader: IoReader):
        """
        Read a Jekyll post from the reader.

        Parameters
        ----------
        reader : IoReader
            The IoReader instance for reading.
        """
        # read source
        return reader.read()

    def write_hugo_post(self, writer: IoWriter, post_header: dict, post_content: str):
        """
        Write a Hugo post to the specified writer.

        Parameters
        ----------
        writer : IoWriter
            The IoWriter instance for writing.
        post_header : dict
            The post header
        post_content : str
            The post content
        """
        data = ["---\n", yaml.dump(post_header), "---\n", post_content]
        writer.write("".join(data))

    def convert_jekyll_to_hugo(self, reader: IoReader, writer: IoWriter):
        """
        Convert a Jekyll post to a Hugo post

        Parameters
        ----------
        reader : IoReader
            The IoReader instance for reading.
        writer : IoWriter
            The IoWriter instance for writing.
        """
        contents = self.read_jekyll_post(reader)

        # fix header
        header = yaml.safe_load(contents.split("---")[1])
        fixed_header = self.fix_hugo_header(header)
        # fix content
        post_content = contents.split("---", 2)[2].lstrip()
        fixed_post_content = self.convert_post_content(post_content)

        self.write_hugo_post(
            writer,
            fixed_header,
            fixed_post_content,
        )
