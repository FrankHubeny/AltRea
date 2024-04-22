"""------------------------------------------------------------------------------
                            Explosion Testing
                                explosion
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                EXPLOSION
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(And(A, B))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.explosionname),
    ("p.status", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_explosion_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise(A)
    p.addpremise(Not(A))
    p.not_elim(1, 2)
    p.explosion(And(A, B))
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                EXPLOSION
                                Stopped Run
                                  
                Statement Is Not False (stopped_notfalse)
------------------------------------------------------------------------------"""


testdata = [
    ("str(p.lines[4][p.statementindex])", "A"),
    ("p.lines[4][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_explosion_stop_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A)
    p.openblock(Not(A))
    p.openblock(A)
    p.not_elim(1, 2)
    p.explosion('A')
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 5),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_explosion_stop_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A)
    p.openblock(Not(A))
    p.openblock(A)
    p.not_elim(1, 2)
    p.explosion('A')
    p.or_intro(4, right=B)
    assert eval(input_n) == expected
        
