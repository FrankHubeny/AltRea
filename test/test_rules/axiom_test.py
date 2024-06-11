"""------------------------------------------------------------------------------
                                AXIOM
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import Not, And, Or, Implies
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

# Clean test of contradiction and explosion

testdata = [
    ("len(prf.lines)", 5),
    #
    ("str(prf.lines[1][prf.statementindex])", str(And(C, Not(C)))),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", "Contradiction"),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    ("prf.lines[1][prf.typeindex]", t.linetype_axiom),
    #
    ("str(prf.lines[4][prf.statementindex])", str(B)),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", "Explosion"),
    ("prf.lines[4][prf.linesindex]", "2, 3"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.complete),
    ("prf.lines[4][prf.typeindex]", t.linetype_axiom),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_axiom_contradiction_explosion_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    B = prf.proposition("B")
    C = prf.proposition("C")
    prf.setlogic()
    prf.goal(B)
    prf.axiom("contradiction", [C])
    prf.conjunction_elim(1, prf.left)
    prf.conjunction_elim(1, prf.right)
    prf.axiom("explosion", [C, B], [2, 3])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Clean Run
------------------------------------------------------------------------------"""

# Clean test of double negation intro and elim

testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Not(Not(C)))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", "DN Intro"),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    ("prf.lines[2][prf.typeindex]", t.linetype_axiom),
    #
    ("str(prf.lines[3][prf.statementindex])", str(C)),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", "DN Elim"),
    ("prf.lines[3][prf.linesindex]", "2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", ""),
    ("prf.lines[3][prf.typeindex]", t.linetype_axiom),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_axiom_dn_intro_elim_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    B = prf.proposition("B")
    C = prf.proposition("C")
    prf.setlogic()
    prf.goal(B)
    prf.premise(C)
    prf.axiom("dneg intro", [C], [1])
    prf.axiom("dneg elim", [C], [2])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Clean Run
------------------------------------------------------------------------------"""

# Clean test of law of excluded middle and weak law of excluded middle

testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Or(C, Not(C)))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", "LEM"),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    ("prf.lines[2][prf.typeindex]", t.linetype_axiom),
    #
    ("str(prf.lines[3][prf.statementindex])", str(Or(Not(C), Not(Not(C))))),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", "Weak LEM"),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", ""),
    ("prf.lines[3][prf.typeindex]", t.linetype_axiom),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_axiom_dn_intro_elim_2(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    B = prf.proposition("B")
    C = prf.proposition("C")
    prf.setlogic()
    prf.goal(B)
    prf.premise(C)
    prf.axiom("lem", [C])
    prf.axiom("wlem", [C])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Clean Run
------------------------------------------------------------------------------"""

# Clean test of modus ponens.
testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Implies(A, B))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    ("prf.lines[2][prf.typeindex]", t.linetype_premise),
    #
    ("str(prf.lines[3][prf.statementindex])", str(B)),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", "Modus Ponens"),
    ("prf.lines[3][prf.linesindex]", "1, 2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.complete),
    ("prf.lines[3][prf.typeindex]", t.linetype_axiom),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_axiom_modusponens_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(B)
    prf.premise(A)
    prf.premise(Implies(A, B))
    prf.axiom("modus ponens", [A, B], [1, 2])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Clean Run
------------------------------------------------------------------------------"""

# Clean test of de morgan laws

testdata = [
    ("len(prf.lines)", 7),
    #
    ("str(prf.lines[1][prf.statementindex])", str(Or(A, B))),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", "Premise"),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    ("prf.lines[1][prf.typeindex]", t.linetype_premise),
    #
    ("str(prf.lines[2][prf.statementindex])", str(And(Not(A), Not(B)))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", "De Morgan"),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    ("prf.lines[2][prf.typeindex]", t.linetype_axiom),
    #
    ("str(prf.lines[3][prf.statementindex])", str(Or(A, B))),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", "De Morgan"),
    ("prf.lines[3][prf.linesindex]", "2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", ""),
    ("prf.lines[3][prf.typeindex]", t.linetype_axiom),
    #
    ("str(prf.lines[4][prf.statementindex])", str(And(A, B))),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", "Premise"),
    ("prf.lines[4][prf.linesindex]", ""),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", ""),
    ("prf.lines[4][prf.typeindex]", t.linetype_premise),
    #
    ("str(prf.lines[5][prf.statementindex])", str(Or(Not(A), Not(B)))),
    ("prf.lines[5][prf.levelindex]", 0),
    ("prf.lines[5][prf.proofidindex]", 0),
    ("prf.lines[5][prf.ruleindex]", "De Morgan"),
    ("prf.lines[5][prf.linesindex]", "4"),
    ("prf.lines[5][prf.proofsindex]", ""),
    ("prf.lines[5][prf.commentindex]", ""),
    ("prf.lines[5][prf.typeindex]", t.linetype_axiom),
    #
    ("str(prf.lines[6][prf.statementindex])", str(And(A, B))),
    ("prf.lines[6][prf.levelindex]", 0),
    ("prf.lines[6][prf.proofidindex]", 0),
    ("prf.lines[6][prf.ruleindex]", "De Morgan"),
    ("prf.lines[6][prf.linesindex]", "5"),
    ("prf.lines[6][prf.proofsindex]", ""),
    ("prf.lines[6][prf.commentindex]", ""),
    ("prf.lines[6][prf.typeindex]", t.linetype_axiom),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_axiom_demorgan_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(B)
    prf.premise(Or(A, B))
    prf.axiom("or to not and", [A, B], [1])
    prf.axiom("not and to or", [A, B], [2])
    prf.premise(And(A, B))
    prf.axiom("and to not or", [A, B], [4])
    prf.axiom("not or to and", [A, B], [5])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Stopped
                        restricted mode with no default axioms
------------------------------------------------------------------------------"""

# Clean test of double negation intro and elim

testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", "dneg intro"),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    (
        "prf.lines[2][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_nosuchaxiom,
    ),
    ("prf.lines[2][prf.typeindex]", ""),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_axiom_restricted_1(input_n, expected):
    prf = Proof()
    B = prf.proposition("B")
    C = prf.proposition("C")
    prf.setlogic()
    prf.setrestricted(True)
    prf.goal(B)
    prf.premise(C)
    prf.axiom("dneg intro", [C], [1])
    prf.axiom("dneg elim", [C], [2])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_nosuchaxiom
------------------------------------------------------------------------------"""

# Error: no such axiom

testdata = [
    ("len(prf.lines)", 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", "r"),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    (
        "prf.lines[1][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_nosuchaxiom,
    ),
    ("prf.lines[1][prf.typeindex]", ""),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_axiom_nosuchaxiom_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    B = prf.proposition("B")
    C = prf.proposition("C")
    prf.setlogic()
    prf.goal(B)
    prf.axiom("r", [C])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                             stopped_nosubs
------------------------------------------------------------------------------"""

# Error: no subs

testdata = [
    ("len(prf.lines)", 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", "r"),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    (
        "prf.lines[1][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_nosuchaxiom,
    ),
    ("prf.lines[1][prf.typeindex]", ""),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_axiom_nosubs_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    B = prf.proposition("B")
    C = prf.proposition("C")
    prf.setlogic()
    prf.goal(B)
    prf.axiom("r", [C])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_premisesdontmatch
------------------------------------------------------------------------------"""

# Error: The premises don't matched identified lines.
testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Implies(A, B))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    ("prf.lines[2][prf.typeindex]", t.linetype_premise),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", "Modus Ponens"),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_premisesdontmatch,
    ),
    ("prf.lines[3][prf.typeindex]", ""),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_axiom_premisesdontmatch_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(B)
    prf.premise(A)
    prf.premise(Implies(A, B))
    prf.axiom("modus ponens", [B, A], [1, 2])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_notwff
------------------------------------------------------------------------------"""

# Error: The substitution values are not instances of altrea.boolean.Wff.

testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Implies(A, B))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    ("prf.lines[2][prf.typeindex]", t.linetype_premise),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", "Modus Ponens"),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_notwff,
    ),
    ("prf.lines[3][prf.typeindex]", ""),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_axiom_notwff_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(B)
    prf.premise(A)
    prf.premise(Implies(A, B))
    prf.axiom("modus ponens", [A, "A"], [1, 2])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_notinteger
------------------------------------------------------------------------------"""

# Error: A line number is not an integer.

testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Implies(A, B))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    ("prf.lines[2][prf.typeindex]", t.linetype_premise),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", "Modus Ponens"),
    ("prf.lines[3][prf.linesindex]", "2.1"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_notinteger,
    ),
    ("prf.lines[3][prf.typeindex]", ""),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_axiom_notinteger_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(B)
    prf.premise(A)
    prf.premise(Implies(A, B))
    prf.axiom("modus ponens", [A, B], [1, 2.1])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_nosuchline
------------------------------------------------------------------------------"""

# Error: A line number is not a previoous line of the proof.

testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Implies(A, B))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    ("prf.lines[2][prf.typeindex]", t.linetype_premise),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", "Modus Ponens"),
    ("prf.lines[3][prf.linesindex]", "3"),
    ("prf.lines[3][prf.proofsindex]", ""),
    (
        "prf.lines[3][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_nosuchline,
    ),
    ("prf.lines[3][prf.typeindex]", ""),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_axiom_nosuchline_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(B)
    prf.premise(A)
    prf.premise(Implies(A, B))
    prf.axiom("modus ponens", [A, B], [3, 2])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_linescope
------------------------------------------------------------------------------"""

# Error: A line number is not a previoous line of the proof.

testdata = [
    ("len(prf.lines)", 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", "Modus Ponens"),
    ("prf.lines[4][prf.linesindex]", "1"),
    ("prf.lines[4][prf.proofsindex]", ""),
    (
        "prf.lines[4][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_linescope,
    ),
    ("prf.lines[4][prf.typeindex]", ""),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_axiom_linescope_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.goal(B)
    prf.hypothesis(A)
    prf.implication_intro()
    prf.premise(Implies(A, B))
    prf.axiom("modus ponens", [A, B], [1, 3])
    assert eval(input_n) == expected
