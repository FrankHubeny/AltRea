"""------------------------------------------------------------------------------
                                IMPLICATION_ELIM
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import Wff, And, Implies
from altrea.rules import Proof

A = Wff("A")
B = Wff("B")
C = Wff("C")
D = Wff("D")
E = Wff("E")
t = Proof()

"""------------------------------------------------------------------------------
                                Clean Run
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
    ("str(prf.lines[2][prf.statementindex])", str(Implies(A, B))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
    ("str(prf.lines[3][prf.statementindex])", str(B)),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.implication_elim_name),
    ("prf.lines[3][prf.linesindex]", "1, 2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.complete),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_elim_clean_1(input_n, expected):
    prf = Proof()
    A = Wff("A")
    B = Wff("B")
    prf.setlogic()
    prf.goal(B, comment="Modus Ponens")
    prf.premise(A)
    prf.premise(Implies(A, B))
    prf.implication_elim(1, 2)
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_nosuchline
------------------------------------------------------------------------------"""

# The first referenced line of the three does not exist in the proof.
testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.implication_elim_name),
    ("prf.lines[3][prf.linesindex]", "3"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_nosuchline,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_elim_nosuchline_1(input_n, expected):
    prf = Proof()
    A = Wff("A")
    B = Wff("B")
    prf.setlogic()
    prf.goal(B, comment="Modus Ponens")
    prf.premise(A)
    prf.premise(Implies(A, B))
    prf.implication_elim(3, 2)
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_notinteger                        
------------------------------------------------------------------------------"""

# The second referenced line of the three does not exist in the proof.
testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.implication_elim_name),
    ("prf.lines[3][prf.linesindex]", "-2.56789"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_notinteger,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_elim_notinteger_2(input_n, expected):
    prf = Proof()
    A = Wff("A")
    B = Wff("B")
    prf.setlogic()
    prf.goal(B, comment="Modus Ponens")
    prf.premise(A)
    prf.premise(Implies(A, B))
    prf.implication_elim(1, -2.56789)
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_linescope
------------------------------------------------------------------------------"""

# The first referenced line is not accessible.
testdata = [
    ("len(prf.lines)", 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.implication_elim_name),
    ("prf.lines[4][prf.linesindex]", "2"),
    ("prf.lines[4][prf.proofsindex]", ""),
    (
        "prf.lines[4][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_linescope,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_elim_linescope_1(input_n, expected):
    prf = Proof()
    A = Wff("A")
    B = Wff("B")
    prf.setlogic()
    prf.goal(B, comment="Modus Ponens")
    prf.premise(Implies(A, B))
    prf.hypothesis(A)
    prf.implication_intro()
    prf.implication_elim(2, 1)
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_linescope
------------------------------------------------------------------------------"""

# The second referenced line is not accessible.
testdata = [
    ("len(prf.lines)", 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", t.implication_elim_name),
    ("prf.lines[4][prf.linesindex]", "2"),
    ("prf.lines[4][prf.proofsindex]", ""),
    (
        "prf.lines[4][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_linescope,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_elim_linescope_2(input_n, expected):
    prf = Proof()
    A = Wff("A")
    B = Wff("B")
    prf.setlogic()
    prf.goal(B, comment="Modus Ponens")
    prf.premise(Implies(A, B))
    prf.hypothesis(A)
    prf.implication_intro()
    prf.implication_elim(1, 2)
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_notantecedent
------------------------------------------------------------------------------"""

# The first referenced line is an implication but the second is not the antecedent of it.
testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.implication_elim_name),
    ("prf.lines[3][prf.linesindex]", "1, 2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_notantecedent,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_elim_notantecedent_1(input_n, expected):
    prf = Proof()
    A = Wff("A")
    B = Wff("B")
    prf.setlogic()
    prf.goal(B, comment="Modus Ponens")
    prf.premise(Implies(A, B))
    prf.premise(And(A, A))
    prf.implication_elim(1, 2)
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_notantecedent
------------------------------------------------------------------------------"""

# The first referenced line is an implication but the second is not the antecedent of it.
testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.implication_elim_name),
    ("prf.lines[3][prf.linesindex]", "2, 1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_notantecedent,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_elim_notantecedent_2(input_n, expected):
    prf = Proof()
    A = Wff("A")
    B = Wff("B")
    prf.setlogic()
    prf.goal(B, comment="Modus Ponens")
    prf.premise(Implies(A, B))
    prf.premise(And(A, A))
    prf.implication_elim(2, 1)
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_notmodusponens
------------------------------------------------------------------------------"""

# Neither line references an implication.
testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.implication_elim_name),
    ("prf.lines[3][prf.linesindex]", "1, 2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_notmodusponens,
    ),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_implication_elim_notmodusponens_1(input_n, expected):
    prf = Proof()
    A = Wff("A")
    B = Wff("B")
    prf.setlogic()
    prf.goal(B, comment="Modus Ponens")
    prf.premise(A)
    prf.premise(And(A, A))
    prf.implication_elim(1, 2)
    prf.hypothesis(A, comment="Nothing can be added after the proof is stopped.")
    assert eval(input_n) == expected
