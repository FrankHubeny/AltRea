# wffs.py
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

    # default_and_connector = '&'
    # default_and_latexconnector = '\\wedge'
    # and_treeconnector = 'And'
    # default_iff_connector = '<>'
    # default_iff_latexconnector = '\\leftrightarrow'
    # iff_treeconnector = 'Iff'
    # default_implies_connector = '>'
    # default_implies_latexconnector = '\\to'
    # implies_treeconnector = 'Implies'
    # default_necessary_connector = 'Nec'
    # default_necessary_latexconnector = '\\Box'
    # necessary_treeconnector = 'N'
    # default_not_connector = '~'
    # default_not_latexconnector = '\\lnot '
    # not_treeconnector = 'Not'
    # default_or_connector = '|'
    # default_or_latexconnector = '\\vee'
    # or_treeconnector = 'Or'
    # possibly_connector = 'Pos'
    # possibly_latexconnector = '\\Diamond'
    # possible_treeconnector = 'P'
    # wff_treeconnector = 'Wff'
    reserved_names = ['And', 'Or', 'Not', 'Implies', 'Iff', 'Wff', 'Falsehood', 'Truth', 'Proposition']

    f_name = 'Falsehood'
    f_latexname = '\\bot'
    falsehood_treeconnector = 'Falsehood'
    t_name = 'Truth'
    t_latexname = '\\top'

    
    def __init__(self, 
                 name: str, 
                 latexname: str = '', 
                 kind: str = 'Proposition'):
        if name in self.reserved_names or latexname in self.reserved_names:
            raise ValueError(f'The name "{name}" or the latexname "{latexname}" is in the list of reserved words: {self.reserved_names} which cannot be used.')
        elif name == '':
            raise ValueError(f'The name "{name}" is the empty string which cannot be used as a name.')
        elif not isinstance(name, str) or not isinstance(latexname, str):
            raise TypeError(f' The name "{str(name)}" or the latexname "{str(latexname)}" was not a string.')
        else:
            self.name = name
            self.latexname = latexname
            self.booleanvalue = None
            self.multivalue = (True)
            self.kind = kind

    def __str__(self):
        return f'{self.name}'
    
    def latex(self):
        if self.latexname == '':
            return f'{self.name}'
        else:
            return f'{self.latexname}'
        
    def tree(self):
        return self.name
    
    def pattern(self, wfflist: list):
        try:
            idx = wfflist.index(self.name)
        except ValueError:
            idx = len(wfflist)
            wfflist.append(self.name)
        return ''.join(['{', str(idx), '}'])
    
    def makeschemafromlist(self, wfflist: list):
        try:
            idx = wfflist.index(self)
            return ''.join(['{', str(idx), '}'])
        except ValueError:
            return self.name
    
    def treetuple(self):
        return self.name
    
    def setvalue(self, value: bool):
        self.booleanvalue = value

    def equals(self, otherwff):
        return str(self) == str(otherwff)
    
    def getvalue(self):
        return self.booleanvalue   
    
    def getmultivalue(self):
        return self.multivalue   
    
    def setmultivalue(self, value):
        self.multivalue = value

class And(Wff):
    """A well formed formula with two arguments which are also well formed formulas connected
    by logical and.
    """

    is_variable = False

    def __init__(self, 
                 left: Wff, 
                 right: Wff, 
                 connector: str = '&', 
                 latexconnector: str = '\\wedge', 
                 treeconnector: str = 'And'):
        self.left = left
        self.right = right
        self.connector = connector
        self.latexconnector = latexconnector
        self.treeconnector = treeconnector
        self.booleanvalue = left.booleanvalue and right.booleanvalue
        leftmultivalue = left.getmultivalue()
        rightmultivalue = right.getmultivalue()
        if leftmultivalue == (False) or rightmultivalue == (False):
            self.multivalue = (False)
        elif leftmultivalue == (True) and rightmultivalue == (True):
            self.multivalue = (True)
        else:
            self.multivalue = (True, False)

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
        
    def tree(self):
        return f'{self.treeconnector}{self.lb}{self.left.tree()}, {self.right.tree()}{self.rb}'
    
    def pattern(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.left.pattern(wfflist)}, {self.right.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.left.makeschemafromlist(wfflist)}, {self.right.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.treeconnector, self.lb, self.left.treetuple(), ',', self.right.treetuple(), self.rb
        
    def getvalue(self):
        return self.left.getvalue() and self.right.getvalue()
    
    def getmultivalue(self):
        leftmultivalue = self.left.getmultivalue()
        rightmultivalue = self.right.getmultivalue()
        if leftmultivalue== (False) or rightmultivalue == (False):
            return (False)
        elif leftmultivalue == (True) and rightmultivalue == (True):
            return (True)
        else:
            return (True, False)
        
class ConsistentWith(Wff):
    """A well formed formula with two arguments which are also well formed formulas connected
    by logical and.
    """

    is_variable = False

    def __init__(self, 
                 left: Wff, 
                 right: Wff, 
                 connector: str = '∘', 
                 latexconnector: str = '\\circ',
                 treeconnector: str = 'ConsistentWith'):
        self.left = left
        self.right = right
        self.connector = connector
        self.latexconnector = latexconnector
        self.treeconnector = treeconnector
        self.booleanvalue = left.booleanvalue and right.booleanvalue
        leftmultivalue = left.getmultivalue()
        rightmultivalue = right.getmultivalue()
        if leftmultivalue == (False) or rightmultivalue == (False):
            self.multivalue = (False)
        elif leftmultivalue == (True) and rightmultivalue == (True):
            self.multivalue = (True)
        else:
            self.multivalue = (True, False)

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
        
    def tree(self):
        return f'{self.treeconnector}{self.lb}{self.left.tree()}, {self.right.tree()}{self.rb}'
    
    def pattern(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.left.pattern(wfflist)}, {self.right.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.left.makeschemafromlist(wfflist)}, {self.right.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.treeconnector, self.lb, self.left.treetuple(), ',', self.right.treetuple(), self.rb
        
    def getvalue(self):
        return self.left.getvalue() and self.right.getvalue()
    
    def getmultivalue(self):
        leftmultivalue = self.left.getmultivalue()
        rightmultivalue = self.right.getmultivalue()
        if leftmultivalue== (False) or rightmultivalue == (False):
            return (False)
        elif leftmultivalue == (True) and rightmultivalue == (True):
            return (True)
        else:
            return (True, False)

class Falsehood(Wff):
    """This well formed formula is the result of a contradiction in a proof which may be useful for explosions.
    """

    is_variable = True
    
    def __init__(self, 
                 wff: Wff,
                 connector = 'Falsehood',
                 latexconnector = '\\bot~',
                 treeconnector = 'Falsehood'):
        # if name in self.reserved_names or latexname in self.reserved_names:
        #     raise ValueError(f'The name "{name}" or the latexname "{latexname}" is in the list of reserved words: {self.reserved_names} which cannot be used.')
        # elif type(name) != str or type(latexname) != str:
        #     raise TypeError(f' The name "{str(name)}" or the latexname "{str(latexname)}" was not a string.')
        # else:
        #     self.booleanvalue = False
        #     if name == '':
        #         self.name = self.f_name
        #     else:
        #         self.name = name
        #     if latexname == '':
        #         if name == '':
        #             self.latex = self.f_latexname
        #         else:
        #             self.latex = self.name
        #     else:
        #         self.latex = latexname
        self.wff = wff
        self.connector = connector
        self.latexconnector = latexconnector
        self.treeconnector = treeconnector
        self.booleanvalue = False
        self.multivalue = (False)

    def __str__(self):
        return f'{self.connector}{self.lb}{self.wff}{self.rb}'
    
    def latex(self):
        return f'{self.latexconnector}{self.lb}{self.wff.latex()}{self.rb}'
    
    def tree(self):
        return f'{self.treeconnector}{self.lb}{self.wff.tree()}{self.rb}'
    
    def pattern(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.wff.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.wff.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.treeconnector, self.lb, self.wff.treetuple(), self.rb
    
    def getvalue(self):
        return self.booleanvalue
    
    def setvalue(self, value: bool = False):
        self.booleanvalue = False

    def getmultivalue(self):
        return self.multivalue

class Iff(Wff):
    """A well formed formula with two arguments which are also well formed formulas
    joined by if and only if.
    """

    is_variable = False

    def __init__(self, 
                 left: Wff, 
                 right: Wff, 
                 connector: str = '≡', 
                 latexconnector: str = '\\equiv ',
                 treeconnector: str = 'Iff'):
        self.left = left
        self.right = right
        self.connector = connector
        self.latexconnector = latexconnector
        self.treeconnector = treeconnector
        self.booleanvalue = ((not left.booleanvalue) or right.booleanvalue) and ((not right.booleanvalue) or left.booleanvalue)
        leftmultivalue = self.left.getmultivalue()
        rightmultivalue = self.right.getmultivalue()
        if leftmultivalue == (False) or rightmultivalue == (False):
            self.multivalue = (False)
        elif leftmultivalue == (True) and rightmultivalue == (True):
            self.multivalue = (True)
        else:
            self.multivalue = (True, False) 

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
        
    def tree(self):
        return f'{self.treeconnector}{self.lb}{self.left.tree()}, {self.right.tree()}{self.rb}'
    
    def pattern(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.left.pattern(wfflist)}, {self.right.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.left.makeschemafromlist(wfflist)}, {self.right.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.treeconnector, self.lb, self.left.treetuple(), ',', self.right.treetuple(), self.rb
    
    def getmultivalue(self):
        leftmultivalue = self.left.getmultivalue()
        rightmultivalue = self.right.getmultivalue()
        if leftmultivalue == (False) or rightmultivalue == (False):
            return (False)
        elif leftmultivalue == (True) and rightmultivalue == (True):
            return (True)
        else:
            return (True, False) 
        
class StrictIff(Wff):
    """A well formed formula with two arguments which are also well formed formulas
    joined by if and only if.
    """

    is_variable = False

    def __init__(self, 
                 left: Wff, 
                 right: Wff, 
                 connector: str = ' ≣ ', 
                 latexconnector: str = '≣',
                 treeconnector: str = 'StrictIff'):
        self.left = left
        self.right = right
        self.connector = connector
        self.latexconnector = latexconnector
        self.treeconnector = treeconnector
        self.booleanvalue = ((not left.booleanvalue) or right.booleanvalue) and ((not right.booleanvalue) or left.booleanvalue)
        leftmultivalue = self.left.getmultivalue()
        rightmultivalue = self.right.getmultivalue()
        if leftmultivalue == (False) or rightmultivalue == (False):
            self.multivalue = (False)
        elif leftmultivalue == (True) and rightmultivalue == (True):
            self.multivalue = (True)
        else:
            self.multivalue = (True, False) 

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
        
    def tree(self):
        return f'{self.treeconnector}{self.lb}{self.left.tree()}, {self.right.tree()}{self.rb}'
    
    def pattern(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.left.pattern(wfflist)}, {self.right.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.left.makeschemafromlist(wfflist)}, {self.right.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.treeconnector, self.lb, self.left.treetuple(), ',', self.right.treetuple(), self.rb
    
    def getmultivalue(self):
        leftmultivalue = self.left.getmultivalue()
        rightmultivalue = self.right.getmultivalue()
        if leftmultivalue == (False) or rightmultivalue == (False):
            return (False)
        elif leftmultivalue == (True) and rightmultivalue == (True):
            return (True)
        else:
            return (True, False) 

class Implies(Wff):
    """A well formed formula with two arguments which are also well formed formulas joined
    by implies.  The antecedent is the first of the two arguments.  The consequent is the
    second.
    """

    is_variable = False

    def __init__(self, 
                 left: Wff, 
                 right: Wff, 
                 connector: str = '⊃', 
                 latexconnector: str = '\\supset ',
                 treeconnector: str = 'Implies'):
        self.left = left
        self.right = right
        self.connector = connector
        self.latexconnector = latexconnector
        self.treeconnector = treeconnector
        self.booleanvalue = None
        leftmultivalue = self.left.getmultivalue()
        rightmultivalue = self.right.getmultivalue()
        if leftmultivalue == (False) or rightmultivalue == (True):
            self.multivalue = (True)
        elif leftmultivalue == (True) and rightmultivalue == (False):
            self.multivalue = (False)
        else:
            self.multivalue = (True, False)
    
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
        
    def tree(self):
        return f'{self.treeconnector}{self.lb}{self.left.tree()}, {self.right.tree()}{self.rb}'
    
    def pattern(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.left.pattern(wfflist)}, {self.right.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.left.makeschemafromlist(wfflist)}, {self.right.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.treeconnector, self.lb, self.left.treetuple(), ',', self.right.treetuple(), self.rb
        
    def getvalue(self):
        return (not self.left.getvalue()) or self.right.getvalue()
    
    def getmultivalue(self):
        leftmultivalue = self.left.getmultivalue()
        rightmultivalue = self.right.getmultivalue()
        if leftmultivalue == (False) or rightmultivalue == (True):
            return (True)
        elif leftmultivalue == (True) and rightmultivalue == (False):
            return (False)
        else:
            return (True, False)

class StrictImplies(Wff):
    """A well formed formula with two arguments which are also well formed formulas joined
    by implies.  The antecedent is the first of the two arguments.  The consequent is the
    second.
    """

    is_variable = False

    def __init__(self, 
                 left: Wff, 
                 right: Wff, 
                 connector: str = ' ⊰ ', 
                 latexconnector: str = '\\prec ', #'\\prec ',
                 treeconnector: str = 'StrictImplies'):
        self.left = left
        self.right = right
        self.connector = connector
        self.latexconnector = latexconnector
        self.treeconnector = treeconnector
        self.booleanvalue = None
        leftmultivalue = self.left.getmultivalue()
        rightmultivalue = self.right.getmultivalue()
        if leftmultivalue == (False) or rightmultivalue == (True):
            self.multivalue = (True)
        elif leftmultivalue == (True) and rightmultivalue == (False):
            self.multivalue = (False)
        else:
            self.multivalue = (True, False)
    
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
        
    def tree(self):
        return f'{self.treeconnector}{self.lb}{self.left.tree()}, {self.right.tree()}{self.rb}'
    
    def pattern(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.left.pattern(wfflist)}, {self.right.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.left.makeschemafromlist(wfflist)}, {self.right.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.treeconnector, self.lb, self.left.treetuple(), ',', self.right.treetuple(), self.rb
        
    def getvalue(self):
        return (not self.left.getvalue()) or self.right.getvalue()
    
    def getmultivalue(self):
        leftmultivalue = self.left.getmultivalue()
        rightmultivalue = self.right.getmultivalue()
        if leftmultivalue == (False) or rightmultivalue == (True):
            return (True)
        elif leftmultivalue == (True) and rightmultivalue == (False):
            return (False)
        else:
            return (True, False)

class Necessary(Wff):
    """A well-formed formula which is necessarily true."""

    is_variable = True
    booleanvalue = True

    def __init__(self, 
                 wff: Wff, 
                 connector: str = '☐', 
                 latexconnector: str = '\\Box~', 
                 treeconnector: str = 'Necessary'):
        self.wff = wff
        self.connector = connector
        self.latexconnector = latexconnector
        self.treeconnector = treeconnector
        self.multivalue = (True)

    def __str__(self):
        if self.wff.is_variable:
            return f'{self.connector}{self.wff}'
        else:
            return f'{self.connector}{self.lb}{self.wff}{self.rb}'
    
    def latex(self):
        if self.wff.is_variable:
            return f'{self.latexconnector} {self.wff.latex()}'
        else:
            return f'{self.latexconnector} {self.lb}{self.wff.latex()}{self.rb}'
        
    def tree(self):
        return f'{self.treeconnector}{self.lb}{self.wff.tree()}{self.rb}'
    
    def pattern(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.wff.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.wff.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.treeconnector, self.lb, self.wff.treetuple(), self.rb
    
    def getvalue(self):
        return self.wff.value()
    
    def getmultivalue(self):
        return self.wff.getmultivalue()
    
class Not(Wff):
    """A well formed formula with one argument which is also a well formed formula joined
    with logical not.
    """

    is_variable = True

    def __init__(self, 
                 negated: Wff, 
                 connector: str = '~', 
                 latexconnector: str = '\\lnot~',
                 treeconnector: str = 'Not'):
        self.negated = negated
        self.booleanvalue = None
        self.connector = connector
        self.latexconnector = latexconnector 
        self.treeconnector = treeconnector  
        negatedmultivalue = negated.getmultivalue() 
        if negatedmultivalue == (True):
            self.multivalue = (False)
        elif negatedmultivalue == (False):
            self.multivalue = (True)
        else:
            self.multivalue = (True, False)

    def __str__(self):
        if self.negated.is_variable:
            return f'{self.connector}{self.negated}'
        else:
            return f'{self.connector}{self.lb}{self.negated}{self.rb}'
        
    def latex(self):
        if self.negated.is_variable:
            return f'{self.latexconnector}{self.negated.latex()}'
        else:
            return f'{self.latexconnector}{self.lb}{self.negated.latex()}{self.rb}'
        
    def tree(self):
        return f'{self.treeconnector}{self.lb}{self.negated.tree()}{self.rb}'
    
    def pattern(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.negated.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.negated.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.treeconnector, self.lb, self.negated.treetuple(), self.rb
    
    def getvalue(self):
        return not self.negated.getvalue()
    
    def getmultivalue(self):
        negatedmultivalue = self.negated.getmultivalue() 
        if negatedmultivalue == (True):
            return (False)
        elif negatedmultivalue == (False):
            return (True)
        else:
            return (True, False) 

class Or(Wff):
    """A well formed formula with two arguments which are also well formed formulas connected
    by logical or.
    """

    is_variable = False

    def __init__(self, 
                 left: Wff, 
                 right: Wff, 
                 connector: str = '|', 
                 latexconnector: str = '\\vee',
                 treeconnector: str = 'Or'):
        self.left = left
        self.right = right
        self.connector = connector
        self.latexconnector = latexconnector
        self.treeconnector = treeconnector
        self.booleanvalue = left.booleanvalue or right.booleanvalue
        leftmultivalue = self.left.getmultivalue()
        rightmultivalue = self.right.getmultivalue()
        if leftmultivalue == (False) and rightmultivalue == (False):
            self.multivalue = (False)
        elif leftmultivalue == (True) or rightmultivalue == (True):
            self.multivalue = (True)
        else:
            self.multivalue = (True, False)

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
            return f'{self.left.latex()} {self.latexconnector} {self.lb}{self.right.latex()})'
        elif self.right.is_variable:
            return f'{self.lb}{self.left.latex()}{self.rb} {self.latexconnector} {self.right.latex()}'
        else:
            return f'{self.lb}{self.left.latex()}{self.rb} {self.latexconnector} {self.lb}{self.right.latex()}{self.rb}'
        
    def tree(self):
        return f'{self.treeconnector}{self.lb}{self.left.tree()}, {self.right.tree()}{self.rb}'
    
    def pattern(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.left.pattern(wfflist)}, {self.right.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.left.makeschemafromlist(wfflist)}, {self.right.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.treeconnector, self.lb, self.left.treetuple(), ',', self.right.treetuple(), self.rb
        
    def getvalue(self):
        return self.left.getvalue() or self.right.getvalue()
    
    def getmultivalue(self):
        leftmultivalue = self.left.getmultivalue()
        rightmultivalue = self.right.getmultivalue()
        if leftmultivalue == (False) and rightmultivalue == (False):
            return (False)
        elif leftmultivalue == (True) or rightmultivalue == (True):
            return (True)
        else:
            return (True, False)

class Possibly(Wff):
    """A well-formed formula which is possibly true."""

    is_variable = True
    booleanvalue = True

    def __init__(self, 
                 wff: Wff, 
                 connector: str = '◇', 
                 latexconnector: str = '\\Diamond~', 
                 treeconnector: str = 'Possibly'):
        self.wff = wff
        self.connector = connector
        self.latexconnector = latexconnector
        self.treeconnector = treeconnector
        self.multivalue = (True)

    def __str__(self):
        if self.wff.is_variable:
            return f'{self.connector}{self.wff}'
        else:
            return f'{self.connector}{self.lb}{self.wff}{self.rb}'
    
    def latex(self):
        if self.wff.is_variable:
            return f'{self.latexconnector} {self.wff.latex()}'
        else:
            return f'{self.latexconnector} {self.lb}{self.wff.latex()}{self.rb}'
        
    def tree(self):
        return f'{self.treeconnector}{self.lb}{self.wff.tree()}{self.rb}'
    
    def pattern(self, wfflist):
        return f'{self.treeconnector}{self.lb}{self.wff.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.treeconnector}{self.lb}{self.wff.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.treeconnector, self.lb, self.wff.treetuple(), self.rb
    
    def getvalue(self):
        return True
    
    def getmultivalue(self):
        return self.multivalue
    
class Truth(Wff):
    """A well formed formula which is always true."""

    is_variable = True
    booleanvalue = True

    def __init__(self, 
                 name: str = '', 
                 latexname: str = ''):
        if name in self.reserved_names or latexname in self.reserved_names:
            raise ValueError(f'The name "{name}" or the latexname "{latexname}" is in the list of reserved words: {self.reserved_names} which cannot be used.')
        elif name == '':
            raise ValueError(f'The name "{name}" is the empty string which cannot be used as a name.')
        elif not isinstance(name, str) or not isinstance(latexname, str):
            raise TypeError(f' The name "{str(name)}" or the latexname "{str(latexname)}" was not a string.')
        else:
            if name == '':
                self.name = self.t_name
            else:
                self.name = name
            if latexname == '':
                self.latexname = self.name
            else:
                self.latexname = latexname
        self.multivalue = (True)

    def __str__(self):
        return f'{self.name}'
    
    def latex(self):
        return f'{self.latexname}'
    
    def tree(self):
        return f'{self.name}'
    
    # def pattern(self):
    #     return f'{self.name}'
    
    def treetuple(self):
        return self.name
    
    def getvalue(self):
        return self.booleanvalue
    
    def setvalue(self, value: bool):
        self.booleanvalue = True

class Proposition(Wff):
    """A well formed formula which is can be either true or false, but not both and not neither."""

    is_variable = True

    def __init__(self, 
                 name: str, 
                 latexname: str = '', 
                 kind: str = 'Proposition'):
        if name in self.reserved_names or latexname in self.reserved_names:
            raise ValueError(f'The name "{name}" or the latexname "{latexname}" is in the list of reserved words: {self.reserved_names} which cannot be used.')
        elif name == '':
            raise ValueError(f'The name "{name}" is the empty string which cannot be used as a name.')
        elif not isinstance(name, str) or not isinstance(latexname, str):
            raise TypeError(f' The name "{str(name)}" or the latexname "{str(latexname)}" was not a string.')
        else:
            if name == '':
                self.name = self.t_name
            else:
                self.name = name
            if latexname == '':
                self.latexname = self.name
            else:
                self.latexname = latexname
        self.kind = kind
        self.multivalue = (True)
        self.booleanvalue = True

    def __str__(self):
        return self.name
    
    def latex(self):
        return self.latexname
    
    def tree(self):
        return self.name
    
    # def pattern(self):
    #     return f'{self.name}'
    
    def treetuple(self):
        return self.name
    
    def getvalue(self):
        return self.booleanvalue
    
    def setvalue(self, value: bool):
        self.booleanvalue = value

    def getmultivalue(self):
        return self.multivalue
    
    def setmultivalue(self, value):
        self.multivalue = value

class Axiom(Wff):
    """This class holds axioms of the logical system."""

    is_variable = True
    

    def __init__(self, schema: Wff):
        self.schema = schema
        self.booleanvalue = True
        self.multivalue = (True)

    def __str__(self):
        return f'{str(self.schema)}'
    
    def latex(self):
        return f'{self.schema.latex()}'

    def tree(self):
        return f'{self.schema.tree()}'
    
    def pattern(self, wfflist: list):
        return f'Axiom({self.schema.pattern(wfflist)})'
    
    def makeschemafromlist(self, wfflist: list):
        return f'Axiom({self.schema.makeschemafromlist(wfflist)})'
    
    def treetuple(self):
        return f'{self.schema.treetuple()}'
        
    def getvalue(self):
        return self.schema.booleanvalue() 
    
    def setvalue(self, val: bool):
        self.booleanvalue = True

    # def getmultivalue(self):
    #     return self.multivalue

class Definition(Wff):
    """This class defines one wff expression to be the same as the other."""

    is_variable = True
    booleanvalue = None
    lb = '('
    rb = ')'
    tree_connector = '|='

    def __init__(self, 
                 left: Wff, 
                 right: Wff, 
                 connector: str = '=', 
                 latexconnector: str = '\\equiv '):
        self.left = left
        self.right = right
        self.connector = connector
        self.latexconnector = latexconnector
        #self.multivalue = (True)

    def __str__(self):
        return f'{str(self.left)} {self.connector} {str(self.right)}'
    
    def latex(self):
        return f'{self.left.latex()} {self.latexconnector} {self.right.latex()}'

    def tree(self):
        return f'{self.left.tree()} {self.connector} {self.right.tree()}'
    
    def pattern(self, wfflist: list):
        return f'Definition({self.left.pattern(wfflist)}, {self.right.pattern(wfflist)})'
    
    def makeschemafromlist(self, wfflist: list):
        return f'Definition({self.left.makeschemafromlist(wfflist)}, {self.right.makeschemafromlist(wfflist)})'
    
    def treetuple(self):
        return f'{self.left.treetuple()} {self.connector} {self.right.treetuple()}'
        
    def getvalue(self):
        return None 
    
    def setvalue(self):
        self.booleanvalue = None

    # def getmultivalue(self):
    #     return self.multivalue

class ConclusionPremises(Wff):
    """A premises and conclusion pairing of Wff objects."""

    is_variable = True
    booleanvalue = None
    multivalue = None
    lb = '{'
    latexlb = '\\{'
    rb = '}'
    latexrb = '\\}'
    tree_connector = ' ⊢ '

    def __init__(self, 
                 conclusion: Wff, 
                 premises: list = [], 
                 connector: str = ' ⊢ ', 
                 derivedconnector: str = ' ⊢ ', 
                 latexconnector: str = '~\\vdash~',
                 derivedlatexconnector: str = '\\vdash '):
        self.conclusion = conclusion
        self.premises = premises
        self.connector = connector
        self.latexconnector = latexconnector
        self.derivedconnector = derivedconnector
        self.derivedlatexconnector = derivedlatexconnector
        #self.multivalue = (True)

    def __str__(self):
        if len(self.premises) > 0:
            prem = str(self.premises[0])
            for i in range(len(self.premises)):
                if i > 0:
                    prem += ''.join([', ', str(self.premises[i])])
            return f'{self.lb}{prem}{self.rb} {self.derivedconnector} {self.conclusion}'
        else:
            return f'{self.derivedconnector} {str(self.conclusion)}'
    
    def latex(self):
        if len(self.premises) > 0:
            prem = self.premises[0].latex()
            for i in range(len(self.premises)):
                if i > 0:
                    prem += ''.join([',~', self.premises[i].latex()])
            return f'{self.latexlb}{prem}{self.latexrb} {self.latexconnector} {self.conclusion.latex()}'
        else:
            return f'{self.latexconnector} {self.conclusion.latex()}'
        
    def latexderived(self):
        if len(self.premises) > 0:
            prem = self.premises[0].latex()
            for i in range(len(self.premises)):
                if i > 0:
                    prem += ''.join([', ', self.premises[i].latex()])
            return f'{self.lb}{prem}{self.rb} {self.derivedlatexconnector} {self.conclusion.latex()}'
        else:
            return f'{self.derivedlatexconnector} {self.conclusion.latex()}'
    
    def tree(self):
        if len(self.premises) > 0:
            prem = ''.join(['[', self.premises[0].tree()])
            for i in range(len(self.premises)):
                if i > 0:
                    prem += ''.join([', ', self.premises[i].tree()])
            prem += ']'
        else: 
            prem = '[]'
        return f'{self.lb}{prem}{self.rb} {self.tree_connector} {self.conclusion.tree()}'
    
    def pattern(self, wfflist: list):
        if len(self.premises) > 0:
            prem = ''.join(['[', self.premises[0].pattern(wfflist)])
            for i in range(len(self.premises)):
                if i > 0:
                    prem += ''.join([', ', self.premises[i].pattern(wfflist)])
            prem += ']'
        else:
            prem = '[]'
        return f'ConclusionPremises({self.conclusion.pattern(wfflist)}, {prem})'
    
    def treetuple(self):
        if len(self.premises) > 0:
            prem = self.premises[0].treetuple()
            for i in range(len(self.premises)):
                if i > 0:
                    prem += ''.join([', ', self.premises[i].treetuple()])
            return f'{self.lb}{prem}{self.rb} {self.latexconnector} {self.conclusion.treetuple()}'
        else:
            return f'{self.latexconnector} {self.conclusion.treetuple()}'
        
    def getvalue(self):
        return None 
    
    def setvalue(self):
        self.booleanvalue = None

    # def getmultivalue(self):
    #     return self.multivalue



