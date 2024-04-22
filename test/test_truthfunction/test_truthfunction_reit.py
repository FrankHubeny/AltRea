"""------------------------------------------------------------------------------
                            Reiteration Testing
                                    reit
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                  REIT
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(B)),
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.reitname),
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

"""------------------------------------------------------------------------------
                                    REIT
                                  Stopped Run
                                  
                Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    REIT
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

