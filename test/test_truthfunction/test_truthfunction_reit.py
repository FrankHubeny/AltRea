"""------------------------------------------------------------------------------
                            reiterateeration Testing
                                    reiterate
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                  reiterate
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(B)),
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.reiterate_name),
    ("p.status", ''),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_clean_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(Implies(A, B))
    p.premise(B)
    p.hypothesis(A)
    p.reiterate(1)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    reiterate
                                  Stopped Run
                                  
                Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

# no such line
testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", t.blankstatement),
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.reiterate_name),
    ("p.lines[len(p.lines)-1][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosuchline),
    ("p.status", t.stopped),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_nosuchline_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(Implies(A, B))
    p.premise(B)
    p.hypothesis(A)
    p.reiterate(5)
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                    reiterate
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

# outside scope

"""------------------------------------------------------------------------------
                                    reiterate
                                  Stopped Run
                                  
                Statement already available (stopped_alreadyavailable)
------------------------------------------------------------------------------"""

# already available at the current level
testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", t.blankstatement),
    ("p.lines[len(p.lines)-1][p.ruleindex]", t.reiterate_name),
    ("p.lines[len(p.lines)-1][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_alreadyavailable),
    ("p.status", t.stopped),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_reiterate_linescope_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(Implies(A, B))
    p.premise(B)
    p.hypothesis(A)
    p.reiterate(1)
    p.reiterate(1)
    assert eval(input_n) == expected