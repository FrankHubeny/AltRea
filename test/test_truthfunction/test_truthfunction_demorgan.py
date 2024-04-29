"""------------------------------------------------------------------------------
                            DeMorgan Rules Testing
                                    demorgan
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                conjunction_elim
                                Clean Run
------------------------------------------------------------------------------"""

# Derive ~A | ~B from ~(A & B)
testdata = [
    ("str(p.lines[0][p.statementindex])", str(Or(Not(A), Not(B)))),
    ("(p.lines[0][p.levelindex])", 0),
    ("(p.lines[0][p.proofidindex])", 0),
    ("(p.lines[0][p.ruleindex])", t.goal_name),
    ("(p.lines[0][p.linesindex])", ""),
    ("(p.lines[0][p.proofsindex])", ""),
    ("(p.lines[0][p.commentindex])", ""),
    #
    ("str(p.lines[1][p.statementindex])", str(Not(And(A, B)))),
    ("(p.lines[1][p.levelindex])", 0),
    ("(p.lines[1][p.proofidindex])", 0),
    ("(p.lines[1][p.ruleindex])", t.premise_name),
    ("(p.lines[1][p.linesindex])", ""),
    ("(p.lines[1][p.proofsindex])", ""),
    ("(p.lines[1][p.commentindex])", ""),
    #
    ("str(p.lines[2][p.statementindex])", str(Or(Not(A), Not(B)))),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.proofidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.demorgan_name),
    ("(p.lines[2][p.linesindex])", "1"),
    ("(p.lines[2][p.proofsindex])", ""),
    ("(p.lines[2][p.commentindex])", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_clean_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Or(Not(A), Not(B)))
    p.addpremise(Not(And(A, B)))
    p.demorgan(1)
    assert eval(input_n) == expected

# Derive ~A & ~B from ~(A | B).
testdata = [
    ("str(p.lines[0][p.statementindex])", str(And(Not(A), Not(B)))),
    ("(p.lines[0][p.levelindex])", 0),
    ("(p.lines[0][p.proofidindex])", 0),
    ("(p.lines[0][p.ruleindex])", t.goal_name),
    ("(p.lines[0][p.linesindex])", ""),
    ("(p.lines[0][p.proofsindex])", ""),
    ("(p.lines[0][p.commentindex])", ""),
    #
    ("str(p.lines[1][p.statementindex])", str(Not(Or(A, B)))),
    ("(p.lines[1][p.levelindex])", 0),
    ("(p.lines[1][p.proofidindex])", 0),
    ("(p.lines[1][p.ruleindex])", t.premise_name),
    ("(p.lines[1][p.linesindex])", ""),
    ("(p.lines[1][p.proofsindex])", ""),
    ("(p.lines[1][p.commentindex])", ""),
    #
    ("str(p.lines[2][p.statementindex])", str(And(Not(A), Not(B)))),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.proofidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.demorgan_name),
    ("(p.lines[2][p.linesindex])", "1"),
    ("(p.lines[2][p.proofsindex])", ""),
    ("(p.lines[2][p.commentindex])", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_clean_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(And(Not(A), Not(B)))
    p.addpremise(Not(Or(A, B)))
    p.demorgan(1)
    assert eval(input_n) == expected

# Derive ~(A & B) from ~A | ~B.
testdata = [
    ("str(p.lines[0][p.statementindex])", str(Not(And(A, B)))),
    ("(p.lines[0][p.levelindex])", 0),
    ("(p.lines[0][p.proofidindex])", 0),
    ("(p.lines[0][p.ruleindex])", t.goal_name),
    ("(p.lines[0][p.linesindex])", ""),
    ("(p.lines[0][p.proofsindex])", ""),
    ("(p.lines[0][p.commentindex])", ""),
    #
    ("str(p.lines[1][p.statementindex])", str(Or(Not(A), Not(B)))),
    ("(p.lines[1][p.levelindex])", 0),
    ("(p.lines[1][p.proofidindex])", 0),
    ("(p.lines[1][p.ruleindex])", t.premise_name),
    ("(p.lines[1][p.linesindex])", ""),
    ("(p.lines[1][p.proofsindex])", ""),
    ("(p.lines[1][p.commentindex])", ""),
    #
    ("str(p.lines[2][p.statementindex])", str(Not(And(A, B)))),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.proofidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.demorgan_name),
    ("(p.lines[2][p.linesindex])", "1"),
    ("(p.lines[2][p.proofsindex])", ""),
    ("(p.lines[2][p.commentindex])", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_clean_3(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Not(And(A, B)))
    p.addpremise(Or(Not(A), Not(B)))
    p.demorgan(1)
    assert eval(input_n) == expected

# Derive ~(A | B) from ~A & ~B.
testdata = [
    ("str(p.lines[0][p.statementindex])", str(Not(Or(A, B)))),
    ("(p.lines[0][p.levelindex])", 0),
    ("(p.lines[0][p.proofidindex])", 0),
    ("(p.lines[0][p.ruleindex])", t.goal_name),
    ("(p.lines[0][p.linesindex])", ""),
    ("(p.lines[0][p.proofsindex])", ""),
    ("(p.lines[0][p.commentindex])", ""),
    #
    ("str(p.lines[1][p.statementindex])", str(And(Not(A), Not(B)))),
    ("(p.lines[1][p.levelindex])", 0),
    ("(p.lines[1][p.proofidindex])", 0),
    ("(p.lines[1][p.ruleindex])", t.premise_name),
    ("(p.lines[1][p.linesindex])", ""),
    ("(p.lines[1][p.proofsindex])", ""),
    ("(p.lines[1][p.commentindex])", ""),
    #
    ("str(p.lines[2][p.statementindex])", str(Not(Or(A, B)))),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.proofidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.demorgan_name),
    ("(p.lines[2][p.linesindex])", "1"),
    ("(p.lines[2][p.proofsindex])", ""),
    ("(p.lines[2][p.commentindex])", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_clean_4(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Not(Or(A, B)))
    p.addpremise(And(Not(A), Not(B)))
    p.demorgan(1)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    DEMORGAN
                                  Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

# No such line
testdata = [
    ("str(p.lines[2][p.statementindex])", t.blankstatement),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.proofidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.demorgan_name),
    ("(p.lines[2][p.linesindex])", "2.5"),
    ("(p.lines[2][p.proofsindex])", ""),
    ("(p.lines[2][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_nosuchline_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Not(Or(A, B)))
    p.addpremise(And(Not(A), Not(B)))
    p.demorgan(2.5)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    DEMORGAN
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""


"""------------------------------------------------------------------------------
                                    DEMORGAN
                                  Stopped Run
                                  
                Referenced line is not DeMorgan form (stopped_notdemorgan)
------------------------------------------------------------------------------"""

# Not demorgan
testdata = [
    ("str(p.lines[2][p.statementindex])", t.blankstatement),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.proofidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.demorgan_name),
    ("(p.lines[2][p.linesindex])", "1"),
    ("(p.lines[2][p.proofsindex])", ""),
    ("(p.lines[2][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_notdemorgan),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_nosuchline_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Not(Or(A, B)))
    p.addpremise(Not(A))
    p.demorgan(1)
    assert eval(input_n) == expected

    