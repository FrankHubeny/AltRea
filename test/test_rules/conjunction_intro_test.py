"""------------------------------------------------------------------------------
                                CONJUNCTION_INTRO
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import And
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
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[1][prf.statementindex])", str(A)),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(B)),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
    ("str(prf.lines[3][prf.statementindex])", str(And(B, A))),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    #("prf.lines[3][prf.ruleindex]", t.conjunction_intro_name),
    ("prf.lines[3][prf.linesindex]", "2, 1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.complete),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_intro_clean_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(And(B, A))
    prf.premise(A)
    prf.premise(B)
    prf.rule('conj intro', [prf.item(2), prf.item(1)], [2, 1])
    # prf.conjunction_intro(2, 1)
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                   Clean Run 2
------------------------------------------------------------------------------"""

# Clean test: reverse order of lines
testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[1][prf.statementindex])", str(A)),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(And(A, A))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    #("prf.lines[2][prf.ruleindex]", t.conjunction_intro_name),
    ("prf.lines[2][prf.linesindex]", "1, 1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.complete),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_intro_clean_2(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    prf.setlogic()
    prf.goal(And(A, A))
    prf.premise(A)
    prf.rule("conj intro", [A, A], [1, 1])
    # prf.conjunction_intro(1, 1)
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                              stopped_nosuchline
------------------------------------------------------------------------------"""

# The first line does not exist in the proof.
testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.conjunction_intro_name),
    ("prf.lines[3][prf.linesindex]", "3"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_nosuchline,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_intro_nosuchline_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(And(A, B))
    prf.premise(A)
    prf.premise(B)
    prf.rule("conj intro", [A, B], [3, 2])
    #prf.conjunction_intro(3, 2)
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                              stopped_nosuchline
------------------------------------------------------------------------------"""

# The second line does not exist in the proof.
testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.conjunction_intro_name),
    ("prf.lines[3][prf.linesindex]", "3"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_nosuchline,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_intro_nosuchline_2(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(And(A, B))
    prf.premise(A)
    prf.premise(B)
    prf.rule("conj intro", [A, B], [1, 3])
    # prf.conjunction_intro(1, 3)
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
    ("prf.lines[3][prf.levelindex]", 2),
    ("prf.lines[3][prf.proofidindex]", 2),
    ("prf.lines[3][prf.ruleindex]", t.conjunction_intro_name),
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
    prf.setlogic()
    prf.goal(And(A, B))
    prf.hypothesis(A)
    prf.hypothesis(B)
    prf.rule("conj intro", [A, B], [1, 2])
    #prf.conjunction_intro(1, 2)
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                              stopped_linescope
------------------------------------------------------------------------------"""

# The second line is not accessible.
testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 2),
    ("prf.lines[3][prf.proofidindex]", 2),
    ("prf.lines[3][prf.ruleindex]", t.conjunction_intro_name),
    ("prf.lines[3][prf.linesindex]", "1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_linescope,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_elim_linescope_2(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(And(A, B))
    prf.hypothesis(A)
    prf.hypothesis(B)
    prf.rule("conj intro", [A, B], [2, 1])
    # prf.conjunction_intro(2, 1)
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                             stopped_premiseslengthsdontmatch
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
        t.stopped + t.colon_connector + t.stopped_premiseslengthsdontmatch,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_conjunction_intro_premiseslengthsdontmatch_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(And(A, B))
    prf.premise(A)
    prf.rule("conj intro", [A, B], [])
    # prf.conjunction_intro(2, 1)
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected


