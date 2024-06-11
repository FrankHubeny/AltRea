"""This module contains procedure to assist with using the MetaMath logic system."""


class Symbol:
    """Construct a symbol."""

    def __init__(self, name: str, latexname: str = ''):
        self.name = name
        if latexname == '':
            self.latexname = self.name
        else:
            self.latexname = latexname

    def __str__(self):
        return self.name
    
    def latex(self):
        return self.latexname

class Term:
    """Construct a MetaMath term."""

    def __init__(self, name: str, term: list):
        for i in term:
            if type(i) != Symbol:
                raise ValueError(f'The string "{i}" in the term "{term}" is not a Symbol.')
        self.name = name
        self.term = term
        self.value = ''.join([str(i) for i in self.term])
        self.latexvalue = ''.join([i.latex() for i in self.term])
        
    def __str__(self):
        return self.value
    
    def latex(self):
        return self.latexvalue
    
class Constant(Symbol):
    """Construct a MetaMath constant."""

    def __init__(self, name: str, latexname: str = ''):
        self.name = name
        self.latexname = latexname

    # def __str__(self):
    #     return self.name
    
    # def latex(self):
    #     return self.latexname
    
class Variable(Symbol):
    """Construct MetaMath variable."""

    def __init__(self, name: str, latexname: str = ''):
        self.name = name
        self.latexname = latexname

    # def __str__(self):
    #     return self.name
    
    # def latex(self):
    #     return self.latexname
    
class Disjoint(Symbol):
    """Construct MetaMath disjoint variable."""

    def __init__(self, name: str, latexname: str = ''):
        self.name = name
        self.latexname = latexname

    # def __str__(self):
    #     return self.name
    
    # def latex(self):
    #     return self.latexname
    
class Wff:
    """The MetaMath well-formed formula class."""

    def __init__(self, label: str, assertion: str):
        self.label = label
        self.assertion = assertion

    def __str__(self):
        return self.label
    
    def latex(self):
        return self.assertion.latex()
    
class Assertion(Wff):
    """Construct a MetaMath assertion."""

    def __init__(self, label: str, assertion: list, premises: list = []):
        self.label = label
        self.assertion = assertion
        self.premises = premises
        self.value = ''.join([str(i) for i in self.assertion])
        self.latexvalue = ''.join([i.latex() for i in self.assertion])

    def __str__(self):
        return self.value
    
    def latex(self):
        return self.latexvalue
    
class FloatingHypothesis(Wff):
    """Construct a MetaMath assertion."""

    def __init__(self, label: str, assertion: str):
        self.label = label
        self.assertion = assertion

    # def __str__(self):
    #     return self.hypothesis
    
    # def latex(self):
    #     return self.hypothesis
    
class EssentialHypothesis(Wff):
    """Construct a MetaMath assertion."""

    def __init__(self, label: str, assertion: str):
        self.name = label
        self.assertion = assertion

    # def __str__(self):
    #     return self.hypothesis
    
    # def latex(self):
    #     return self.hypothesis
    
class Proof:
    """Construct a MetaMath assertion."""

    def __init__(self, label: str, provedstatement: str, prooflines: list):
        self.label = label
        self.provedstatement = provedstatement
        self.prooflines = prooflines

    def __str__(self):
        return self.label
    
    def latex(self):
        return self.label