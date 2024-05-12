"""------------------------------------------------------------------------------
                                    NEGATION_INTRO
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
    ('len(prf.lines)', 6),
    #
    ("str(prf.lines[3][prf.statementindex])", str(A)),
    ("prf.lines[3][prf.levelindex]", 1),
    ("prf.lines[3][prf.proofidindex]", 1),
    ("prf.lines[3][prf.ruleindex]", t.reiterate_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", ""),
    #
    ("str(prf.lines[4][prf.statementindex])", str(t.false_name)),
    ("prf.lines[4][prf.levelindex]", 1),
    ("prf.lines[4][prf.proofidindex]", 1),
    ("prf.lines[4][prf.ruleindex]", t.negation_elim_name),
    ("prf.lines[4][prf.linesindex]", "2, 3"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", ""),
    #
    ("str(prf.lines[5][prf.statementindex])", str(Not(Not(A)))),
    ("prf.lines[5][prf.levelindex]", 0),
    ("prf.lines[5][prf.proofidindex]", 0),
    ("prf.lines[5][prf.ruleindex]", t.negation_intro_name),
    ("prf.lines[5][prf.linesindex]", ""),
    ("prf.lines[5][prf.proofsindex]", "2-4"),
    ("prf.lines[5][prf.commentindex]", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_intro_clean_1(input_n, expected):
    prf = Proof()
    A = prf.wff('A')
    B = prf.wff('B')
    C = prf.wff('C')
    D = prf.wff('D')
    E = prf.wff('E')
    prf.setlogic('C')
    prf.goal(Not(Not(A)))
    prf.premise(A)
    prf.hypothesis(Not(A))
    prf.reiterate(1)
    prf.negation_elim(2, 3)
    prf.negation_intro()
    
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                Clean Run 2
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Not(A))),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
    ("str(prf.lines[3][prf.statementindex])", str(t.false_name)),
    ("prf.lines[3][prf.levelindex]", 1),
    ("prf.lines[3][prf.proofidindex]", 1),
    ("prf.lines[3][prf.ruleindex]", t.negation_elim_name),
    ("prf.lines[3][prf.linesindex]", "1, 2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", ""),
    #
    ("str(prf.lines[4][prf.statementindex])", str(Not(And(A, Not(A))))),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.negation_intro_name),
    ("prf.lines[4][prf.linesindex]", ""),
    ("prf.lines[4][prf.proofsindex]", "1-3"),
    ("prf.lines[4][prf.commentindex]", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_intro_clean_2(input_n, expected):
    prf = Proof()
    A = prf.wff('A')
    B = prf.wff('B')
    C = prf.wff('C')
    D = prf.wff('D')
    E = prf.wff('E')
    prf.setlogic('C')
    prf.goal(Not(And(A, Not(A))))
    prf.hypothesis(A)
    prf.addhypothesis(Not(A))
    prf.negation_elim(1, 2)
    prf.negation_intro()  
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_closemainproof
------------------------------------------------------------------------------"""

# An attempt was made to close the main proof.  This can only be closed by completing the proof.
testdata = [
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.negation_intro_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_closemainproof),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_intro_closemainproof_1(input_n, expected):
    prf = Proof()
    A = prf.wff('A')
    B = prf.wff('B')
    C = prf.wff('C')
    D = prf.wff('D')
    E = prf.wff('E')
    prf.setlogic('C')
    prf.goal(Not(Not(A)))
    prf.premise(A)
    prf.negation_intro()
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_notfalse
------------------------------------------------------------------------------"""

# The previous statement must be false.
testdata = [
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.negation_intro_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_notfalse),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_intro_notfalse_1(input_n, expected):
    prf = Proof()
    A = prf.wff('A')
    B = prf.wff('B')
    C = prf.wff('C')
    D = prf.wff('D')
    E = prf.wff('E')
    prf.setlogic('C')
    prf.goal(Not(Not(A)))
    prf.hypothesis(A)
    prf.negation_intro()
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                        
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                        
------------------------------------------------------------------------------"""
    