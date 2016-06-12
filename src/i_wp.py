from imp_ast import *

def wp(commands, Q, arrays):
    return wp_(commands, Q, len(commands) - 1, arrays)

def wp_(commands, Q, index, arrays):
    if index < 0:
        return Q

    command = commands[index]

    if isinstance(command, ArrayDeclaration):
        return wp_(command, Q, index - 1, arrays)

    if isinstance(command, AssignStatement):
        Q = wp_assign(command, Q, arrays)
        return wp_(commands, Q, index - 1, arrays)

    if isinstance(command, ArrayAssignStatement):
        Q = wp_array_assign(command, Q, arrays)
        return wp_(commands, Q, index - 1, arrays)

    if isinstance(command, IfStatement):
        Q = wp_if(command, Q, arrays)
        return wp_(commands, Q, index - 1, arrays)

    if isinstance(command, WhileStatement):
        Q = wp_while(command, Q, arrays)
        return wp_(commands, Q, index - 1, arrays)

    raise Exception("wp: unsupported " + str(command))

def wp_assign(command, Q, arrays):
    name = command.name
    exp = command.aexp
    replaced = update_value(VarAexp(name), exp, Q)

    safe_exp = safe(command.aexp, arrays)

    return simplify([replaced, safe_exp])

def wp_array_assign(command, Q, arrays):
    name = command.name
    index = command.index
    exp = command.aexp
    replaced = update_value(ArrayAexp(name, index), exp, Q)

    safe_index = safe(ArrayAexp(name, index), arrays)
    safe_exp = safe(exp, arrays)

    return simplify([replaced, safe_index, safe_exp])

def wp_if(command, Q, arrays):
    condition = command.condition
    top = command.true_stmt
    bot = command.false_stmt
    top_wp = wp(top, Q, arrays)
    bot_wp = wp(bot, Q, arrays)

    left_clause = ImplBexp(condition, top_wp)
    right_clause = ImplBexp(NotBexp(condition), bot_wp)
    both = AndBexp(left_clause, right_clause)

    safe_condition = safe(condition, arrays)

    return simplify([both, safe_condition])

def wp_while(command, Q, arrays):
    inv = command.invariant.condition
    return inv

def update_value(variable, value, Q):
    if isinstance(Q, TrueBexp) or isinstance(Q, FalseBexp):
        return Q

    if isinstance(Q, IntAexp):
        return Q

    if isinstance(Q, VarAexp):
        if isinstance(variable, VarAexp) and Q.name == variable.name:
            return value
        else:
            return Q

    if isinstance(Q, ArrayAexp):
        if isinstance(variable, VarAexp):
            name = Q.name
            index = update_value(variable, value, Q.index)
            return ArrayAexp(name, index)

        elif isinstance(variable, ArrayAexp) and Q.index == variable.index:
            return ArrayAexp(Q.name, value)

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

def safe(exp, arrays):
    if isinstance(exp, IntAexp) or isinstance(exp, VarAexp):
        return TrueBexp()

    elif isinstance(exp, ArrayAexp):
        safe_index = AndBexp(
            RelopBexp('>=', exp.index, IntAexp(0)),
            RelopBexp('<', exp.index, IntAexp(arrays[exp.name]))
        )
        return safe_index

    elif isinstance(exp, BinopAexp):
        left = safe(exp.left, arrays)
        right = safe(exp.right, arrays)
        by_zero = TrueBexp()

        if exp.op == "/":
            by_zero = RelopBexp('!=', exp.right, IntAexp(0))

        return simplify([left, right, by_zero])

    elif isinstance(exp, RelopBexp) or isinstance(exp, AndBexp) or isinstance(exp, OrBexp):
        left = safe(exp.left, arrays)
        right = safe(exp.right, arrays)
        
        return simplify([left, right])

    elif isinstance(exp, NotBexp):
        not_exp = safe(exp.exp, arrays)
        return not_exp
    
    else:
        raise Exception("safe: unsupported : " + str(exp))

def simplify(l):
    l_no_true = []
    for i in xrange(len(l)):
        if l[i] != TrueBexp():
            l_no_true.append(l[i])

    if len(l_no_true) == 0:
        return TrueBexp()
    else:
        result = l_no_true[0]
        for i in xrange(1, len(l_no_true)):
            result = AndBexp(result, l[i])

        return result
