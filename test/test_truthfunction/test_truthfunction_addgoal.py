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

testdata = [
    ("len(p.lines)", 1),
    ("p.lines[0][p.ruleindex]", t.goalname),
    ("p.lines[0][p.commentindex]", 'My Comment'),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_addgoal_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C, 'My Comment')
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
def test_addgoal_stop_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal('C')
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 1),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_addgoal_stop_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal('C')
    p.addpremise(A)
    assert eval(input_n) == expected
        