from typing import Any

from automatapy.automata import EpsilonNFA, Epsilon
from regex import RegexVisitor, Alternation, KleeneStar, Regex, Letter, Concatenation


class RegexConverter(RegexVisitor):

    def visit_letter(self, regex: Letter) -> EpsilonNFA:
        nfa = EpsilonNFA()
        q1, q2 = nfa.add_state(initial=True), nfa.add_state(final=True)
        nfa.add_transition(q1, regex.letter, q2)
        return nfa

    def visit_concatenation(self, regex: Concatenation) -> EpsilonNFA:
        nfa1: EpsilonNFA = regex.r1.accept(self)
        nfa2: EpsilonNFA = regex.r2.accept(self)
        nfa1.ts.states = nfa1.ts.states.union(nfa2.ts.states)
        for s1 in nfa1.get_final_states():
            for s2 in nfa2.get_initial_states():
                nfa1.add_transition(s1, Epsilon(), s2)
        nfa1.ts.final_states = nfa2.ts.final_states
        for t in nfa2.get_transitions():
            nfa1.add_transition(t.source, t.letter, t.target)
        return nfa1

    def visit_kleenestar(self, regex: KleeneStar) -> EpsilonNFA:
        nfa: EpsilonNFA = regex.r.accept(self)
        q_init, q_final = nfa.add_state(), nfa.add_state()
        for q in nfa.get_initial_states():
            nfa.add_transition(q_init, Epsilon(), q)
        for q in nfa.get_final_states():
            nfa.add_transition(q, Epsilon(), q_final)
        nfa.ts.initial_states = set([q_init])
        nfa.ts.final_states = set([q_final])
        nfa.add_transition(q_final, Epsilon(), q_init)
        nfa.add_transition(q_init, Epsilon(), q_final)
        return nfa

    def visit_alternation(self, regex: Alternation) -> EpsilonNFA:
        nfa1: EpsilonNFA = regex.r1.accept(self)
        nfa2: EpsilonNFA = regex.r2.accept(self)
        nfa1.ts.states = nfa1.ts.states.union(nfa2.ts.states)
        for t in nfa2.get_transitions():
            nfa1.add_transition(t.source, t.letter, t.target)
        q_init, q_final = nfa1.add_state(), nfa1.add_state()
        for q in nfa1.get_initial_states():
            nfa1.add_transition(q_init, Epsilon(), q)
        for q in nfa2.get_initial_states():
            nfa1.add_transition(q_init, Epsilon(), q)
        for q in nfa1.get_final_states():
            nfa1.add_transition(q, Epsilon(), q_final)
        for q in nfa2.get_final_states():
            nfa1.add_transition(q, Epsilon(), q_final)
        nfa1.ts.initial_states = set([q_init])
        nfa1.ts.final_states = set([q_final])
        return nfa1
