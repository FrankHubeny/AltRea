"""------------------------------------------------------------------------------
                                Or Testing
                            or_intro   or_elim
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                     OR_ELIM
                                   Clean Run
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    OR_ELIM
                                  Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    OR_ELIM
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    OR_INTRO
                                    Clean Run
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    OR_INTRO
                                  Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    OR_INTRO
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[2][p.statementindex])", "C"),
    ("p.lines[2][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_or_stop_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A)
    p.addpremise(B)
    p.or_intro(1, left='C')
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 3),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_or_stop_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A)
    p.addpremise(B)
    p.or_intro(1, left='C')
    p.or_intro(1, right=A)
    assert eval(input_n) == expected
        
"""Is the premise entered as a string on the right?"""

testdata = [
    ("str(p.lines[2][p.statementindex])", "C"),
    ("p.lines[2][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_or_stop_3(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A)
    p.addpremise(B)
    p.or_intro(1, right='C')
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 3),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_or_stop_4(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A)
    p.addpremise(B)
    p.or_intro(1, right='C')
    p.or_intro(1, right=A)
    assert eval(input_n) == expected
        