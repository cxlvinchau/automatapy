import abc
from typing import Set, Hashable, Dict, Tuple, Union, Sequence

from automatapy.automata.core import State, Transition, TransitionSystem
from typing import Collection

from collections import deque


class Engine:

    def __init__(self):
        self.ts: TransitionSystem = None

    @abc.abstractmethod
    def accepts(self):
        pass

    def set_transition_system(self, ts: TransitionSystem):
        self.ts = ts


class NondeterministicEngine(Engine):
    """Nondeterministic engine implementation"""

    def accepts(self, word: Sequence[Hashable]):
        """
        Checks whether the given word is accepted

        Parameters
        ----------
        word: Sequence[Hashable]
            Word

        Returns
        -------
        bool
            True if it is accepted, False otherwise
        """
        current = self.ts.initial_states
        while len(word) > 0:
            current = self.ts.get_successor(current, word[0])
            word = word[1:]
        return len(current.intersection(self.ts.final_states)) > 0



