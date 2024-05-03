"""------------------------------------------------------------------------------
                                    REITERATE
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.rules import Proof
A = Wff('A')
B = Wff('B')
C = Wff('C')
D = Wff('D')
E = Wff('E')
t = Proof()

"""------------------------------------------------------------------------------
                                Clean Run
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(prf.lines)', 4),
    ('len(prf.log)', 5),
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
                               stopped_linescope
------------------------------------------------------------------------------"""

# The line is not accessible.
testdata = [
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.reiterate_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_linescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_linescope_1(input_n, expected):
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
                        
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                        
------------------------------------------------------------------------------"""
    