import unittest

from automatapy.automata import NFA


class NFATest(unittest.TestCase):

    def setUp(self) -> None:
        self.nfa = NFA()
        q1, q2 = self.nfa.add_state(initial=True), self.nfa.add_state()
        self.nfa.add_transition(q1, "a", q2)
        self.nfa.add_transition(q1, "a", q1)
        self.nfa.add_transition(q2, "b", q1)
        self.nfa.set_final(q1)

    def test_accept(self):
        self.assertFalse(self.nfa.accepts("abba"))
        self.assertTrue(self.nfa.accepts("abab"))
        self.assertTrue(self.nfa.accepts("ab"))
        self.assertTrue(self.nfa.accepts(""))

    def test_determinize(self):
        dfa = self.nfa.determinize()
        print(dfa.ts.to_dot())


if __name__ == '__main__':
    unittest.main()
