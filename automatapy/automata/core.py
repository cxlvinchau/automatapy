from typing import Hashable, Set, Dict, List

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


class TransitionSystem:

    def __init__(self):
        self.states: Set[State] = set()
        self.transitions: Set[Transition] = set()
        self.state_to_transitions: Dict[State, Set[Transition]]= dict()
        self.state_id: int = -1
        self.alphabet: Set[Hashable] = set()
        self.initial_states = set()

    def add_state(self, name=None, properties=None, initial=False, final=False) -> State:
        """
        Adds a state to the transition system

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
        Adds a transition to the transition system

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
        transition = Transition(source, letter, target)
        self.transitions.add(transition)
        self.state_to_transitions.setdefault(source, set()).add(transition)
        return transition

    def set_initial(self, state: State):
        """
        Adds a state to the set of initial states

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
        Adds a state to the set of final states

        Parameters
        ----------
        state : State
            State to be made final

        Returns
        -------

        """
        self.final_states.add(state)

    def enabled_letters(self, state: State) -> Set[Hashable]:
        """
        Returns the letters enabled in the given state

        Parameters
        ----------
        state : State
            State

        Returns
        -------
        Set[Hashable]
            Set of letters enabled in the given state

        """
        return set([transition.letter for transition in self.state_to_transitions.get(state, [])])
