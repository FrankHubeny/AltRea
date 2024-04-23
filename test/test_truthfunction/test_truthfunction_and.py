"""------------------------------------------------------------------------------
                And Introduction and And Elimination Testing
                        and_intro   and_elim
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                AND_ELIM
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[0][p.statementindex])", str(A)+", "+str(B)),
    ("p.lines[0][p.levelindex]", 0),
    ("p.lines[0][p.blockidindex]", 0),
    ("p.lines[0][p.ruleindex]", t.goalname),
    ("p.lines[0][p.linesindex]", ""),
    ("p.lines[0][p.blocksindex]", ""),
    ("p.lines[0][p.commentindex]", "one - two"),
    #
    ("str(p.lines[1][p.statementindex])", str(And(A, B))),
    ("p.lines[1][p.levelindex]", 0),
    ("p.lines[1][p.blockidindex]", 0),
    ("p.lines[1][p.ruleindex]", t.premisename),
    ("p.lines[1][p.linesindex]", ""),
    ("p.lines[1][p.blocksindex]", ""),
    ("p.lines[1][p.commentindex]", ""),
    #
    ("str(p.lines[2][p.statementindex])", str(A)),
    ("p.lines[2][p.levelindex]", 0),
    ("p.lines[2][p.blockidindex]", 0),
    ("p.lines[2][p.ruleindex]", t.and_elimname),
    ("p.lines[2][p.linesindex]", "1"),
    ("p.lines[2][p.blocksindex]", ""),
    ("p.lines[2][p.commentindex]", "PARTIAL COMPLETION"),
    #
    ("str(p.lines[3][p.statementindex])", str(B)),
    ("p.lines[3][p.levelindex]", 0),
    ("p.lines[3][p.blockidindex]", 0),
    ("p.lines[3][p.ruleindex]", t.and_elimname),
    ("p.lines[3][p.linesindex]", "1"),
    ("p.lines[3][p.blocksindex]", ""),
    ("p.lines[3][p.commentindex]", "COMPLETE"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_clean_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A, 'one')
    p.addgoal(B, 'two')
    p.addpremise(And(A, B))
    p.and_elim(1)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    AND_ELIM
                                  Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

# Line = -1
testdata = [
    ("str(p.lines[2][p.statementindex])", ""),
    ("p.lines[2][p.levelindex]", 0),
    ("p.lines[2][p.blockidindex]", 0),
    ("p.lines[2][p.ruleindex]", t.and_elimname),
    ("p.lines[2][p.linesindex]", "-1"),
    ("p.lines[2][p.blocksindex]", ""),
    ("p.lines[2][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_nosuchline_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A, 'one')
    p.addgoal(B, 'two')
    p.addpremise(And(A, B))
    p.and_elim(-1)
    assert eval(input_n) == expected

# Line = A, a Wff
testdata = [
    ("str(p.lines[2][p.statementindex])", ""),
    ("p.lines[2][p.levelindex]", 0),
    ("p.lines[2][p.blockidindex]", 0),
    ("p.lines[2][p.ruleindex]", t.and_elimname),
    ("p.lines[2][p.linesindex]", "A"),
    ("p.lines[2][p.blocksindex]", ""),
    ("p.lines[2][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_nosuchline_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A, 'one')
    p.addgoal(B, 'two')
    p.addpremise(And(A, B))
    p.and_elim(A)
    assert eval(input_n) == expected

# Line = 10
testdata = [
    ("str(p.lines[2][p.statementindex])", ""),
    ("p.lines[2][p.levelindex]", 0),
    ("p.lines[2][p.blockidindex]", 0),
    ("p.lines[2][p.ruleindex]", t.and_elimname),
    ("p.lines[2][p.linesindex]", "10"),
    ("p.lines[2][p.blocksindex]", ""),
    ("p.lines[2][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_nosuchline_3(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A, 'one')
    p.addgoal(B, 'two')
    p.addpremise(And(A, B))
    p.and_elim(10)
    assert eval(input_n) == expected

# Proof does not continue after being stopped
testdata = [
    ("len(p.lines)", 3),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_nosuchline_4(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(A, 'one')
    p.addgoal(B, 'two')
    p.addpremise(And(A, B))
    p.and_elim(10)
    p.and_elim(1)
    assert eval(input_n) == expected
        
"""------------------------------------------------------------------------------
                                    AND_ELIM
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[2][p.statementindex])", t.blankstatement),
    ("p.lines[2][p.ruleindex]", t.and_elimname),
    ("p.lines[2][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_linescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_nosuchline_3(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.openblock(And(A, B))
    p.closeblock()
    p.and_elim(1)
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 3),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_stop_4(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.openblock(And(A, B))
    p.closeblock()
    p.and_elim(1)
    p.openblock(A)
    assert eval(input_n) == expected
        
"""Is the line a conjunction?"""

testdata = [
    ("str(p.lines[2][p.statementindex])", t.blankstatement),
    ("p.lines[2][p.ruleindex]", t.and_elimname),
    ("p.lines[2][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_notconjunction),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_stop_5(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.addpremise(A)
    p.and_elim(1)
    assert eval(input_n) == expected

"""Does proof continue after it has been stopped?"""

testdata = [
    ("len(p.lines)", 3),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_elim_stop_6(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    C = Wff('C')
    p = Proof()
    p.addgoal(C)
    p.addpremise(A)
    p.and_elim(1)
    p.or_intro(1, left=C)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    AND_INTRO
                                    Clean Run

                                No user comments
------------------------------------------------------------------------------"""

# Clean run with no errors
testdata = [
    ("str(p.lines[0][p.statementindex])", str(And(A, B))),
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
    ("str(p.lines[2][p.statementindex])", str(B)),
    ("(p.lines[2][p.levelindex])", 0),
    ("(p.lines[2][p.blockidindex])", 0),
    ("(p.lines[2][p.ruleindex])", t.premisename),
    ("(p.lines[2][p.linesindex])", ""),
    ("(p.lines[2][p.blocksindex])", ""),
    ("(p.lines[2][p.commentindex])", ""),
    #
    ("str(p.lines[3][p.statementindex])", str(And(A, B))),
    ("(p.lines[3][p.levelindex])", 0),
    ("(p.lines[3][p.blockidindex])", 0),
    ("(p.lines[3][p.ruleindex])", t.and_introname),
    ("(p.lines[3][p.linesindex])", "1, 2"),
    ("(p.lines[3][p.blocksindex])", ""),
    ("(p.lines[3][p.commentindex])", "COMPLETE"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_intro_clean_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise(A)
    p.addpremise(B)
    p.and_intro(1, 2)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    AND_INTRO
                                    Clean Run

                                With user comments
------------------------------------------------------------------------------"""

# Clean run with no errors but with user comments
testdata = [
    ("(p.lines[0][p.commentindex])", "goal"),
    #
    ("(p.lines[1][p.commentindex])", "first premise"),
    #
    ("(p.lines[2][p.commentindex])", "second premise"),
    #
    ("(p.lines[3][p.commentindex])", "COMPLETE - joining first and second premises"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_intro_clean_comments_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(And(A, B), comments='goal')
    p.addpremise(A, comments='first premise')
    p.addpremise(B, comments='second premise')
    p.and_intro(1, 2, comments='joining first and second premises')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                    AND_INTRO
                                  Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

# Line = 10
testdata = [
    ("str(p.lines[3][p.statementindex])", t.blankstatement),
    ("(p.lines[3][p.levelindex])", 0),
    ("(p.lines[3][p.blockidindex])", 0),
    ("(p.lines[3][p.ruleindex])", t.and_introname),
    ("(p.lines[3][p.linesindex])", "10"),
    ("(p.lines[3][p.blocksindex])", ""),
    ("(p.lines[3][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_intro_nosuchline_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise(A)
    p.addpremise(B)
    p.and_intro(10, 2)
    assert eval(input_n) == expected

# Line = A
testdata = [
    ("str(p.lines[3][p.statementindex])", t.blankstatement),
    ("(p.lines[3][p.levelindex])", 0),
    ("(p.lines[3][p.blockidindex])", 0),
    ("(p.lines[3][p.ruleindex])", t.and_introname),
    ("(p.lines[3][p.linesindex])", "A"),
    ("(p.lines[3][p.blocksindex])", ""),
    ("(p.lines[3][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_intro_nosuchline_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise(A)
    p.addpremise(B)
    p.and_intro(1, A)
    assert eval(input_n) == expected

# Line = -1.5
testdata = [
    ("str(p.lines[3][p.statementindex])", t.blankstatement),
    ("(p.lines[3][p.levelindex])", 0),
    ("(p.lines[3][p.blockidindex])", 0),
    ("(p.lines[3][p.ruleindex])", t.and_introname),
    ("(p.lines[3][p.linesindex])", "-1.5"),
    ("(p.lines[3][p.blocksindex])", ""),
    ("(p.lines[3][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_intro_nosuchline_3(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise(A)
    p.addpremise(B)
    p.and_intro(-1.5, 2)
    assert eval(input_n) == expected

# Proof is stopped
testdata = [
    ("len(p.lines)", 4),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_intro_nosuchline_4(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise(A)
    p.addpremise(B)
    p.and_intro(-1.5, 2)
    p.and_intro(1, 2)
    p.and_intro(1, 2)
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                    AND_INTRO
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

# The referenced line is in a closed block
testdata = [
    ("str(p.lines[3][p.statementindex])", t.blankstatement),
    ("(p.lines[3][p.levelindex])", 0),
    ("(p.lines[3][p.blockidindex])", 0),
    ("(p.lines[3][p.ruleindex])", t.and_introname),
    ("(p.lines[3][p.linesindex])", "2"),
    ("(p.lines[3][p.blocksindex])", ""),
    ("(p.lines[3][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_linescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_intro_linescope_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise(A)
    p.openblock(B)
    p.closeblock()
    p.and_intro(1, 2)
    assert eval(input_n) == expected

# Proof is stopped
testdata = [
    ("len(p.lines)", 4),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_and_intro_linescope_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.addgoal(And(A, B))
    p.addpremise(A)
    p.openblock(B)
    p.closeblock()
    p.and_intro(1, 2)
    p.and_intro(1, 1)
    p.and_intro(1, 1)
    assert eval(input_n) == expected
