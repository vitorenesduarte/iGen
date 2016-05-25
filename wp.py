import sys

# Add imp-interpreter folder to sys.path
sys.path.append('imp-interpreter')

from imp_ast import *

def wp(commands, Q):
    if not commands:
        return Q
    command = commands.pop() # last command on list

    print str(command) + "\n\n"

    if isinstance(command, AssignStatement):
        Q = wp_assign(command, Q)
        return wp(commands, Q)
    
    if isinstance(command, IfStatement):
        Q = wp_if(command, Q)
        return wp(commands, Q)

    if isinstance(command, WhileStatement):
        Q = wp_while(command, Q)
        return wp(commands, Q)

    if isinstance(command, AssumeStatement):
        Q = wp_assume(command, Q)
        return wp(commands, Q)

    if isinstance(command, AssertStatement):
        Q = wp_assert(command, Q)
        return wp(commands, Q)

    raise Exception("unsupported command " + str(command))

def wp_assign(command, Q):
    variable = command.name
    value = command.aexp

def wp_if(command, Q):
    return command

def wp_while(command, Q):
    return command

def wp_assume(command, Q):
    return command

def wp_assert(command, Q):
    return command


