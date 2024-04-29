"""------------------------------------------------------------------------------
                        Law of Excluded Middle Testing
                                    lem
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                   LEM
                                Clean Run
------------------------------------------------------------------------------"""

# Clean run with no errors
testdata = [
    ("str(p.lines[2][p.statementindex])", str(Or(A, Not(A)))),
    ("(p.lines[2][p.levelindex])", 1),
    ("(p.lines[2][p.proofidindex])", 1),
    ("(p.lines[2][p.ruleindex])", t.disjunction_intro_name),
    ("(p.lines[2][p.linesindex])", "1"),
    ("(p.lines[2][p.proofsindex])", ""),
    ("(p.lines[2][p.commentindex])", ""),
    #
    ("str(p.lines[3][p.statementindex])", str(Not(A))),
    ("(p.lines[3][p.levelindex])", 1),
    ("(p.lines[3][p.proofidindex])", 2),
    ("(p.lines[3][p.ruleindex])", t.hypothesis_name),
    ("(p.lines[3][p.linesindex])", ""),
    ("(p.lines[3][p.proofsindex])", ""),
    ("(p.lines[3][p.commentindex])", ""),
    #
    ("str(p.lines[4][p.statementindex])", str(Or(A, Not(A)))),
    ("(p.lines[4][p.levelindex])", 1),
    ("(p.lines[4][p.proofidindex])", 2),
    ("(p.lines[4][p.ruleindex])", t.disjunction_intro_name),
    ("(p.lines[4][p.linesindex])", "3"),
    ("(p.lines[4][p.proofsindex])", ""),
    ("(p.lines[4][p.commentindex])", ""),
    #
    ("str(p.lines[5][p.statementindex])", str(Or(A, Not(A)))),
    ("(p.lines[5][p.levelindex])", 0),
    ("(p.lines[5][p.proofidindex])", 0),
    ("(p.lines[5][p.ruleindex])", t.lem_name),
    ("(p.lines[5][p.linesindex])", ""),
    ("(p.lines[5][p.proofsindex])", "1, 2"),
    ("(p.lines[5][p.commentindex])", t.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def _lem_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Or(A, Not(A)))
    p.hypothesis(A)
    p.disjunction_intro(1, right=Not(A))
    p.closeblock()
    p.hypothesis(Not(A))
    p.disjunction_intro(3, left=A)
    p.closeblock()
    p.lem(1,2)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                      LEM
                                  Stopped Run
                                  
                Block Does Not Exist (stopped_nosuchblock)
------------------------------------------------------------------------------"""

# Block id does not exist
testdata = [
    ("str(p.lines[5][p.statementindex])", t.blankstatement),
    ("(p.lines[5][p.levelindex])", 0),
    ("(p.lines[5][p.proofidindex])", 0),
    ("(p.lines[5][p.ruleindex])", t.lem_name),
    ("(p.lines[5][p.linesindex])", ""),
    ("(p.lines[5][p.proofsindex])", ""),
    ("(p.lines[5][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_nosuchblock),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def _lem_nosuchblock_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Or(A, Not(A)))
    p.hypothesis(A)
    p.disjunction_intro(1, right=Not(A))
    p.closeblock()
    p.hypothesis(Not(A))
    p.disjunction_intro(3, left=A)
    p.closeblock()
    p.lem(3,2)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                      LEM
                                  Stopped Run
                                  
                Block Is Outside Accessible Scope (stopped_notsamelevel)
------------------------------------------------------------------------------"""

# Not same level
testdata = [
    ("str(p.lines[5][p.statementindex])", t.blankstatement),
    ("(p.lines[5][p.levelindex])", 0),
    ("(p.lines[5][p.proofidindex])", 0),
    ("(p.lines[5][p.ruleindex])", t.lem_name),
    ("(p.lines[5][p.linesindex])", ""),
    ("(p.lines[5][p.proofsindex])", ""),
    ("(p.lines[5][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_notsamelevel),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def _lem_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Or(A, Not(A)))
    p.hypothesis(A)
    p.disjunction_intro(1, right=Not(A))
    # p.closeblock()
    p.hypothesis(Not(A))
    p.disjunction_intro(3, left=A)
    p.closeblock()
    p.closeblock()
    p.lem(1,2)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                      LEM
                                  Stopped Run
                                  
                        Blocks Not Work With LEM Rule (stopped_notlem)
------------------------------------------------------------------------------"""

# blocks not work with LEM rule
testdata = [
    ("str(p.lines[5][p.statementindex])", t.blankstatement),
    ("(p.lines[5][p.levelindex])", 0),
    ("(p.lines[5][p.proofidindex])", 0),
    ("(p.lines[5][p.ruleindex])", t.lem_name),
    ("(p.lines[5][p.linesindex])", ""),
    ("(p.lines[5][p.proofsindex])", ""),
    ("(p.lines[5][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_notlem),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def _lem_notlem_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Or(A, Not(A)))
    p.hypothesis(A)
    p.disjunction_intro(1, right=Not(A))
    p.closeblock()
    p.hypothesis(A)
    p.disjunction_intro(3, left=A)
    p.closeblock()
    p.lem(1,2)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                      LEM
                                  Stopped Run
                                  
                        Blocks Not Same Level (stopped_notsamelevel)
------------------------------------------------------------------------------"""

# blocks not same level
testdata = [
    ("str(p.lines[5][p.statementindex])", t.blankstatement),
    ("(p.lines[5][p.levelindex])", 0),
    ("(p.lines[5][p.proofidindex])", 0),
    ("(p.lines[5][p.ruleindex])", t.lem_name),
    ("(p.lines[5][p.linesindex])", ""),
    ("(p.lines[5][p.proofsindex])", ""),
    ("(p.lines[5][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_notsamelevel),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def _lem_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(Or(A, Not(A)))
    p.hypothesis(A)
    p.disjunction_intro(1, right=Not(A))
    # p.closeblock()
    p.hypothesis(Not(A))
    p.disjunction_intro(3, left=A)
    p.closeblock()
    p.closeblock()
    p.lem(1,2)
    assert eval(input_n) == expected
