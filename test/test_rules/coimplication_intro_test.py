"""------------------------------------------------------------------------------
                                COIMPLICATION_INTRO
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import Implies, Iff, And
from altrea.rules import Proof

t = Proof()
A = t.proposition("A")
B = t.proposition("B")
C = t.proposition("C")
D = t.proposition("D")
E = t.proposition("E")

"""------------------------------------------------------------------------------
                                Clean Run
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[1][prf.statementindex])", str(And(Implies(A, B), Implies(B, A)))),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Iff(A, B))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    #("prf.lines[2][prf.ruleindex]", t.coimplication_intro_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.complete),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_coimplication_intro_clean_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    prf.goal(Iff(A, B))
    prf.premise(And(Implies(A, B), Implies(B, A)))
    prf.rule("coimp intro", [A, B], [1])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                              stopped_nosuchline
------------------------------------------------------------------------------"""

# The first line does not exist in the proof.
testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    #("prf.lines[2][prf.ruleindex]", t.coimplication_intro_name),
    ("prf.lines[2][prf.linesindex]", "0"),
    ("prf.lines[2][prf.proofsindex]", ""),
    (
        "prf.lines[2][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_nosuchline,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_coimplication_elim_nosuchline_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    prf.goal(Iff(A, B))
    prf.premise(And(Implies(A, B), Implies(B, A)))
    prf.rule("coimp intro", [A, B], [0])
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                stopped_linescope
------------------------------------------------------------------------------"""

# The first line is not accessible.
testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    #("prf.lines[3][prf.ruleindex]", t.coimplication_intro_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_linescope,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_coimplication_intro_linescope_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    
    prf.goal(Iff(A, B))
    
    prf.opensubproof()
    prf.hypothesis(And(Implies(A, B), Implies(B, A)))
    prf.closesubproof()
    prf.implication_intro()
    prf.rule("coimp intro", [A, B], [1])
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")

    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                stopped_premisesdontmatch
------------------------------------------------------------------------------"""

# The premises don't match.
testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    #("prf.lines[3][prf.ruleindex]", t.coimplication_intro_name),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_premisesdontmatch,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_coimplication_intro_premisesdontmatch_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    prf.goal(Iff(A, B))
    prf.premise(And(Implies(A, B), Implies(B, A)))
    prf.premise(A)
    prf.rule("coimp intro", [A, B], [2])
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected


