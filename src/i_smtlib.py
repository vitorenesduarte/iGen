from imp_ast import *

def to_smtlib(vcs):
    smtlib = []
    declarations = set()
    asserts = []

    for i in xrange(0, len(vcs)):
        vc = vcs[i]
        asserts.append(to_assert(vc))
        vc_declarations = extract_declarations(vc)
        for vc_declaration in vc_declarations:
            declarations.add(vc_declaration)

    smtlib.append(get_set_logic())
    smtlib.append(produce_unsat_cores())
    for declaration in declarations:
        smtlib.append(get_declaration(declaration))

    for assertion in asserts:
        smtlib.append(assertion)

    smtlib.append(check_sat())

    return smtlib

def get_set_logic():
    return "(set-logic QF_UFLIA)"

def produce_unsat_cores():
    return "(set-option :produce-unsat-cores true)"

def get_declaration(variable):
    return "(declare-fun %s () Int)" % variable

def to_assert(vc):
    return "(assert %s)" % vc

def check_sat():
    return "(check-sat)"

def extract_declarations(vc):
    if isinstance(vc, TrueBexp) or isinstance(vc, FalseBexp) or isinstance(vc, IntAexp):
        return []

    if isinstance(vc, VarAexp):
        return [vc.name]

    if isinstance(vc, BinopAexp) or isinstance(vc, RelopBexp) or isinstance(vc, AndBexp) or isinstance(vc, ImplBexp):
        left = extract_declarations(vc.left)
        right = extract_declarations(vc.right)
        return left + right

    if isinstance(vc, NotBexp):
        return extract_declarations(vc.exp)
