"""------------------------------------------------------------------------------
                                IMPLICATION_INTRO
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import And, Implies
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
# Clean test
testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[0][prf.statementindex])", str(Implies(A, A))),
    ("prf.lines[0][prf.levelindex]", 0),
    ("prf.lines[0][prf.proofidindex]", 0),
    ("prf.lines[0][prf.ruleindex]", t.goal_name),
    ("prf.lines[0][prf.linesindex]", ""),
    ("prf.lines[0][prf.proofsindex]", ""),
    ("prf.lines[0][prf.commentindex]", "Reflexivity of Implication"),
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
    ("prf.lines[2][prf.commentindex]", "COMPLETE"),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_intro_clean_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    prf.setlogic()
    
    prf.goal(Implies(A, A), comment="Reflexivity of Implication")
    
    prf.opensubproof()
    prf.hypothesis(A)
    prf.closesubproof()
    prf.implication_intro()

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Clean Run 2
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ("len(prf.lines)", 12),
    #
    ("str(prf.lines[9][prf.statementindex])", str(Implies(C, And(A, B)))),
    ("prf.lines[9][prf.levelindex]", 2),
    ("prf.lines[9][prf.proofidindex]", 2),
    ("prf.lines[9][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[9][prf.linesindex]", ""),
    ("prf.lines[9][prf.proofsindex]", "5-8"),
    ("prf.lines[9][prf.commentindex]", ""),
    #
    ("str(prf.lines[10][prf.statementindex])", str(Implies(D, Implies(C, And(A, B))))),
    ("prf.lines[10][prf.levelindex]", 1),
    ("prf.lines[10][prf.proofidindex]", 1),
    ("prf.lines[10][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[10][prf.linesindex]", ""),
    ("prf.lines[10][prf.proofsindex]", "4-9"),
    ("prf.lines[10][prf.commentindex]", ""),
    #
    (
        "str(prf.lines[11][prf.statementindex])",
        str(Implies(E, Implies(D, Implies(C, And(A, B))))),
    ),
    ("prf.lines[11][prf.levelindex]", 0),
    ("prf.lines[11][prf.proofidindex]", 0),
    ("prf.lines[11][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[11][prf.linesindex]", ""),
    ("prf.lines[11][prf.proofsindex]", "3-10"),
    ("prf.lines[11][prf.commentindex]", "COMPLETE"),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_intro_clean_2(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    B = prf.proposition("B")
    C = prf.proposition("C")
    D = prf.proposition("D")
    E = prf.proposition("E")
    prf.setlogic()
    
    prf.goal(Implies(E, Implies(D, Implies(C, And(A, B)))))
    prf.premise(A)
    prf.premise(B)
    
    prf.opensubproof()
    prf.hypothesis(E)
    prf.opensubproof()
    prf.hypothesis(D)
    prf.opensubproof()
    prf.hypothesis(C)
    prf.reiterate(1)
    prf.reiterate(2)
    prf.rule("conj intro", [A, B], [6, 7])
    prf.closesubproof()
    prf.implication_intro()
    prf.closesubproof()
    prf.implication_intro()
    prf.closesubproof()
    prf.implication_intro()

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Clean Run 3 
------------------------------------------------------------------------------"""

# Clean test: check that multiple hypotheses are included in the antecedent of the implication
testdata = [
    ("len(prf.lines)", 6),
    #
    ("str(prf.lines[3][prf.statementindex])", str(C)),
    ("prf.lines[3][prf.levelindex]", 1),
    ("prf.lines[3][prf.proofidindex]", 1),
    ("prf.lines[3][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", ""),
    #
    ("str(prf.lines[4][prf.statementindex])", str(And(B, A))),
    ("prf.lines[4][prf.levelindex]", 1),
    ("prf.lines[4][prf.proofidindex]", 1),
    #("prf.lines[4][prf.ruleindex]", t.conjunction_intro_name),
    ("prf.lines[4][prf.linesindex]", "1, 2"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", ""),
    #
    (
        "str(prf.lines[5][prf.statementindex])",
        str(Implies(And(And(B, A), C), And(B, A))),
    ),
    ("prf.lines[5][prf.levelindex]", 0),
    ("prf.lines[5][prf.proofidindex]", 0),
    ("prf.lines[5][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[5][prf.linesindex]", ""),
    ("prf.lines[5][prf.proofsindex]", "1-4"),
    ("prf.lines[5][prf.commentindex]", ""),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_intro_clean_3(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    B = prf.proposition("B")
    C = prf.proposition("C")
    prf.setlogic()
    
    prf.goal(Implies(A, A))
    
    prf.opensubproof()
    prf.hypothesis(B)
    prf.hypothesis(A)
    prf.hypothesis(C)
    prf.rule("conj intro", [B, A], [1, 2])
    prf.closesubproof()
    prf.implication_intro()

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Clean Run 1 Strict Subproof 
------------------------------------------------------------------------------"""
# Clean test
testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[0][prf.statementindex])", str(Implies(A, A))),
    ("prf.lines[0][prf.levelindex]", 0),
    ("prf.lines[0][prf.proofidindex]", 0),
    ("prf.lines[0][prf.ruleindex]", t.goal_name),
    ("prf.lines[0][prf.linesindex]", ""),
    ("prf.lines[0][prf.proofsindex]", ""),
    ("prf.lines[0][prf.commentindex]", "Strict Subproof"),
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
    #("prf.lines[2][prf.ruleindex]", t.implication_intro_strict_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", "1-1"),
    ("prf.lines[2][prf.commentindex]", "COMPLETE"),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_intro_strict_clean_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    prf.setlogic()
    
    prf.goal(Implies(A, A), comment="Strict Subproof")
    
    prf.openstrictsubproof()
    prf.hypothesis(A)
    
    prf.closestrictsubproof()
    prf.implication_intro()

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                              stopped_unavailablesubproof
------------------------------------------------------------------------------"""

# An attempt was made to close the main proof.  This can only be closed by completing the proof.
testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    (
        "prf.lines[2][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_unavailablesubproof,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_intro_unavailablesubproof_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    prf.setlogic()
    prf.goal(Implies(A, A))
    prf.premise(A)
    prf.implication_intro()
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected
