# Copyright (c) 2011, Jay Conrod.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Jay Conrod nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL JAY CONROD BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from equality import *

class Statement(Equality):
    pass

class Aexp(Equality):
    pass

class Bexp(Equality):
    pass

class TrueBexp(Bexp):
    def __repr__(self):
        return 'true'

    def pretty(self):
        return 'true'

class FalseBexp(Bexp):
    def __repr__(self):
        return 'false'

    def pretty(self):
        return 'false'

class IntAexp(Aexp):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return '%d' % self.i

    def pretty(self):
        return '%d' % self.i

    def eval(self, env):
        return self.i

class VarAexp(Aexp):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '%s' % self.name

    def pretty(self):
        return '%s' % self.name

    def eval(self, env):
        if self.name in env:
            return env[self.name]
        else:
            return 0

class ArrayAexp(Aexp):
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __repr__(self):
        return '%s[%s]' % (self.name, self.index)

class BinopAexp(Aexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return '(%s %s %s)' % (self.op, self.left, self.right)

    def pretty(self):
        return '(%s %s %s)' % (self.left.pretty(), self.op, self.right.pretty())

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '+':
            value = left_value + right_value
        elif self.op == '-':
            value = left_value - right_value
        elif self.op == '*':
            value = left_value * right_value
        elif self.op == '/':
            value = left_value / right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value

class RelopBexp(Bexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return '(%s %s %s)' % (self.op, self.left, self.right)

    def pretty(self):
        return '(%s %s %s)' % (self.left.pretty(), self.op, self.right.pretty())

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '<':
            value = left_value < right_value
        elif self.op == '<=':
            value = left_value <= right_value
        elif self.op == '>':
            value = left_value > right_value
        elif self.op == '>=':
            value = left_value >= right_value
        elif self.op == '=':
            value = left_value == right_value
        elif self.op == '!=':
            value = left_value != right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value

class AndBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '(and %s %s)' % (self.left, self.right)

    def pretty(self):
        return '(%s and %s)' % (self.left.pretty(), self.right.pretty())

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value and right_value

class OrBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '(or %s %s)' % (self.left, self.right)

    def pretty(self):
        return '(%s or %s)' % (self.left.pretty(), self.right.pretty())

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value or right_value

class ImplBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '(=> %s %s)' % (self.left, self.right)
    
    def pretty(self):
        return '(%s => %s)' % (self.left.pretty(), self.right.pretty())

class NotBexp(Bexp):
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return '(not %s)' % self.exp

    def pretty(self):
        return '(not %s)' % self.exp.pretty()

    def eval(self, env):
        value = self.exp.eval(env)
        return not value

class AssignStatement(Statement):
    def __init__(self, name, aexp):
        self.name = name
        self.aexp = aexp

    def __repr__(self):
        return '(:= %s %s)' % (self.name, self.aexp)

    def eval(self, env):
        value = self.aexp.eval(env)
        env[self.name] = value

class ArrayAssignStatement(Statement):
    def __init__(self, name, index, aexp):
        self.name = name
        self.index = index
        self.aexp = aexp

    def __repr__(self):
        return '(:= %s[%s] %s)' % (self.name, self.index, self.aexp)


class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return '(seq %s %s)' % (self.first, self.second)

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)

class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def __repr__(self):
        return '(%s? %s %s)' % (self.condition, self.true_stmt, self.false_stmt)

    def eval(self, env):
        condition_value = self.condition.eval(env)
        if condition_value:
            self.true_stmt.eval(env)
        else:
            if self.false_stmt:
                self.false_stmt.eval(env)

class WhileStatement(Statement):
    def __init__(self, condition, body, invariant=TrueBexp()):
        self.condition = condition
        self.body = body
        self.invariant = invariant

    def __repr__(self):
        return '(%s?* %s %s)' % (self.condition, self.body, self.invariant)

    def eval(self, env):
        condition_value = self.condition.eval(env)
        while condition_value:
            self.body.eval(env)
            condition_value = self.condition.eval(env)

class VCStatement(Statement):
    def __init__(self, condition):
        self.condition = condition

    def eval(self, env):
        return

class PreStatement(VCStatement):
    def __repr__(self):
        return '(pre %s)' % (self.condition)

class PosStatement(VCStatement):
    def __repr__(self):
        return '(pos %s)' % (self.condition)

class InvStatement(VCStatement):
    def __repr__(self):
        return '(inv %s)' % (self.condition)

class AssumeStatement(VCStatement):
    def __repr__(self):
        return '(assume %s)' % (self.condition)

class AssertStatement(VCStatement):
    def __repr__(self):
        return '(assert %s)' % (self.condition)

class ArrayDeclaration:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

    def __repr__(self):
        return 'new %s[%s]' % (self.name, self.capacity)
