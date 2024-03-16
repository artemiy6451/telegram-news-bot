import re


class RegexEqual(str):
    string: str

    def __eq__(self, pattern):
        return bool(re.search(pattern, self))

    def __getitem__(self, group) -> str:
        return self.string[group]
