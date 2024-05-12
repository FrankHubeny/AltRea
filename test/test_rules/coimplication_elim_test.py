"""------------------------------------------------------------------------------
                                COIMPLICATION_ELIM
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
                                Clean Run
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[1][prf.statementindex])", str(Iff(A, B))),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(A)),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
    ("str(prf.lines[3][prf.statementindex])", str(B)),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.coimplication_elim_name),
    ("prf.lines[3][prf.linesindex]", "1, 2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_coimplication_elim_clean_1(input_n, expected):
    prf = Proof()
    A = prf.wff('A')
    B = prf.wff('B')
    C = prf.wff('C')
    D = prf.wff('D')
    E = prf.wff('E')
    prf.setlogic('C')
    prf.goal(B)
    prf.premise(Iff(A, B))
    prf.premise(A)
    prf.coimplication_elim(1, 2)
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
    ("prf.lines[3][prf.ruleindex]", t.coimplication_elim_name),
    ("prf.lines[3][prf.linesindex]", "5"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_coimplication_elim_nosuchline_1(input_n, expected):
    prf = Proof()
    A = prf.wff('A')
    B = prf.wff('B')
    C = prf.wff('C')
    D = prf.wff('D')
    E = prf.wff('E')
    prf.setlogic('C')
    prf.goal(B)
    prf.premise(Iff(A, B))
    prf.premise(A)
    prf.coimplication_elim(5, 2)
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
    ("prf.lines[3][prf.ruleindex]", t.coimplication_elim_name),
    ("prf.lines[3][prf.linesindex]", "4"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_coimplication_elim_nosuchline_2(input_n, expected):
    prf = Proof()
    A = prf.wff('A')
    B = prf.wff('B')
    C = prf.wff('C')
    D = prf.wff('D')
    E = prf.wff('E')
    prf.setlogic('C')
    prf.goal(B)
    prf.premise(Iff(A, B))
    prf.premise(A)
    prf.coimplication_elim(1, 4)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_linescope
------------------------------------------------------------------------------"""

# The first line is not accessible
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 2),
    ("prf.lines[3][prf.proofidindex]", 2),
    ("prf.lines[3][prf.ruleindex]", t.coimplication_elim_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_linescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_coimplication_elim_linescope_1(input_n, expected):
    prf = Proof()
    A = prf.wff('A')
    B = prf.wff('B')
    C = prf.wff('C')
    D = prf.wff('D')
    E = prf.wff('E')
    prf.setlogic('C')
    prf.goal(B)
    prf.hypothesis(Iff(A, B))
    prf.hypothesis(A)
    prf.coimplication_elim(1, 2)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_linescope
------------------------------------------------------------------------------"""

# The second line is not accessible
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 2),
    ("prf.lines[3][prf.proofidindex]", 2),
    ("prf.lines[3][prf.ruleindex]", t.coimplication_elim_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_linescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_coimplication_elim_linescope_2(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    prf.setlogic('C')
    prf.goal(B)
    prf.hypothesis(Iff(A, B))
    prf.hypothesis(A)
    prf.coimplication_elim(2, 1)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                          stopped_notcoimplicationelim
------------------------------------------------------------------------------"""

# Neither of the lines is a coimplication.
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.coimplication_elim_name),
    ("prf.lines[3][prf.linesindex]", "2, 1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_notcoimplicationelim),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_coimplication_elim_notcoimplicationelim_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    prf.setlogic('C')
    prf.goal(B)
    prf.premise(C)
    prf.premise(A)
    prf.coimplication_elim(2, 1)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                          stopped_notcoimplicationelim
------------------------------------------------------------------------------"""

# The first statement is a coimplication but the second is not on either its left or right side.
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.coimplication_elim_name),
    ("prf.lines[3][prf.linesindex]", "1, 2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_notcoimplicationelim),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_coimplication_elim_notcoimplicationelim_2(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    prf.setlogic('C')
    prf.goal(Iff(A, B))
    prf.premise(Iff(C, A))
    prf.premise(B)
    prf.coimplication_elim(1, 2)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                          stopped_notcoimplicationelim
------------------------------------------------------------------------------"""

# The second statement is a coimplication but the first is not on either its left or right side.
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.coimplication_elim_name),
    ("prf.lines[3][prf.linesindex]", "2, 1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_notcoimplicationelim),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_coimplication_elim_notcoimplicationelim_2(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    prf.setlogic('C')
    prf.goal(Iff(A, B))
    prf.premise(Iff(C, A))
    prf.premise(B)
    prf.coimplication_elim(2, 1)
    prf.hypothesis(A, comment='Nothing can be added after the proof is stopped.')
    assert eval(input_n) == expected


