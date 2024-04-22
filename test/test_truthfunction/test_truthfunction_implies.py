import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff
from altrea.truthfunction import Proof
from altrea.exception import *
B = Wff('B')
A = Wff('A')
C = Wff('C')
globalproof = Proof()

"""IMPLIES TESTS"""

"""Test 1: Does the elimination rule work correctly?"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(B)),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.implies_elimname),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_implies_elim_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(B)
    p.addpremise(A)
    p.addpremise(Implies(A, B))
    p.implies_elim(2,1)
    assert eval(input_n) == expected

"""Test 2: Does the introduction rule work correctly?"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Implies(B, A))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.implies_introname),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_implies_intro_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Implies(B, A))
    p.addpremise(A)
    p.openblock(B)
    p.reit(1)
    p.closeblock()
    p.implies_intro(1)
    assert eval(input_n) == expected

"""This test addressing a formatting issue.  The table returns True rather than A >> A."""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Implies(A, A))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.implies_introname),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_intro_4(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Implies(A, A))
    p.openblock(A)
    p.closeblock()
    p.implies_intro(1)
    assert eval(input_n) == expected
