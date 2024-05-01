"""------------------------------------------------------------------------------
                                Or Testing
                            disjunction_intro   disjunction_elim
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                     disjunction_elim
                                   Clean Run
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    disjunction_elim
                                  Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    disjunction_elim
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    disjunction_intro
                                    Clean Run
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    disjunction_intro
                                  Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    disjunction_intro
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[2][p.statementindex])", "C"),
    ("p.lines[2][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
    ("len(p.lines)", 3),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def _or_stop_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(A)
    p.premise(B)
    p.disjunction_intro(1, left='C')
    p.disjunction_intro(1, right=A)
    assert eval(input_n) == expected


        
"""Is the premise entered as a string on the right?"""

testdata = [
    ("str(p.lines[2][p.statementindex])", "C"),
    ("p.lines[2][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
    ("len(p.lines)", 3),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def _or_stop_3(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(A)
    p.premise(B)
    p.disjunction_intro(1, right='C')
    p.disjunction_intro(1, right=A)
    assert eval(input_n) == expected

