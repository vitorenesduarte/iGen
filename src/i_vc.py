from imp_ast import *
from i_wp import *

def get_capacity(name, arrays):
    if name in arrays:
        return arrays[name]

    raise Exception("get_capacity: undeclared array " + str(name))

def vc(commands, Q, ints, arrays):
    return vc_(commands, Q, len(commands) - 1, ints, arrays)

def vc_(commands, Q, index, ints, arrays):
    if index < 0:
        return ([], ints)

    command = commands[index]

    if isinstance(command, ArrayDeclaration) or isinstance(command, ArrayAssignStatement):
        vcs = []

    elif isinstance(command, AssignStatement):
        ints.add(command.name)
        vcs = []

    elif isinstance(command, IfStatement):
        (vcs, ints) = vc_if(command, Q, ints, arrays)

    elif isinstance(command, WhileStatement):
        (vcs, ints) = vc_while(command, Q, ints, arrays)

    else:
        raise Exception("vc: unsupported " + str(command))

    Q_ = wp([command], Q, arrays)
    (more_vcs, ints) = vc_(commands, Q_, index - 1, ints, arrays)
    return (more_vcs + vcs, ints)

def vc_if(command, Q, ints, arrays):
    condition = command.condition
    top = command.true_stmt
    bot = command.false_stmt

    (top_vc, top_ints) = vc(top, Q, ints, arrays)
    (bot_vc, bot_ints) = vc(bot, Q, ints, arrays)

    ints.update([e for e in top_ints])
    ints.update([e for e in bot_ints])

    return (top_vc + bot_vc, ints)

def vc_while(command, Q, ints, arrays):
    condition = command.condition
    body = command.body
    invariant = command.invariant.condition

    safe_condition = safe(condition, arrays)
    safe_vc = ImplBexp(
        invariant,
        safe_condition
    )
    fst_vc = ImplBexp(
        AndBexp(invariant, condition),
        wp(body, invariant, arrays)
    )
    snd_vc = ImplBexp(
        AndBexp(invariant, NotBexp(condition)),
        Q
    )

    while_vcs = []
    if safe_condition != TrueBexp():
        while_vcs.append(safe_vc)

    while_vcs.append(fst_vc)
    while_vcs.append(snd_vc)

    (other_vcs, body_ints) = vc(body, invariant, ints, arrays)
    ints.update([e for e in body_ints])

    return (while_vcs + other_vcs, ints)
