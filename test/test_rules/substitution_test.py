"""------------------------------------------------------------------------------
                                SUBSTITUTION
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import Wff, Not, And, Or, Implies, Iff, Proposition, Falsehood, Truth
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

# Clean test substituting one letter for another.

testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Not(B))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.substitution_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    ("prf.lines[2][prf.typeindex]", t.linetype_substitution),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_substitution_clean_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic()
    prf.goal(C)
    prf.premise(B)
    prf.substitution(1, [B], [Not(B)])
    assert eval(input_n) == expected