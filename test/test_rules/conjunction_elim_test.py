"""------------------------------------------------------------------------------
                                CONJUNCTION_ELIM
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import And, Implies, Iff
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
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[2][prf.statementindex])", str(A)),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    #("prf.lines[2][prf.ruleindex]", t.coimplication_intro_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    (
        "prf.lines[2][prf.commentindex]",
        "The left side is the default.",
    ),
    #
    ("str(prf.lines[3][prf.statementindex])", str(B)),
    ("prf.lines[3][prf.levelindex]", 1),
    ("prf.lines[3][prf.proofidindex]", 1),
    #("prf.lines[3][prf.ruleindex]", t.coimplication_intro_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        "Now do the right side.",
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_elim_clean_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    prf.goal(Iff(And(A, B), And(B, A)))
    prf.hypothesis(And(A, B))
    prf.rule('conj elim l', [A, B], [1], comment='The left side is the default.')
    prf.rule('conj elim r', [A, B], [1], comment='Now do the right side.')
    #prf.conjunction_elim(1, side='left', comment='The left side is the default.')
    #prf.conjunction_elim(1, side='right', comment='Now do the right side.')
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                              stopped_nosuchline
------------------------------------------------------------------------------"""

# The line does not exist in the proof.
testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    #("prf.lines[2][prf.ruleindex]", "Conjunction Elim"),
    ("prf.lines[2][prf.linesindex]", "0"),
    ("prf.lines[2][prf.proofsindex]", ""),#
    (
        "prf.lines[2][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_nosuchline,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_elim_nosuchline_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    B = prf.proposition("B")
    C = prf.proposition("C")
    prf.setlogic()
    prf.goal(C)
    prf.premise(And(A, B))
    #prf.conjunction_elim(0, side="left")
    prf.rule('conj elim l', [A, B], [0])
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                              stopped_linescope
------------------------------------------------------------------------------"""

# The line is not accessible.
testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 2),
    ("prf.lines[3][prf.proofidindex]", 2),
    #("prf.lines[3][prf.ruleindex]", t.conjunction_elim_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_linescope,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_elim_linescope_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    B = prf.proposition("B")
    C = prf.proposition("C")
    prf.setlogic()
    prf.goal(C)
    prf.hypothesis(And(A, B))
    prf.hypothesis(C)
    prf.rule('conj elim l', [A, B], [1])
    #prf.conjunction_elim(1, side="left")
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                             stopped_premisesdontmatch
------------------------------------------------------------------------------"""

# The line is not a conjunction.
testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    #("prf.lines[2][prf.ruleindex]", t.conjunction_elim_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    (
        "prf.lines[2][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_premisesdontmatch,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_elim_premisesdontmatch_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    C = prf.proposition("C")
    prf.setlogic()
    prf.goal(C)
    prf.premise(A)
    prf.rule("conj elim l", [A, C], [1])
    #prf.conjunction_elim(1, side="left")
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected


