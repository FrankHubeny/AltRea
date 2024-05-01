"""------------------------------------------------------------------------------
                                HYPOTHESIS
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
                            hypothesis, ADDhypothesis
                                Clean Run
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(p.lines)', 6),
    ('p.prooflist[1]', [1, [2, 4], 0, [2, 3]]),
    ('str(p.lines[5][p.statementindex])', str(Implies(And(A, B), C))),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_hypothesis_clean_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.setlogic('C')
    p.goal(Implies(And(A, B), C))
    p.premise(C)
    p.hypothesis(A)
    p.addhypothesis(B)
    p.reiterate(1)
    p.implication_intro()
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                            hypothesis, ADDhypothesis
                                  Stopped Run
                                  
                Logic Is Not Defined (stopped_undefinedlogic)
------------------------------------------------------------------------------"""
    