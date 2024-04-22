"""------------------------------------------------------------------------------
                            Implication Testing
                        implies_intro implies_elim
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                               IMPLIES_ELIM
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(B)),
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.implies_elimname),
    ("p.status", t.complete),
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

"""------------------------------------------------------------------------------
                                IMPLIES_ELIM
                                Stopped Run
                                  
                Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""


"""------------------------------------------------------------------------------
                                IMPLIES_ELIM
                                Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""


"""Test 2: Does the introduction rule work correctly?"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Implies(B, A))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.implies_introname),
    ("p.status", t.complete),
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
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.implies_introname),
    ("p.status", t.complete),
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

"""------------------------------------------------------------------------------
                                    IMPLIES_INTRO
                                    Clean Run
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    IMPLIES_INTRO
                                    Stopped Run
                                  
                        Block Does Not Exist (stopped_nosuchblock)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    IMPLIES_INTRO
                                    Stopped Run
                                  
                Block Is Outside Accessible Scope (stopped_blockscope)
------------------------------------------------------------------------------"""
