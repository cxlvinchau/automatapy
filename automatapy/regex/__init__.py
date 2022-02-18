from __future__ import annotations
from abc import abstractmethod

from typing import Any


class Regex:

    @abstractmethod
    def accept(self, regex_visitor: RegexVisitor):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Letter(Regex):

    def __init__(self, letter):
        self.letter = letter

    def accept(self, regex_visitor: RegexVisitor):
        return regex_visitor.visit_letter(self)

    def __str__(self):
        return str(self.letter)


class Alternation(Regex):

    def __init__(self, r1: Regex, r2: Regex):
        self.r1 = r1
        self.r2 = r2

    def accept(self, regex_visitor: RegexVisitor):
        return regex_visitor.visit_alternation(self)

    def __str__(self):
        return f"({str(self.r1)} + {str(self.r2)})"


class KleeneStar(Regex):

    def __init__(self, r: Regex):
        self.r = r

    def accept(self, regex_visitor: RegexVisitor):
        return regex_visitor.visit_kleenestar(self)

    def __str__(self):
        return f"({str(self.r)})*"


class Concatenation(Regex):

    def __init__(self, r1: Regex, r2: Regex):
        self.r1 = r1
        self.r2 = r2

    def accept(self, regex_visitor: RegexVisitor):
        return regex_visitor.visit_concatenation(self)

    def __str__(self):
        return str(self.r1) + str(self.r2)


class RegexVisitor:

    @abstractmethod
    def visit_letter(self, regex: Letter) -> Any:
        pass

    @abstractmethod
    def visit_concatenation(self, regex: Regex) -> Any:
        pass

    @abstractmethod
    def visit_kleenestar(self, regex: KleeneStar) -> Any:
        pass

    @abstractmethod
    def visit_alternation(self, regex: Alternation) -> Any:
        pass

