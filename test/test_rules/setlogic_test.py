"""------------------------------------------------------------------------------
                                SETLOGIC
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
    ('len(prf.lines)', 1),
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
                        
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                        
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                        
------------------------------------------------------------------------------"""
    