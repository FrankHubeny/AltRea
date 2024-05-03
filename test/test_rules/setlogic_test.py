"""------------------------------------------------------------------------------
                                SETLOGIC
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
    ('len(prf.lines)', 1),
    ('len(prf.log)', 1),
    #
    ("str(prf.lines[0][prf.statementindex])", t.blankstatement),
    ("prf.lines[0][prf.levelindex]", 0),
    ("prf.lines[0][prf.proofidindex]", 0),
    ("prf.lines[0][prf.ruleindex]", ""),
    ("prf.lines[0][prf.linesindex]", ""),
    ("prf.lines[0][prf.proofsindex]", ""),
    ("prf.lines[0][prf.commentindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_setlogic_clean_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    prf.setlogic('C')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_undefinedlogic
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(prf.lines)', 1),
    ('len(prf.log)', 1),
    #
    ("str(prf.lines[0][prf.statementindex])", t.blankstatement),
    ("prf.lines[0][prf.levelindex]", 0),
    ("prf.lines[0][prf.proofidindex]", 0),
    ("prf.lines[0][prf.ruleindex]", ""),
    ("prf.lines[0][prf.linesindex]", ""),
    ("prf.lines[0][prf.proofsindex]", ""),
    ("prf.lines[0][prf.commentindex]", t.stopped + t.stopped_connector + t.stopped_undefinedlogic),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_setlogic_undefinedlogic_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    prf.setlogic('X')
    prf.goal(A, comments="This should not be displayed.")
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                        
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                        
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                        
------------------------------------------------------------------------------"""
    