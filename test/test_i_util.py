import unittest
import os, sys

from imp_parser import *
from imp_lexer import *

from i_util import *

class TestParseParsed(unittest.TestCase):
    def program_test(self, code, expected):
        tokens = imp_lex(code)
        result = imp_parse(tokens)
        self.assertNotEquals(None, result)
        parsed = parse_parsed(result.value)
        self.assertEquals(expected, parsed)

    def test_assign(self):
        code = 'x := 1'
        expected = [
            AssignStatement('x', IntAexp(1))
        ]
        self.program_test(code, expected)

    def test_compound(self):
        code = 'x := 1; y := 2'
        expected = [
            AssignStatement('x', IntAexp(1)),
            AssignStatement('y', IntAexp(2))
        ]
        self.program_test(code, expected)

    def test_if(self):
        code = 'if 1 < 2 then x := 1 else x := 2; y := 10 end'
        expected = [
            IfStatement(
                RelopBexp('<', IntAexp(1), IntAexp(2)),
                [AssignStatement('x', IntAexp(1))],
                [
                    AssignStatement('x', IntAexp(2)),
                    AssignStatement('y', IntAexp(10))
                ]
            )
        ]
        self.program_test(code, expected)

    def test_while(self):
        code = 'x := 10; y := 0; while x > 0 do y := y + 1; x := 20 end'
        expected = [
            AssignStatement('x', IntAexp(10)),
            AssignStatement('y', IntAexp(0)),
            WhileStatement(
                RelopBexp('>', VarAexp('x'), IntAexp(0)),
                [
                    AssignStatement('y', BinopAexp('+', VarAexp('y'), IntAexp(1))),
                    AssignStatement('x', IntAexp(20))
                ],
                InvStatement(TrueBexp())
            )
        ]
        self.program_test(code, expected)
