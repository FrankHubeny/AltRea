"""------------------------------------------------------------------------------
                                    REITERATE
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, Proposition, Falsehood, Truth
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

# Clean test
testdata = [
    ('len(prf.lines)', 4),
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
    A = Wff('A')
    prf.setlogic('C')
    prf.goal(Not(Not(A)))
    prf.premise(A)
    prf.hypothesis(Not(A))
    prf.reiterate(1)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
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
    ("prf.lines[3][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_nosuchline_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    prf.setlogic('C')
    prf.goal(Not(Not(A)))
    prf.premise(A)
    prf.hypothesis(Not(A))
    prf.reiterate(10)
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
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
    ("prf.lines[3][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_notreiteratescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_notreiteratescope_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    prf.setlogic('C')
    prf.goal(Not(Not(A)))
    prf.hypothesis(A)
    prf.implication_intro()
    prf.reiterate(1)
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
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
    ("prf.lines[2][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_notreiteratescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_notreiteratescope_2(input_n, expected):
    prf = Proof()
    A = Wff('A')
    prf.setlogic('C')
    prf.goal(Not(Not(A)))
    prf.hypothesis(A)
    prf.reiterate(1)
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
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
    ("prf.lines[2][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_notreiteratescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_notreiteratescope_3(input_n, expected):
    prf = Proof()
    A = Wff('A')
    prf.setlogic('C')
    prf.goal(Not(Not(A)))
    prf.premise(A)
    prf.reiterate(1)
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
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
    ("prf.lines[5][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_notreiteratescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_notreiteratescope_4(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    prf.goal(Not(Not(A)))
    prf.hypothesis(A)
    prf.hypothesis(B)
    prf.implication_intro()
    prf.hypothesis(C)
    prf.reiterate(2)
    assert eval(input_n) == expected

