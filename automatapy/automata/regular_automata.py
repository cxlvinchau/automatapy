from automatapy.automata.engine import Engine, NondeterministicEngine, DeterministicEngine
from typing import Collection, Sequence, Hashable
from automatapy.automata.core import State, Transition
import abc


class FiniteAutomaton:

    def __init__(self, engine: Engine):
        self.engine: Engine = engine

    def get_states(self) -> Collection[State]:
        """
        Returns the states of the automaton

        Returns
        -------
        Set[State]

        """
        return self.engine.get_states()

    def get_transitions(self) -> Collection[Transition]:
        """
        Returns the transitions of the automaton

        Returns
        -------
        Set[Transition]

        """
        return self.engine.get_transitions()

    def add_state(self, name=None, properties=None, initial=False, final=False):
        """
        Adds a state to the automaton

        Parameters
        ----------
        name : str
            Name of the state
        properties : Dict[str, Any]
            Properties of the state
        initial : bool
            Determines whether the state is an initial state
        final : bool
            Determines whether the state is final

        Returns
        -------
        State
            A newly created state

        """
        return self.engine.add_state(name=name, properties=properties, initial=initial, final=final)

    def set_final(self, state: State):
        """
        Makes the given state final

        Parameters
        ----------
        state : State
            State that is made final

        Returns
        -------

        """
        self.engine.set_final(state)

    def add_transition(self, source: State, letter: Hashable, target: State):
        return self.engine.add_transition(source, letter, target)


class EpsilonNFA(FiniteAutomaton):
    pass


class NFA(FiniteAutomaton):
    """Nondeterministic finite automaton implementation"""

    def __init__(self):
        super().__init__(NondeterministicEngine())

    def accepts(self, sequence: Sequence):
        """
        Checks whether the automaton accepts the given sequence

        Parameters
        ----------
        sequence : Sequence
            Sequence to be checked

        Returns
        -------
        bool

        """
        return self.engine.accepts(sequence)


class DFA(FiniteAutomaton):

    def __init__(self):
        super().__init__(DeterministicEngine())
