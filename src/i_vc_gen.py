import copy
from imp_ast import *
from i_wp import *
from i_vc import *

def get_ints_declarations_on_pre(pre):
    if isinstance(pre, TrueBexp) or isinstance(pre, FalseBexp) or isinstance(pre, IntAexp):
        return []

    elif isinstance(pre, VarAexp):
        return [pre.name]

    elif isinstance(pre, BinopAexp) or isinstance(pre, RelopBexp) or isinstance(pre, AndBexp) or isinstance(pre, OrBexp):
        return get_ints_declarations_on_pre(pre.left) + get_ints_declarations_on_pre(pre.right)

    elif isinstance(pre, NotBexp):
        return get_ints_declarations_on_pre(pre.exp)

    else:
        raise Exception("get_ints_declarations_on_pre: unsupported " + str(pre))

def get_arrays_declarations(commands):
    arrays = {}

    for i in xrange(0, len(commands)):
        command = commands[i]
        if isinstance(command, ArrayDeclaration):
            arrays[command.name] = command.capacity

    return arrays

def vc_gen(triple):
    (pre, commands, pos) = triple
    ints = get_ints_declarations_on_pre(pre.condition)
    arrays = get_arrays_declarations(commands)

    pre_implies_wp = ImplBexp(
        pre.condition,
        wp(commands, pos.condition, arrays)
    )

    (vcs, ints) = vc(commands, pos.condition, set(ints), arrays)

    return ([pre_implies_wp] + vcs, ints, arrays)

