"""------------------------------------------------------------------------------
                        Implication Introduction
                                implication_intro
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
                            IMPLICATION_INTRO
                                Clean Run
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(p.lines)', 12),
    #
    ("str(p.lines[9][p.statementindex])", str(Implies(C, And(A, B)))),
    ("p.lines[9][p.levelindex]", 2),
    ("p.lines[9][p.proofidindex]", 2),
    ("p.lines[9][p.ruleindex]", t.implication_intro_name),
    ("p.lines[9][p.linesindex]", ""),
    ("p.lines[9][p.proofsindex]", "5-8"),
    ("p.lines[9][p.commentindex]", ""),
    #
    ("str(p.lines[10][p.statementindex])", str(Implies(D, Implies(C, And(A, B))))),
    ("p.lines[10][p.levelindex]", 1),
    ("p.lines[10][p.proofidindex]", 1),
    ("p.lines[10][p.ruleindex]", t.implication_intro_name),
    ("p.lines[10][p.linesindex]", ""),
    ("p.lines[10][p.proofsindex]", "4-9"),
    ("p.lines[10][p.commentindex]", ""),
    #
    ("str(p.lines[11][p.statementindex])", str(Implies(E, Implies(D, Implies(C, And(A, B)))))),
    ("p.lines[11][p.levelindex]", 0),
    ("p.lines[11][p.proofidindex]", 0),
    ("p.lines[11][p.ruleindex]", t.implication_intro_name),
    ("p.lines[11][p.linesindex]", ""),
    ("p.lines[11][p.proofsindex]", "3-10"),
    ("p.lines[11][p.commentindex]", "COMPLETE"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_intro_clean_1(input_n, expected):
    p = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    D = Wff('D')
    E = Wff('E')
    p.setlogic('C')
    p.goal(Implies(E, Implies(D, Implies(C, And(A, B)))))
    p.premise(A)
    p.premise(B)
    p.hypothesis(E)
    p.hypothesis(D)
    p.hypothesis(C)
    p.reiterate(1)
    p.reiterate(2)
    p.conjunction_intro(6, 7)
    p.implication_intro()
    p.implication_intro()
    p.implication_intro()
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                IMPLICATION_INTRO
                                  Stopped Run
                                  
                Logic Is Not Defined (stopped_undefinedlogic)
------------------------------------------------------------------------------"""
    