"""------------------------------------------------------------------------------
                                    ADDHYPOTHESIS
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
    ('len(prf.lines)', 4),
    ('len(prf.log)', 5),
    #
    ("str(prf.lines[1][prf.statementindex])", str(A)),
    ("prf.lines[1][prf.levelindex]", 1),
    ("prf.lines[1][prf.proofidindex]", 1),
    ("prf.lines[1][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", "Each call to `hypothesis` creates a sub proof."),
    #
    ("str(prf.lines[2][prf.statementindex])", str(C)),
    ("prf.lines[2][prf.levelindex]", 2),
    ("prf.lines[2][prf.proofidindex]", 2),
    ("prf.lines[2][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", "Now I have a sub sub proof."),
    #
    ("str(prf.lines[3][prf.statementindex])", str(B)),
    ("prf.lines[3][prf.levelindex]", 2),
    ("prf.lines[3][prf.proofidindex]", 2),
    ("prf.lines[3][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", "This adds a second hypothesis."),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_addhypothesis_clean_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    prf.goal(B)
    prf.hypothesis(A, comments='Each call to `hypothesis` creates a sub proof.')
    prf.hypothesis(C, comments='Now I have a sub sub proof.')
    prf.addhypothesis(B, comments='This adds a second hypothesis.')    
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_string
------------------------------------------------------------------------------"""

testdata = [
    ('len(prf.lines)', 3),
    ('len(prf.log)', 4),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 1),
    ("prf.lines[1][prf.proofidindex]", 1),
    ("prf.lines[1][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_addhypothesis_string_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    prf.goal(B, comments='There is a difference between the Wff A and the string "A"')
    prf.hypothesis(A)  
    prf.addhypothesis('~A')


    
"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_nosubproof
------------------------------------------------------------------------------"""

testdata = [
    ('len(prf.lines)', 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 1),
    ("prf.lines[1][prf.proofidindex]", 1),
    ("prf.lines[1][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosubproof),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_addhypothesis_nosubproof_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    prf.goal(B, comments='There is a difference between the Wff A and the string "A"')
    # prf.hypothesis(A)  
    prf.addhypothesis(Not(A))
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_string
------------------------------------------------------------------------------"""

testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 1),
    ("prf.lines[1][prf.proofidindex]", 1),
    ("prf.lines[1][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_addhypothesis_string_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    prf.goal(B, comments='There is a difference between the Wff A and the string "A"')
    prf.hypothesis(A)  
    prf.addhypothesis('~A')
    

    