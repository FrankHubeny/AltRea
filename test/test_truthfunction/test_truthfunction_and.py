import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff
from altrea.truthfunction import Proof
from altrea.exception import *
A = Wff('A')
B = Wff('B')
globalproof = Proof()

"""AND TESTS"""

"""AND_ELIM------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[2][p.statementindex])", str(A)),
    ("str(p.lines[3][p.statementindex])", str(B)),
    ("p.lines[2][p.ruleindex]", globalproof.and_elimname),
    ("p.lines[3][p.ruleindex]", globalproof.and_elimname),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.addpremise(And(A, B))
    p.and_elim(1)
    assert eval(input_n) == expected

"""AND_ELIM Stop Conditions"""

"""Does the line exist?"""

testdata = [
    ("str(p.lines[2][p.statementindex])", globalproof.blankstatement),
    ("p.lines[2][p.ruleindex]", globalproof.and_elimname),
    ("p.lines[2][p.commentindex]", globalproof.stopped + globalproof.stopped_connector + globalproof.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_stop_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.addpremise(And(A, B))
    p.and_elim(2)
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 3),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_stop_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.addpremise(And(A, B))
    p.and_elim(2)
    p.or_intro(1, left=C)
    assert eval(input_n) == expected
        
"""Is the line within scope?"""

testdata = [
    ("str(p.lines[2][p.statementindex])", globalproof.blankstatement),
    ("p.lines[2][p.ruleindex]", globalproof.and_elimname),
    ("p.lines[2][p.commentindex]", globalproof.stopped + globalproof.stopped_connector + globalproof.stopped_linescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_stop_3(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.openblock(And(A, B))
    p.closeblock()
    p.and_elim(1)
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 3),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_stop_4(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.openblock(And(A, B))
    p.closeblock()
    p.and_elim(1)
    p.openblock(A)
    assert eval(input_n) == expected
        
"""Is the line a conjunction?"""

testdata = [
    ("str(p.lines[2][p.statementindex])", globalproof.blankstatement),
    ("p.lines[2][p.ruleindex]", globalproof.and_elimname),
    ("p.lines[2][p.commentindex]", globalproof.stopped + globalproof.stopped_connector + globalproof.stopped_notconjunction),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_stop_5(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.addpremise(A)
    p.and_elim(1)
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 3),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_stop_6(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.addpremise(A)
    p.and_elim(1)
    p.or_intro(1, left=C)
    assert eval(input_n) == expected

"""AND_INTRO------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[3][p.statementindex])", str(And(A, B))),
    ("p.lines[3][p.ruleindex]", globalproof.and_introname),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_intro_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise(A)
    p.addpremise(B)
    p.and_intro(1, 2)
    assert eval(input_n) == expected

"""AND_INTRO Stop Conditions"""

"""Does the line exist?"""

testdata = [
    ("str(p.lines[3][p.statementindex])", globalproof.blankstatement),
    ("p.lines[3][p.ruleindex]", globalproof.and_introname),
    ("p.lines[3][p.commentindex]", globalproof.stopped + globalproof.stopped_connector + globalproof.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_intro_stop_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise(A)
    p.addpremise(B)
    p.and_intro(4, 2)
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 4),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_intro_stop_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise(A)
    p.addpremise(B)
    p.and_intro(4, 2)
    p.and_intro(1, 2)
    p.and_intro(1, 2)
    assert eval(input_n) == expected
        
