import sys

# Add imp-interpreter folder to sys.path
sys.path.append('imp-interpreter')

# Import what's need from there
from imp_ast import *
from combinators import *

def parse_parsed(command):
    return parse_parsed_r(command, [])

def parse_parsed_r(command, seq):
    if isinstance(command, Result):
        return parse_parsed_r(command.value, seq)

    elif isinstance(command, CompoundStatement):
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
        body = command.body

        bodyParsed = parse_parsed(body)
        newWhile = WhileStatement(condition, bodyParsed)

        return [newWhile] + seq

    else:
        return [command] + seq
