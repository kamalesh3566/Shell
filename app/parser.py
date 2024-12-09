import typing

END = "\0"
SPACE = " "
SINGLE = "'"
DOUBLE = '"'
BACKSLASH = "\\"


class LineParser:
    def __init__(self, line: str):
        self._iterator = iter(line)
        self._builder = ""

    def parse(self):
        strings: typing.List[str] = []
        while (character := self._next()) != END:
            if character == SPACE:
                if self._builder:
                    strings.append(self._builder)
                    self._builder = ""
            elif character == SINGLE:
                self._single_quote()
            elif character == DOUBLE:
                self._double_quote()
            elif character == BACKSLASH:
                self._backslash(False)
            else:
                self._builder += character
        if self._builder:
            strings.append(self._builder)
        return strings

    def _single_quote(self):
        # Collect everything literally until the closing single quote
        while (character := self._next()) != END and character != SINGLE:
            self._builder += character

    def _double_quote(self):
        while (character := self._next()) != END and character != DOUBLE:
            if character == BACKSLASH:
                self._backslash(True)
            else:
                self._builder += character

    def _backslash(self, in_quote: bool):
        character = self._next()
        if character == END:
            return
        if in_quote:
            # Handle special cases for backslash within double quotes
            if character in [DOUBLE, BACKSLASH, "$", "\n"]:
                self._builder += character
            else:
                # Preserve the backslash literally if it doesn't escape a special character
                self._builder += BACKSLASH + character
        else:
            self._builder += character

    def _next(self):
        return next(self._iterator, END)
