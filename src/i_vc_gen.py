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

    (vcs, ints, arrays) = give_me_my_vcs(commands, pos.condition)

    more_vcs = {}
    more_vcs['pre_implies_wp'] = [pre_implies_wp]

    all_vcs = merge(more_vcs, vcs)

    return (vcs_to_list(all_vcs), ints, arrays)

def vcs_to_list(vcs_map):
    result = []

    for key in vcs_map:
        vcs_list = vcs_map[key]

        for i in xrange(0, len(vcs_list)):
            vc = vcs_list[i]
            vc_name = key + "_" + str(i)
            result.append((vc, vc_name))

    return result
