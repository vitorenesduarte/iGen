import unittest

from nose.tools import nottest

from imp_parser import *
from imp_lexer import *

from i_util import *
from i_wp import *

class TestUpdateValue(unittest.TestCase):
    maxDiff = None

    @nottest
    def program_test(self, condition, variable, value, expected):
        condition = update_value(variable, value, condition)
        self.assertEquals(expected, condition)

    def test_true_and_false(self):
        condition_true = TrueBexp()
        condition_false = FalseBexp()
        self.program_test(condition_true, VarAexp('x'), IntAexp(3), condition_true)
        self.program_test(condition_false, VarAexp('x'), IntAexp(3), condition_false)

    def test_var(self):
        condition = VarAexp('x')
        expected_one = VarAexp('y')
        expected_two = BinopAexp('+', VarAexp('y'), IntAexp(1))
        self.program_test(condition, VarAexp('x'), expected_one, expected_one)
        self.program_test(condition, VarAexp('x'), expected_two, expected_two)
        
    def test_binop(self):
        condition = BinopAexp('+', VarAexp('y'), IntAexp(1))
        expected_one = condition
        expected_two = BinopAexp('+', IntAexp(3), IntAexp(1))
        self.program_test(condition, VarAexp('x'), IntAexp(1), expected_one)
        self.program_test(condition, VarAexp('y'), IntAexp(3), expected_two)

    def test_relop(self):
        condition = RelopBexp('<', VarAexp('y'), BinopAexp('+', VarAexp('x'), IntAexp(1)))
        expected_one = RelopBexp('<', VarAexp('z'), BinopAexp('+', VarAexp('x'), IntAexp(1)))
        expected_two = RelopBexp('<', VarAexp('y'), BinopAexp('+', IntAexp(17), IntAexp(1)))
        self.program_test(condition, VarAexp('y'), VarAexp('z'), expected_one)
        self.program_test(condition, VarAexp('x'), IntAexp(17), expected_two)

    def test_and(self):
        condition = AndBexp(TrueBexp(), RelopBexp('<', VarAexp('z'), VarAexp('z')))
        expected = AndBexp(TrueBexp(), RelopBexp('<', VarAexp('x'), VarAexp('x')))
        self.program_test(condition, VarAexp('z'), VarAexp('x'), expected)

    def test_or(self):
        condition = OrBexp(
            RelopBexp('>', 
                VarAexp('z'), 
                BinopAexp('+', VarAexp('z'), IntAexp(1))
            ), 
            FalseBexp()
        )
        expected = OrBexp(
            RelopBexp('>', 
                BinopAexp('+', VarAexp('z'), IntAexp(1)), 
                BinopAexp('+', 
                    BinopAexp('+', VarAexp('z'), IntAexp(1)), 
                    IntAexp(1)
                )
            ),
            FalseBexp()
        )
        self.program_test(condition, VarAexp('z'), BinopAexp('+', VarAexp('z'), IntAexp(1)), expected)

    def test_impl(self):
        condition = ImplBexp(
            RelopBexp('=', VarAexp('x'), VarAexp('y')),
            RelopBexp('=', VarAexp('y'), VarAexp('x'))
        )
        expected = ImplBexp(
            RelopBexp('=', IntAexp(1), VarAexp('y')),
            RelopBexp('=', VarAexp('y'), IntAexp(1))
        )
        self.program_test(condition, VarAexp('x'), IntAexp(1), expected)

    def test_not(self):
        condition = NotBexp(RelopBexp('=', VarAexp('z'), IntAexp(1)))
        expected_one = condition
        expected_two = NotBexp(RelopBexp('=', VarAexp('x'), IntAexp(1)))
        self.program_test(condition, VarAexp('y'), IntAexp(1), expected_one)
        self.program_test(condition, VarAexp('z'), VarAexp('x'), expected_two)

class TestWP(unittest.TestCase):
    maxDiff = None

    @nottest
    def program_test(self, code, expected):
        tokens = imp_lex(code)
        result = imp_parse(tokens)
        self.assertNotEquals(None, result)
        (pre, commands, pos)  = to_triple(result.value)
        number = len(commands)
        arrays = {}

        weakest = wp(commands, pos.condition, arrays)
        self.assertEquals(expected, weakest)
        self.assertEquals(number, len(commands))

    def test_no_commands(self):
        code = 'pos x > 0 end'
        expected = RelopBexp('>', VarAexp('x'), IntAexp(0))
        self.program_test(code, expected)

    def test_assign_with_true(self):
        code = 'x := 1'
        expected = TrueBexp()
        self.program_test(code, expected)

    def test_assign(self):
        code = 'x := 1; pos x > 0 end'
        expected = RelopBexp('>', IntAexp(1), IntAexp(0))
        self.program_test(code, expected)

    def test_seq(self):
        code = 'y := 1; y := 2; x := 1; pos y = x end'
        expected = RelopBexp('=', IntAexp(2), IntAexp(1))
        self.program_test(code, expected)

    def test_if(self):
        code = 'if x > 0 then x := 1 else x := 2 end; pos x > 0 end'
        expected = AndBexp(
            ImplBexp(
                RelopBexp('>', VarAexp('x'), IntAexp(0)),
                RelopBexp('>', IntAexp(1), IntAexp(0))
            ),
            ImplBexp(
                NotBexp(RelopBexp('>', VarAexp('x'), IntAexp(0))),
                RelopBexp('>', IntAexp(2), IntAexp(0))
            )
        )
        self.program_test(code, expected)

    def test_while(self):
        code = 'while x > 0 do inv x >= 0 end; x := x + 1 end; x := 2; y := x + 1; pos x > 0 and y > 0 end'
        expected = RelopBexp('>=', VarAexp('x'), IntAexp(0))
        self.program_test(code, expected)
