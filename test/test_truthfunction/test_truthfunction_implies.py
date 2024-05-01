"""------------------------------------------------------------------------------
                            Implication Testing
                        implies_intro implication_elim
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
P = Wff('P')
t = Proof()

"""------------------------------------------------------------------------------
                               implication_elim
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[0][p.statementindex])", str(B)),
    ("(p.lines[0][p.levelindex])", 0),
    ("(p.lines[0][p.proofidindex])", 0),
    ("(p.lines[0][p.ruleindex])", t.goal_name),
    ("(p.lines[0][p.linesindex])", ""),
    ("(p.lines[0][p.proofsindex])", ""),
    ("(p.lines[0][p.commentindex])", ""),
    #
    ("str(p.lines[1][p.statementindex])", str(A)),
    ("(p.lines[1][p.levelindex])", 0),
    ("(p.lines[1][p.proofidindex])", 0),
    ("(p.lines[1][p.ruleindex])", t.premise_name),
    ("(p.lines[1][p.linesindex])", ""),
    ("(p.lines[1][p.proofsindex])", ""),
    ("(p.lines[1][p.commentindex])", ""),
    #
    ("str(p.lines[2][p.statementindex])", str(Implies(A, B))),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.proofidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.premise_name),
    ("(p.lines[2][p.linesindex])", ""),
    ("(p.lines[2][p.proofsindex])", ""),
    ("(p.lines[2][p.commentindex])", ""),
    #
    ("str(p.lines[3][p.statementindex])", str(B)),
    ("(p.lines[3][p.levelindex])", 0),
    ("(p.lines[3][p.proofidindex])", 0),
    ("(p.lines[3][p.ruleindex])", t.implication_elim_name),
    ("(p.lines[3][p.linesindex])", "2, 1"),
    ("(p.lines[3][p.proofsindex])", ""),
    ("(p.lines[3][p.commentindex])", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_elim_clean_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(B)
    p.premise(A)
    p.premise(Implies(A, B))
    p.implication_elim(2,1)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                implication_elim
                                Stopped Run
                                  
                Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

# First line does not exist
testdata = [
    ("str(p.lines[3][p.statementindex])", t.blankstatement),
    ("(p.lines[3][p.levelindex])", 0),
    ("(p.lines[3][p.proofidindex])", 0),
    ("(p.lines[3][p.ruleindex])", t.implication_elim_name),
    ("(p.lines[3][p.linesindex])", ""),
    ("(p.lines[3][p.proofsindex])", ""),
    ("(p.lines[3][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_elim_nosuchline_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(B)
    p.premise(A)
    p.premise(Implies(A, B))
    p.implication_elim(3,1)
    assert eval(input_n) == expected

# Second line does not exist
testdata = [
    ("str(p.lines[3][p.statementindex])", t.blankstatement),
    ("(p.lines[3][p.levelindex])", 0),
    ("(p.lines[3][p.proofidindex])", 0),
    ("(p.lines[3][p.ruleindex])", t.implication_elim_name),
    ("(p.lines[3][p.linesindex])", ""),
    ("(p.lines[3][p.proofsindex])", ""),
    ("(p.lines[3][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_elim_nosuchline_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(B)
    p.premise(A)
    p.premise(Implies(A, B))
    p.implication_elim(2, 1.5)
    assert eval(input_n) == expected
    

"""------------------------------------------------------------------------------
                                implication_elim
                                Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

# Line outside scope

"""------------------------------------------------------------------------------
                                implication_elim
                                Stopped Run
                                  
                Not antecedent (stopped_notantecedent)
------------------------------------------------------------------------------"""

# One statement is not the antecedent of the other
testdata = [
    ("str(p.lines[3][p.statementindex])", t.blankstatement),
    ("(p.lines[3][p.levelindex])", 0),
    ("(p.lines[3][p.proofidindex])", 0),
    ("(p.lines[3][p.ruleindex])", t.implication_elim_name),
    ("(p.lines[3][p.linesindex])", ""),
    ("(p.lines[3][p.proofsindex])", ""),
    ("(p.lines[3][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_notantecedent),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_elim_notantecedent_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(B)
    p.premise(And(A, B))
    p.premise(Implies(A, B))
    p.implication_elim(1, 2)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    IMPLIES_INTRO
                                    Clean Run
------------------------------------------------------------------------------"""



"""------------------------------------------------------------------------------
                                    IMPLIES_INTRO
                                    Stopped Run
                                  
                        Block Does Not Exist (stopped_nosuchblock)
------------------------------------------------------------------------------"""

# nosuchblock


"""------------------------------------------------------------------------------
                                    IMPLIES_INTRO
                                    Stopped Run
                                  
                    Block Not Closed (stopped_blocknotclosed)
------------------------------------------------------------------------------"""

# block not closed

"""------------------------------------------------------------------------------
                                    IMPLIES_INTRO
                                    Stopped Run
                                  
                    Block Not In Scope (stopped_blockscope)
------------------------------------------------------------------------------"""

# blockscope

