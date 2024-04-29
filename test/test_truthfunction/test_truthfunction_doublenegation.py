"""------------------------------------------------------------------------------
        Double Negation Introduction and Double Negation Elimination Testing
                                doublenegation_intro  doublenegation_elim
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                    doublenegation_intro
                                    Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[0][p.statementindex])", str(Not(Not(A)))),
    ("(p.lines[0][p.levelindex])", 0),
    ("(p.lines[0][p.proofidindex])", 0),
    ("(p.lines[0][p.ruleindex])", t.goal_name),
    ("(p.lines[0][p.linesindex])", ""),
    ("(p.lines[0][p.proofsindex])", ""),
    ("(p.lines[0][p.commentindex])", "double negative goal"),
    #
    ("str(p.lines[1][p.statementindex])", str(A)),
    ("(p.lines[1][p.levelindex])", 0),
    ("(p.lines[1][p.proofidindex])", 0),
    ("(p.lines[1][p.ruleindex])", t.premise_name),
    ("(p.lines[1][p.linesindex])", ""),
    ("(p.lines[1][p.proofsindex])", ""),
    ("(p.lines[1][p.commentindex])", "make this a double negative"),
    #
    ("str(p.lines[2][p.statementindex])", str(Not(Not(A)))),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.proofidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.doublenegation_intro_name),
    ("(p.lines[2][p.linesindex])", "1"),
    ("(p.lines[2][p.proofsindex])", ""),
    ("(p.lines[2][p.commentindex])", "COMPLETE - double negative works"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_doublenegation_intro_clean_1(input_n, expected):
    A = Wff('A')
    p = Proof()
    p.addgoal(Not(Not(A)), comments='double negative goal')
    p.addpremise(A, comments='make this a double negative')
    p.doublenegation_intro(1, comments='double negative works')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                    doublenegation_intro
                                  Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[2][p.statementindex])", t.blankstatement),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.proofidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.doublenegation_intro_name),
    ("(p.lines[2][p.linesindex])", "2"),
    ("(p.lines[2][p.proofsindex])", ""),
    ("(p.lines[2][p.commentindex])", "STOPPED: The referenced line does not exist. - double negative works?"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_doublenegation_intro_nosuchline_1(input_n, expected):
    A = Wff('A')
    p = Proof()
    p.addgoal(Not(Not(A)))
    p.addpremise(A)
    p.doublenegation_intro(2, comments='double negative works?')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                    doublenegation_intro
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

# Referenced line is out of scope in a block that has been closed.



"""------------------------------------------------------------------------------
                                doublenegation_elim
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[0][p.statementindex])", str(A)),
    ("(p.lines[0][p.levelindex])", 0),
    ("(p.lines[0][p.proofidindex])", 0),
    ("(p.lines[0][p.ruleindex])", t.goal_name),
    ("(p.lines[0][p.linesindex])", ""),
    ("(p.lines[0][p.proofsindex])", ""),
    ("(p.lines[0][p.commentindex])", "derive this"),
    #
    ("str(p.lines[1][p.statementindex])", str(Not(Not(A)))),
    ("(p.lines[1][p.levelindex])", 0),
    ("(p.lines[1][p.proofidindex])", 0),
    ("(p.lines[1][p.ruleindex])", t.premise_name),
    ("(p.lines[1][p.linesindex])", ""),
    ("(p.lines[1][p.proofsindex])", ""),
    ("(p.lines[1][p.commentindex])", "from this"),
    #
    ("str(p.lines[2][p.statementindex])", str(Not(Not(Not(Not(A)))))),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.proofidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.doublenegation_intro_name),
    ("(p.lines[2][p.linesindex])", "1"),
    ("(p.lines[2][p.proofsindex])", ""),
    ("(p.lines[2][p.commentindex])", "hmm, I'm going in the wrong direction"),
    #
    ("str(p.lines[3][p.statementindex])", str(Not(Not(A)))),
    ("(p.lines[3][p.levelindex])", 0),
    ("(p.lines[3][p.proofidindex])", 0),
    ("(p.lines[3][p.ruleindex])", t.doublenegation_elim_name),
    ("(p.lines[3][p.linesindex])", "2"),
    ("(p.lines[3][p.proofsindex])", ""),
    ("(p.lines[3][p.commentindex])", ""),
    #
    ("str(p.lines[4][p.statementindex])", str(A)),
    ("(p.lines[4][p.levelindex])", 0),
    ("(p.lines[4][p.proofidindex])", 0),
    ("(p.lines[4][p.ruleindex])", t.doublenegation_elim_name),
    ("(p.lines[4][p.linesindex])", "3"),
    ("(p.lines[4][p.proofsindex])", ""),
    ("(p.lines[4][p.commentindex])", "COMPLETE - that's better!"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_doublenegation_elim_clean_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A, comments='derive this')
    p.addpremise(Not(Not(A)), comments='from this')
    p.doublenegation_intro(1, comments="hmm, I'm going in the wrong direction")
    p.doublenegation_elim(2)
    p.doublenegation_elim(3, comments="that's better!")
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    doublenegation_elim
                                  Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""


"""------------------------------------------------------------------------------
                                    doublenegation_elim
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""


"""------------------------------------------------------------------------------
                                    doublenegation_elim
                                  Stopped Run
                                  
                   Not a Double Negation (stopped_notdoublenegative)
------------------------------------------------------------------------------"""

# ~A is a negative not a double negative like ~~A
testdata = [
    ("str(p.lines[2][p.statementindex])", t.blankstatement),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.proofidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.doublenegation_elim_name),
    ("(p.lines[2][p.linesindex])", "1"),
    ("(p.lines[2][p.proofsindex])", ""),
    ("(p.lines[2][p.commentindex])", "STOPPED: The referenced line is not a double negation. - It's a good thing I can't derive A from ~A"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_doublenegation_elim_notdoublenegation_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A)
    p.addpremise(Not(A), comments='just a negative, not a double negative')
    p.doublenegation_elim(1, comments="It's a good thing I can't derive A from ~A")
    assert eval(input_n) == expected

