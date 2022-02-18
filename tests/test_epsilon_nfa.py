import unittest

from automatapy.automata import EpsilonNFA, Epsilon


class EpsilonNFATest(unittest.TestCase):

    def setUp(self) -> None:
        self.eps_nfa = EpsilonNFA()
        q1, q2, q3 = self.eps_nfa.add_state(initial=True), self.eps_nfa.add_state(final=True), self.eps_nfa.add_state(final=True)
        self.eps_nfa.add_transition(q1, Epsilon(), q2)
        self.eps_nfa.add_transition(q1, Epsilon(), q3)
        self.eps_nfa.add_transition(q2, "a", q2)
        self.eps_nfa.add_transition(q3, "b", q3)

    def test_to_nfa(self):
        nfa = self.eps_nfa.to_nfa()
        self.assertTrue(nfa.accepts(""))
        self.assertTrue(nfa.accepts("aaaaaaaaa"))
        self.assertTrue(nfa.accepts("bbbbbbbbb"))
        self.assertFalse(nfa.accepts("abbbbbbbbb"))



if __name__ == '__main__':
    unittest.main()
