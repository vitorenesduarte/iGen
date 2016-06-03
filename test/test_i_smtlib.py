import unittest

from nose.tools import nottest

from imp_parser import *
from imp_lexer import *

from i_util import *
from i_vc_gen import *
from i_smtlib import *

class TestSMTLIB(unittest.TestCase):
    maxDiff = None

    @nottest
    def program_test(self, code, expected):
        tokens = imp_lex(code)
        result = imp_parse(tokens)
        self.assertNotEquals(None, result)
        triple = to_triple(result.value)
        vcs = vc_gen(triple)
        number = len(vcs)

        smtlib = to_smtlib(vcs)

        self.assertEquals(expected, smtlib)
        self.assertEquals(number, len(vcs))

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

        set_logic = '(set-logic QF_UFLIA)'
        produce_cores = '(set-option :produce-unsat-cores true)'
        declare_x = '(declare-const x Int)'
        vc1_smtlib = '(assert %s)' % vc1
        vc2_smtlib = '(assert %s)' % vc2
        vc3_smtlib = '(assert %s)' % vc3
        check_sat = '(check-sat)'

        expected = [
            set_logic,
            produce_cores,
            declare_x,
            vc1_smtlib,
            vc2_smtlib,
            vc3_smtlib,
            check_sat
        ]
        self.program_test(code, expected)

