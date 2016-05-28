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
        self.program_test(condition_true, 'x', IntAexp(3), condition_true)
        self.program_test(condition_false, 'x', IntAexp(3), condition_false)

    def test_var(self):
        condition = VarAexp('x')
        expected_one = VarAexp('y')
        expected_two = BinopAexp('+', VarAexp('y'), IntAexp(1))
        self.program_test(condition, 'x', expected_one, expected_one)
        self.program_test(condition, 'x', expected_two, expected_two)
        
    def test_binop(self):
        condition = BinopAexp('+', VarAexp('y'), IntAexp(1))
        expected_one = condition
        expected_two = BinopAexp('+', IntAexp(3), IntAexp(1))
        self.program_test(condition, 'x', IntAexp(1), expected_one)
        self.program_test(condition, 'y', IntAexp(3), expected_two)

    def test_relop(self):
        condition = RelopBexp('<', VarAexp('y'), BinopAexp('+', VarAexp('x'), IntAexp(1)))
        expected_one = RelopBexp('<', VarAexp('z'), BinopAexp('+', VarAexp('x'), IntAexp(1)))
        expected_two = RelopBexp('<', VarAexp('y'), BinopAexp('+', IntAexp(17), IntAexp(1)))
        self.program_test(condition, 'y', VarAexp('z'), expected_one)
        self.program_test(condition, 'x', IntAexp(17), expected_two)

    def test_and(self):
        condition = AndBexp(TrueBexp(), RelopBexp('<', VarAexp('z'), VarAexp('z')))
        expected = AndBexp(TrueBexp(), RelopBexp('<', VarAexp('x'), VarAexp('x')))
        self.program_test(condition, 'z', VarAexp('x'), expected)

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
        self.program_test(condition, 'z', BinopAexp('+', VarAexp('z'), IntAexp(1)), expected)

    def test_impl(self):
        condition = ImplBexp(
            RelopBexp('=', VarAexp('x'), VarAexp('y')),
            RelopBexp('=', VarAexp('y'), VarAexp('x'))
        )
        expected = ImplBexp(
            RelopBexp('=', IntAexp(1), VarAexp('y')),
            RelopBexp('=', VarAexp('y'), IntAexp(1))
        )
        self.program_test(condition, 'x', IntAexp(1), expected)

    def test_not(self):
        condition = NotBexp(RelopBexp('=', VarAexp('z'), IntAexp(1)))
        expected_one = condition
        expected_two = NotBexp(RelopBexp('=', VarAexp('x'), IntAexp(1)))
        self.program_test(condition, 'y', IntAexp(1), expected_one)
        self.program_test(condition, 'z', VarAexp('x'), expected_two)

