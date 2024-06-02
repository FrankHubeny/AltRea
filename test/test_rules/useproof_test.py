"""------------------------------------------------------------------------------
                                USEPROOF
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

# Clean test of contradiction and explosion

testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[1][prf.statementindex])", str(And(C, Not(C)))),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", 'Contradiction'),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    ("prf.lines[1][prf.typeindex]", t.linetype_axiom),
    #
    ("str(prf.lines[4][prf.statementindex])", str(B)),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", 'Explosion'),
    ("prf.lines[4][prf.linesindex]", "2, 3"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.complete),
    ("prf.lines[4][prf.typeindex]", t.linetype_axiom),
    #
]
@pytest.mark.parametrize("input_n,expected", testdata)
def _useproof_contradiction_explosion_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic()
    prf.goal(B)
    prf.axiom('contradiction', [C])
    prf.conjunction_elim(1, prf.left)
    prf.conjunction_elim(1, prf.right)
    prf.axiom('explosion', [C, B], [2, 3])
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_nosuchsavedproof
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_premisesdontmatch
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_nosubs
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_notwff
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_notinteger
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_nosuchline
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_linescope
------------------------------------------------------------------------------"""

