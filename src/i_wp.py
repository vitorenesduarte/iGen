from imp_ast import *

def wp(commands, Q):
    return wp_(commands, Q, len(commands) - 1)

def wp_(commands, Q, index):
    if index < 0:
        return Q

    command = commands[index]

    if isinstance(command, AssignStatement):
        Q = wp_assign(command, Q)
        return wp_(commands, Q, index - 1)

    if isinstance(command, ArrayAssignStatement):
        Q = wp_array_assign(command, Q)
        return wp_(commands, Q, index - 1)
    
    if isinstance(command, IfStatement):
        Q = wp_if(command, Q)
        return wp_(commands, Q, index - 1)

    if isinstance(command, WhileStatement):
        Q = wp_while(command, Q)
        return wp_(commands, Q, index - 1)

    if isinstance(command, AssumeStatement):
        Q = wp_assume(command, Q)
        return wp_(commands, Q, index - 1)

    if isinstance(command, AssertStatement):
        Q = wp_assert(command, Q)
        return wp_(commands, Q, index - 1)

    raise Exception("wp: unsupported " + str(command))

def wp_assign(command, Q):
    variable = command.name
    value = command.aexp
    return update_value(variable, value, Q)

def wp_array_assign(command, Q):
    return "ola"

def wp_if(command, Q):
    condition = command.condition
    top = command.true_stmt
    bot = command.false_stmt
    top_wp = wp(top, Q)
    bot_wp = wp(bot, Q)

    left_clause = ImplBexp(condition, top_wp)
    right_clause = ImplBexp(NotBexp(condition), bot_wp)
    return AndBexp(left_clause, right_clause)

def wp_while(command, Q):
    return command.invariant.condition

def wp_assume(command, Q):
    P = command.condition
    return ImplBexp(P, Q)

def wp_assert(command, Q):
    P = command.condition
    return AndBexp(P, Q)

def update_value(variable, value, Q):
    if isinstance(Q, TrueBexp) or isinstance(Q, FalseBexp):
        return Q

    if isinstance(Q, IntAexp):
        return Q

    if isinstance(Q, VarAexp):
        if Q.name == variable:
            return value
        else:
            return Q

    if isinstance(Q, BinopAexp):
        op = Q.op
        left = update_value(variable, value, Q.left)
        right = update_value(variable, value, Q.right)
        return BinopAexp(op, left, right)

    if isinstance(Q, RelopBexp):
        op = Q.op
        left = update_value(variable, value, Q.left)
        right = update_value(variable, value, Q.right)
        return RelopBexp(op, left, right)

    if isinstance(Q, AndBexp):
        left = update_value(variable, value, Q.left)
        right = update_value(variable, value, Q.right)
        return AndBexp(left, right)
    
    if isinstance(Q, OrBexp):
        left = update_value(variable, value, Q.left)
        right = update_value(variable, value, Q.right)
        return OrBexp(left, right)

    if isinstance(Q, ImplBexp):
        left = update_value(variable, value, Q.left)
        right = update_value(variable, value, Q.right)
        return ImplBexp(left, right)

    if isinstance(Q, NotBexp):
        exp = update_value(variable, value, Q.exp)
        return NotBexp(exp)

    raise Exception("update_value: unsupported " + str(Q))
