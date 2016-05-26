from imp_ast import *

def extract_while_invariant(loop):
    body = parse_parsed(loop.body)
    inv = InvStatement(TrueBexp())

    for i in xrange(0, len(body)):
        command = body[i]
        if isinstance(command, InvStatement):
            body.pop(i)
            return (body, command)

    return (body, inv)

def parse_parsed(command):
    return parse_parsed_r(command, [])

def parse_parsed_r(command, seq):
    if isinstance(command, CompoundStatement):
        fst = command.first
        snd = command.second

        sndParsed = parse_parsed(snd)
        
        return parse_parsed_r(fst, sndParsed + seq)

    elif isinstance(command, IfStatement):
        condition = command.condition
        top = command.true_stmt
        bot = command.false_stmt

        topParsed = parse_parsed(top)
        botParsed = parse_parsed(bot)
        newIf = IfStatement(condition, topParsed, botParsed)

        return [newIf] + seq

    elif isinstance(command, WhileStatement):
        condition = command.condition

        (body, invariant) = extract_while_invariant(command)
        newWhile = WhileStatement(condition, body, invariant)

        return [newWhile] + seq

    elif command == None:
        return seq

    else:
        return [command] + seq

def to_triple(program):
    program = parse_parsed(program)
    pre = PreStatement(TrueBexp())
    pos = PosStatement(TrueBexp())
    commands = []

    for i in xrange(0, len(program)):
        command = program[i]
        if isinstance(command, PreStatement):
            pre = command
        elif isinstance(command, PosStatement):
            pos = command
        else:
            commands.append(command)

    return (pre, commands, pos)
