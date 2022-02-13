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

    def add_state(self, name=None, properties=None, initial=False, final=False) -> State:
        """
        Adds a state to the engine

        Parameters
        ----------
        name : str
            Name of the state
        properties : Dict[str, Any]
            Dictionary with properties
        initial : bool
            Determines whether the state is initial or not
        final : bool
            Determines whether the state is final or not

        Returns
        -------

        """
        self.state_id += 1
        state = State(self.state_id, name=name, properties=properties)
        self.states.add(state)
        if initial:
            self.add_initial_state(state)
        if final:
            self.final_states.add(state)
        return state

    def add_transition(self, source: State, letter: Hashable, target: State) -> Transition:
        """
        Adds a transition to the engine

        Parameters
        ----------
        source : State
            Source state
        letter : Hashable
            Letter read by the transition
        target : State
            Target state

        Returns
        -------
        Transition
            Transition from source state to target state reading the specified letter

        """
        succ_dict = self.state_to_successor.setdefault(source, dict())
        succs = succ_dict.setdefault(letter, set())
        succs.add(target)
        transition = Transition(source, letter, target)
        self.transitions.add(transition)
        return transition

    def add_initial_state(self, state: State):
        """
        Adds an initial state

        Parameters
        ----------
        state : State
            Initial state to be added

        Returns
        -------

        """
        self.initial_states.add(state)

    def set_final(self, state: State):
        """
        Makes the given state final

        Parameters
        ----------
        state : State
            State to be made final

        Returns
        -------

        """
        self.final_states.add(state)

    def enabled_letters(self, state: State):
        """
        Returns the letters enabled in the given state

        Parameters
        ----------
        state : State
            State

        Returns
        -------
        List[Hashable]
            List of letters enabled in the given state

        """
        return list(self.state_to_successor.get(state, dict()).keys())

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
