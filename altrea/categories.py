# categories.py
"""This module contains the classes for categorical propositions."""

from altrea.terms import Term


class Categorical:
    """Parent class for categories."""

    quantifier_all = "All "
    quantifier_some = "Some "
    quantifier_no = "No "
    copula_are = " are "
    copula_arenot = " are not "
    quality_affirmative = "Affirmative"
    quality_negative = "Negative"
    quantity_universal = "Universal"
    quantity_particular = "Particular"
    letter_a = "A"
    letter_e = "E"
    letter_i = "I"
    letter_o = "O"
    distributed = "Distributed"
    undistributed = "Undistributed"

    def __init__(self):
        self.subjectterm = None
        self.predicateterm = None
        self.quantifier = ""
        self.copula = ""

    def __str__(self):
        return "".join(
            [
                self.quantifier,
                str(self.subjectterm),
                self.copula,
                str(self.predicateterm),
                ".",
            ]
        )


class All(Categorical):
    """A class for the categorical proposition 'All S are P'."""

    def __init__(self, subjectterm: Term, predicateterm: Term):
        self.subjectterm = subjectterm
        self.predicateterm = predicateterm
        self.quantifier = self.quantifier_all
        self.copula = self.copula_are
        self.quality = self.quality_affirmative
        self.quantity = self.quantity_universal
        self.letter = self.letter_a
        self.subjectterm.distributed = self.distributed
        self.predicateterm.distributed = self.undistributed


class Some(Categorical):
    """A class for the categorical proposition 'Some S are P'."""

    def __init__(self, subjectterm: Term, predicateterm: Term):
        self.subjectterm = subjectterm
        self.predicateterm = predicateterm
        self.quantifier = self.quantifier_some
        self.copula = self.copula_are
        self.quality = self.quality_affirmative
        self.quantity = self.quantity_particular
        self.letter = self.letter_i
        self.subjectterm.distributed = self.undistributed
        self.predicateterm.distributed = self.undistributed

    # def __str__(self):
    #     return ''.join([self.quantifier, self.subjectterm, self.copula, self.predicateterm, '.'])


class No(Categorical):
    """A class for the categorical proposition 'No S are P'."""

    def __init__(self, subjectterm: Term, predicateterm: Term):
        self.subjectterm = subjectterm
        self.predicateterm = predicateterm
        self.quantifier = self.quantifier_no
        self.copula = self.copula_are
        self.quality = self.quality_negative
        self.quantity = self.quantity_universal
        self.letter = self.letter_e
        self.subjectterm.distributed = self.distributed
        self.predicateterm.distributed = self.distributed


class SomeNot(Categorical):
    """A class for the categorical proposition 'Some S are P'."""

    def __init__(self, subjectterm: Term, predicateterm: Term):
        self.subjectterm = subjectterm
        self.predicateterm = predicateterm
        self.quantifier = self.quantifier_some
        self.copula = self.copula_arenot
        self.quality = self.quality_negative
        self.quantity = self.quantity_particular
        self.letter = self.letter_i
        self.subjectterm.distributed = self.undistributed
        self.predicateterm.distributed = self.distributed
