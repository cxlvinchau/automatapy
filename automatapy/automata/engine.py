import abc
from typing import Set, Hashable, Dict, Tuple, Union, Sequence

from automatapy.automata.core import State, Transition
from typing import Collection

from collections import deque


class Engine:

    @abc.abstractmethod
    def add_state(self, name=None, properties=None, initial=False, final=False) -> State:
        pass

    @abc.abstractmethod
    def add_transition(self, source: State, letter: Hashable, target: State) -> Transition:
        pass

    @abc.abstractmethod
    def set_final(self, state: State):
        pass

    @abc.abstractmethod
    def get_states(self) -> Collection[State]:
        pass

    @abc.abstractmethod
    def get_transitions(self) -> Collection[Transition]:
        pass


class NondeterministicEngine(Engine):
    """Nondeterministic engine implementation"""

    def __init__(self):
        self.states: Set[State] = set()
        self.initial_states: Set[State] = set()
        self.final_states: Set[State] = set()
        self.transitions: Set[Transition] = set()
        self.alphabet: Set[Hashable] = set()
        self.state_to_successor: Dict[State, Dict[Hashable, Union[Set[State], State]]] = dict()
        self.state_id = -1

    def get_successors(self, state: State, letter: Hashable = None) -> Union[Set[State], Set[Tuple[Hashable, State]]]:
        """
        Returns the successors of the state

        Parameters
        ----------
        state : State
            State for which the successors are returned
        letter : Hashable
            Letter for which successors should be returned, if None all successors are returned

        Returns
        -------
        Union[Set[State], Set[Tuple[Hashable, State]]]

        """
        if letter is None:
            return set([(letter, succ) for letter in self.state_to_successor.get(state, dict()).keys for succ in
                        self.state_to_successor[state][letter]])
        return self.state_to_successor.get(state, dict()).get(letter, set())

    def accepts(self, sequence: Sequence):
        """
        Checks whether the sequence is accepted by the automaton

        Parameters
        ----------
        sequence: A sequence of letters

        Returns
        -------
        bool

        """
        current = self.initial_states
        for letter in sequence:
            succ = set()
            for state in current:
                succ = succ.union(self.get_successors(state, letter))
            current = succ
        return len(current.intersection(self.final_states)) > 0

    def determinize(self):
        engine = DeterministicEngine()
        queue = deque([frozenset(self.initial_states)])
        set_to_state = {queue[0]: engine.add_state(properties={"states": queue[0]}, initial=True)}
        while queue:
            current = queue.popleft()


    def get_states(self) -> Collection[State]:
        return self.states

    def get_transitions(self) -> Collection[Transition]:
        return self.transitions


class DeterministicEngine(NondeterministicEngine):
    """Deterministic engine implementation"""

    def add_transition(self, source: State, letter: Hashable, target: State) -> Transition:
        succ_dict = self.state_to_successor.setdefault(source, dict())
        succ_dict[letter] = target
        transition = Transition(source, letter, target)
        self.transitions.add(transition)
        return transition

    def get_successors(self, state: State, letter: Hashable = None) -> Union[
        Set[State], Set[Tuple[Hashable, State]], None]:
        if letter is None:
            return set([(letter, self.state_to_successor[letter]) for letter in
                        self.state_to_successor.get(state, dict()).keys()])
        return self.state_to_successor.get(state, dict()).get(letter, None)

    def add_initial_state(self, state: State):
        if len(self.initial_states) >= 1:
            raise ValueError("Initial state already set")
        self.initial_states.add(state)
