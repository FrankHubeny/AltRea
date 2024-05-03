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
    ('len(prf.lines)', 12),
    #
    ("str(prf.lines[9][prf.statementindex])", str(Implies(C, And(A, B)))),
    ("prf.lines[9][prf.levelindex]", 2),
    ("prf.lines[9][prf.proofidindex]", 2),
    ("prf.lines[9][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[9][prf.linesindex]", ""),
    ("prf.lines[9][prf.proofsindex]", "5-8"),
    ("prf.lines[9][prf.commentindex]", ""),
    #
    ("str(prf.lines[10][prf.statementindex])", str(Implies(D, Implies(C, And(A, B))))),
    ("prf.lines[10][prf.levelindex]", 1),
    ("prf.lines[10][prf.proofidindex]", 1),
    ("prf.lines[10][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[10][prf.linesindex]", ""),
    ("prf.lines[10][prf.proofsindex]", "4-9"),
    ("prf.lines[10][prf.commentindex]", ""),
    #
    ("str(prf.lines[11][prf.statementindex])", str(Implies(E, Implies(D, Implies(C, And(A, B)))))),
    ("prf.lines[11][prf.levelindex]", 0),
    ("prf.lines[11][prf.proofidindex]", 0),
    ("prf.lines[11][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[11][prf.linesindex]", ""),
    ("prf.lines[11][prf.proofsindex]", "3-10"),
    ("prf.lines[11][prf.commentindex]", "COMPLETE"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_intro_clean_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    D = Wff('D')
    E = Wff('E')
    prf.setlogic('C')
    prf.goal(Implies(E, Implies(D, Implies(C, And(A, B)))))
    prf.premise(A)
    prf.premise(B)
    prf.hypothesis(E)
    prf.hypothesis(D)
    prf.hypothesis(C)
    prf.reiterate(1)
    prf.reiterate(2)
    prf.conjunction_intro(6, 7)
    prf.implication_intro()
    prf.implication_intro()
    prf.implication_intro()
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                IMPLICATION_INTRO
                                  Stopped Run
                                  
                Logic Is Not Defined (stopped_undefinedlogic)
------------------------------------------------------------------------------"""
    