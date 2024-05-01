"""------------------------------------------------------------------------------
                                Add Goal Testing
                                    goal
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                 goal
                                Clean Run
------------------------------------------------------------------------------"""

# Clean run with no comments
testdata = [
    ("str(p.lines[0][p.statementindex])", str(A)),
    ("(p.lines[0][p.levelindex])", 0),
    ("(p.lines[0][p.proofidindex])", 0),
    ("(p.lines[0][p.ruleindex])", t.goal_name),
    ("(p.lines[0][p.linesindex])", ""),
    ("(p.lines[0][p.proofsindex])", ""),
    ("(p.lines[0][p.commentindex])", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_goal_clean_1(input_n, expected):
    A = Wff('A')
    p = Proof()
    p.setlogic('C')
    p.goal(A)
    assert eval(input_n) == expected

# Clean run with comments and two goals
testdata = [
    ("str(p.lines[0][p.statementindex])", str(A)+', '+str(B)),
    ("(p.lines[0][p.levelindex])", 0),
    ("(p.lines[0][p.proofidindex])", 0),
    ("(p.lines[0][p.ruleindex])", t.goal_name),
    ("(p.lines[0][p.linesindex])", ""),
    ("(p.lines[0][p.proofsindex])", ""),
    ("(p.lines[0][p.commentindex])", "My first goal - My second goal"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_goal_clean_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(A, 'My first goal')
    p.goal(B, 'My second goal')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    goal
                                  Stopped Run
                                  
                        Input Is A String (stopped_string)
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[0][p.statementindex])", ""),
    ("p.lines[0][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_goal_string_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.setlogic('C')
    p.goal('C')
    assert eval(input_n) == expected

# Proof should not continue after it has stopped
testdata = [
    ("len(p.lines)", 1),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_goal_string_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.setlogic('C')
    p.goal('C')
    p.premise(A)
    assert eval(input_n) == expected
        