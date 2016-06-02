import sys
import subprocess

# Add imp-interpreter and src folder to sys.path
sys.path.append('imp-interpreter')
sys.path.append('src')

from imp_parser import *
from imp_lexer import *

from i_util import *
from i_vc_gen import *
from i_smtlib import *

def usage():
    sys.stderr.write('Usage: iGen filename\n')
    sys.exit(1)

def write_to_file(smtlib_list):
    with open('.smtlib', 'w') as smt_file:
        for i in xrange(0, len(smtlib_list)):
            smt_file.write(smtlib_list[i] + "\n")

def execute():
    command = "z3 .smtlib"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0].rstrip()
    return output

def pretty(vcs):
    pretty_vcs = []

    for i in xrange(len(vcs)):
        pretty_vcs.append(vcs[i].pretty())

    return pretty_vcs

def run_vc_gen(text):
    tokens = imp_lex(text)
    parse_result = imp_parse(tokens)
    if not parse_result:
        return "Parse error"

    parse_result = parse_result.value
    triple = to_triple(parse_result)
    vcs = vc_gen(triple)
    smtlib = to_smtlib(vcs)
    write_to_file(smtlib)
    return (pretty(vcs), execute())
