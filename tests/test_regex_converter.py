import unittest

from automatapy.automata import EpsilonNFA
from automatapy.regex import Letter, Alternation, KleeneStar, Concatenation
from automatapy.regex.regex_converter import RegexConverter


class RegexConverterTest(unittest.TestCase):

    def setUp(self) -> None:
        self.converter = RegexConverter()

    def test_letter(self):
        a = Letter("a")
        nfa = a.accept(self.converter)

    def test_alternation(self):
        a, b = Letter("a"), Letter("b")
        r = Alternation(a, b)
        nfa = r.accept(self.converter)

    def test_kleenestar(self):
        a = Letter("a")
        r = KleeneStar(a)
        nfa = r.accept(self.converter)
        #print(nfa.ts.to_dot())

    def test_concatenation(self):
        a, b = Letter("a"), Letter("b")
        r = Concatenation(a, b)
        nfa = r.accept(self.converter)
        #print(nfa.ts.to_dot())

    def test_regex_1(self):
        a, b = Letter("a"), Letter("b")
        r = Alternation(Concatenation(a, b), KleeneStar(a))
        nfa: EpsilonNFA = r.accept(self.converter)
        print(nfa.ts.to_dot())
        print()
        nfa = nfa.to_nfa()
        dfa = nfa.determinize()
        print(dfa.ts.to_dot())


if __name__ == '__main__':
    unittest.main()
