from imp_ast import *
from i_wp import *

def vc(commands, Q):
    return vc_(commands, Q, len(commands) - 1)

def vc_(commands, Q, index):
    if index < 0:
        return []

    command = commands[index]

    if isinstance(command, AssignStatement):
        vcs = []
    
    elif isinstance(command, IfStatement):
        vcs = vc_if(command, Q)

    elif isinstance(command, WhileStatement):
        vcs = vc_while(command, Q)

    else:
        raise Exception("vc: unsupported " + str(command))

    Q_ = wp([command], Q)
    return vcs + vc_(commands, Q_, index - 1)


def vc_if(command, Q):
    condition = command.condition
    top = command.true_stmt
    bot = command.false_stmt
    topVC = vc(top, Q)
    botVC = vc(bot, Q)

    return topVC + botVC

def vc_while(command, Q):
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
    other_vcs = vc(body, invariant)

    return [fst_vc, snd_vc] + other_vcs

