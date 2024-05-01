"""------------------------------------------------------------------------------
                                Negation Testing
                                negation_intro   negation_elim
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                    negation_elim
                                   Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(F())),
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.negation_elim_name),
    ("p.status", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_elim_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(And(A, B))
    p.premise(A)
    p.premise(Not(A))
    p.negation_elim(1, 2)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    negation_elim
                                  Stopped Run
                                  
                Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    negation_elim
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""


testdata = [
    ("str(p.lines[2][p.statementindex])", t.blankstatement),
    ("p.lines[2][p.ruleindex]", t.negation_elim_name),
    ("p.lines[2][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_elim_stop_1a(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.setlogic('C')
    p.goal(C)
    p.premise(A)
    p.negation_elim(1, 2)
    assert eval(input_n) == expected

testdata = [
    ("str(p.lines[2][p.statementindex])", t.blankstatement),
    ("p.lines[2][p.ruleindex]", t.negation_elim_name),
    ("p.lines[2][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_elim_stop_1b(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.setlogic('C')
    p.goal(C)
    p.premise(A)
    p.negation_elim(2, 1)
    assert eval(input_n) == expected
    
"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 3),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_elim_stop_2a(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.setlogic('C')
    p.goal(C)
    p.premise(A)
    p.negation_elim(1, 2)
    p.disjunction_intro(1, left=C)
    assert eval(input_n) == expected

testdata = [
    ("len(p.lines)", 3),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_elim_stop_2b(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.setlogic('C')
    p.goal(C)
    p.premise(A)
    p.negation_elim(2, 1)
    p.disjunction_intro(1, left=C)
    assert eval(input_n) == expected

"""Are the two statements contradictory as assumed?"""

testdata = [
    ("str(p.lines[3][p.statementindex])", t.blankstatement),
    ("p.lines[3][p.ruleindex]", t.negation_elim_name),
    ("p.lines[3][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_notcontradiction),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_elim_stop_3(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.setlogic('C')
    p.goal(C)
    p.premise(A)
    p.premise(B)
    p.negation_elim(1, 2)
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 4),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_elim_stop_4(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.setlogic('C')
    p.goal(C)
    p.premise(A)
    p.premise(B)
    p.negation_elim(1, 2)
    assert eval(input_n) == expected

    
"""------------------------------------------------------------------------------
                                    negation_intro
                                    Clean Run
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    negation_intro
                                  Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    negation_intro
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""
