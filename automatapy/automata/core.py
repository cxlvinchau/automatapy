from typing import Hashable

from automatapy.utils import SingletonMetaclass


class State:

    def __init__(self, state_id, name=None, properties=None):
        self.name = name
        self.state_id = state_id
        self.properties = properties

    def __eq__(self, other):
        if isinstance(other, State):
            return self.state_id == other.state_id
        return False

    def __hash__(self):
        return hash(self.state_id) + hash(self.name)

    def __str__(self):
        return f"q{self.state_id}" if self.name is None else self.name

    def __repr__(self):
        return f"State({self.state_id}, name={self.name}, properties={self.properties})"


class Epsilon(metaclass=SingletonMetaclass):

    def __eq__(self, other):
        return isinstance(Epsilon)

    def __hash__(self):
        return hash("epsilon")


class Transition:

    def __init__(self, source: State, letter: Hashable, target: State):
        self.source = source
        self.letter = letter
        self.target = target

    def __eq__(self, other):
        if isinstance(other, Transition):
            return other.source == self.source and other.letter == self.letter and other.target == self.target
        return False

    def __hash__(self):
        return hash(self.source) + hash(self.letter) + hash(self.target)
