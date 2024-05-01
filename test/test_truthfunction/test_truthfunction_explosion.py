"""------------------------------------------------------------------------------
                            Explosion Testing
                                explosion
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                EXPLOSION
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("str(p.lines[4][p.statementindex])", str(And(A, B))),
    ("(p.lines[4][p.levelindex])", 0),
    ("(p.lines[4][p.proofidindex])", 0),
    ("(p.lines[4][p.ruleindex])", t.explosion_name),
    ("(p.lines[4][p.linesindex])", "3"),
    ("(p.lines[4][p.proofsindex])", ""),
    ("(p.lines[4][p.commentindex])", "COMPLETE"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_explosion_clean_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(And(A, B))
    p.premise(A)
    p.premise(Not(A))
    p.negation_elim(1, 2)
    p.explosion(And(A, B))
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                EXPLOSION
                                Stopped Run
                                  
                No previous line to use (stopped_nosuchline)
------------------------------------------------------------------------------"""

# No previous line
testdata = [
    ("str(p.lines[1][p.statementindex])", t.blankstatement),
    ("(p.lines[1][p.levelindex])", 0),
    ("(p.lines[1][p.proofidindex])", 0),
    ("(p.lines[1][p.ruleindex])", t.explosion_name),
    ("(p.lines[1][p.linesindex])", "0"),
    ("(p.lines[1][p.proofsindex])", ""),
    ("(p.lines[1][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_nosuchline), 
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_explosion_nosuchline_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(And(A, B))
    # p.premise(A)
    # p.premise(Not(A))
    # p.negation_elim(1, 2)
    p.explosion(And(A, B))
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                EXPLOSION
                                Stopped Run
                                  
                No goal (stopped_nogoal)
------------------------------------------------------------------------------"""

# No goal
testdata = [
    ("str(p.lines[1][p.statementindex])", t.blankstatement),
    ("(p.lines[1][p.levelindex])", 0),
    ("(p.lines[1][p.proofidindex])", 0),
    ("(p.lines[1][p.ruleindex])", t.explosion_name),
    ("(p.lines[1][p.linesindex])", ""),
    ("(p.lines[1][p.proofsindex])", ""),
    ("(p.lines[1][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_nogoal), 
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_explosion_nogoal_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    #p.goal(And(A, B))
    # p.premise(A)
    # p.premise(Not(A))
    # p.negation_elim(1, 2)
    p.explosion(And(A, B))
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                EXPLOSION
                                Stopped Run
                                  
                Block is closed (stopped_blockclosed)
------------------------------------------------------------------------------"""

# block is not accessible


"""------------------------------------------------------------------------------
                                EXPLOSION
                                Stopped Run
                                  
                Statement Is Not False (stopped_notfalse)
------------------------------------------------------------------------------"""

# block is not accessible
testdata = [
    ("str(p.lines[3][p.statementindex])", t.blankstatement),
    ("(p.lines[3][p.levelindex])", 1),
    ("(p.lines[3][p.proofidindex])", 1),
    ("(p.lines[3][p.ruleindex])", t.explosion_name),
    ("(p.lines[3][p.linesindex])", "2"),
    ("(p.lines[3][p.proofsindex])", ""),
    ("(p.lines[3][p.commentindex])", t.stopped + t.stopped_connector + t.stopped_notfalse), 
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_explosion_notfalse_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(And(A, B))
    p.premise(A)
    p.hypothesis(Not(A))
    # p.negation_elim(1, 2)
    # p.closeblock()
    p.explosion(And(A, B))
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                EXPLOSION
                                Stopped Run
                                  
                Statement Is String Type (stopped_string)
------------------------------------------------------------------------------"""

# Statement is string type
testdata = [
    ("str(p.lines[3][p.statementindex])", "A"),
    ("p.lines[3][p.commentindex]", t.stopped + t.stopped_connector + t.stopped_string),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def _explosion_string_1(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(A)
    p.hypothesis(Not(A))
    p.hypothesis(A)
    p.negation_elim(1, 2)
    p.explosion('A')
    assert eval(input_n) == expected

# Does proof continue after it has been stopped
testdata = [
    ("len(p.lines)", 4),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def _explosion_stop_continue_2(input_n, expected):
    A = Wff('A')
    B = Wff('B')
    p = Proof()
    p.setlogic('C')
    p.goal(A)
    p.hypothesis(Not(A))
    p.hypothesis(A)
    p.negation_elim(1, 2)
    p.explosion('A')
    p.disjunction_intro(4, right=B)
    assert eval(input_n) == expected
        
