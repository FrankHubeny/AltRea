"""------------------------------------------------------------------------------
                                EXPLOSION
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.rules import Proof
A = Wff('A')
B = Wff('B')
C = Wff('C')
D = Wff('D')
E = Wff('E')
t = Proof()

"""------------------------------------------------------------------------------
                                Clean Run 1
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(prf.lines)', 5),
    ('len(prf.log)', 8),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Not(A))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
    ("str(prf.lines[3][prf.statementindex])", str(t.falsename)),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.negation_elim_name),
    ("prf.lines[3][prf.linesindex]", "1, 2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", ""),
    #
    ("str(prf.lines[4][prf.statementindex])", str(C)),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.explosion_name),
    ("prf.lines[4][prf.linesindex]", "3"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_explosion_clean_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    mygoal = C
    prf.setlogic('C')
    prf.goal(mygoal)
    prf.premise(A)
    prf.premise(Not(A))
    prf.negation_elim(1, 2)
    prf.explosion(mygoal)    
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                Clean Run 2
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(prf.lines)', 16),
    #
    ("str(prf.lines[13][prf.statementindex])", str(Implies(B, Implies(A, B)))),
    ("prf.lines[13][prf.levelindex]", 1),
    ("prf.lines[13][prf.proofidindex]", 1),
    ("prf.lines[13][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[13][prf.linesindex]", ""),
    ("prf.lines[13][prf.proofsindex]", "9-12"),
    ("prf.lines[13][prf.commentindex]", ""),
    #
    ("str(prf.lines[14][prf.statementindex])", str(Implies(A, B))),
    ("prf.lines[14][prf.levelindex]", 1),
    ("prf.lines[14][prf.proofidindex]", 1),
    ("prf.lines[14][prf.ruleindex]", t.disjunction_elim_name),
    ("prf.lines[14][prf.linesindex]", "1, 8, 13"),
    ("prf.lines[14][prf.proofsindex]", ""),
    ("prf.lines[14][prf.commentindex]", ""),
    #
    ("str(prf.lines[15][prf.statementindex])", str(Implies(Or(Not(A), B), Implies(A, B)))),
    ("prf.lines[15][prf.levelindex]", 0),
    ("prf.lines[15][prf.proofidindex]", 0),
    ("prf.lines[15][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[15][prf.linesindex]", ""),
    ("prf.lines[15][prf.proofsindex]", "1-14"),
    ("prf.lines[15][prf.commentindex]", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_explosion_clean_2(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    prf.goal(Implies(Or(Not(A), B), Implies(A, B)))
    prf.hypothesis(Or(Not(A), B))
    prf.hypothesis(Not(A))
    prf.hypothesis(A)
    prf.reiterate(2)
    prf.negation_elim(3, 4)
    prf.explosion(B)
    prf.implication_intro()
    prf.implication_intro()
    prf.hypothesis(B)
    prf.hypothesis(A)
    prf.reiterate(9)
    prf.implication_intro()
    prf.implication_intro()
    prf.disjunction_elim(1, 8, 13)
    prf.implication_intro() 
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_string
------------------------------------------------------------------------------"""

# Stop if the right input value is a string.
testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.explosion_name),
    ("prf.lines[4][prf.linesindex]", ""),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_explosion_string_2(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    prf.goal(C)
    prf.premise(A)
    prf.premise(Not(A))
    prf.negation_elim(1, 2)
    prf.explosion('C')
    prf.hypothesis(A, comments='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_nosuchline
------------------------------------------------------------------------------"""

testdata = [
    ('len(prf.lines)', 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.explosion_name),
    ("prf.lines[1][prf.linesindex]", "0"),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_explosion_nosuchline_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    prf.goal(Or(A, B))
    prf.explosion(C)
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_notfalse
------------------------------------------------------------------------------"""

testdata = [
    ('len(prf.lines)', 3),
    ('len(prf.log)', 4),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.explosion_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_notfalse),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_explosion_linescope_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    prf.goal(C)
    prf.hypothesis(A)
    prf.explosion(C)
    assert eval(input_n) == expected
    

    