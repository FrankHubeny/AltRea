"""------------------------------------------------------------------------------
                                Negation Testing
                                not_intro   not_elim
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                    NOT_ELIM
                                   Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(F())),
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.not_elimname),
    ("p.status", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_not_elim_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise(A)
    p.addpremise(Not(A))
    p.not_elim(1, 2)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    NOT_ELIM
                                  Stopped Run
                                  
                Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    NOT_ELIM
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""


testdata = [
    ("str(p.lines[2][p.statementindex])", t.blankstatement),
    ("p.lines[2][p.ruleindex]", t.not_elimname),
    ("p.lines[2][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_not_elim_stop_1a(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.addpremise(A)
    p.not_elim(1, 2)
    assert eval(input_n) == expected

testdata = [
    ("str(p.lines[2][p.statementindex])", t.blankstatement),
    ("p.lines[2][p.ruleindex]", t.not_elimname),
    ("p.lines[2][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_not_elim_stop_1b(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.addpremise(A)
    p.not_elim(2, 1)
    assert eval(input_n) == expected
    
"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 3),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_not_elim_stop_2a(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.addpremise(A)
    p.not_elim(1, 2)
    p.or_intro(1, left=C)
    assert eval(input_n) == expected

testdata = [
    ("len(p.lines)", 3),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_not_elim_stop_2b(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.addpremise(A)
    p.not_elim(2, 1)
    p.or_intro(1, left=C)
    assert eval(input_n) == expected

"""Are the two statements contradictory as assumed?"""

testdata = [
    ("str(p.lines[3][p.statementindex])", t.blankstatement),
    ("p.lines[3][p.ruleindex]", t.not_elimname),
    ("p.lines[3][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_notcontradiction),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_not_elim_stop_3(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.addpremise(A)
    p.addpremise(B)
    p.not_elim(1, 2)
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 4),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_not_elim_stop_4(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.addpremise(A)
    p.addpremise(B)
    p.not_elim(1, 2)
    assert eval(input_n) == expected

    
"""------------------------------------------------------------------------------
                                    NOT_INTRO
                                    Clean Run
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    NOT_INTRO
                                  Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    NOT_INTRO
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""
