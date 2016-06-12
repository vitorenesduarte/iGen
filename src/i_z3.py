from imp_ast import *
from z3 import *

UI = "unbounded_integers"
BV = "bit_vectors"
BV_BITS = 16

def get_solver(tactic):
    if tactic == UI:
        return Tactic("qfauflia").solver()

    if tactic == BV:
        return Tactic("qfaufbv").solver()

    else:
        raise Exception("get_solver: unsupported " + str(tactic))

def get_declaration(tactic, name):
    if tactic == UI:
        return Int(name)

    if tactic == BV:
        return BitVec(name, BV_BITS)

    raise Exception("get_declaration: unsupported " + str(tactic))

def declare_ints(tactic, ints):
    int_decls = {}

    for int_i in ints:
        int_decls[int_i] = get_declaration(tactic, int_i)

    return int_decls

def declare_arrays(tactic, arrays):
    return {}

def z3it(tactic, vcs, ints, arrays):
    solver = get_solver(tactic)
    solver.set(unsat_core = True)
    int_decls = declare_ints(tactic, ints)
    array_decls = declare_arrays(tactic, arrays)

    for i in xrange(0, len(vcs)):
        vc = vcs[i]
        vc_assert = z3fy(vc, int_decls, array_decls)
        solver.assert_and_track(vc_assert, "vc" + str(i))

    return (solver.check(), solver.unsat_core())

def z3fy(vc, int_decls, array_decls):
    if isinstance(vc, TrueBexp):
        return True
    
    if isinstance(vc, FalseBexp):
        return False
    
    if isinstance(vc, IntAexp):
        return vc.i

    if isinstance(vc, VarAexp):
        return int_decls[vc.name]

    if isinstance(vc, BinopAexp):
        left = z3fy(vc.left, int_decls, array_decls)
        right = z3fy(vc.right, int_decls, array_decls)

        if vc.op == "+":
            result = left + right
        elif vc.op == "-":
            result = left - right
        elif vc.op == "*":
            result = left * right
        elif vc.op == "/":
            result = left / right
        else:
            raise Exception("z3fy: unsupported operator " + str(vc.op))

        return result

    if isinstance(vc, RelopBexp):
        left = z3fy(vc.left, int_decls, array_decls)
        right = z3fy(vc.right, int_decls, array_decls)

        if vc.op == '<':
            result = left < right
        elif vc.op == '<=':
            result = left <= right
        elif vc.op == '>':
            result = left > right
        elif vc.op == '>=':
            result = left >= right
        elif vc.op == '=':
            result = left == right
        elif vc.op == '!=':
            result = left != right
        else:
            raise Exception("z3fy: unsupported operator " + str(vc.op))

        return result

    if isinstance(vc, AndBexp):
        left = z3fy(vc.left, int_decls, array_decls)
        right = z3fy(vc.right, int_decls, array_decls)
        return And(left, right)

    if isinstance(vc, OrBexp):
        left = z3fy(vc.left, int_decls, array_decls)
        right = z3fy(vc.right, int_decls, array_decls)
        return Or(left, right)

    if isinstance(vc, ImplBexp):
        left = z3fy(vc.left, int_decls, array_decls)
        right = z3fy(vc.right, int_decls, array_decls)
        return Implies(left, right)

    if isinstance(vc, NotBexp):
        exp = z3fy(vc.exp, int_decls, array_decls)
        return Not(exp)
    
    raise Exception("z3fy: unsupported " + str(vc))
