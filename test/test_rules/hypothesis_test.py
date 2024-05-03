"""------------------------------------------------------------------------------
                                HYPOTHESIS
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
                                Clean Run
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(prf.lines)', 5),
    ('len(prf.log)', 7),
    #
    ("str(prf.lines[2][prf.statementindex])", str(A)),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
    ("str(prf.lines[3][prf.statementindex])", str(B)),
    ("prf.lines[3][prf.levelindex]", 1),
    ("prf.lines[3][prf.proofidindex]", 1),
    ("prf.lines[3][prf.ruleindex]", t.reiterate_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", ""),
    #
    ("str(prf.lines[4][prf.statementindex])", str(Implies(A, B))),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[4][prf.linesindex]", ""),
    ("prf.lines[4][prf.proofsindex]", "2-3"),
    ("prf.lines[4][prf.commentindex]", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_hypothesis_clean_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    prf.goal(Implies(A, B))
    prf.premise(B)
    prf.hypothesis(A)
    prf.reiterate(1)
    prf.implication_intro()
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_string
------------------------------------------------------------------------------"""

testdata = [
    ('len(prf.lines)', 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_hypothesis_string_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    prf.goal(B, comments='There is a difference between the Wff A and the string "A"')
    prf.hypothesis('A')  

"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_nogoal
------------------------------------------------------------------------------"""

testdata = [
    ('len(prf.lines)', 2),
    #
    ("str(prf.lines[1][prf.statementindex])", str(B)),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_nogoal),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_hypothesis_nogoal_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    #prf.goal(B, comments='There is a difference between the Wff A and the string "A"')
    prf.hypothesis(A)  
    