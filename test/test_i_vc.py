import unittest

from nose.tools import nottest

from imp_parser import *
from imp_lexer import *

from i_util import *
from i_vc import *

class TestVC(unittest.TestCase):
    maxDiff = None

    @nottest
    def program_test(self, code, e_vcs, e_ints, e_arrays):
        tokens = imp_lex(code)
        result = imp_parse(tokens)
        self.assertNotEquals(None, result)
        (pre, commands, pos)  = to_triple(result.value)
        number = len(commands)

        arrays = {}
        result = vc(commands, pos.condition, set(), arrays)
        print result
        (vcs, ints) = result
        self.assertEquals(e_vcs, vcs)
        self.assertEquals(e_ints, ints)
        self.assertEquals(e_arrays, arrays)
        self.assertEquals(number, len(commands))

    def test_no_commands(self):
        code = 'pos x > 0 end'
        expected = []
        self.program_test(code, expected, set(), {})

    def test_assign(self):
        code = 'x := 1; pos x > 0 end'
        expected = []
        self.program_test(code, expected, set(['x']), {})

    def test_if(self):
        code = 'if x > 0 then x := 1 else x := 2 end; pos x > 0 end'
        expected = []
        self.program_test(code, expected, set(['x']), {})

    def test_while(self):
        code = 'pre x > 100 end; while x < 1000 do inv 100 < x and x <= 1000 end; x := x + 1 end; pos x = 1000 end'
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
        pos = RelopBexp('=', VarAexp('x'), IntAexp(1000))

        vc2 = ImplBexp(
            AndBexp(invariant, condition),
            wp
        )
        vc3 = ImplBexp(
            AndBexp(invariant, NotBexp(condition)),
            pos
        )

        expected = [vc2, vc3]
        self.program_test(code, expected, set(['x']), {})

