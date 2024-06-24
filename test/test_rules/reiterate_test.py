"""------------------------------------------------------------------------------
                                    REITERATE
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import Wff, Not, Necessary
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
    ("len(prf.lines)", 4),
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
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
    ("str(prf.lines[3][prf.statementindex])", str(A)),
    ("prf.lines[3][prf.levelindex]", 1),
    ("prf.lines[3][prf.proofidindex]", 1),
    ("prf.lines[3][prf.ruleindex]", t.reiterate_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", ""),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_clean_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    prf.setlogic()
    
    prf.goal(Not(Not(A)))
    prf.premise(A)
    
    prf.opensubproof()
    prf.hypothesis(Not(A))
    prf.reiterate(1)

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                              stopped_nosuchline
------------------------------------------------------------------------------"""

# The line does not exist in the proof.
testdata = [
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 1),
    ("prf.lines[3][prf.proofidindex]", 1),
    ("prf.lines[3][prf.ruleindex]", t.reiterate_name),
    ("prf.lines[3][prf.linesindex]", "10"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_nosuchline,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_nosuchline_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    prf.setlogic()
    
    prf.goal(Not(Not(A)))
    prf.premise(A)
    
    prf.opensubproof()
    prf.hypothesis(Not(A))
    prf.reiterate(10)

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                            stopped_notreiteratescope
------------------------------------------------------------------------------"""

# The line is not accessible.
testdata = [
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.reiterate_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_notreiteratescope,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_notreiteratescope_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    prf.setlogic()
    
    prf.goal(Not(Not(A)))
    
    prf.opensubproof()
    prf.hypothesis(A)
    prf.implication_intro()
    prf.reiterate(1)

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                           stopped_notreiteratescope
------------------------------------------------------------------------------"""

# The line is not accessible because it is already in the current proof.
testdata = [
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.reiterate_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    (
        "prf.lines[2][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_notreiteratescope,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_notreiteratescope_2(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    prf.setlogic()
    
    prf.goal(Not(Not(A)))
    
    prf.opensubproof()
    prf.hypothesis(A)
    prf.reiterate(1)

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                           stopped_notreiteratescope
------------------------------------------------------------------------------"""

# The line is not accessible because it is at the main proof level.  There is no previous proof to reiterate from.
testdata = [
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.reiterate_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    (
        "prf.lines[2][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_notreiteratescope,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_notreiteratescope_3(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    prf.setlogic()
    prf.goal(Not(Not(A)))
    prf.premise(A)
    prf.reiterate(1)
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                           stopped_notreiteratescope
------------------------------------------------------------------------------"""

# The line is not accessible because it is not in a proof from the previous proof chain.
testdata = [
    ("str(prf.lines[5][prf.statementindex])", t.blankstatement),
    ("prf.lines[5][prf.levelindex]", 2),
    ("prf.lines[5][prf.proofidindex]", 3),
    ("prf.lines[5][prf.ruleindex]", t.reiterate_name),
    ("prf.lines[5][prf.linesindex]", "2"),
    ("prf.lines[5][prf.proofsindex]", ""),
    (
        "prf.lines[5][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_notreiteratescope,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_notreiteratescope_4(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    B = prf.proposition("B")
    C = prf.proposition("C")
    prf.setlogic()
    
    prf.goal(Not(Not(A)))
    
    prf.opensubproof()
    prf.hypothesis(A)
    prf.opensubproof()
    prf.hypothesis(B)
    prf.implication_intro()
    prf.opensubproof()
    prf.hypothesis(C)
    prf.reiterate(2)

    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                           stopped_notnecessary
------------------------------------------------------------------------------"""

# The line is not accessible because it is not in a proof from the previous proof chain.
testdata = [
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    #("prf.lines[2][prf.ruleindex]", t.reiterate_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    (
        "prf.lines[2][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_notnecessary,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_strict_notreiteratescope_5(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    prf.setlogic()
    prf.goal(Not(Not(A)))
    prf.premise(A)
    prf.openstrictsubproof(1)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                           stopped_notnecessary
------------------------------------------------------------------------------"""

# The line is not accessible because it is not in a proof from the previous proof chain.
testdata = [
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 1),
    ("prf.lines[4][prf.proofidindex]", 1),
    ("prf.lines[4][prf.ruleindex]", t.reiterate_name),
    ("prf.lines[4][prf.linesindex]", "2"),
    ("prf.lines[4][prf.proofsindex]", ""),
    (
        "prf.lines[4][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_notnecessary,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_strict_notreiteratescope_6(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(Not(Not(A)))
    prf.premise(Necessary(A))
    prf.premise(B)
    prf.openstrictsubproof(1)
    prf.reiterate(2)
    assert eval(input_n) == expected
