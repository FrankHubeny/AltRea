"""------------------------------------------------------------------------------
                                    PREMISE
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, TrueFalse, Falsehood, Truth
from altrea.rules import Proof
t = Proof()
A = t.truefalse('A')
B = t.truefalse('B')
C = t.truefalse('C')
D = t.truefalse('D')
E = t.truefalse('E')

"""------------------------------------------------------------------------------
                                   Clean Run
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[0][prf.statementindex])", str(Not(Not(A)))),
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
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Not(A))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_premise_clean_1(input_n, expected):
    prf = Proof()
    A = prf.truefalse('A')
    B = prf.truefalse('B')
    C = prf.truefalse('C')
    D = prf.truefalse('D')
    E = prf.truefalse('E')
    prf.setlogic('C')
    prf.goal(Not(Not(A)))
    prf.premise(A)
    prf.premise(Not(A))
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
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_premise_string_1(input_n, expected):
    prf = Proof()
    A = prf.truefalse('A')
    B = prf.truefalse('B')
    C = prf.truefalse('C')
    D = prf.truefalse('D')
    E = prf.truefalse('E')
    prf.setlogic('C')
    prf.goal(Not(Not(A)))
    prf.premise('A') 
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_nogoal
------------------------------------------------------------------------------"""

testdata = [
    ('len(prf.lines)', 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_nogoal),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_premise_nogoal_1(input_n, expected):
    prf = Proof()
    A = prf.truefalse('A')
    B = prf.truefalse('B')
    C = prf.truefalse('C')
    D = prf.truefalse('D')
    E = prf.truefalse('E')
    prf.setlogic('C')
    # prf.goal(Not(Not(A)))
    prf.premise(A) 
    assert eval(input_n) == expected


    