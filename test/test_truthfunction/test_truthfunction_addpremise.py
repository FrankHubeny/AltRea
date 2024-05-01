"""------------------------------------------------------------------------------
                            Add Premise Testing
                                premise
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                premise
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("len(p.lines)", 2),
    ("str(p.lines[1][0])", str(A)),
    ("p.lines[1][p.ruleindex]", t.premise_name),
    ("p.lines[1][p.commentindex]", "A comment"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_premise_clean_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(And(A, B))
    p.premise(A, "A comment")
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    premise
                                  Stopped Run
                                  
                        String Input (stopped_string)
------------------------------------------------------------------------------"""

# Test input as string and that it stops
testdata = [
    ("str(p.lines[1][p.statementindex])", "C"),
    ("p.lines[1][p.ruleindex]", t.premise_name),
    ("p.lines[1][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
    ("len(p.lines)", 2),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_premise_string_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.setlogic('C')
    p.goal(And(A, B))
    p.premise('C')
    p.premise(C)
    assert eval(input_n) == expected
