"""------------------------------------------------------------------------------
                                CONJUNCTION_INTRO
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, Proposition, Falsehood, Truth
from altrea.rules import Proof
t = Proof()
A = t.proposition('A')
B = t.proposition('B')
C = t.proposition('C')
D = t.proposition('D')
E = t.proposition('E')

"""------------------------------------------------------------------------------
                                   Clean Run 1
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[1][prf.statementindex])", str(A)),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(B)),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
    ("str(prf.lines[3][prf.statementindex])", str(And(A, B))),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.conjunction_intro_name),
    ("prf.lines[3][prf.linesindex]", "1, 2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_intro_clean_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic('C')
    prf.goal(And(A, B))
    prf.premise(A)
    prf.premise(B)
    prf.conjunction_intro(1, 2)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                   Clean Run 2
------------------------------------------------------------------------------"""

# Clean test: reverse order of lines
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[1][prf.statementindex])", str(A)),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(B)),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
    ("str(prf.lines[3][prf.statementindex])", str(And(B, A))),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.conjunction_intro_name),
    ("prf.lines[3][prf.linesindex]", "2, 1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_intro_clean_2(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic('C')
    prf.goal(And(B, A))
    prf.premise(A)
    prf.premise(B)
    prf.conjunction_intro(2, 1)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                              stopped_nosuchline
------------------------------------------------------------------------------"""

# The first line does not exist in the proof.
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.conjunction_intro_name),
    ("prf.lines[3][prf.linesindex]", "3"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_intro_nosuchline_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic('C')
    prf.goal(And(A, B))
    prf.premise(A)
    prf.premise(B)
    prf.conjunction_intro(3, 2)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                              stopped_nosuchline
------------------------------------------------------------------------------"""

# The second line does not exist in the proof.
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.conjunction_intro_name),
    ("prf.lines[3][prf.linesindex]", "3"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_intro_nosuchline_2(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic('C')
    prf.goal(And(A, B))
    prf.premise(A)
    prf.premise(B)
    prf.conjunction_intro(1, 3)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                              stopped_linescope
------------------------------------------------------------------------------"""

# The first line is not accessible.
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 2),
    ("prf.lines[3][prf.proofidindex]", 2),
    ("prf.lines[3][prf.ruleindex]", t.conjunction_intro_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_linescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_elim_linescope_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic('C')
    prf.goal(And(A, B))
    prf.hypothesis(A)
    prf.hypothesis(B)
    prf.conjunction_intro(1, 2)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                              stopped_linescope
------------------------------------------------------------------------------"""

# The second line is not accessible.
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 2),
    ("prf.lines[3][prf.proofidindex]", 2),
    ("prf.lines[3][prf.ruleindex]", t.conjunction_intro_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_linescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_elim_linescope_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic('C')
    prf.goal(And(A, B))
    prf.hypothesis(A)
    prf.hypothesis(B)
    prf.conjunction_intro(2, 1)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    