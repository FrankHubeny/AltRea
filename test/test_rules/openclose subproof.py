"""------------------------------------------------------------------------------
                            OPENSUBPROOF CLOSESUBPROOF
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import Necessary, Implies, And
from altrea.rules import Proof

t = Proof()
A = t.proposition("A")
B = t.proposition("B")
C = t.proposition("C")
D = t.proposition("D")
E = t.proposition("E")

"""------------------------------------------------------------------------------
                                Clean Run 1
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[1][prf.statementindex])", str(A)),
    ("prf.lines[1][prf.levelindex]", 1),
    ("prf.lines[1][prf.proofidindex]", 1),
    ("prf.lines[1][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Implies(A, A))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", "1-1"),
    ("prf.lines[2][prf.commentindex]", ""),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_openclosesubproof_clean_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    
    prf.goal(B)
    
    prf.opensubproof()
    prf.hypothesis(A)
    prf.closesubproof()
    prf.implication_intro()

    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                Clean Run 2
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 5),
    #
    ("str(prf.lines[1][prf.statementindex])", str(A)),
    ("prf.lines[1][prf.levelindex]", 1),
    ("prf.lines[1][prf.proofidindex]", 1),
    ("prf.lines[1][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(B)),
    ("prf.lines[2][prf.levelindex]", 2),
    ("prf.lines[2][prf.proofidindex]", 2),
    ("prf.lines[2][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", "1-1"),
    ("prf.lines[2][prf.commentindex]", ""),
    #
    ("str(prf.lines[3][prf.statementindex])", str(Implies(B, B))),
    ("prf.lines[3][prf.levelindex]", 1),
    ("prf.lines[3][prf.proofidindex]", 1),
    ("prf.lines[3][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", "2-2"),
    ("prf.lines[3][prf.commentindex]", ""),
    #
    ("str(prf.lines[3][prf.statementindex])", str(Implies(A, Implies(B, B)))),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", "1-3"),
    ("prf.lines[3][prf.commentindex]", ""),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_openclosesubproof_clean_2(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    
    prf.goal(B)
    
    prf.opensubproof()
    prf.hypothesis(A)
    prf.opensubproof()
    prf.hypothesis(B)
    prf.closesubproof()
    prf.implication_intro()
    prf.closesubproof()
    prf.implication_intro()

    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                stopped_unavailablesubproof
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 1),
    ("prf.lines[1][prf.proofidindex]", 1),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_unavailablesubproof),
    ("prf.lines[2][prf.typeindex]", t.linetype_premise),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_openclosesubproof_unavailablesubproof_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    
    prf.goal(B)
    
    prf.opensubproof()
    prf.premise(A)

    assert eval(input_n) == expected

