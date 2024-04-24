"""------------------------------------------------------------------------------
                            Implication Testing
                        implies_intro implies_elim
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
P = Wff('P')
t = Proof()

"""------------------------------------------------------------------------------
                               IMPLIES_ELIM
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[0][p.statementindex])", str(B)),
    ("(p.lines[0][p.levelindex])", 0),
    ("(p.lines[0][p.blockidindex])", 0),
    ("(p.lines[0][p.ruleindex])", t.goalname),
    ("(p.lines[0][p.linesindex])", ""),
    ("(p.lines[0][p.blocksindex])", ""),
    ("(p.lines[0][p.commentindex])", ""),
    #
    ("str(p.lines[1][p.statementindex])", str(A)),
    ("(p.lines[1][p.levelindex])", 0),
    ("(p.lines[1][p.blockidindex])", 0),
    ("(p.lines[1][p.ruleindex])", t.premisename),
    ("(p.lines[1][p.linesindex])", ""),
    ("(p.lines[1][p.blocksindex])", ""),
    ("(p.lines[1][p.commentindex])", ""),
    #
    ("str(p.lines[2][p.statementindex])", str(Implies(A, B))),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.blockidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.premisename),
    ("(p.lines[2][p.linesindex])", ""),
    ("(p.lines[2][p.blocksindex])", ""),
    ("(p.lines[2][p.commentindex])", ""),
    #
    ("str(p.lines[3][p.statementindex])", str(B)),
    ("(p.lines[3][p.levelindex])", 0),
    ("(p.lines[3][p.blockidindex])", 0),
    ("(p.lines[3][p.ruleindex])", t.implies_elimname),
    ("(p.lines[3][p.linesindex])", "2, 1"),
    ("(p.lines[3][p.blocksindex])", ""),
    ("(p.lines[3][p.commentindex])", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_implies_elim_clean_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(B)
    p.addpremise(A)
    p.addpremise(Implies(A, B))
    p.implies_elim(2,1)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                IMPLIES_ELIM
                                Stopped Run
                                  
                Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

# First line does not exist
testdata = [
    ("str(p.lines[3][p.statementindex])", t.blankstatement),
    ("(p.lines[3][p.levelindex])", 0),
    ("(p.lines[3][p.blockidindex])", 0),
    ("(p.lines[3][p.ruleindex])", t.implies_elimname),
    ("(p.lines[3][p.linesindex])", ""),
    ("(p.lines[3][p.blocksindex])", ""),
    ("(p.lines[3][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_implies_elim_nosuchline_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(B)
    p.addpremise(A)
    p.addpremise(Implies(A, B))
    p.implies_elim(3,1)
    assert eval(input_n) == expected

# Second line does not exist
testdata = [
    ("str(p.lines[3][p.statementindex])", t.blankstatement),
    ("(p.lines[3][p.levelindex])", 0),
    ("(p.lines[3][p.blockidindex])", 0),
    ("(p.lines[3][p.ruleindex])", t.implies_elimname),
    ("(p.lines[3][p.linesindex])", ""),
    ("(p.lines[3][p.blocksindex])", ""),
    ("(p.lines[3][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_implies_elim_nosuchline_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(B)
    p.addpremise(A)
    p.addpremise(Implies(A, B))
    p.implies_elim(2, 1.5)
    assert eval(input_n) == expected
    

"""------------------------------------------------------------------------------
                                IMPLIES_ELIM
                                Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

# Line outside scope

"""------------------------------------------------------------------------------
                                IMPLIES_ELIM
                                Stopped Run
                                  
                Not antecedent (stopped_notantecedent)
------------------------------------------------------------------------------"""

# One statement is not the antecedent of the other
testdata = [
    ("str(p.lines[3][p.statementindex])", t.blankstatement),
    ("(p.lines[3][p.levelindex])", 0),
    ("(p.lines[3][p.blockidindex])", 0),
    ("(p.lines[3][p.ruleindex])", t.implies_elimname),
    ("(p.lines[3][p.linesindex])", ""),
    ("(p.lines[3][p.blocksindex])", ""),
    ("(p.lines[3][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_notantecedent),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_implies_elim_notantecedent_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(B)
    p.addpremise(And(A, B))
    p.addpremise(Implies(A, B))
    p.implies_elim(1, 2)
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

