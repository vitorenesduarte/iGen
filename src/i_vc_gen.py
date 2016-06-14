import copy
from imp_ast import *
from i_wp import *
from i_vc import *

def get_arrays_declarations(commands):
    arrays = {}

    for i in xrange(0, len(commands)):
        command = commands[i]
        if isinstance(command, ArrayDeclaration):
            arrays[command.name] = command.capacity

    return arrays

def vc_gen(triple):
    (pre, commands, pos) = triple
    arrays = get_arrays_declarations(commands)

    pre_implies_wp = ImplBexp(
        pre.condition,
        wp(commands, pos.condition, arrays)
    )

    (vcs, ints) = vc(commands, pos.condition, arrays)

    return ([pre_implies_wp] + vcs, ints, arrays)

