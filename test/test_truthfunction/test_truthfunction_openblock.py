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

"""------------------------------------------------------------------------------
                                    OPENBLOCK
                                   Stopped Run
                                  
                        Input Is String (stopped_string)
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[1][p.statementindex])", "B"),
    ("p.lines[1][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_openblock_stop_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A)
    p.openblock('B')
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 2),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_openblock_stop_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A)
    p.openblock('B')
    p.or_intro(1, left=A)
    assert eval(input_n) == expected
        

