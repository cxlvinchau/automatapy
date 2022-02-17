from automatapy.automata.engine import Engine, NondeterministicEngine, EpsilonEngine
from typing import Collection, Sequence, Hashable
from automatapy.automata.core import State, Transition, TransitionSystem
import abc


class FiniteAutomaton:

    def __init__(self, engine: Engine, ts: TransitionSystem = None):
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
        """
        Adds a transition to the automaton

        Parameters
        ----------
        source: State
            Source of the transition
        letter: Hashable
            Letter to be read
        target: State
            Target of the transition

        Returns
        -------
        Transition
            The specified transition
        """
        return self.ts.add_transition(source, letter, target)


class EpsilonNFA(FiniteAutomaton):
    """Epsilon nondeterministic finite automaton implementation"""

    def __init__(self, **kwargs):
        super().__init__(EpsilonEngine(), **kwargs)
        self.engine.set_transition_system(self.ts)

    def to_nfa(self):
        """
        Converts the epsilon NFA to an NFA

        Returns
        -------
        NFA
            Nondeterministic finite automaton

        """
        ts = self.engine.remove_epsilon()
        return NFA(ts=ts)


class NFA(FiniteAutomaton):
    """Nondeterministic finite automaton implementation"""

    def __init__(self, **kwargs):
        super().__init__(NondeterministicEngine(), **kwargs)
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

    def determinize(self, alphabet=None):
        """
        Determinizes the nondeterministic finite automaton with the powerset construction

        Parameters
        ----------
        alphabet: Set[Hashable]
            Optional argument. Powerset construction is constructed w.r.t. to the alphabet. If None, then the construction
            is done with the alphabet of the NFA

        Returns
        -------
        DFA
            Deterministic finite automaton

        """
        ts = self.engine.determinize(alphabet)
        return DFA(ts=ts)


class DFA(FiniteAutomaton):

    def __init__(self, **kwargs):
        super().__init__(NondeterministicEngine(), **kwargs)
        self.engine.set_transition_system(self.ts)
        pass
