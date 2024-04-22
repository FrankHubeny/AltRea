"""------------------------------------------------------------------------------
        Double Negation Introduction and Double Negation Elimination Testing
                                dn_intro  dn_elim
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                DN_ELIM
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Not(Not(A)))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.dn_introname),
    ("p.status", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_dn_elim_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Not(Not(A)))
    p.addpremise(A)
    p.dn_intro(1)
    assert eval(input_n) == expected
    
"""Test: Does dn_intro add two negations?"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Not(Not(A)))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.dn_introname),
    ("p.status", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_dn_intro_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Not(Not(A)))
    p.addpremise(A)
    p.dn_intro(1)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    DN_ELIM
                                  Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    DN_ELIM
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    DN_INTRO
                                    Clean Run
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    DN_INTRO
                                  Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    DN_INTRO
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""