"""------------------------------------------------------------------------------
                            Proof Initialization Testing
                                    Proof
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                  PROOF
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("p.name", ''), 
    ("p.prooflist", [[0, [1], 0, []]] ),
    ("p.premises", []),
    ("p.status", ''),
    ("p.comments", ''),
    ("len(p.lines)", 1),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_init_clean_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    assert eval(input_n) == expected

#Test 2: Are the additions of optional values set correctly?
testdata = [
    ("p.name", "Some Name"),
    ("p.logic", "CO"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_init_clean_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof(name="Some Name")
    p.setlogic('CO')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    PROOF
                                  Stopped Run
                                  
                Logic Is Not Defined (stopped_undefinedlogic)
------------------------------------------------------------------------------"""

testdata = [
    ("len(p.lines)", 1),
    ("str(p.lines[0][p.statementindex])", t.blankstatement),
    ("(p.lines[0][p.levelindex])", 0),
    ("(p.lines[0][p.proofidindex])", 0),
    ("(p.lines[0][p.ruleindex])", ''),
    ("(p.lines[0][p.linesindex])", ""),
    ("(p.lines[0][p.proofsindex])", ""),
    ("p.lines[0][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_undefinedlogic),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_init_undefinedlogic_1(input_n, expected):
    C = Wff('C')
    p = Proof()
    p.setlogic('X')
    p.goal(C)
    assert eval(input_n) == expected

        
