import abc
from typing import Set, Hashable, Dict, Tuple, Union, Sequence

from automatapy.automata.core import State, Transition, TransitionSystem, Epsilon
from typing import Collection

from collections import deque


class Engine:

    def __init__(self):
        self.ts: TransitionSystem = None

    def set_transition_system(self, ts: TransitionSystem):
        self.ts = ts


class EpsilonEngine(Engine):

    def remove_epsilon(self) -> TransitionSystem:
        """
        Removes the epsilon transitions from a transition system. The resulting transition system does not contain any
        epsilon transitions

        Returns
        -------
        TransitionSystem
            Transition system without epsilon transitions

        """
        # Add transitions from initial states to worklist
        worklist = []
        for state in self.ts.initial_states:
            for letter in self.ts.enabled_letters(state):
                for target in self.ts.get_successor(state, letter):
                    worklist.append(Transition(state, letter, target))
        ts = TransitionSystem()
        state_dict: Dict[State, State] = dict()
        # Add initial states to visited dictionary
        for state in self.ts.initial_states:
            state_dict[state] = ts.add_state(initial=True)
            if state in self.ts.final_states:
                ts.set_final(state_dict[state])
        # delta contains non-epsilon transitions, epsilon_delta contains epsilon transitions
        delta, epsilon_delta = set(), set()
        while worklist:
            t = worklist.pop()
            print(t)
            # Create new state if it has not been visited before
            if t.target not in state_dict:
                state_dict[t.target] = ts.add_state()
                if t.target in self.ts.final_states:
                    ts.set_final(state_dict[t.target])
            # Check whether the transition is an epsilon transition
            if t.letter == Epsilon():
                # Epsilon case
                epsilon_delta.add(t)
                if state_dict[t.target] in ts.final_states:
                    ts.set_final(state_dict[t.source])
                for letter in self.ts.enabled_letters(t.target):
                    for target in self.ts.get_successor(t.target, letter):
                        t1 = Transition(t.source, letter, target)
                        if t1 not in delta and t1 not in epsilon_delta:
                            worklist.append(t1)
            else:
                delta.add(t)
                # Add to transition system
                ts.add_transition(state_dict[t.source], t.letter, state_dict[t.target])
                # Iterate over epsilon successors of target
                for target in self.ts.get_successor(t.target, Epsilon()):
                    t1 = Transition(t.source, t.letter, target)
                    if t1 not in delta:
                        worklist.append(t1)
                for letter in self.ts.enabled_letters(t.target, ignore_epsilon=True):
                    for target in self.ts.get_successor(t.target, letter):
                        t1 = Transition(t.target, letter, target)
                        if t1 not in delta:
                            worklist.append(t1)
        print([str(t) for t in epsilon_delta])
        print([str(t) for t in delta])
        return ts


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
