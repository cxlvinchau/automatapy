import unittest

from automatapy.regex import Letter, Alternation


class RegexTest(unittest.TestCase):


    def test_create_regex(self):
        a, b = Letter("a"), Letter("b")
        r = Alternation(a, b)
        print(r)

if __name__ == '__main__':
    unittest.main()
