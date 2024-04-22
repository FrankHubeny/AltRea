import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff
from altrea.truthfunction import Proof
from altrea.exception import *
A = Wff('A')
B = Wff('B')
globalproof = Proof()

"""REIT TESTS"""

"""Test: Does reit perform correctly?"""
testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(B)),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.reitname),
    ("p.status", ''),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_reit_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Implies(A, B))
    p.addpremise(B)
    p.openblock(A)
    p.reit(1)
    assert eval(input_n) == expected


