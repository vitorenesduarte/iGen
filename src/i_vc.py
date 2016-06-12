from imp_ast import *
from i_wp import *

def vc(commands, Q):
    return vc_(commands, Q, len(commands) - 1, set(), set())

def vc_(commands, Q, index, ints, arrays):
    if index < 0:
        return ([], ints, arrays)

    command = commands[index]

    if isinstance(command, AssignStatement):
        vcs = []
        ints.add(command.name)
    
    elif isinstance(command, IfStatement):
        (vcs, ints, arrays) = vc_if(command, Q, ints, arrays)

    elif isinstance(command, WhileStatement):
        (vcs, ints, arrays) = vc_while(command, Q, ints, arrays)

    else:
        raise Exception("vc: unsupported " + str(command))

    Q_ = wp([command], Q)
    (other_vcs, ints, arrays) = vc_(commands, Q_, index - 1, ints, arrays)
    return (vcs + other_vcs, ints, arrays)

def vc_if(command, Q, ints, arrays):
    condition = command.condition
    top = command.true_stmt
    bot = command.false_stmt
    (topVC, top_ints, top_arrays) = vc(top, Q)
    (botVC, bot_ints, bot_arrays) = vc(bot, Q)

    ints.update([e for e in top_ints])
    ints.update([e for e in bot_ints])
    arrays.update([e for e in top_arrays])
    arrays.update([e for e in bot_arrays])

    return (topVC + botVC,  ints, arrays)

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
    (other_vcs, body_ints, body_arrays) = vc(body, invariant)

    ints.update([e for e in body_ints])
    arrays.update([e for e in body_arrays])

    return ([fst_vc, snd_vc] + other_vcs, ints, arrays)

