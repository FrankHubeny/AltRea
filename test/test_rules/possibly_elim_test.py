"""------------------------------------------------------------------------------
                                    POSSIBLY_ELIM
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import Wff, Not, And, Or, Implies, Iff, Proposition, Falsehood, Truth, Necessary
from altrea.rules import Proof
t = Proof()
A = t.proposition('A')
B = t.proposition('B')
C = t.proposition('C')
D = t.proposition('D')
E = t.proposition('E')

"""------------------------------------------------------------------------------
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[1][prf.statementindex])", str(Necessary(A))),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Necessary(A))),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.reiterate_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
]
@pytest.mark.parametrize("input_n,expected", testdata)
def _possibly_elim_clean_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic()
    prf.goal(B)
    prf.premise(Necessary(A))
    prf.startstrictsubproof(1)
    assert eval(input_n) == expected