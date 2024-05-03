"""------------------------------------------------------------------------------
                                CONJUNCTION_ELIM
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
    ('len(prf.lines)', 13),
    ('len(prf.log)', 15),
    #
    ("str(prf.lines[7][prf.statementindex])", str(B)),
    ("prf.lines[7][prf.levelindex]", 1),
    ("prf.lines[7][prf.proofidindex]", 2),
    ("prf.lines[7][prf.ruleindex]", t.conjunction_elim_name),
    ("prf.lines[7][prf.linesindex]", "6"),
    ("prf.lines[7][prf.proofsindex]", ""),
    ("prf.lines[7][prf.commentindex]", ""),
    #
    ("str(prf.lines[8][prf.statementindex])", str(A)),
    ("prf.lines[8][prf.levelindex]", 1),
    ("prf.lines[8][prf.proofidindex]", 2),
    ("prf.lines[8][prf.ruleindex]", t.conjunction_elim_name),
    ("prf.lines[8][prf.linesindex]", "6"),
    ("prf.lines[8][prf.proofsindex]", ""),
    ("prf.lines[8][prf.commentindex]", ""),
    #
    ("str(prf.lines[9][prf.statementindex])", str(And(A, B))),
    ("prf.lines[9][prf.levelindex]", 1),
    ("prf.lines[9][prf.proofidindex]", 2),
    ("prf.lines[9][prf.ruleindex]", t.conjunction_intro_name),
    ("prf.lines[9][prf.linesindex]", "8, 7"),
    ("prf.lines[9][prf.proofsindex]", ""),
    ("prf.lines[9][prf.commentindex]", "The order is reversed."),
    #
    ("str(prf.lines[10][prf.statementindex])", str(Implies(And(B, A), And(A, B)))),
    ("prf.lines[10][prf.levelindex]", 0),
    ("prf.lines[10][prf.proofidindex]", 0),
    ("prf.lines[10][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[10][prf.linesindex]", ""),
    ("prf.lines[10][prf.proofsindex]", "6-9"),
    ("prf.lines[10][prf.commentindex]", ""),
    #
    ("str(prf.lines[11][prf.statementindex])", str(Iff(And(B, A), And(A, B)))),
    ("prf.lines[11][prf.levelindex]", 0),
    ("prf.lines[11][prf.proofidindex]", 0),
    ("prf.lines[11][prf.ruleindex]", t.coimplication_intro_name),
    ("prf.lines[11][prf.linesindex]", "10, 5"),
    ("prf.lines[11][prf.proofsindex]", ""),
    ("prf.lines[11][prf.commentindex]", "The order will be like the first statement on line 10."),
    #
    ("str(prf.lines[12][prf.statementindex])", str(Iff(And(A, B), And(B, A)))),
    ("prf.lines[12][prf.levelindex]", 0),
    ("prf.lines[12][prf.proofidindex]", 0),
    ("prf.lines[12][prf.ruleindex]", t.coimplication_intro_name),
    ("prf.lines[12][prf.linesindex]", "5, 10"),
    ("prf.lines[12][prf.proofsindex]", ""),
    ("prf.lines[12][prf.commentindex]", t.complete + t.comments_connector + "Now it works using line 5 first."),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_elim_clean_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    prf.goal(Iff(And(A, B), And(B, A)))
    prf.hypothesis(And(A, B), comments="Don't use `addhypothesis` to start the subproof.")
    prf.conjunction_elim(1, comments='The left side is the default.')
    prf.conjunction_elim(1, side='right', comments='Now do the right side.')
    prf.conjunction_intro(3, 2, comments='Put the conjuncts on the opposite side.')
    prf.implication_intro()
    prf.hypothesis(And(B, A))
    prf.conjunction_elim(6)
    prf.conjunction_elim(6, side='right')
    prf.conjunction_intro(8, 7, comments='The order is reversed.')
    prf.implication_intro()
    prf.coimplication_intro(10, 5, comments='The order will be like the first statement on line 10.')
    prf.coimplication_intro(5, 10, comments='Now it works using line 5 first.')    
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                              stopped_nosuchline
------------------------------------------------------------------------------"""

# The line does not exist in the proof.
testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.conjunction_elim_name),
    ("prf.lines[2][prf.linesindex]", "0"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_elim_nosuchline_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    prf.goal(C)
    prf.premise(And(A, B))
    prf.conjunction_elim(0)
    prf.hypothesis(A, comments='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                              stopped_linescope
------------------------------------------------------------------------------"""

# The line is not accessible.
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 2),
    ("prf.lines[3][prf.proofidindex]", 2),
    ("prf.lines[3][prf.ruleindex]", t.conjunction_elim_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_linescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_elim_linescope_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    prf.goal(C)
    prf.hypothesis(And(A, B))
    prf.hypothesis(C)
    prf.conjunction_elim(1)
    prf.hypothesis(A, comments='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                             stopped_notconjunction
------------------------------------------------------------------------------"""

# The line is not a conjunction.
testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.conjunction_elim_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_notconjunction),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_elim_notconjunction_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    prf.goal(C)
    prf.premise(A)
    prf.conjunction_elim(1)
    prf.hypothesis(A, comments='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_sidenotselected
------------------------------------------------------------------------------"""

# The side either the default 'left' or 'right' was not selected likely from mispelling.
testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.conjunction_elim_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_sidenotselected),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_elim_sidenotselected_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    prf.setlogic('C')
    prf.goal(C)
    prf.premise(And(A, B))
    prf.conjunction_elim(1, side='righ')
    prf.hypothesis(A, comments='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected

