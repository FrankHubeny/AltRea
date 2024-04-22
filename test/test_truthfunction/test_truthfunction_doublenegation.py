import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff
from altrea.truthfunction import Proof
from altrea.exception import *
A = Wff('A')
B = Wff('B')
globalproof = Proof()

"""DOUBLENEGATION TESTS"""

"""Test 1: Does dn_elim remove two negations?"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Not(Not(A)))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.dn_introname),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_dn_elim_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Not(Not(A)))
    p.addpremise(A)
    p.dn_intro(1)
    assert eval(input_n) == expected
    
"""Test: Does dn_intro add two negations?"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Not(Not(A)))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.dn_introname),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_dn_intro_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Not(Not(A)))
    p.addpremise(A)
    p.dn_intro(1)
    assert eval(input_n) == expected

