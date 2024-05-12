"""------------------------------------------------------------------------------
                                DISJUNCTION_INTRO
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.rules import Proof
t = Proof()
A = t.wff('A')
B = t.wff('B')
C = t.wff('C')
D = t.wff('D')
E = t.wff('E')

"""------------------------------------------------------------------------------
                                Clean Run 1
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[1][prf.statementindex])", str(A)),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Or(A, B))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.disjunction_intro_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_disjunction_intro_clean_1(input_n, expected):
    prf = Proof()
    A = prf.wff('A')
    B = prf.wff('B')
    C = prf.wff('C')
    D = prf.wff('D')
    E = prf.wff('E')
    prf.setlogic('C')
    prf.goal(Or(A, B))
    prf.premise(A)
    prf.disjunction_intro(1, right=B)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                Clean Run 2
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[1][prf.statementindex])", str(B)),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Or(A, B))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.disjunction_intro_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_disjunction_intro_clean_2(input_n, expected):
    prf = Proof()
    A = prf.wff('A')
    B = prf.wff('B')
    C = prf.wff('C')
    D = prf.wff('D')
    E = prf.wff('E')
    prf.setlogic('C')
    prf.goal(Or(A, B))
    prf.premise(B)
    prf.disjunction_intro(1, left=A)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_string
------------------------------------------------------------------------------"""

# Stop if the left input value is a string.
testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.disjunction_intro_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_disjunction_intro_string_1(input_n, expected):
    prf = Proof()
    A = prf.wff('A')
    B = prf.wff('B')
    C = prf.wff('C')
    D = prf.wff('D')
    E = prf.wff('E')
    prf.setlogic('C')
    prf.goal(Or(A, B))
    prf.premise(B)
    prf.disjunction_intro(1, left='A')
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_string
------------------------------------------------------------------------------"""

# Stop if the right input value is a string.
testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.disjunction_intro_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_disjunction_intro_string_2(input_n, expected):
    prf = Proof()
    A = prf.wff('A')
    B = prf.wff('B')
    C = prf.wff('C')
    D = prf.wff('D')
    E = prf.wff('E')
    prf.setlogic('C')
    prf.goal(Or(A, B))
    prf.premise(B)
    prf.disjunction_intro(1, right='A')
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_nosuchline
------------------------------------------------------------------------------"""

testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.disjunction_intro_name),
    ("prf.lines[2][prf.linesindex]", "-2"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_disjunction_intro_nosuchline_1(input_n, expected):
    prf = Proof()
    A = prf.wff('A')
    B = prf.wff('B')
    C = prf.wff('C')
    D = prf.wff('D')
    E = prf.wff('E')
    prf.setlogic('C')
    prf.goal(Or(A, B))
    prf.premise(A)
    prf.disjunction_intro(-2, right=B)
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_linescope
------------------------------------------------------------------------------"""

testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.disjunction_intro_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_linescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_disjunction_intro_linescope_1(input_n, expected):
    prf = Proof()
    A = prf.wff('A')
    B = prf.wff('B')
    C = prf.wff('C')
    D = prf.wff('D')
    E = prf.wff('E')
    prf.setlogic('C')
    prf.goal(Or(A, B))
    prf.hypothesis(A)
    prf.implication_intro()
    prf.disjunction_intro(1, right=B)
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                              stopped_novaluepassed
------------------------------------------------------------------------------"""

# No item was passed to the function.
testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.disjunction_intro_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_novaluepassed),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_disjunction_intro_string_2(input_n, expected):
    prf = Proof()
    A = prf.wff('A')
    B = prf.wff('B')
    C = prf.wff('C')
    D = prf.wff('D')
    E = prf.wff('E')
    prf.setlogic('C')
    prf.goal(Or(A, B))
    prf.premise(B)
    prf.disjunction_intro(1)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
