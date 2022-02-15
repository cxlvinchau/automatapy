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

    def determinize(self, alphabet=None):
        """
        Returns a deterministic version of the nondeterministic transition system

        Returns
        -------
        TransitionSystem
            Deterministic transition system
        """
        ts = TransitionSystem()
        alphabet = self.ts.alphabet if alphabet is None else alphabet
        worklist = [ts.add_state(name=f"q0", properties={"states": frozenset(self.ts.initial_states)}, initial=True,
                                 final=len(frozenset(self.ts.initial_states).intersection(self.ts.final_states)) > 0)]
        set_to_state = {worklist[0].properties["states"]: worklist[0]}
        counter = 0
        while worklist:
            current = worklist.pop()
            for letter in alphabet:
                succ = frozenset(self.ts.get_successor(current.properties["states"], letter))
                if succ not in set_to_state:
                    counter += 1
                    state = ts.add_state(name=f"q{counter}", properties={"states": succ})
                    if len(succ.intersection(self.ts.final_states)) > 0:
                        ts.set_final(state)
                    worklist.append(state)
                    set_to_state[succ] = state
                ts.add_transition(current, letter, set_to_state[succ])
        return ts