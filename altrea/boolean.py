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
    lb = '('
    rb = ')'
    
    def __init__(self, name: str):
        self.name = name
        self.booleanvalue = None

    def __str__(self):
        return f'{self.name}'
    
    def latex(self):
        return f'{self.name}'
    
    def setvalue(self, value: bool):
        self.booleanvalue = value

    def equals(self, otherwff):
        return str(self) == str(otherwff)
    
    def getvalue(self):
        return self.booleanvalue   

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
        self.booleanvalue = left.booleanvalue and right.booleanvalue

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
        
    def getvalue(self):
        return self.left.getvalue() and self.right.getvalue()

class F(Wff):
    """This well formed formula is the result of a contradiction in a proof which may be useful for explosions.
    """

    is_variable = True

    def __init__(self):
        self.contradiction = '\\bot'

    def __str__(self):
        return 'X'
    
    def latex(self):
        return self.contradiction
    
    def getvalue(self):
        return False

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
        self.booleanvalue = ((not left.booleanvalue) or right.booleanvalue) and ((not right.booleanvalue) or left.booleanvalue)

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
        self.booleanvalue = None
        #self.booleanvalue = (not left.booleanvalue) or right.booleanvalue
    
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
        
    def getvalue(self):
        return (not self.left.getvalue()) or self.right.getvalue()

class N(Wff):
    """A well-formed formula which is necessarily true."""

    is_variable = True

    def __init__(self, wff):
        self.necessary = '\\Box'
        self.wff = wff

    def __str__(self):
        if self.wff.is_variable:
            return f'Nec {self.wff}'
        else:
            return f'Nec({self.wff})'
    
    def latex(self):
        if self.wff.is_variable:
            return f'{self.necessary} {self.wff}'
        else:
            return f'{self.necessary} ({self.wff})'
    
    def getvalue(self):
        return True
    
class Not(Wff):
    """A well formed formula with one argument which is also a well formed formula joined
    with logical not.
    """

    is_variable = True

    def __init__(self, negated: Wff):
        self.negated = negated
        self.connector = '~'
        self.latexconnector = '\\lnot '
        self.booleanvalue = None
        #self.booleanvalue = not negated.booleanvalue

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
    
    def getvalue(self):
        return not self.negated.getvalue()

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
        self.booleanvalue = left.booleanvalue or right.booleanvalue

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
        
    def getvalue(self):
        return self.left.getvalue() or self.right.getvalue()

class P(Wff):
    """A well-formed formula which is possibly true."""

    is_variable = True

    def __init__(self, wff):
        self.necessary = '\\Diamond'
        self.wff = wff

    def __str__(self):
        if self.wff.is_variable:
            return f'Pos {self.wff}'
        else:
            return f'Pos({self.wff})'
    
    def latex(self):
        if self.wff.is_variable:
            return f'{self.necessary} {self.wff}'
        else:
            return f'{self.necessary} ({self.wff})'
    
    def getvalue(self):
        return True
    
class T():
    """A well formed formula which is always true."""

    is_variable = False

    def __init__(self):
        self.tautology = '\\top'

    def __str__(self):
        return 'T'
    
    def latex(self):
        return self.tautology
    
    def getvalue(self):
        return True


