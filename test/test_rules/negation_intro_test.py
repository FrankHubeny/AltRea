"""------------------------------------------------------------------------------
                                    NEGATION_INTRO
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import Not, And, Falsehood
from altrea.rules import Proof

t = Proof()
A = t.proposition("A")
B = t.proposition("B")
C = t.proposition("C")
D = t.proposition("D")
E = t.proposition("E")

"""------------------------------------------------------------------------------
                                Clean Run 1
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ("len(prf.lines)", 7),
    #
    ("str(prf.lines[3][prf.statementindex])", str(A)),
    ("prf.lines[3][prf.levelindex]", 1),
    ("prf.lines[3][prf.proofidindex]", 1),
    ("prf.lines[3][prf.ruleindex]", t.reiterate_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", ""),
    #
    ("str(prf.lines[4][prf.statementindex])", str(Falsehood())),
    ("prf.lines[4][prf.levelindex]", 1),
    ("prf.lines[4][prf.proofidindex]", 1),
    #("prf.lines[4][prf.ruleindex]", t.negation_elim_name),
    ("prf.lines[4][prf.linesindex]", "3, 2"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", ""),
    #
    ("str(prf.lines[6][prf.statementindex])", str(Not(Not(A)))),
    ("prf.lines[6][prf.levelindex]", 0),
    ("prf.lines[6][prf.proofidindex]", 0),
    #("prf.lines[6][prf.ruleindex]", t.negation_intro_name),
    ("prf.lines[6][prf.linesindex]", "5"),
    ("prf.lines[6][prf.proofsindex]", ""),
    ("prf.lines[6][prf.commentindex]", t.complete),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_intro_clean_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    prf.setlogic()
    
    prf.goal(Not(Not(A)))
    prf.premise(A)
    
    prf.opensubproof()
    prf.hypothesis(Not(A))
    prf.reiterate(1)
    prf.rule("neg elim", [A], [3, 2])
    prf.implication_intro()
    prf.rule("neg intro", [Not(A), A], [5])

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Clean Run 2
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ("len(prf.lines)", 6),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Not(A))),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
    ("str(prf.lines[3][prf.statementindex])", str(Falsehood())),
    ("prf.lines[3][prf.levelindex]", 1),
    ("prf.lines[3][prf.proofidindex]", 1),
    #("prf.lines[3][prf.ruleindex]", t.negation_elim_name),
    ("prf.lines[3][prf.linesindex]", "1, 2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", ""),
    #
    ("str(prf.lines[5][prf.statementindex])", str(Not(And(A, Not(A))))),
    ("prf.lines[5][prf.levelindex]", 0),
    ("prf.lines[5][prf.proofidindex]", 0),
    #("prf.lines[5][prf.ruleindex]", t.negation_intro_name),
    ("prf.lines[5][prf.linesindex]", "4"),
    ("prf.lines[5][prf.proofsindex]", ""),
    ("prf.lines[5][prf.commentindex]", t.complete),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_negation_intro_clean_2(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    prf.setlogic()
    
    prf.goal(Not(And(A, Not(A))))
    
    prf.opensubproof()
    prf.hypothesis(A)
    prf.addhypothesis(Not(A))
    prf.rule("neg elim", [A], [1, 2])
    prf.implication_intro()
    prf.rule("neg intro", [prf.item(4).left, A], [4])

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                stopped_notfalse
------------------------------------------------------------------------------"""

# The previous statement must be false.
testdata = [
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    #("prf.lines[3][prf.ruleindex]", t.negation_intro_name),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_premisesdontmatch,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_intro_notfalse_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    prf.setlogic()
    
    prf.goal(Not(Not(A)))
    
    prf.opensubproof()
    prf.hypothesis(A)
    prf.implication_intro()
    prf.rule("neg intro", [A, A], [2])

    assert eval(input_n) == expected
