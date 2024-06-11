"""------------------------------------------------------------------------------
                                SETLOGIC
------------------------------------------------------------------------------"""

import pytest

from altrea.rules import Proof
t = Proof()
A = t.proposition('A')
B = t.proposition('B')
C = t.proposition('C')
D = t.proposition('D')
E = t.proposition('E')

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
    prf.setlogic()
    assert eval(input_n) == expected

    
"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_logicnotfound
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(prf.lines)', 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", "Set Logic"),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_logicnotfound),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_setlogic_logicnotfound_1(input_n, expected):
    prf = Proof()
    prf.setlogic("_?_")
    assert eval(input_n) == expected



"""------------------------------------------------------------------------------
                                  Stopped Run
                        
------------------------------------------------------------------------------"""
    