import copy
from imp_ast import *
from i_wp import *
from i_vc import *

def vc_gen(triple):
    (pre, commands, pos) = triple

    pre_implies_wp = ImplBexp(
        pre.condition,
        wp(commands, pos.condition)
    )

    

    vcs = vc(commands, pos.condition)

    return [pre_implies_wp] + vcs
