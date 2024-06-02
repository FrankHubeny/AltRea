"""------------------------------------------------------------------------------
                                PROPOSITION
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import Wff, Not, And, Or, Implies, Iff, Proposition, Falsehood, Truth
from altrea.rules import Proof
t = Proof()
A = t.proposition('A', '\\alpha ')
B = t.proposition('B', '\\textbf{\u05e9}')
主 = t.proposition('主')
samsonisgood = t.proposition('Samson is good', '\\textbf{Samson is good}')
"""------------------------------------------------------------------------------
                                Clean Run
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[1][prf.statementindex])", str(B)),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    ("prf.lines[1][prf.typeindex]", t.linetype_premise),
    #
    ("str(prf.lines[2][prf.statementindex])", str(主)),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    ("prf.lines[2][prf.typeindex]", t.linetype_premise),
    #
    ("str(prf.lines[3][prf.statementindex])", str(samsonisgood)),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.premise_name),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", ""),
    ("prf.lines[3][prf.typeindex]", t.linetype_premise),
    #
    ("str(prf.lines[4][prf.statementindex])", str(And(B, samsonisgood))),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.conjunction_intro_name),
    ("prf.lines[4][prf.linesindex]", "1, 3"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", ''),
    ("prf.lines[4][prf.typeindex]", t.linetype_transformationrule),
    #
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_proposition_clean_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A', '\\alpha ')
    B = prf.proposition('B', '\\textbf{\u05e9}')
    主 = prf.proposition('主')
    samsonisgood = prf.proposition('Samson is good', '\\textbf{Samson is good}')
    prf.setlogic()
    prf.goal(A)
    prf.premise(B)
    prf.premise(主)
    prf.premise(samsonisgood)
    prf.conjunction_intro(1,3)
    assert eval(input_n) == expected

