import sys
import subprocess

# Add imp-interpreter and src folder to sys.path
sys.path.append('imp-interpreter')
sys.path.append('src')

from imp_parser import *
from imp_lexer import *

from i_util import *
from i_vc_gen import *
from i_z3 import *

def usage():
    sys.stderr.write('Usage: iGen filename\n')
    sys.exit(1)

def pretty(vcs):
    pretty_vcs = []

    for i in xrange(len(vcs)):
        (vc, vc_name) = vcs[i]
        pretty_vcs.append(vc.pretty())

    return pretty_vcs

def run_vc_gen(text):
    tokens = imp_lex(text)
    parse_result = imp_parse(tokens)
    if not parse_result:
        return "Parse error"

    parse_result = parse_result.value
    triple = to_triple(parse_result)
    (vcs, ints, arrays) = vc_gen(triple)
    result = z3it("unbounded_integers", vcs, ints, arrays)
    (sat_or_unsat, unsat_core) = result
    return (pretty(vcs), sat_or_unsat, unsat_core)
