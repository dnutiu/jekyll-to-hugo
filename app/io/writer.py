from abc import abstractmethod, ABCMeta
from pathlib import Path
from typing import Callable
from app import utils


class IoWriter(metaclass=ABCMeta):
    """
    Abstract class for writing posts.
    """

    @abstractmethod
    def write(self, data: str):
        """
        Write a post

        Parameters
        ----------
        data: str
            The post data to write
        """
        raise NotImplementedError


class FileWriter(IoWriter):
    """
    Writes a post to a file.
    """

    def __init__(self, output_path: Path):
        utils.guard_against_none(output_path, "output_path")

        self.output_path = output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, data: str):
        with open(self.output_path, "w") as fo:
            fo.write(data)


class CallbackWriter(IoWriter):
    """
    Writes a post to a string.
    """

    def __init__(self, callback: Callable[[str], None]):
        utils.guard_against_none(callback, "callback")

        self.callback = callback

    def write(self, data: str):
        self.callback(data)
