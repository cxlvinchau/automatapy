from automatapy.automata.engine import Engine, NondeterministicEngine
from typing import Collection, Sequence, Hashable
from automatapy.automata.core import State, Transition, TransitionSystem
import abc


class FiniteAutomaton:

    def __init__(self, ts: TransitionSystem = None, engine: Engine = None):
        self.ts: TransitionSystem = ts if ts is not None else TransitionSystem()
        self.engine: Engine = engine

    def get_states(self) -> Collection[State]:
        """
        Returns the states of the automaton

        Returns
        -------
        Set[State]

        """
        return self.ts.states

    def get_transitions(self) -> Collection[Transition]:
        """
        Returns the transitions of the automaton

        Returns
        -------
        Set[Transition]

        """
        return self.ts.transitions

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
        return self.ts.add_state(name=name, properties=properties, initial=initial, final=final)

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
        self.ts.set_final(state)

    def add_transition(self, source: State, letter: Hashable, target: State):
        return self.ts.add_transition(source, letter, target)


class EpsilonNFA(FiniteAutomaton):
    pass


class NFA(FiniteAutomaton):
    """Nondeterministic finite automaton implementation"""

    def __init__(self):
        super().__init__(engine=NondeterministicEngine())
        self.engine.set_transition_system(self.ts)

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
        pass
