"""------------------------------------------------------------------------------
                                    NECESSARY_ELIM
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import Necessary
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

testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[1][prf.statementindex])", str(Necessary(A))),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(A)),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.necessary_elim_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.complete),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_necessary_elim_clean_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    prf.setlogic()
    prf.goal(A)
    prf.premise(Necessary(A))
    prf.necessary_elim(1)
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Stopped
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
def test_necessary_elim_ruleclass_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    prf.proofrules = prf.rule_axiomatic
    prf.setlogic()
    prf.goal(A)
    prf.premise(Necessary(A))
    prf.necessary_elim(1)
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Stopped
                                stopped_notnecessary
------------------------------------------------------------------------------"""

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
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.necessary_elim_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    (
        "prf.lines[2][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_notnecessary,
    ),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_necessary_elim_notnecessary_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(A)
    prf.premise(B)
    prf.necessary_elim(1)
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Stopped
                                stopped_nosuchline
------------------------------------------------------------------------------"""

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
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.necessary_elim_name),
    ("prf.lines[2][prf.linesindex]", "2"),
    ("prf.lines[2][prf.proofsindex]", ""),
    (
        "prf.lines[2][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_nosuchline,
    ),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_necessary_elim_nosuchline_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(A)
    prf.premise(B)
    prf.necessary_elim(2)
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Stopped
                                stopped_linescope
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.necessary_elim_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_linescope,
    ),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_necessary_elim_linescope_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(A)
    prf.hypothesis(Necessary(B))
    prf.implication_intro()
    prf.necessary_elim(1)
    assert eval(input_n) == expected
