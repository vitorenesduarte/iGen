from imp_ast import *
from i_wp import *

def get_capacity(name, arrays):
    if name in arrays:
        return arrays[name]

    raise Exception("get_capacity: undeclared array " + str(name))

def get_arrays_declarations(commands):
    arrays = {}

    for i in xrange(0, len(commands)):
        command = commands[i]
        if isinstance(command, ArrayDeclaration):
            arrays[command.name] = command.capacity

    return arrays

def give_me_my_vcs(commands, Q):
    arrays = get_arrays_declarations(commands)
    (vcs, ints) = vc(commands, Q, arrays)
    return (vcs, ints, arrays)

def vc(commands, Q, arrays):
    return vc_(commands, Q, len(commands) - 1, set(), arrays)

def vc_(commands, Q, index, ints, arrays):
    if index < 0:
        vcs = {}
        vcs['safe'] = []
        vcs['commands'] = []
        return (vcs, ints)

    command = commands[index]

    if isinstance(command, ArrayDeclaration):
        vcs = {}

    elif isinstance(command, AssignStatement):
        ints.add(command.name)

        safe_exp = safe(command.aexp)
        vcs = {}
        vcs['safe'] = safe_exp

    elif isinstance(command, ArrayAssignStatement):
        safe_index = safe(ArrayAexp(command.name, command.index))
        safe_exp = safe(command.aexp)
        vcs = {}
        vcs['safe'] = safe_index + safe_exp
    
    elif isinstance(command, IfStatement):
        (vcs, ints) = vc_if(command, Q, ints, arrays)

    elif isinstance(command, WhileStatement):
        (vcs, ints) = vc_while(command, Q, ints, arrays)

    else:
        raise Exception("vc: unsupported " + str(command))

    Q_ = wp([command], Q)
    (more_vcs, ints) = vc_(commands, Q_, index - 1, ints, arrays)
    return (merge(vcs, more_vcs), ints)

def vc_if(command, Q, ints, arrays):
    condition = command.condition
    top = command.true_stmt
    bot = command.false_stmt

    (top_vc, top_ints) = vc(top, Q, arrays)
    (bot_vc, bot_ints) = vc(bot, Q, arrays)
    top_bot_vcs = merge(top_vc, bot_vc)

    safe_condition = safe(condition)
    vcs = {}
    vcs['safe'] = safe_condition

    ints.update([e for e in top_ints])
    ints.update([e for e in bot_ints])

    return (merge(top_bot_vcs, vcs),  ints)

def vc_while(command, Q, ints, arrays):
    condition = command.condition
    body = command.body
    invariant = command.invariant.condition

    fst_vc = ImplBexp(
        AndBexp(invariant, condition),
        wp(body, invariant)
    )
    snd_vc = ImplBexp(
        AndBexp(invariant, NotBexp(condition)),
        Q
    )

    safe_condition = safe(condition)
    vcs = {}
    vcs['commands'] = [fst_vc, snd_vc]
    vcs['safe'] = safe_condition

    (other_vcs, body_ints) = vc(body, invariant, arrays)
    ints.update([e for e in body_ints])

    return (merge(other_vcs, vcs), ints)

def safe(exp):
    return []
    
    raise Exception("safe: unsupported : " + str(exp))

def merge(dict_a, dict_b):
    result = {}
    keys = set(dict_a.keys() + dict_b.keys())

    for key in keys:
        v_a = []
        v_b = []
        if key in dict_a:
            v_a = dict_a[key]

        if key in dict_b:
            v_b = dict_b[key]

        result[key] = v_a + v_b

    return result

