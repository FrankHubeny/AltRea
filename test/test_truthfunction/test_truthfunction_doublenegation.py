"""------------------------------------------------------------------------------
        Double Negation Introduction and Double Negation Elimination Testing
                                dn_intro  dn_elim
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                    DN_INTRO
                                    Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[0][p.statementindex])", str(Not(Not(A)))),
    ("(p.lines[0][p.levelindex])", 0),
    ("(p.lines[0][p.blockidindex])", 0),
    ("(p.lines[0][p.ruleindex])", t.goalname),
    ("(p.lines[0][p.linesindex])", ""),
    ("(p.lines[0][p.blocksindex])", ""),
    ("(p.lines[0][p.commentindex])", "double negative goal"),
    #
    ("str(p.lines[1][p.statementindex])", str(A)),
    ("(p.lines[1][p.levelindex])", 0),
    ("(p.lines[1][p.blockidindex])", 0),
    ("(p.lines[1][p.ruleindex])", t.premisename),
    ("(p.lines[1][p.linesindex])", ""),
    ("(p.lines[1][p.blocksindex])", ""),
    ("(p.lines[1][p.commentindex])", "make this a double negative"),
    #
    ("str(p.lines[2][p.statementindex])", str(Not(Not(A)))),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.blockidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.dn_introname),
    ("(p.lines[2][p.linesindex])", "1"),
    ("(p.lines[2][p.blocksindex])", ""),
    ("(p.lines[2][p.commentindex])", "COMPLETE - double negative works"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_dn_intro_clean_1(input_n, expected):
    A = Wff('A')
    p = Proof()
    p.addgoal(Not(Not(A)), comments='double negative goal')
    p.addpremise(A, comments='make this a double negative')
    p.dn_intro(1, comments='double negative works')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                    DN_INTRO
                                  Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[2][p.statementindex])", t.blankstatement),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.blockidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.dn_introname),
    ("(p.lines[2][p.linesindex])", "2"),
    ("(p.lines[2][p.blocksindex])", ""),
    ("(p.lines[2][p.commentindex])", "STOPPED: The referenced line does not exist. - double negative works?"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_dn_intro_nosuchline_1(input_n, expected):
    A = Wff('A')
    p = Proof()
    p.addgoal(Not(Not(A)))
    p.addpremise(A)
    p.dn_intro(2, comments='double negative works?')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                    DN_INTRO
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

# Referenced line is out of scope in a block that has been closed.
testdata = [
    ("str(p.lines[2][p.statementindex])", t.blankstatement),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.blockidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.dn_introname),
    ("(p.lines[2][p.linesindex])", "1"),
    ("(p.lines[2][p.blocksindex])", ""),
    ("(p.lines[2][p.commentindex])", "STOPPED: Reference line is out of scope. - line is out of scope so inaccessible"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_dn_intro_linescope_1(input_n, expected):
    A = Wff('A')
    p = Proof()
    p.addgoal(Not(Not(A)))
    p.openblock(A)
    p.closeblock()
    p.dn_intro(1, comments='line is out of scope so inaccessible')
    assert eval(input_n) == expected

# No other line can be added after the proof is stopped
testdata = [
    ("len(p.lines)", 3),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_dn_intro_stopped_1(input_n, expected):
    A = Wff('A')
    p = Proof()
    p.addgoal(Not(Not(A)))
    p.openblock(A)
    p.closeblock()
    p.dn_intro(1, comments='line is out of scope so inaccessible')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                DN_ELIM
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[0][p.statementindex])", str(A)),
    ("(p.lines[0][p.levelindex])", 0),
    ("(p.lines[0][p.blockidindex])", 0),
    ("(p.lines[0][p.ruleindex])", t.goalname),
    ("(p.lines[0][p.linesindex])", ""),
    ("(p.lines[0][p.blocksindex])", ""),
    ("(p.lines[0][p.commentindex])", "derive this"),
    #
    ("str(p.lines[1][p.statementindex])", str(Not(Not(A)))),
    ("(p.lines[1][p.levelindex])", 0),
    ("(p.lines[1][p.blockidindex])", 0),
    ("(p.lines[1][p.ruleindex])", t.premisename),
    ("(p.lines[1][p.linesindex])", ""),
    ("(p.lines[1][p.blocksindex])", ""),
    ("(p.lines[1][p.commentindex])", "from this"),
    #
    ("str(p.lines[2][p.statementindex])", str(Not(Not(Not(Not(A)))))),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.blockidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.dn_introname),
    ("(p.lines[2][p.linesindex])", "1"),
    ("(p.lines[2][p.blocksindex])", ""),
    ("(p.lines[2][p.commentindex])", "hmm, I'm going in the wrong direction"),
    #
    ("str(p.lines[3][p.statementindex])", str(Not(Not(A)))),
    ("(p.lines[3][p.levelindex])", 0),
    ("(p.lines[3][p.blockidindex])", 0),
    ("(p.lines[3][p.ruleindex])", t.dn_elimname),
    ("(p.lines[3][p.linesindex])", "2"),
    ("(p.lines[3][p.blocksindex])", ""),
    ("(p.lines[3][p.commentindex])", ""),
    #
    ("str(p.lines[4][p.statementindex])", str(A)),
    ("(p.lines[4][p.levelindex])", 0),
    ("(p.lines[4][p.blockidindex])", 0),
    ("(p.lines[4][p.ruleindex])", t.dn_elimname),
    ("(p.lines[4][p.linesindex])", "3"),
    ("(p.lines[4][p.blocksindex])", ""),
    ("(p.lines[4][p.commentindex])", "COMPLETE - that's better!"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_dn_elim_clean_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A, comments='derive this')
    p.addpremise(Not(Not(A)), comments='from this')
    p.dn_intro(1, comments="hmm, I'm going in the wrong direction")
    p.dn_elim(2)
    p.dn_elim(3, comments="that's better!")
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    DN_ELIM
                                  Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[2][p.statementindex])", t.blankstatement),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.blockidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.dn_elimname),
    ("(p.lines[2][p.linesindex])", "-8"),
    ("(p.lines[2][p.blocksindex])", ""),
    ("(p.lines[2][p.commentindex])", "STOPPED: The referenced line does not exist."),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_dn_elim_nosuchline_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A)
    p.openblock(Not(Not(A)))
    p.closeblock()
    p.dn_elim(-8)
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                    DN_ELIM
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[2][p.statementindex])", t.blankstatement),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.blockidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.dn_elimname),
    ("(p.lines[2][p.linesindex])", "1"),
    ("(p.lines[2][p.blocksindex])", ""),
    ("(p.lines[2][p.commentindex])", "STOPPED: Reference line is out of scope."),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_dn_elim_linescope_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A)
    p.openblock(Not(Not(A)), comments='This line is in a higher level block and so inaccessible')
    p.closeblock()
    p.dn_elim(1)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    DN_ELIM
                                  Stopped Run
                                  
                   Not a Double Negation (stopped_notdoublenegative)
------------------------------------------------------------------------------"""

# ~A is a negative not a double negative like ~~A
testdata = [
    ("str(p.lines[2][p.statementindex])", t.blankstatement),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.blockidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.dn_elimname),
    ("(p.lines[2][p.linesindex])", "1"),
    ("(p.lines[2][p.blocksindex])", ""),
    ("(p.lines[2][p.commentindex])", "STOPPED: The referenced line is not a double negation. - It's a good thing I can't derive A from ~A"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_dn_elim_notdoublenegation_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A)
    p.addpremise(Not(A), comments='just a negative, not a double negative')
    p.dn_elim(1, comments="It's a good thing I can't derive A from ~A")
    assert eval(input_n) == expected

