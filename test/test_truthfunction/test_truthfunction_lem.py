"""------------------------------------------------------------------------------
                        Law of Excluded Middle Testing
                                    lem
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                   LEM
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Or(A, Not(A)))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.lem_name),
    ("p.status", t.complete),
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

"""------------------------------------------------------------------------------
                                      LEM
                                  Stopped Run
                                  
                Block Does Not Exist (stopped_nosuchblock)
------------------------------------------------------------------------------"""


"""------------------------------------------------------------------------------
                                      LEM
                                  Stopped Run
                                  
                Block Is Outside Accessible Scope (stopped_blockscope)
------------------------------------------------------------------------------"""

