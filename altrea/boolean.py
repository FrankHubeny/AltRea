# boolean.py
"""This file contains classes for logical statements and functions on them.

It contains the following classes:
- `Wff` - A well formed formula with the base consisting of one propositional variable.
- `And` - A Wff with two arguments which are Wffs representing logical and.
- `Or` - A Wff with two arguments which are Wffs representing logical or.
- `Not` - A Wff with one argument which is a Wff representing logical not.
- `Implies` - A Wff with two arguments which are Wffs representing logical implies.
- `Iff` - A Wff with two arguments which are Wffs representing logical if and only if.
"""

class Wff:
    """The construction of a well formed formula consisting of one propositional variable.
    """

    is_variable = True
    value = True
    lb = '('
    rb = ')'
    
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f'{self.name}'
    
    def latex(self):
        return f'{self.name}'
    
    def eval(self, value: bool):
        self.value = value
    

class And(Wff):
    """A well formed formula with two arguments which are also well formed formulas connected
    by logical and.
    """

    is_variable = False

    def __init__(self, left: Wff, right: Wff):
        self.left = left
        self.right = right
        self.connector = '&'
        self.latexconnector = '\\wedge'

    def __str__(self):
        if self.left.is_variable and self.right.is_variable:
            return f'{self.left} {self.connector} {self.right}'
        elif self.left.is_variable:
            return f'{self.left} {self.connector} {self.lb}{self.right}{self.rb}'
        elif self.right.is_variable:
            return f'{self.lb}{self.left}{self.rb} {self.connector} {self.right}'
        else:
            return f'{self.lb}{self.left}{self.rb} {self.connector} {self.lb}{self.right}{self.rb}'
        
    def latex(self):
        if self.left.is_variable and self.right.is_variable:
            return f'{self.left.latex()} {self.latexconnector} {self.right.latex()}'
        elif self.left.is_variable:
            return f'{self.left.latex()} {self.latexconnector} {self.lb}{self.right.latex()}{self.rb}'
        elif self.right.is_variable:
            return f'{self.lb}{self.left.latex()}{self.rb} {self.latexconnector} {self.right.latex()}'
        else:
            return f'{self.lb}{self.left.latex()}{self.rb} {self.latexconnector} {self.lb}{self.right.latex()}{self.rb}'
        
    def eval(self):
        return self.left.value and self.right.value
    
class Or(Wff):
    """A well formed formula with two arguments which are also well formed formulas connected
    by logical or.
    """

    is_variable = False

    def __init__(self, left: Wff, right: Wff):
        self.left = left
        self.right = right
        self.connector = '|'
        self.latexconnector = '\\vee'

    def __str__(self):
        if self.left.is_variable and self.right.is_variable:
            return f'{self.left} {self.connector} {self.right}'
        elif self.left.is_variable:
            return f'{self.left} {self.connector} ({self.right})'
        elif self.right.is_variable:
            return f'({self.left}) {self.connector} {self.right}'
        else:
            return f'({self.left}) {self.connector} ({self.right})'
        
    def latex(self):
        if self.left.is_variable and self.right.is_variable:
            return f'{self.left.latex()} {self.latexconnector} {self.right.latex()}'
        elif self.left.is_variable:
            return f'{self.left.latex()} {self.latexconnector} ({self.right.latex()})'
        elif self.right.is_variable:
            return f'({self.left.latex()}) {self.latexconnector} {self.right.latex()}'
        else:
            return f'({self.left.latex()}) {self.latexconnector} ({self.right.latex()})'
        
    def eval(self):
        return self.left.value or self.right.value
    
class Not(Wff):
    """A well formed formula with one argument which is also a well formed formula joined
    with logical not.
    """

    is_variable = True

    def __init__(self, negated: Wff):
        self.negated = negated
        self.connector = '~'
        self.latexconnector = '\\lnot '

    def __str__(self):
        if self.negated.is_variable:
            return f'{self.connector}{self.negated}'
        else:
            return f'{self.connector}({self.negated})'
        
    def latex(self):
        if self.negated.is_variable:
            return f'{self.latexconnector}{self.negated.latex()}'
        else:
            return f'{self.latexconnector}({self.negated.latex()})'
    
    def eval(self):
        return not self.negated.value

    
class Implies(Wff):
    """A well formed formula with two arguments which are also well formed formulas joined
    by implies.  The antecedent is the first of the two arguments.  The consequent is the
    second.
    """

    is_variable = False

    def __init__(self, left: Wff, right: Wff):
        self.left = left
        self.right = right
        self.connector = '->'
        self.latexconnector = '\\to'
    
    def __str__(self):
        if self.left.is_variable and self.right.is_variable:
            return f'{self.left} {self.connector} {self.right}'
        elif self.left.is_variable:
            return f'{self.left} {self.connector} ({self.right})'
        elif self.right.is_variable:
            return f'({self.left}) {self.connector} {self.right}'
        else:
            return f'({self.left}) {self.connector} ({self.right})'
        
    def latex(self):
        if self.left.is_variable and self.right.is_variable:
            return f'{self.left.latex()} {self.latexconnector} {self.right.latex()}'
        elif self.left.is_variable:
            return f'{self.left.latex()} {self.latexconnector} ({self.right.latex()})'
        elif self.right.is_variable:
            return f'({self.left.latex()}) {self.latexconnector} {self.right.latex()}'
        else:
            return f'({self.left.latex()}) {self.latexconnector} ({self.right.latex()})'
        
    def eval(self):
        return (not self.left.value) or self.right.value

class Iff(Wff):
    """A well formed formula with two arguments which are also well formed formulas
    joined by if and only if.
    """

    is_variable = False

    def __init__(self, left: Wff, right: Wff):
        self.left = left
        self.right = right
        self.connector = '<->'
        self.latexconnector = '\\leftrightarrow'

    def __str__(self):
        if self.left.is_variable and self.right.is_variable:
            return f'{self.left} {self.connector} {self.right}'
        elif self.left.is_variable:
            return f'{self.left} {self.connector} ({self.right})'
        elif self.right.is_variable:
            return f'({self.left}) {self.connector} {self.right}'
        else:
            return f'({self.left}) {self.connector} ({self.right})'
        
    def latex(self):
        if self.left.is_variable and self.right.is_variable:
            return f'{self.left.latex()} {self.latexconnector} {self.right.latex()}'
        elif self.left.is_variable:
            return f'{self.left.latex()} {self.latexconnector} ({self.right.latex()})'
        elif self.right.is_variable:
            return f'({self.left.latex()}) {self.latexconnector} {self.right.latex()}'
        else:
            return f'({self.left.latex()}) {self.latexconnector} ({self.right.latex()})'
        
    def eval(self):
        return ((not self.left.value) or self.right.value) and ((not self.right.value) or self.left.value)
        
A = Wff('A')
B = Wff('B')
C = Wff('C')
D = Wff('D')
E = Wff('E')
F = Wff('F')
G = Wff('G')
H = Wff('H')
I = Wff('I')
J = Wff('J')
K = Wff('K')
L = Wff('L')
M = Wff('M')
N = Wff('N')
O = Wff('O')
P = Wff('P')
Q = Wff('Q')
R = Wff('R')
S = Wff('S')
T = Wff('T')
U = Wff('U')
V = Wff('V')
W = Wff('W')
X = Wff('X')
Y = Wff('Y')
Z = Wff('Z')
