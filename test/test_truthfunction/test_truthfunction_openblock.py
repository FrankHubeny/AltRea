import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff
from altrea.truthfunction import Proof
from altrea.exception import *
A = Wff('A')
B = Wff('B')
globalproof = Proof()

"""OPENBLOCK TESTS"""

"""Test 1: Does openblock perform correctly?"""

"""Stop Conditions"""

"""Is the assumption entered as a string?"""

testdata = [
    ("str(p.lines[1][p.statementindex])", "B"),
    ("p.lines[1][p.commentindex]", globalproof.stopped + globalproof.stopped_connector + globalproof.stopped_string),
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
        

