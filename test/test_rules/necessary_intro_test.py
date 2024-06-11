"""------------------------------------------------------------------------------
                                    NECESSARY_INTRO
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
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Necessary(A))),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.reiterate_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
    ("str(prf.lines[3][prf.statementindex])", str(Necessary(Necessary(A)))),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.necessary_intro_name),
    ("prf.lines[3][prf.linesindex]", "2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", ""),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_necessary_intro_clean_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    prf.setlogic()
    prf.goal(A)
    prf.premise(Necessary(A))
    prf.startstrictsubproof(1)
    prf.necessary_intro([2])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Clean Run (two lines)
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 6),
    #
    ("str(prf.lines[4][prf.statementindex])", str(Necessary(Necessary(A)))),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.necessary_intro_name),
    ("prf.lines[4][prf.linesindex]", "2"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", ""),
    #
    ("str(prf.lines[5][prf.statementindex])", str(Necessary(A))),
    ("prf.lines[5][prf.levelindex]", 0),
    ("prf.lines[5][prf.proofidindex]", 0),
    ("prf.lines[5][prf.ruleindex]", t.necessary_intro_name),
    ("prf.lines[5][prf.linesindex]", "3"),
    ("prf.lines[5][prf.proofsindex]", ""),
    ("prf.lines[5][prf.commentindex]", ""),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_necessary_intro_clean_2(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    prf.setlogic()
    prf.goal(A)
    prf.premise(Necessary(A))
    prf.startstrictsubproof(1)
    prf.necessary_elim(2)
    prf.necessary_intro([2, 3])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Error: ruleclass
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 1),
    ("prf.lines[3][prf.proofidindex]", 1),
    ("prf.lines[3][prf.ruleindex]", t.necessary_intro_name),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_ruleclass,
    ),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_necessary_intro_ruleclass_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    prf.setlogic()
    prf.goal(A)
    prf.premise(Necessary(A))
    prf.startstrictsubproof(1)
    prf.proofrules = prf.rule_axiomatic
    prf.necessary_intro([2])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Error: nolines
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 1),
    ("prf.lines[3][prf.proofidindex]", 1),
    ("prf.lines[3][prf.ruleindex]", t.necessary_intro_name),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_nolines,
    ),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_necessary_intro_nolines_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    prf.setlogic()
    prf.goal(A)
    prf.premise(Necessary(A))
    prf.startstrictsubproof(1)
    prf.necessary_intro([])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Error: linescope
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 1),
    ("prf.lines[3][prf.proofidindex]", 1),
    ("prf.lines[3][prf.ruleindex]", t.necessary_intro_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_linescope,
    ),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_necessary_intro_linescope_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    prf.setlogic()
    prf.goal(A)
    prf.premise(Necessary(A))
    prf.startstrictsubproof(1)
    prf.necessary_intro([1])
    assert eval(input_n) == expected
