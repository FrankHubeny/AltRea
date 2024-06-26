"""------------------------------------------------------------------------------
                                    PREMISE
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import Not, Possibly
from altrea.rules import Proof

t = Proof()
A = t.proposition("A")
B = t.proposition("B")
C = t.proposition("C")
D = t.proposition("D")
E = t.proposition("E")

"""------------------------------------------------------------------------------
                                   Clean Run
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[0][prf.statementindex])", str(Not(Not(A)))),
    ("prf.lines[0][prf.levelindex]", 0),
    ("prf.lines[0][prf.proofidindex]", 0),
    ("prf.lines[0][prf.ruleindex]", t.goal_name),
    ("prf.lines[0][prf.linesindex]", ""),
    ("prf.lines[0][prf.proofsindex]", ""),
    ("prf.lines[0][prf.commentindex]", ""),
    #
    ("str(prf.lines[1][prf.statementindex])", str(A)),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Not(A))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.contradicted),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_premise_clean_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    prf.setlogic()
    prf.goal(Not(Not(A)))
    prf.premise(A)
    prf.premise(Not(A))
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_notwff
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    (
        "prf.lines[1][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_notwff,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_premise_notwff_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    prf.setlogic()
    prf.goal(Not(Not(A)))
    prf.premise("A")
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                stopped_nogoal
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    (
        "prf.lines[1][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_nogoal,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_premise_nogoal_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    prf.setlogic()
    # prf.goal(Not(Not(A)))
    prf.premise(A)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                stopped_ruleclass
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    (
        "prf.lines[1][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_ruleclass,
    ),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_premise_ruleclass_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    prf.proofrules = prf.rule_axiomatic
    prf.setlogic()
    prf.goal(Possibly(A))
    prf.premise(A)
    prf.rule("pos intro", [A], [1])
    assert eval(input_n) == expected

