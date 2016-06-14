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
    arrays_decls = {}

    for key in arrays:
        arrays_decls[key] = Array(key, IntSort(), IntSort())

    return arrays_decls

def get_index(index, int_decls):
    if isinstance(index, VarAexp):
        return index_decls[index.name]

    if isinstance(index, IntAexp):
        return index.i

    raise Exception("get_index: unsupported " + str(index))

def merge(vcs):
    # assuming at least one vc
    result = vcs[0]

    for i in xrange(1, len(vcs)):
        result = AndBexp(result, vcs[i])

    return result

def z3it(tactic, vcs, ints, arrays):
    solver = get_solver(tactic)
    solver.set(unsat_core = True)
    int_decls = declare_ints(tactic, ints)
    array_decls = declare_arrays(tactic, arrays)

    #unique_vc = merge(vcs)
    #unique_vc_z3 = z3fy(unique_vc, int_decls, array_decls)
    #solver.assert_and_track(Not(unique_vc_z3), "unique")

    for i in xrange(0, len(vcs)):
        vc = vcs[i]
        vc_assert = z3fy(vc, int_decls, array_decls)
        solver.assert_and_track(Not(vc_assert), "vc_" + str(i))

    result = solver.check()
    if str(result) == "sat":
        model_or_unsat_core = solver.model()
    else:
        model_or_unsat_core = solver.unsat_core()

    return (result, model_or_unsat_core)

def z3fy(vc, int_decls, array_decls):
    if isinstance(vc, TrueBexp):
        return True
    
    if isinstance(vc, FalseBexp):
        return False
    
    if isinstance(vc, IntAexp):
        return vc.i

    if isinstance(vc, VarAexp):
        return int_decls[vc.name]

    if isinstance(vc, ArrayAexp):
        z3index = z3fy(vc.index, int_decls, array_decls)
        return array_decls[vc.name][z3index]

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
