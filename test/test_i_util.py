import unittest

from imp_parser import *
from imp_lexer import *

from i_util import *

class TestExtractWhileInvariant(unittest.TestCase):
    maxDiff = None

    def program_test(self, loop, expected):
        tokens = imp_lex(loop)
        result = imp_parse(tokens)
        self.assertNotEquals(None, result)
        (body, invariant) = extract_while_invariant(result.value)
        self.assertEquals(expected, invariant.condition)

    def test_extract_true(self):
        code = 'while x > 0 do x := 1 end'
        expected = TrueBexp()
        self.program_test(code, expected)

    def test_extract_simple(self):
        code = 'while x <= y do inv x = y + 1 end; x := 1 end'
        expected = RelopBexp('=', VarAexp('x'), BinopAexp('+', VarAexp('y'), IntAexp(1)))
        self.program_test(code, expected)

    def test_extract_not_so_simple(self):
        code = 'while x = y do inv x = y or x != y end; x := 1 end'
        expected = OrBexp(
            RelopBexp('=', VarAexp('x'), VarAexp('y')),
            RelopBexp('!=', VarAexp('x'), VarAexp('y'))
        )
        self.program_test(code, expected)

class TestParseParsed(unittest.TestCase):
    maxDiff = None

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

    def test_if_inside_if(self):
        code = 'if x + 1 < 3 then x := 3 else if 3 >= x + 1 then x := 4 else x := 5 end end'
        expected = [
            IfStatement(
                RelopBexp('<', BinopAexp('+', VarAexp('x'), IntAexp(1)), IntAexp(3)),
                [AssignStatement('x', IntAexp(3))],
                [IfStatement(
                    RelopBexp('>=', IntAexp(3), BinopAexp('+', VarAexp('x'), IntAexp(1))),
                    [AssignStatement('x', IntAexp(4))],
                    [AssignStatement('x', IntAexp(5))]
                )]
            )
        ]
        self.program_test(code, expected)

    def test_while(self):
        code = 'x := 10; y := 0; while x > 0 do y := y + 1; x := 20 end; i := i + 1'
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
            ),
            AssignStatement('i', BinopAexp('+', VarAexp('i'), IntAexp(1)))
        ]
        self.program_test(code, expected)

    def test_while_with_invariant(self):
        code = 'while 0 < x do inv x <= 0 and i > 2 and i > 3 end end'
        expected = [
            WhileStatement(
                RelopBexp('<', IntAexp(0), VarAexp('x')),
                [],
                InvStatement(
                    AndBexp(
                        AndBexp(
                            RelopBexp('<=', VarAexp('x'), IntAexp(0)),
                            RelopBexp('>', VarAexp('i'), IntAexp(2))
                        ),
                        RelopBexp('>', VarAexp('i'), IntAexp(3))
                    )
                )
            )
        ]
        self.program_test(code, expected)

