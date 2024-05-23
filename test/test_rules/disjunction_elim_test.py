"""------------------------------------------------------------------------------
                                DISJUNCTION_ELIM
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
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[2][prf.statementindex])", str(A)),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
    ("str(prf.lines[3][prf.statementindex])", str(Implies(A, A))),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", "2-2"),
    ("prf.lines[3][prf.commentindex]", ""),
    #
    ("str(prf.lines[4][prf.statementindex])", str(A)),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.disjunction_elim_name),
    ("prf.lines[4][prf.linesindex]", "1, 3, 3"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_disjunction_elim_clean_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic('C')
    prf.goal(A)
    prf.premise(Or(A, A))
    prf.hypothesis(A)
    prf.implication_intro()
    prf.disjunction_elim(1, 3, 3)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                Clean Run 2
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(prf.lines)', 13),
    #
    ("str(prf.lines[10][prf.statementindex])", str(A)),
    ("prf.lines[10][prf.levelindex]", 1),
    ("prf.lines[10][prf.proofidindex]", 2),
    ("prf.lines[10][prf.ruleindex]", t.implication_elim_name),
    ("prf.lines[10][prf.linesindex]", "8, 9"),
    ("prf.lines[10][prf.proofsindex]", ""),
    ("prf.lines[10][prf.commentindex]", ""),
    #
    ("str(prf.lines[11][prf.statementindex])", str(Implies(C, A))),
    ("prf.lines[11][prf.levelindex]", 0),
    ("prf.lines[11][prf.proofidindex]", 0),
    ("prf.lines[11][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[11][prf.linesindex]", ""),
    ("prf.lines[11][prf.proofsindex]", "8-10"),
    ("prf.lines[11][prf.commentindex]", ""),
    #
    ("str(prf.lines[12][prf.statementindex])", str(A)),
    ("prf.lines[12][prf.levelindex]", 0),
    ("prf.lines[12][prf.proofidindex]", 0),
    ("prf.lines[12][prf.ruleindex]", t.disjunction_elim_name),
    ("prf.lines[12][prf.linesindex]", "3, 7, 11"),
    ("prf.lines[12][prf.proofsindex]", ""),
    ("prf.lines[12][prf.commentindex]", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_disjunction_elim_clean_2(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic('C')
    prf.goal(A)
    prf.premise(Implies(B, A))
    prf.premise(Implies(C, A))
    prf.premise(Or(B, C))
    prf.hypothesis(B)
    prf.reiterate(1)
    prf.implication_elim(4, 5)
    prf.implication_intro()
    prf.hypothesis(C)
    prf.reiterate(2)
    prf.implication_elim(8, 9)
    prf.implication_intro()
    prf.disjunction_elim(3, 7, 11)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                              stopped_nosuchline
------------------------------------------------------------------------------"""

# The first referenced line of the three does not exist in the proof.
testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.disjunction_elim_name),
    ("prf.lines[4][prf.linesindex]", "10"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_nosuchline),
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
    prf.goal(A)
    prf.premise(Or(A, A))
    prf.hypothesis(A)
    prf.implication_intro()
    prf.disjunction_elim(10, 3, 3)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                              stopped_nosuchline
------------------------------------------------------------------------------"""

# The second referenced line of the three does not exist in the proof.
testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.disjunction_elim_name),
    ("prf.lines[4][prf.linesindex]", "-10"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_nosuchline),
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
    prf.goal(A)
    prf.premise(Or(A, A))
    prf.hypothesis(A)
    prf.implication_intro()
    prf.disjunction_elim(1, -10, 3)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                              stopped_nointeger
------------------------------------------------------------------------------"""
# The third referenced line of the three does not exist in the proof.
testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.disjunction_elim_name),
    ("prf.lines[4][prf.linesindex]", "3.1416"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_notinteger),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_intro_notinteger_3(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic('C')
    prf.goal(A)
    prf.premise(Or(A, A))
    prf.hypothesis(A)
    prf.implication_intro()
    prf.disjunction_elim(1, 3, 3.1416)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                              stopped_linescope
------------------------------------------------------------------------------"""

# The first line of the three is not accessible.
testdata = [
    ('len(prf.lines)', 6),
    #
    ("str(prf.lines[5][prf.statementindex])", t.blankstatement),
    ("prf.lines[5][prf.levelindex]", 1),
    ("prf.lines[5][prf.proofidindex]", 1),
    ("prf.lines[5][prf.ruleindex]", t.disjunction_elim_name),
    ("prf.lines[5][prf.linesindex]", "1"),
    ("prf.lines[5][prf.proofsindex]", ""),
    ("prf.lines[5][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_linescope),
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
    prf.goal(A)
    prf.premise(Or(A, A))
    prf.hypothesis(C)
    prf.hypothesis(A)
    prf.implication_intro()
    prf.disjunction_elim(1, 4, 4)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                              stopped_linescope
------------------------------------------------------------------------------"""

# The second line of the three is not accessible.
testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.disjunction_elim_name),
    ("prf.lines[4][prf.linesindex]", "2"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_linescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_elim_linescope_2(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic('C')
    prf.goal(A)
    prf.premise(Or(A, A))
    prf.hypothesis(A)
    prf.implication_intro()
    prf.disjunction_elim(1, 2, 3)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                              stopped_linescope
------------------------------------------------------------------------------"""

# The third line of the three is not accessible.
testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.disjunction_elim_name),
    ("prf.lines[4][prf.linesindex]", "2"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_linescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_elim_linescope_3(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic('C')
    prf.goal(A)
    prf.premise(Or(A, A))
    prf.hypothesis(A)
    prf.implication_intro()
    prf.disjunction_elim(1, 3, 2)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                              stopped_notdisjunction
------------------------------------------------------------------------------"""

# The first referenced line is not a disjunction.
testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.disjunction_elim_name),
    ("prf.lines[4][prf.linesindex]", "1"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_notdisjunction),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_intro_nodisjunction_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic('C')
    prf.goal(A)
    prf.premise(And(A, A))
    prf.hypothesis(A)
    prf.implication_intro()
    prf.disjunction_elim(1, 3, 3)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                             stopped_notimplication
------------------------------------------------------------------------------"""

# The second referenced line is not an implication.
testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.disjunction_elim_name),
    ("prf.lines[4][prf.linesindex]", "1"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_notimplication),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_intro_notimplication_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic('C')
    prf.goal(A)
    prf.premise(Or(A, A))
    prf.hypothesis(A)
    prf.implication_intro()
    prf.disjunction_elim(1, 1, 3)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                             stopped_notimplication
------------------------------------------------------------------------------"""

# The third referenced line is not an implication.
testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.disjunction_elim_name),
    ("prf.lines[4][prf.linesindex]", "1"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_notimplication),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_intro_notimplication_2(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic('C')
    prf.goal(A)
    prf.premise(Or(A, A))
    prf.hypothesis(A)
    prf.implication_intro()
    prf.disjunction_elim(1, 3, 1)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_notsamestatement
------------------------------------------------------------------------------"""

# The consequents of the two implications are not the same.
testdata = [
    ('len(prf.lines)', 13),
    #
    ("str(prf.lines[12][prf.statementindex])", t.blankstatement),
    ("prf.lines[12][prf.levelindex]", 0),
    ("prf.lines[12][prf.proofidindex]", 0),
    ("prf.lines[12][prf.ruleindex]", t.disjunction_elim_name),
    ("prf.lines[12][prf.linesindex]", "7, 11"),
    ("prf.lines[12][prf.proofsindex]", ""),
    ("prf.lines[12][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_notsamestatement),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_intro_notsameconclusion_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic('C')
    prf.goal(A)
    prf.premise(Implies(B, A))
    prf.premise(Implies(C, B))
    prf.premise(Or(B, C))
    prf.hypothesis(B)
    prf.reiterate(1)
    prf.implication_elim(4, 5)
    prf.implication_intro()
    prf.hypothesis(C)
    prf.reiterate(2)
    prf.implication_elim(8, 9)
    prf.implication_intro()
    prf.disjunction_elim(3, 7, 11)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    