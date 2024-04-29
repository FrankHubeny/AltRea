"""------------------------------------------------------------------------------
                            Open Block Testing
                                openblock
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                    OPENBLOCK
                                    Clean Run
------------------------------------------------------------------------------"""

# Clean run
testdata = [
    ("str(p.lines[1][p.statementindex])", "B"),
    ("p.lines[1][p.commentindex]", "opening the block"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_hypothesis_stop_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A)
    p.hypothesis(B, comments="opening the block")
    assert eval(input_n) == expected

    
"""------------------------------------------------------------------------------
                                    OPENBLOCK
                                   Stopped Run
                                  
                        Input Is String (stopped_string)
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[1][p.statementindex])", ""),
    ("p.lines[1][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
    ("len(p.lines)", 2),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_hypothesis_stop_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A)
    p.hypothesis('B')
    p.hypothesis(B)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    OPENBLOCK
                                   Stopped Run
                                  
                        No goal (stopped_nogoal)
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[1][p.statementindex])", ""),
    ("p.lines[1][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_nogoal),
    ("len(p.lines)", 2),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_openblock_stop_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    # p.addgoal(A)
    p.hypothesis(B)
    assert eval(input_n) == expected


