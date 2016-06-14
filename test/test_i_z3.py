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

        [
            (vc0, s_us_0, s_m_0),
            (vc1, s_us_1, s_m_1),
            (vc2, s_us_2, s_m_2)
        ] = z3it("unbounded_integers", vcs, ints, arrays)
        
        self.assertEquals(expected[0], str(s_us_0))
        self.assertEquals(expected[1], str(s_us_1))
        self.assertEquals(expected[2], str(s_us_2))

        [
            (vc0, s_us_0, s_m_0),
            (vc1, s_us_1, s_m_1),
            (vc2, s_us_2, s_m_2)
        ] = z3it("bit_vectors", vcs, ints, arrays)

        self.assertEquals(expected[0], str(s_us_0))
        self.assertEquals(expected[1], str(s_us_1))
        self.assertEquals(expected[2], str(s_us_2))

        self.assertEquals(number, len(vcs))

    def test_tp_v1(self):
        code = 'pre x > 100 end; while x < 1000 do inv 100 < x and x <= 1000 end; x := x + 1 end; pos x = 1000 end'

        expected = ["sat", "unsat", "unsat"]
        self.program_test(code, expected)

    def test_tp_v2(self):
        code = 'pre x >= 0 and x <= 1000 end; while x < 1000 do inv x >= 0 and x <= 1000 end; x := x + 1 end;pos x = 1000 end'

        expected = ["unsat", "unsat", "unsat"]
        self.program_test(code, expected)
