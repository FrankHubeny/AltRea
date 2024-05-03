"""------------------------------------------------------------------------------
                                    GOAL
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
    ('len(prf.lines)', 2),
    #
    ("str(prf.lines[0][prf.statementindex])", str(A)),
    ("prf.lines[0][prf.levelindex]", 0),
    ("prf.lines[0][prf.proofidindex]", 0),
    ("prf.lines[0][prf.ruleindex]", t.goal_name),
    ("prf.lines[0][prf.linesindex]", ""),
    ("prf.lines[0][prf.proofsindex]", ""),
    ("prf.lines[0][prf.commentindex]", ""),
    #
    ("str(prf.lines[1][prf.statementindex])", str(A)),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_goal_clean_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    prf.setlogic('C')
    prf.goal(A)
    prf.premise(A)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_string
------------------------------------------------------------------------------"""

# Input cannot be a string.
testdata = [
    ('len(prf.lines)', 1),
    #
    ("str(prf.lines[0][prf.statementindex])", t.blankstatement),
    ("prf.lines[0][prf.levelindex]", 0),
    ("prf.lines[0][prf.proofidindex]", 0),
    ("prf.lines[0][prf.ruleindex]", ""),
    ("prf.lines[0][prf.linesindex]", ""),
    ("prf.lines[0][prf.proofsindex]", ""),
    ("prf.lines[0][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_goal_string_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    prf.setlogic('C')
    prf.goal('A')
    prf.premise(A)
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_nologic
------------------------------------------------------------------------------"""

# A logic needs to declared before the goal so the goal comes under the constraint of the logic.
testdata = [
    ('len(prf.lines)', 1),
    #
    ("str(prf.lines[0][prf.statementindex])", t.blankstatement),
    ("prf.lines[0][prf.levelindex]", 0),
    ("prf.lines[0][prf.proofidindex]", 0),
    ("prf.lines[0][prf.ruleindex]", ""),
    ("prf.lines[0][prf.linesindex]", ""),
    ("prf.lines[0][prf.proofsindex]", ""),
    ("prf.lines[0][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_nologic),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_goal_nologic_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    # prf.setlogic('C')
    prf.goal(A)
    prf.premise(A)
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                        
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                        
------------------------------------------------------------------------------"""
    