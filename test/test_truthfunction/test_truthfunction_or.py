import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff
from altrea.truthfunction import Proof
from altrea.exception import *
A = Wff('A')
B = Wff('B')
globalproof = Proof()

"""OR TESTS"""

"""Test 1: Does the or elimination perform correctly?"""

"""Or elimination error checking.
            
- AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
- ConclusionsNotTheSame: The conclusions of blocks are not the same.
- NoSuchLine: The referenced line does not exist in the proof.
- ScopeError: The referenced statement is not accessible.
"""

"""Test 1: Does the or introduction perform correctly?"""


"""Stop Conditions"""

"""Is the premise entered as a string on the left?"""

testdata = [
    ("str(p.lines[2][p.statementindex])", "C"),
    ("p.lines[2][p.commentindex]", globalproof.stopped + globalproof.stopped_connector + globalproof.stopped_string),
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
    ("p.lines[2][p.commentindex]", globalproof.stopped + globalproof.stopped_connector + globalproof.stopped_string),
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
        