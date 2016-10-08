"""Converts an infix expression to postfix and evaluates it

Stack: list that follows the LIFO principle
    __init__: initializes the stack
    __str__: displays the stack
    isEmpty: determines if the stack is empty
    push: adds an element to the stack
    peek: looks at the element on top of the stack (without removal)
    pop: removes/returns the element from the top of the stack
    size: determines the number of elements in the stack

Calculator: houses the infix to postfix conversion and evaluation
    in_to_post: converts an infix expression to postfix
    evaluate: evaluates the postfix expression
    claculate: wrapper for in_to_post and evaluate
"""

import math


class Stack:
    """list that follows the LIFO principle; for use in Calculator methods"""

    def __init__(self):
        """initializes the stack"""
        self.elements = []

    def __str__(self):
        """displays the stack"""
        return str(self.elements)

    def isEmpty(self):
        """determines if a stack is empty"""
        if self.elements == []:
            return True
        else:
            return False

    def push(self, element):
        """adds an element to the stack"""
        self.elements.append(element)

    def peek(self):
        """looks at the element on top of the stack (without removing it)"""
        return self.elements[-1]

    def pop(self):
        """removes the element from the top of the stack"""
        return self.elements.pop()

    def size(self):
        """determines the number of elements in the stack"""
        return len(self.elements)


class Calculator:
    """houses the infix to postfix conversion and evaluation"""

    # dictionary for the operators
    operators = {
        '+': (1, 1),
        '-': (2, 1),
        '*': (3, 1),
        '/': (4, 1),
        '^': (5, 1),
        '!': (6, 1)
    }
    # dictionary for the parentheses
    parens = {
        '(': (7, 1),
        ')': (8, 1)
    }
    # precedence table (incoming token->first column, onstack token->first row)
    precedence = [
        [' ',     '+',     '-',     '*',     '/',     '^',     '!',     '('     ')'],
        ['+',   False,   False,   False,   False,   False,   False,    True,   True],
        ['-',   False,   False,   False,   False,   False,   False,    True,   True],
        ['*',    True,    True,   False,   False,   False,   False,    True,   True],
        ['/',    True,    True,   False,   False,   False,   False,    True,   True],
        ['^',    True,    True,    True,    True,   False,   False,    True,   True],
        ['!',    True,    True,    True,    True,    True,   False,    True,   True],
        ['(',    True,    True,    True,    True,    True,    True,    True,   True],
        [')',    False,  False,   False,   False,   False,   False,    True,   True],
    ]
    # list of number characters
    num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']

    @classmethod
    def in_to_post(cls, e):
        """converts infix expression to postfix expression (while tokenizing the
        elements) using the Shunting Yard Algorithm"""
        ops = Stack()
        out = []
        neg = Stack()
        store = []
        e = e.replace(' ', '')

        for i in range(len(e)):
            if e[i] in cls.num:
                if i != (len(e) - 1) and e[i + 1] in cls.num:
                    store.append(e[i])
                elif store != []:
                    store.append(e[i])
                    s = ''.join(store)
                    store = []
                    if neg.isEmpty() is False:
                        neg.pop()
                        t = (-float(s), 0)
                    else:
                        t = (float(s), 0)
                    out.append(t)
                else:
                    if not neg.isEmpty():
                        neg.pop()
                        t = (-float(e[i]), 0)
                        out.append(t)
                    else:
                        out.append((float(e[i]), 0))
            elif e[i] in cls.operators:
                x = cls.operators[e[i]]
                if i + 2 < len(e):
                    if e[i + 1] in cls.operators:
                        return 'Error: Consecutive Operators'
                if x == (2, 1):
                    if i == 0:
                        neg.push(e[i])
                    elif e[i - 1] in cls.num:
                        if ops.isEmpty:
                            ops.push(x)
                        else:
                            for i in range(ops.size()):
                                if not cls.precedence[int(x[0])][int(ops.peek()[0])]:
                                    z = ops.pop()
                                    out.append(z)
                            ops.push(x)
                    elif e[i - 1] in cls.parens and cls.parens[e[i - 1]] == (8, 1):
                        if ops.isEmpty:
                            ops.push(x)
                        else:
                            for i in range(ops.size()):
                                if not cls.precedence[int(x[0])][int(ops.peek()[0])]:
                                    z = ops.pop()
                                    out.append(z)
                            ops.push(x)
                    else:
                        neg.push(e[i])
                else:
                    if ops.isEmpty:
                        ops.push(x)
                    else:
                        for i in range(ops.size()):
                            if not cls.precedence[int(x[0])][int(ops.peek()[0])]:
                                z = ops.pop()
                                out.append(z)
                        ops.push(x)
            elif e[i] in cls.parens:
                q = cls.parens[e[i]]
                if q == (7, 1):
                    ops.push(q)
                elif q == (8, 1):
                    if ops.isEmpty:
                        return 'Error: Mismatched Parentheses'
                    else:
                        while ops.peek() != (7, 1):
                            w = ops.pop()
                            out.append(w)
                            if ops.isEmpty:
                                return 'Error: Mismatched Parentheses'
                        if ops.peek() == (7, 1):
                            ops.pop()
        while not ops.isEmpty():
            u = ops.pop()
            out.append(u)
        return out

    @classmethod
    def evaluate(cls, out):
        """evaulates postfix expression"""
        if out == 'Error: Consecutive Operators' or out == 'Error: Mismatched Parentheses':
            return out
        numbers = Stack()
        for i in out:
            if i[1] == 0:
                numbers.push((i)[0])
            else:
                if i == (7, 1):
                    return 'Error: Mismatched Parentheses'
                if i == (1, 1):
                    value = numbers.pop() + numbers.pop()
                    numbers.push(value)
                elif i == (2, 1):
                    value = -numbers.pop() + numbers.pop()
                    numbers.push(value)
                elif i == (3, 1):
                    value = numbers.pop() * numbers.pop()
                    numbers.push(value)
                elif i == (4, 1):
                    x = numbers.pop()
                    y = numbers.pop()
                    value = y / x
                    numbers.push(value)
                elif i == (5, 1):
                    x = numbers.pop()
                    y = numbers.pop()
                    value = y ** x
                    numbers.push(value)
                elif i == (6, 1):
                    value = math.factorial(numbers.pop())
                    numbers.push(value)
        if numbers.size() > 1:
            return 'Input Error'
        else:
            return numbers.pop()

    @classmethod
    def calculate(cls, e):
        """wrapper for in_to_post() and evaluate()"""
        return cls.evaluate(cls.in_to_post(e))
