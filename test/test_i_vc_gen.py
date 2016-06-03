import unittest

from nose.tools import nottest

from imp_parser import *
from imp_lexer import *

from i_util import *
from i_vc_gen import *

class TestVCGen(unittest.TestCase):
    maxDiff = None

    @nottest
    def program_test(self, code, expected):
        tokens = imp_lex(code)
        result = imp_parse(tokens)
        self.assertNotEquals(None, result)
        (pre, commands, pos)  = to_triple(result.value)
        number = len(commands)

        vcs = vc_gen((pre, commands, pos))
        self.assertEquals(expected, vcs)
        self.assertEquals(number, len(commands))

    def test_tp(self):
        code = 'pre x > 100 end; while x < 1000 do inv 100 < x and x <= 1000 end; x := x + 1 end; pos x > 1000 end'
        invariant = AndBexp(
            RelopBexp('<', IntAexp(100), VarAexp('x')),
            RelopBexp('<=', VarAexp('x'), IntAexp(1000))
        )
        condition = RelopBexp('<', VarAexp('x'), IntAexp(1000))
        x_plus_one = BinopAexp('+', VarAexp('x'), IntAexp(1))
        wp = AndBexp(
            RelopBexp('<', IntAexp(100), x_plus_one),
            RelopBexp('<=', x_plus_one, IntAexp(1000))
        )
        pre = RelopBexp('>', VarAexp('x'), IntAexp(100))
        pos = RelopBexp('>', VarAexp('x'), IntAexp(1000))

        vc1 = ImplBexp(
            pre, 
            invariant
        )
        vc2 = ImplBexp(
            AndBexp(invariant, condition),
            wp
        )
        vc3 = ImplBexp(
            AndBexp(invariant, NotBexp(condition)),
            pos
        )

        expected = [vc1, vc2, vc3]
        self.program_test(code, expected)

