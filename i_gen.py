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

def to_valid_or_unknown(sat_or_unsat):
    if sat_or_unsat == "unsat":
        return "valid"
    else:
        return "unknown"

def pretty(result):
    result_str = []

    for i in xrange(len(result)):
        (vc, sat_or_unsat, model_or_unsat_core) = result[i]
        vc_str = (vc.pretty(), to_valid_or_unknown(str(sat_or_unsat)), str(model_or_unsat_core))
        result_str.append(vc_str)

    return result_str

def run_vc_gen(text, theory):
    tokens = imp_lex(text)
    parse_result = imp_parse(tokens)
    if not parse_result:
        return "Parse error"

    parse_result = parse_result.value
    triple = to_triple(parse_result)
    (vcs, ints, arrays) = vc_gen(triple)
    result = z3it(theory, vcs, ints, arrays)
    return pretty(result)
