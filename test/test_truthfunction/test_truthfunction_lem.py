import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff
from altrea.truthfunction import Proof
from altrea.exception import *
A = Wff('A')
B = Wff('B')
globalproof = Proof()

"""LEM TESTS"""

"""Test 1: Does the LEM rule work correctly?"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Or(A, Not(A)))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.lem_name),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_lem_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Or(A, Not(A)))
    p.openblock(A)
    p.or_intro(1, right=Not(A))
    p.closeblock()
    p.openblock(Not(A))
    p.or_intro(3, left=A)
    p.closeblock()
    p.lem(1,2)
    assert eval(input_n) == expected
