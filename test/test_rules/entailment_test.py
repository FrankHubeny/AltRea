"""------------------------------------------------------------------------------
                                ENTAILMENT
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import And, Implies, Iff, Not
from altrea.rules import Proof
t = Proof()
A = t.proposition('A')
B = t.proposition('B')
C = t.proposition('C')
D = t.proposition('D')
E = t.proposition('E')

"""------------------------------------------------------------------------------
                                Clean Run (rule)
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[2][prf.statementindex])", str(B)),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", "Conjunction Elim Left"),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.complete),
    ("prf.lines[2][prf.typeindex]", t.linetype_rule),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_entailment_rule_clean_1(input_n, expected):
    prf = Proof("testproof", "Special", "Trivial Proof")
    B = prf.proposition("B")
    prf.setlogic()
    prf.saveaxiom(
        "contradiction",
        "Contradiction",
        "All Contradictions Are True",
        And(prf.mvalpha, Not(prf.mvalpha)),
        [],
    )
    prf.axiom("contradiction", [B], [])
    prf.entailment(
        prf.mvalpha, 
        [And(prf.mvalpha, prf.mvbeta)], 
        name="conjeliml", 
        displayname= "Conjunction Elim Left", 
        description="Conjunction Elimination Left Side", 
        kind=prf.label_rule) 
    prf.goal(B)
    prf.rule("conjeliml", [prf.item(1).left, prf.item(1).right], [1])
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                Clean Run (axiom)
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 2),
    #
    ("str(prf.lines[1][prf.statementindex])", str(And(B, Not(B)))),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", "Contradiction"),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    ("prf.lines[1][prf.typeindex]", t.linetype_axiom),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_entailment_rule_clean_1(input_n, expected):
    prf = Proof("testproof", "Special", "Trivial Proof")
    B = prf.proposition("B")
    prf.setlogic()
    prf.entailment(
        And(prf.mvalpha, Not(prf.mvalpha)), 
        [], 
        name="contra", 
        displayname= "Contradiction", 
        description="Assume Contradictions", 
        kind=prf.label_axiom) 
    prf.goal(B)
    prf.axiom("contra", [B], [])
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                Clean Run (definition)
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[2][prf.statementindex])", str(B)),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", "A=B"),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.complete),
    ("prf.lines[2][prf.typeindex]", t.linetype_definition),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_entailment_definition_clean_1(input_n, expected):
    prf = Proof()
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    prf.entailment(
        prf.mvalpha, 
        [prf.mvbeta], 
        name="identity", 
        displayname= "A=B", 
        description="Everything Equals Everything", 
        kind=prf.label_definition) 
    prf.goal(B)
    prf.premise(A)
    prf.definition("identity", [A, B], [1])
    assert eval(input_n) == expected


