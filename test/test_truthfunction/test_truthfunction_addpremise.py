import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff
from altrea.truthfunction import Proof
from altrea.exception import *
A = Wff('A')
B = Wff('B')
globalproof = Proof()

"""ADDPREMISE TESTS"""

"""Test: Is a premise entered correctly?"""

testdata = [
    ("len(p.lines)", 2),
    ("str(p.lines[1][0])", str(A)),
    ("p.lines[1][p.ruleindex]", globalproof.premisename),
    ("p.lines[1][p.commentindex]", "A comment"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_premise_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise(A, "A comment")
    assert eval(input_n) == expected

"""Stop Conditions"""

"""Is the premise entered as a string?"""

testdata = [
    ("str(p.lines[1][p.statementindex])", "C"),
    ("p.lines[1][p.ruleindex]", globalproof.premisename),
    ("p.lines[1][p.commentindex]", globalproof.stopped + globalproof.stopped_connector + globalproof.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_premise_stop_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise('C')
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 2),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_premise_stop_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise('C')
    p.addpremise(A)
    assert eval(input_n) == expected
        