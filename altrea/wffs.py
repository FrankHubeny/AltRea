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

    default_and_connector = '&'
    default_and_latexconnector = '\\wedge'
    and_treeconnector = 'And'
    default_iff_connector = '<>'
    default_iff_latexconnector = '\\leftrightarrow'
    iff_treeconnector = 'Iff'
    default_implies_connector = '>'
    default_implies_latexconnector = '\\to'
    implies_treeconnector = 'Implies'
    default_necessary_connector = 'Nec'
    default_necessary_latexconnector = '\\Box'
    necessary_treeconnector = 'N'
    default_not_connector = '~'
    default_not_latexconnector = '\\lnot '
    not_treeconnector = 'Not'
    default_or_connector = '|'
    default_or_latexconnector = '\\vee'
    or_treeconnector = 'Or'
    possibly_connector = 'Pos'
    possibly_latexconnector = '\\Diamond'
    possible_treeconnector = 'P'
    wff_treeconnector = 'Wff'
    reserved_names = ['And', 'Or', 'Not', 'Implies', 'Iff', 'Wff', 'Falsehood', 'Truth', 'Proposition']

    f_name = 'Falsehood'
    f_latexname = '\\bot'
    falsehood_treeconnector = 'Falsehood'
    t_name = 'Truth'
    t_latexname = '\\top'

    
    def __init__(self, name: str, latexname: str = '', kind: str = 'Proposition'):
        if name in self.reserved_names or latexname in self.reserved_names:
            raise ValueError(f'The name "{name}" or the latexname "{latexname}" is in the list of reserved words: {self.reserved_names} which cannot be used.')
        elif name == '':
            raise ValueError(f'The name "{name}" is the empty string which cannot be used as a name.')
        elif type(name) != str or type(latexname) != str:
            raise TypeError(f' The name "{str(name)}" or the latexname "{str(latexname)}" was not a string.')
        else:
            self.name = name
            self.latexname = latexname
            self.booleanvalue = None
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

class And(Wff):
    """A well formed formula with two arguments which are also well formed formulas connected
    by logical and.
    """

    is_variable = False

    def __init__(self, left: Wff, right: Wff, and_connector: str = '&', and_latexconnector: str = '\\wedge'):
        self.left = left
        self.right = right
        self.and_connector = and_connector
        self.and_latexconnector = and_latexconnector
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
    
    def pattern(self, wfflist: list):
        return f'{self.and_treeconnector}{self.lb}{self.left.pattern(wfflist)}, {self.right.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.and_treeconnector}{self.lb}{self.left.makeschemafromlist(wfflist)}, {self.right.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.and_treeconnector, self.lb, self.left.treetuple(), ',', self.right.treetuple(), self.rb
        
    def getvalue(self):
        return self.left.getvalue() and self.right.getvalue()

class Falsehood(Wff):
    """This well formed formula is the result of a contradiction in a proof which may be useful for explosions.
    """

    is_variable = True
    booleanvalue = False

    def __init__(self, wff: Wff):
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


    def __str__(self):
        return f'{self.f_name}{self.lb}{self.wff}{self.rb}'
    
    def latex(self):
        return f'{self.f_latexname}{self.lb}{self.wff.latex()}{self.rb}'
    
    def tree(self):
        return f'{self.falsehood_treeconnector}{self.lb}{self.wff.tree()}{self.rb}'
    
    def pattern(self, wfflist: list):
        return f'{self.falsehood_treeconnector}{self.lb}{self.wff.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.falsehood_treeconnector}{self.lb}{self.wff.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.falsehood_treeconnector, self.lb, self.wff.treetuple(), self.rb
    
    def getvalue(self):
        return self.booleanvalue
    
    def setvalue(self, value: bool = False):
        self.booleanvalue = False

class Iff(Wff):
    """A well formed formula with two arguments which are also well formed formulas
    joined by if and only if.
    """

    is_variable = False

    def __init__(self, left: Wff, right: Wff, iff_connector: str = '<>', iff_latexconnector: str = '\\equiv '):
        self.left = left
        self.right = right
        self.iff_connector = iff_connector
        self.iff_latexconnector = iff_latexconnector
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
    
    def pattern(self, wfflist: list):
        return f'{self.iff_treeconnector}{self.lb}{self.left.pattern(wfflist)}, {self.right.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.iff_treeconnector}{self.lb}{self.left.makeschemafromlist(wfflist)}, {self.right.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.iff_treeconnector, self.lb, self.left.treetuple(), ',', self.right.treetuple(), self.rb

class Implies(Wff):
    """A well formed formula with two arguments which are also well formed formulas joined
    by implies.  The antecedent is the first of the two arguments.  The consequent is the
    second.
    """

    is_variable = False

    def __init__(self, left: Wff, right: Wff, implies_connector: str = '>', implies_latexconnector: str = '\\supset '):
        self.left = left
        self.right = right
        self.implies_connector = implies_connector
        self.implies_latexconnector = implies_latexconnector
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
    
    def pattern(self, wfflist: list):
        return f'{self.implies_treeconnector}{self.lb}{self.left.pattern(wfflist)}, {self.right.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.implies_treeconnector}{self.lb}{self.left.makeschemafromlist(wfflist)}, {self.right.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.implies_treeconnector, self.lb, self.left.treetuple(), ',', self.right.treetuple(), self.rb
        
    def getvalue(self):
        return (not self.left.getvalue()) or self.right.getvalue()

class Necessary(Wff):
    """A well-formed formula which is necessarily true."""

    is_variable = True

    def __init__(self, wff, necessary_connector: str = 'Nec', necessary_latexconnector: str = '\\Box'):
        self.truefalse = wff
        self.necessary_connector = necessary_connector
        self.necessary_latexconnector = necessary_latexconnector

    def __str__(self):
        if self.is_variable:
            return f'{self.necessary_connector} {self.truefalse}'
        else:
            return f'{self.necessary_connector}{self.lb}{self.truefalse}{self.rb}'
    
    def latex(self):
        if self.is_variable:
            return f'{self.necessary_latexconnector} {self.truefalse}'
        else:
            return f'{self.necessary_latexconnector} {self.lb}{self.truefalse}{self.rb}'
        
    def tree(self):
        return f'{self.necessary_treeconnector}{self.lb}{self.truefalse.tree()}{self.rb}'
    
    def pattern(self, wfflist: list):
        return f'{self.necessary_treeconnector}{self.lb}{self.truefalse.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.necessary_treeconnector}{self.lb}{self.truefalse.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.necessary_treeconnector, self.lb, self.truefalse.treetuple(), self.rb
    
    def getvalue(self):
        return True
    
class Not(Wff):
    """A well formed formula with one argument which is also a well formed formula joined
    with logical not.
    """

    is_variable = True

    def __init__(self, negated: Wff, not_connector: str = '~', not_latexconnector: str = '\\lnot '):
        self.negated = negated
        self.booleanvalue = None
        self.not_connector = not_connector
        self.not_latexconnector = not_latexconnector      

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
    
    def pattern(self, wfflist: list):
        return f'{self.not_treeconnector}{self.lb}{self.negated.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.not_treeconnector}{self.lb}{self.negated.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.not_treeconnector, self.lb, self.negated.treetuple(), self.rb
    
    def getvalue(self):
        return not self.negated.getvalue()

class Or(Wff):
    """A well formed formula with two arguments which are also well formed formulas connected
    by logical or.
    """

    is_variable = False

    def __init__(self, left: Wff, right: Wff, or_connector: str = '|', or_latexconnector: str = '\\vee'):
        self.left = left
        self.right = right
        self.or_connector = or_connector
        self.or_latexconnector = or_latexconnector
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
    
    def pattern(self, wfflist: list):
        return f'{self.or_treeconnector}{self.lb}{self.left.pattern(wfflist)}, {self.right.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.or_treeconnector}{self.lb}{self.left.makeschemafromlist(wfflist)}, {self.right.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.or_treeconnector, self.lb, self.left.treetuple(), ',', self.right.treetuple(), self.rb
        
    def getvalue(self):
        return self.left.getvalue() or self.right.getvalue()

class Possibly(Wff):
    """A well-formed formula which is possibly true."""

    is_variable = True

    def __init__(self, wff, possibly_connector: str = 'Pos', possibly_latexconnector: str = '\\Diamond'):
        self.truefalse = wff
        self.possibly_connector = possibly_connector
        self.possibly_latexconnector = possibly_latexconnector

    def __str__(self):
        if self.is_variable:
            return f'{self.possibly_connector} {self.truefalse}'
        else:
            return f'{self.possibly_connector}{self.lb}{self.truefalse}{self.rb}'
    
    def latex(self):
        if self.is_variable:
            return f'{self.possibly_latexconnector} {self.truefalse}'
        else:
            return f'{self.possibly_latexconnector} {self.lb}{self.truefalse}{self.rb}'
        
    def tree(self):
        return f'{self.possible_treeconnector}{self.lb}{self.truefalse.tree()}{self.rb}'
    
    def pattern(self, wfflist):
        return f'{self.possible_treeconnector}{self.lb}{self.truefalse.pattern(wfflist)}{self.rb}'
    
    def makeschemafromlist(self, wfflist: list):
        return f'{self.possible_treeconnector}{self.lb}{self.truefalse.makeschemafromlist(wfflist)}{self.rb}'
    
    def treetuple(self):
        return self.possible_treeconnector, self.lb, self.truefalse.treetuple(), self.rb
    
    def getvalue(self):
        return True
    
class Truth(Wff):
    """A well formed formula which is always true."""

    is_variable = True
    booleanvalue = True

    def __init__(self, name: str = '', latexname: str = ''):
        if name in self.reserved_names or latexname in self.reserved_names:
            raise ValueError(f'The name "{name}" or the latexname "{latexname}" is in the list of reserved words: {self.reserved_names} which cannot be used.')
        elif name == '':
            raise ValueError(f'The name "{name}" is the empty string which cannot be used as a name.')
        elif type(name) != str or type(latexname) != str:
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
    booleanvalue = True

    def __init__(self, name: str, latexname: str = '', kind: str = 'Proposition'):
        if name in self.reserved_names or latexname in self.reserved_names:
            raise ValueError(f'The name "{name}" or the latexname "{latexname}" is in the list of reserved words: {self.reserved_names} which cannot be used.')
        elif name == '':
            raise ValueError(f'The name "{name}" is the empty string which cannot be used as a name.')
        elif type(name) != str or type(latexname) != str:
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

class Axiom(Wff):
    """This class holds axioms of the logical system."""

    is_variable = True
    booleanvalue = True

    def __init__(self, schema: Wff):
        self.schema = schema

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

class Definition(Wff):
    """This class defines one wff expression to be the same as the other."""

    is_variable = True
    booleanvalue = None
    lb = '('
    rb = ')'
    tree_connector = '|='

    def __init__(self, left: Wff, right: Wff, connector: str = '=', latexconnector: str = '\\equiv '):
        self.left = left
        self.right = right
        self.connector = connector
        self.latexconnector = latexconnector

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

class ConclusionPremises(Wff):
    """A premises and conclusion pairing of Wff objects."""

    is_variable = True
    booleanvalue = None
    lb = '{'
    rb = '}'
    tree_connector = '|-'

    def __init__(self, 
                 conclusion: Wff, 
                 premises: list = [], 
                 connector: str = '|=', 
                 derivedconnector: str = '|-', 
                 latexconnector: str = '\\models ',
                 derivedlatexconnector: str = '\\vdash '):
        self.conclusion = conclusion
        self.premises = premises
        self.connector = connector
        self.latexconnector = latexconnector
        self.derivedconnector = derivedconnector
        self.derivedlatexconnector = derivedlatexconnector

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
                    prem += ''.join([', ', self.premises[i].latex()])
            return f'{self.lb}{prem}{self.rb} {self.latexconnector} {self.conclusion.latex()}'
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