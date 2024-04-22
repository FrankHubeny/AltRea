"""------------------------------------------------------------------------------
                            DeMorgan Rules Testing
                                    demorgan
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                AND_ELIM
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Or(Not(A), Not(B)))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.demorgan_name),
    ("p.status", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Or(Not(A), Not(B)))
    p.addpremise(Not(And(A, B)))
    p.demorgan(1)
    assert eval(input_n) == expected

"""Test 2: Derive ~A & ~B from ~(A | B)."""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(And(Not(A), Not(B)))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.demorgan_name),
    ("p.status", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(And(Not(A), Not(B)))
    p.addpremise(Not(Or(A, B)))
    p.demorgan(1)
    assert eval(input_n) == expected

"""Test 3: Derive ~(A & B) from ~A | ~B."""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Not(And(A, B)))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.demorgan_name),
    ("p.status", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_3(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Not(And(A, B)))
    p.addpremise(Or(Not(A), Not(B)))
    p.demorgan(1)
    assert eval(input_n) == expected

"""Test 4: Derive ~(A | B) from ~A & ~B."""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Not(Or(A, B)))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.demorgan_name),
    ("p.status", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_4(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Not(Or(A, B)))
    p.addpremise(And(Not(A), Not(B)))
    p.demorgan(1)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    DEMORGAN
                                  Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""


"""------------------------------------------------------------------------------
                                    DEMORGAN
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

    