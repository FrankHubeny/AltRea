"""------------------------------------------------------------------------------
                            Close Block Testing
                                closeblock
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                CLOSEBLOCK
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("p.level", 0),
    ("level1", 2),
    ("level2", 1),
    ("level3", 0),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_closeblock_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    D = Wff('D')
    p = Proof()
    p.addgoal(And(A, B))
    p.openblock(C)
    p.openblock(D)
    level1 = p.level
    p.closeblock()
    level2 = p.level
    blocklist = p.blocklist[1:]
    p.closeblock()
    level3 = p.level
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                    CLOSEBLOCK
                                  Stopped Run
                                  
                Closing the Zero Block (stopped_closezeroblock)
------------------------------------------------------------------------------"""


testdata = [
    ("str(p.lines[2][p.statementindex])", ""),
    ("p.lines[2][p.ruleindex]", t.closeblockname),
    ("p.lines[2][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_closezeroblock),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_premise_stop_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise(C)
    p.closeblock()
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 3),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_premise_stop_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise(C)
    p.closeblock()
    p.addpremise(A)
    assert eval(input_n) == expected
        