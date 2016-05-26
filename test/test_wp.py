import unittest

from imp_parser import *
from imp_lexer import *

from i_util import *
from wp import *

class TestWP(unittest.TestCase):
    maxDiff = None

    def program_test(self, code, expected):
        tokens = imp_lex(loop)
        result = imp_parse(tokens)
        self.assertNotEquals(None, result)
        (pre, commands, pos) = to_triple(result.value)
        self.assertEquals(expected, invariant.condition)

    def test_extract_true(self):
        code = 'while x > 0 do x := 1 end'
        expected = TrueBexp()
        self.program_test(code, expected)

