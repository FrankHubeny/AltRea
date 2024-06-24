"""------------------------------------------------------------------------------
                                DISJUNCTION_INTRO
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import Or
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
    ("str(prf.lines[1][prf.statementindex])", str(A)),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Or(A, B))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    #("prf.lines[2][prf.ruleindex]", t.disjunction_intro_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.complete),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_disjunction_intro_clean_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(Or(A, B))
    prf.premise(A)
    prf.rule("disj intro r", [A, B], [1])
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                Clean Run 2
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[1][prf.statementindex])", str(B)),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Or(A, B))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    #("prf.lines[2][prf.ruleindex]", t.disjunction_intro_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.complete),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_disjunction_intro_clean_2(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(Or(A, B))
    prf.premise(B)
    prf.rule("disj intro l", [B, A], [1])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                stopped_notwff
------------------------------------------------------------------------------"""

# Stop if the left input value is a string.
testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    #("prf.lines[2][prf.ruleindex]", t.disjunction_intro_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    (
        "prf.lines[2][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_notwff,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_disjunction_intro_notwff_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(Or(A, B))
    prf.premise(B)
    prf.rule("disj intro l", ["A", B], [1])
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_nosuchline
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    #("prf.lines[2][prf.ruleindex]", t.disjunction_intro_name),
    ("prf.lines[2][prf.linesindex]", "-2"),
    ("prf.lines[2][prf.proofsindex]", ""),
    (
        "prf.lines[2][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_nosuchline,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_disjunction_intro_nosuchline_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(Or(A, B))
    prf.premise(A)
    prf.rule("disj intro r", [A, B], [-2])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                               stopped_linescope
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    #("prf.lines[3][prf.ruleindex]", t.disjunction_intro_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_linescope,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_disjunction_intro_linescope_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    
    prf.goal(Or(A, B))
    
    prf.opensubproof()
    prf.hypothesis(A)
    prf.implication_intro()
    prf.rule("disj intro r", [A, B], [1])

    assert eval(input_n) == expected



