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

    and_connector = '&'
    and_latexconnector = '\\wedge'
    and_treeconnector = 'And'
    iff_connector = '<>'
    iff_latexconnector = '\\leftrightarrow'
    iff_treeconnector = 'Iff'
    implies_connector = '>'
    implies_latexconnector = '\\to'
    implies_treeconnector = 'Implies'
    necessary_connector = 'Nec'
    necessary_latexconnector = '\\Box'
    necessary_treeconnector = 'N'
    not_connector = '~'
    not_latexconnector = '\\lnot '
    not_treeconnector = 'Not'
    or_connector = '|'
    or_latexconnector = '\\vee'
    or_treeconnector = 'Or'
    possible_connector = 'Pos'
    possible_latexconnector = '\\Diamond'
    possible_treeconnector = 'P'
    wff_treeconnector = 'Wff'

    f_name = 'X'
    f_latexname = '\\bot'
    t_name = 'T'
    t_latexname = '\\top'

    
    def __init__(self, name: str, latexname: str = ''):
        self.name = name
        self.latexname = latexname
        self.booleanvalue = None

    def __str__(self):
        return f'{self.name}'
    
    def latex(self):
        if self.latexname == '':
            return f'{self.name}'
        else:
            return f'{self.latexname}'
        
    def tree(self):
        #return f'{self.wff_treeconnector}{self.lb}{self.name}{self.rb}'
        return self.name
    
    def pattern(self):
        return '{}'
    
    def treetuple(self):
        return self.name
    
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
        self.booleanvalue = left.booleanvalue and right.booleanvalue

    def __str__(self):
        if self.left.is_variable and self.right.is_variable:
            return f'{self.left} {self.and_connector} {self.right}'
        elif self.left.is_variable:
            return f'{self.left} {self.and_connector} {self.lb}{self.right}{self.rb}'
        elif self.right.is_variable:
            return f'{self.lb}{self.left}{self.rb} {self.and_connector} {self.right}'
        else:
            return f'{self.lb}{self.left}{self.rb} {self.and_connector} {self.lb}{self.right}{self.rb}'
        
    def latex(self):
        if self.left.is_variable and self.right.is_variable:
            return f'{self.left.latex()} {self.and_latexconnector} {self.right.latex()}'
        elif self.left.is_variable:
            return f'{self.left.latex()} {self.and_latexconnector} {self.lb}{self.right.latex()}{self.rb}'
        elif self.right.is_variable:
            return f'{self.lb}{self.left.latex()}{self.rb} {self.and_latexconnector} {self.right.latex()}'
        else:
            return f'{self.lb}{self.left.latex()}{self.rb} {self.and_latexconnector} {self.lb}{self.right.latex()}{self.rb}'
        
    def tree(self):
        return f'{self.and_treeconnector}{self.lb}{self.left.tree()}, {self.right.tree()}{self.rb}'
    
    def pattern(self):
        return f'{self.and_treeconnector}{self.lb}{self.left.pattern()}, {self.right.pattern()}{self.rb}'
    
    def treetuple(self):
        return self.and_treeconnector, self.lb, self.left.treetuple(), ',', self.right.treetuple(), self.rb
        
    def getvalue(self):
        return self.left.getvalue() and self.right.getvalue()

class F(Wff):
    """This well formed formula is the result of a contradiction in a proof which may be useful for explosions.
    """

    is_variable = True

    def __init__(self):
        self.value = False

    def __str__(self):
        return f'{self.f_name}'
    
    def latex(self):
        return f'{self.f_latexname}'
    
    def tree(self):
        return f'{self.f_name}'
    
    def pattern(self):
        return f'{self.f_name}'
    
    def treetuple(self):
        return self.f_name
    
    def getvalue(self):
        return self.value

class Iff(Wff):
    """A well formed formula with two arguments which are also well formed formulas
    joined by if and only if.
    """

    is_variable = False

    def __init__(self, left: Wff, right: Wff):
        self.left = left
        self.right = right
        self.booleanvalue = ((not left.booleanvalue) or right.booleanvalue) and ((not right.booleanvalue) or left.booleanvalue)

    def __str__(self):
        if self.left.is_variable and self.right.is_variable:
            return f'{self.left} {self.iff_connector} {self.right}'
        elif self.left.is_variable:
            return f'{self.left} {self.iff_connector} {self.lb}{self.right}{self.rb}'
        elif self.right.is_variable:
            return f'{self.lb}{self.left}{self.rb} {self.iff_connector} {self.right}'
        else:
            return f'{self.lb}{self.left}{self.rb} {self.iff_connector} {self.lb}{self.right}{self.rb}'
        
    def latex(self):
        if self.left.is_variable and self.right.is_variable:
            return f'{self.left.latex()} {self.iff_latexconnector} {self.right.latex()}'
        elif self.left.is_variable:
            return f'{self.left.latex()} {self.iff_latexconnector} {self.lb}{self.right.latex()}{self.rb}'
        elif self.right.is_variable:
            return f'{self.lb}{self.left.latex()}{self.rb} {self.iff_latexconnector} {self.right.latex()}'
        else:
            return f'{self.lb}{self.left.latex()}{self.rb} {self.iff_latexconnector} {self.lb}{self.right.latex()}{self.rb}'
        
    def tree(self):
        return f'{self.iff_treeconnector}{self.lb}{self.left.tree()}, {self.right.tree()}{self.rb}'
    
    def pattern(self):
        return f'{self.iff_treeconnector}{self.lb}{self.left.pattern()}, {self.right.pattern()}{self.rb}'
    
    def treetuple(self):
        return self.iff_treeconnector, self.lb, self.left.treetuple(), ',', self.right.treetuple(), self.rb

class Implies(Wff):
    """A well formed formula with two arguments which are also well formed formulas joined
    by implies.  The antecedent is the first of the two arguments.  The consequent is the
    second.
    """

    is_variable = False

    def __init__(self, left: Wff, right: Wff):
        self.left = left
        self.right = right
        self.booleanvalue = None
    
    def __str__(self):
        if self.left.is_variable and self.right.is_variable:
            return f'{self.left} {self.implies_connector} {self.right}'
        elif self.left.is_variable:
            return f'{self.left} {self.implies_connector} {self.lb}{self.right}{self.rb}'
        elif self.right.is_variable:
            return f'{self.lb}{self.left}{self.rb} {self.implies_connector} {self.right}'
        else:
            return f'{self.lb}{self.left}{self.rb} {self.implies_connector} {self.lb}{self.right}{self.rb}'
        
    def latex(self):
        if self.left.is_variable and self.right.is_variable:
            return f'{self.left.latex()} {self.implies_latexconnector} {self.right.latex()}'
        elif self.left.is_variable:
            return f'{self.left.latex()} {self.implies_latexconnector} {self.lb}{self.right.latex()}{self.rb}'
        elif self.right.is_variable:
            return f'{self.lb}{self.left.latex()}{self.rb} {self.implies_latexconnector} {self.right.latex()}'
        else:
            return f'{self.lb}{self.left.latex()}{self.rb} {self.implies_latexconnector} {self.lb}{self.right.latex()}{self.rb}'
        
    def tree(self):
        return f'{self.implies_treeconnector}{self.lb}{self.left.tree()}, {self.right.tree()}{self.rb}'
    
    def pattern(self):
        return f'{self.implies_treeconnector}{self.lb}{self.left.pattern()}, {self.right.pattern()}{self.rb}'
    
    def treetuple(self):
        return self.implies_treeconnector, self.lb, self.left.treetuple(), ',', self.right.treetuple(), self.rb
        
    def getvalue(self):
        return (not self.left.getvalue()) or self.right.getvalue()

class N(Wff):
    """A well-formed formula which is necessarily true."""

    is_variable = True

    def __init__(self, wff):
        self.wff = wff

    def __str__(self):
        if self.is_variable:
            return f'{self.necessary_connector} {self.wff}'
        else:
            return f'{self.necessary_connector}{self.lb}{self.wff}{self.rb}'
    
    def latex(self):
        if self.is_variable:
            return f'{self.necessary_latexconnector} {self.wff}'
        else:
            return f'{self.necessary_latexconnector} {self.lb}{self.wff}{self.rb}'
        
    def tree(self):
        return f'{self.necessary_treeconnector}{self.lb}{self.wff.tree()}{self.rb}'
    
    def pattern(self):
        return f'{self.necessary_treeconnector}{self.lb}{self.wff.pattern()}{self.rb}'
    
    def treetuple(self):
        return self.necessary_treeconnector, self.lb, self.wff.treetuple(), self.rb
    
    def getvalue(self):
        return True
    
class Not(Wff):
    """A well formed formula with one argument which is also a well formed formula joined
    with logical not.
    """

    is_variable = True

    def __init__(self, negated: Wff):
        self.negated = negated
        self.booleanvalue = None

    def __str__(self):
        if self.negated.is_variable:
            return f'{self.not_connector}{self.negated}'
        else:
            return f'{self.not_connector}{self.lb}{self.negated}{self.rb}'
        
    def latex(self):
        if self.negated.is_variable:
            return f'{self.not_latexconnector}{self.negated.latex()}'
        else:
            return f'{self.not_latexconnector}{self.lb}{self.negated.latex()}{self.rb}'
        
    def tree(self):
        return f'{self.not_treeconnector}{self.lb}{self.negated.tree()}{self.rb}'
    
    def pattern(self):
        return f'{self.not_treeconnector}{self.lb}{self.negated.pattern()}{self.rb}'
    
    def treetuple(self):
        return self.not_treeconnector, self.lb, self.negated.treetuple(), self.rb
    
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
        self.booleanvalue = left.booleanvalue or right.booleanvalue

    def __str__(self):
        if self.left.is_variable and self.right.is_variable:
            return f'{self.left} {self.or_connector} {self.right}'
        elif self.left.is_variable:
            return f'{self.left} {self.or_connector} {self.lb}{self.right}{self.rb}'
        elif self.right.is_variable:
            return f'{self.lb}{self.left}{self.rb} {self.or_connector} {self.right}'
        else:
            return f'{self.lb}{self.left}{self.rb} {self.or_connector} {self.lb}{self.right}{self.rb}'
        
    def latex(self):
        if self.left.is_variable and self.right.is_variable:
            return f'{self.left.latex()} {self.or_latexconnector} {self.right.latex()}'
        elif self.left.is_variable:
            return f'{self.left.latex()} {self.or_latexconnector} {self.lb}{self.right.latex()})'
        elif self.right.is_variable:
            return f'{self.lb}{self.left.latex()}{self.rb} {self.or_latexconnector} {self.right.latex()}'
        else:
            return f'{self.lb}{self.left.latex()}{self.rb} {self.or_latexconnector} {self.lb}{self.right.latex()}{self.rb}'
        
    def tree(self):
        return f'{self.or_treeconnector}{self.lb}{self.left.tree()}, {self.right.tree()}{self.rb}'
    
    def pattern(self):
        return f'{self.or_treeconnector}{self.lb}{self.left.pattern()}, {self.right.pattern()}{self.rb}'
    
    def treetuple(self):
        return self.or_treeconnector, self.lb, self.left.treetuple(), ',', self.right.treetuple(), self.rb
        
    def getvalue(self):
        return self.left.getvalue() or self.right.getvalue()

class P(Wff):
    """A well-formed formula which is possibly true."""

    is_variable = True

    def __init__(self, wff):
        self.wff = wff

    def __str__(self):
        if self.is_variable:
            return f'{self.possible_connector} {self.wff}'
        else:
            return f'{self.possible_connector}{self.lb}{self.wff}{self.rb}'
    
    def latex(self):
        if self.is_variable:
            return f'{self.possible_latexconnector} {self.wff}'
        else:
            return f'{self.possible_latexconnector} {self.lb}{self.wff}{self.rb}'
        
    def tree(self):
        return f'{self.possible_treeconnector}{self.lb}{self.wff.tree()}{self.rb}'
    
    def pattern(self):
        return f'{self.possible_treeconnector}{self.lb}{self.wff.pattern()}{self.rb}'
    
    def treetuple(self):
        return self.possible_treeconnector, self.lb, self.wff.treetuple(), self.rb
    
    def getvalue(self):
        return True
    
class T(Wff):
    """A well formed formula which is always true."""

    is_variable = False

    def __init__(self):
        self.value = True

    def __str__(self):
        return f'{self.t_name}'
    
    def latex(self):
        return f'{self.t_latexname}'
    
    def tree(self):
        return f'{self.t_name}'
    
    def pattern(self):
        return f'{self.t_name}'
    
    def treetuple(self):
        return self.t_name
    
    def getvalue(self):
        return self.value


