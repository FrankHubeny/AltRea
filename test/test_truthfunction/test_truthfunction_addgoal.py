"""------------------------------------------------------------------------------
                                Add Goal Testing
                                    addgoal
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                 ADDGOAL
                                Clean Run
------------------------------------------------------------------------------"""

# Clean run with no comments
testdata = [
    ("str(p.lines[0][p.statementindex])", str(A)),
    ("(p.lines[0][p.levelindex])", 0),
    ("(p.lines[0][p.blockidindex])", 0),
    ("(p.lines[0][p.ruleindex])", t.goalname),
    ("(p.lines[0][p.linesindex])", ""),
    ("(p.lines[0][p.blocksindex])", ""),
    ("(p.lines[0][p.commentindex])", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_addgoal_clean_1(input_n, expected):
    A = Wff('A')
    p = Proof()
    p.addgoal(A)
    assert eval(input_n) == expected

# Clean run with comments and two goals
testdata = [
    ("str(p.lines[0][p.statementindex])", str(A)+', '+str(B)),
    ("(p.lines[0][p.levelindex])", 0),
    ("(p.lines[0][p.blockidindex])", 0),
    ("(p.lines[0][p.ruleindex])", t.goalname),
    ("(p.lines[0][p.linesindex])", ""),
    ("(p.lines[0][p.blocksindex])", ""),
    ("(p.lines[0][p.commentindex])", "My first goal - My second goal"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_addgoal_clean_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A, 'My first goal')
    p.addgoal(B, 'My second goal')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    ADDGOAL
                                  Stopped Run
                                  
                        Input Is A String (stopped_string)
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[0][p.statementindex])", ""),
    ("p.lines[0][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_addgoal_string_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal('C')
    assert eval(input_n) == expected

# Proof should not continue after it has stopped
testdata = [
    ("len(p.lines)", 1),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_addgoal_string_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal('C')
    p.addpremise(A)
    assert eval(input_n) == expected
        