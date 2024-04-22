import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff
from altrea.truthfunction import Proof
from altrea.exception import *
A = Wff('A')
B = Wff('B')
globalproof = Proof()

"""INIT TESTS"""

"""Test 1: Are initialization parameters set correctly for a proof?"""

testdata = [
    ("p.name", None), 
    ("p.blocklist", [ [0,[1]] ]),
    ("p.blocks", []),
    ("p.premises", []),
    ("p.status", ''),
    ("p.comments", ''),
    ("len(p.lines)", 1),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_init_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    assert eval(input_n) == expected

"""Test 2: Are the additions of optional values set correctly?"""

testdata = [
    ("p.name", None),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_init_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    assert eval(input_n) == expected

"""Stop Conditions"""

"""Is the premise entered as a string?"""

testdata = [
    ("p.lines[0][p.ruleindex]", globalproof.goalname),
    ("p.lines[0][p.commentindex]", globalproof.stopped + globalproof.stopped_connector + globalproof.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_init_stop_1(input_n, expected):
    A = Wff('A')
    p = Proof()
    p.addgoal('A')
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 1),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_init_stop_2(input_n, expected):
    A = Wff('A')
    p = Proof()
    p.addgoal('A')
    p.addpremise(A)
    assert eval(input_n) == expected
        
