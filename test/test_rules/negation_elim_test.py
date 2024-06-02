"""------------------------------------------------------------------------------
                                    NEGATION_ELIM
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import Wff, Not, And, Or, Implies, Iff, Proposition, Falsehood, Truth
from altrea.rules import Proof
t = Proof()
A = t.proposition('A')
B = t.proposition('B')
C = t.proposition('C')
D = t.proposition('D')
E = t.proposition('E')

"""------------------------------------------------------------------------------
                                Clean Run
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[1][prf.statementindex])", str(A)),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Not(A))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
    ("str(prf.lines[3][prf.statementindex])", str(Falsehood(And(A, Not(A))))),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.negation_elim_name),
    ("prf.lines[3][prf.linesindex]", "1, 2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.vacuous),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_elim_clean_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic()
    prf.goal(And(A, A))
    prf.premise(A)
    prf.premise(Not(A))
    prf.negation_elim(1, 2)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_nosuchline
------------------------------------------------------------------------------"""

# The first line does not exist in the proof.
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.negation_elim_name),
    ("prf.lines[3][prf.linesindex]", "3"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_elim_nosuchline_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic()
    prf.goal(And(A, A))
    prf.premise(A)
    prf.premise(Not(A))
    prf.negation_elim(3, 2)
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_nosuchline
------------------------------------------------------------------------------"""

# The second line does not exist in the proof.
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.negation_elim_name),
    ("prf.lines[3][prf.linesindex]", "3567"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_nosuchline),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_elim_nosuchline_2(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic()
    prf.goal(And(A, A))
    prf.premise(A)
    prf.premise(Not(A))
    prf.negation_elim(1, 3567)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_linescope
------------------------------------------------------------------------------"""

# The first line is not accessible.
testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.negation_elim_name),
    ("prf.lines[4][prf.linesindex]", "2"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_linescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_elim_linescope_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic()
    prf.goal(And(A, A))
    prf.premise(A)
    prf.hypothesis(Not(A))
    prf.implication_intro()
    prf.negation_elim(2, 1)
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_linescope
------------------------------------------------------------------------------"""

# The second line is not accessible.
testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.negation_elim_name),
    ("prf.lines[4][prf.linesindex]", "2"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_linescope),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_elim_linescope_2(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic()
    prf.goal(And(A, A))
    prf.premise(A)
    prf.hypothesis(Not(A))
    prf.implication_intro()
    prf.negation_elim(1, 2)
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_notcontradiction
------------------------------------------------------------------------------"""

# The two lines are not negations of each other.
testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.negation_elim_name),
    ("prf.lines[3][prf.linesindex]", "1, 2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_notcontradiction),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_elim_notcontradiction_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic()
    prf.goal(And(A, A))
    prf.premise(A)
    prf.premise(A)
    prf.negation_elim(1, 2)
    assert eval(input_n) == expected
