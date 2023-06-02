import re

from app import utils


class RegexHeuristics:
    """
    Regex heuristics class for applying modifying a line using regex lines.
    """

    def __init__(self, configurator):
        utils.guard_against_none(configurator, "configurator")

        self.configurator = configurator
        self._rules = {
            "^(</*pre.*?>)`{0,3}(?P<content>.*?)(<\/pre>)?$": self._remove_pre_tag,
        }

    def _remove_pre_tag(self, match) -> str:
        """
        Removes the pre tag from the match.
        """
        return match.group("content")

    def handle_regex_heuristics(self, line: str) -> str:
        """
        Manipulates a line by using regex heuristics.
        """
        for regex, callback in self._rules.items():
            match = re.match(regex, line)
            if match:
                return callback(match)
            else:
                return line
