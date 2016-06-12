import unittest

from nose.tools import nottest

from imp_parser import *
from imp_lexer import *

from i_util import *
from i_vc_gen import *
from i_z3 import *

class TestZ3(unittest.TestCase):
    maxDiff = None

    @nottest
    def program_test(self, code, expected):
        tokens = imp_lex(code)
        result = imp_parse(tokens)
        self.assertNotEquals(None, result)
        triple = to_triple(result.value)
        (vcs, ints, arrays) = vc_gen(triple)
        number = len(vcs)

        (result1, _) = z3it("unbounded_integers", vcs, ints, arrays)
        (result2, _) = z3it("bit_vectors", vcs, ints, arrays)

        self.assertEquals(expected, str(result1))
        self.assertEquals(expected, str(result2))
        self.assertEquals(number, len(vcs))

    def test_tp(self):
        code = 'pre x > 100 end; while x < 1000 do inv 100 < x and x <= 1000 end; x := x + 1 end; pos x > 1000 end'
        self.program_test(code, "sat")

