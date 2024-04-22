import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff
from altrea.truthfunction import Proof
from altrea.exception import *
A = Wff('A')
B = Wff('B')
globalproof = Proof()

"""ADDGOAL TESTS"""

testdata = [
    ("len(p.lines)", 1),
    ("p.lines[0][p.ruleindex]", globalproof.goalname),
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

"""ADDGOAL Stop Conditions"""

"""Is the premise entered as a string?"""

testdata = [
    ("str(p.lines[0][p.statementindex])", ""),
    ("p.lines[0][p.commentindex]", globalproof.stopped + globalproof.stopped_connector + globalproof.stopped_string),
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
        