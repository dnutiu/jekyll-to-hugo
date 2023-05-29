from pathlib import Path

import yaml
from bs4 import BeautifulSoup, Tag

from app.utils import key_error_silence


class WordpressMarkdownConverter:
    """
    Markdown converter that converts jekyll posts to hugo posts.
    """

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
        with key_error_silence():
            del header["restapi_import_id"]
        with key_error_silence():
            del header["original_post_id"]
        with key_error_silence():
            del header["timeline_notification"]
        with key_error_silence():
            del header["wordads_ufa"]
        header["guid"] = header["guid"].replace("http://localhost", "")
        header["author"] = "Denis Nuțiu"
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
                    if "is-provider-youtube" in content.attrs.get("class", []):
                        video_link = content.findNext("iframe").attrs["src"]
                        video_id_part = video_link.rsplit("/")
                        video_id = video_id_part[-1].split("?")[0]
                        fixed_lines.append(f"{{{{< youtube {video_id} >}}}}\n")
                    else:
                        tags = list(map(str, content.contents))
                        if tags:
                            fixed_tags = self.remove_html_tags(tags)
                            if fixed_tags:
                                fixed_lines.extend(fixed_tags)
                else:
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
        post_content = post_content.replace("http://localhost/", "/")
        post_content = post_content.replace(
            "https://nuculabs.wordpress.com/", "https://nuculabs.dev/posts/"
        )
        # fix unknown tags
        post_lines = post_content.split("\n")
        fixed_lines = self.remove_html_tags(post_lines)

        return "\n".join(fixed_lines)

    def read_jekyll_post(self, path: Path):
        """
        Read a Jekyll post from the specified path

        Parameters
        ----------
        path : Path
            The path to the Jekyll post
        """
        # read source
        with open(path, "r") as fh:
            contents = fh.read()
        return contents

    def write_hugo_post(self, output_path, post_header: dict, post_content: str):
        """
        Write a Hugo post to the specified path

        Parameters
        ----------
        output_path : Path
            The path to the Hugo post
        post_header : dict
            The post header
        post_content : str
            The post content
        """
        with open(output_path, "w") as fo:
            header = ["---\n", yaml.dump(post_header), "---\n"]
            fo.writelines(header)
            fo.write(post_content)

    def convert_jekyll_to_hugo(self, jekyll_post_path: Path, hugo_post_output: Path):
        """
        Convert a Jekyll post to a Hugo post

        Parameters
        ----------
        jekyll_post_path : Path
            The path to the Jekyll post
        hugo_post_output : Path
            The path to the Hugo post
        """
        contents = self.read_jekyll_post(jekyll_post_path)

        # fix header
        header = yaml.safe_load(contents.split("---")[1])
        fixed_header = self.fix_hugo_header(header)
        # fix content
        post_content = contents.split("---", 2)[2].lstrip()
        fixed_post_content = self.convert_post_content(post_content)

        self.write_hugo_post(
            hugo_post_output.joinpath(jekyll_post_path.name),
            fixed_header,
            fixed_post_content,
        )
