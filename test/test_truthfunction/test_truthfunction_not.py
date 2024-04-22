import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
from altrea.exception import *
A = Wff('A')
B = Wff('B')
globalproof = Proof()

"""NOT TESTS"""

"""Test 1: Does the not elimination perform correctly?"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(F())),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.not_elimname),
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

"""Stop Conditions"""

"""Does the line exist?"""

testdata = [
    ("str(p.lines[2][p.statementindex])", globalproof.blankstatement),
    ("p.lines[2][p.ruleindex]", globalproof.not_elimname),
    ("p.lines[2][p.commentindex]", globalproof.stopped + globalproof.stopped_connector + globalproof.stopped_nosuchline),
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
    ("str(p.lines[2][p.statementindex])", globalproof.blankstatement),
    ("p.lines[2][p.ruleindex]", globalproof.not_elimname),
    ("p.lines[2][p.commentindex]", globalproof.stopped + globalproof.stopped_connector + globalproof.stopped_nosuchline),
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
    ("str(p.lines[3][p.statementindex])", globalproof.blankstatement),
    ("p.lines[3][p.ruleindex]", globalproof.not_elimname),
    ("p.lines[3][p.commentindex]", globalproof.stopped + globalproof.stopped_connector + globalproof.stopped_notcontradiction),
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

"""Is the line within scope?"""

testdata = [
    ("str(p.lines[3][p.statementindex])", globalproof.blankstatement),
    ("p.lines[3][p.ruleindex]", globalproof.not_elimname),
    ("p.lines[3][p.commentindex]", globalproof.stopped + globalproof.stopped_connector + globalproof.stopped_linescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_stop_5(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.addpremise(A)
    p.openblock(Not(A))
    p.closeblock()
    p.not_elim(1, 2)
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 4),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_stop_6(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.addpremise(A)
    p.openblock(Not(A))
    p.closeblock()
    p.not_elim(1, 2)
    p.reit(1)
    assert eval(input_n) == expected
    

