"""------------------------------------------------------------------------------
                                ENTAILMENT
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import And, Implies, Iff, Or, Necessary
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

# Clean test of coimplication intro and elim by definitiion

testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[1][prf.statementindex])", str(Or(A, B))),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    ("prf.lines[1][prf.typeindex]", t.linetype_premise),
    #
    ("str(prf.lines[2][prf.statementindex])", str(And(A, B))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    ("prf.lines[2][prf.typeindex]", t.linetype_premise),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_item_clean_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    prf.goal(Implies(Or(A, B), And(A, B)))
    prf.premise(prf.item(0).left)
    prf.premise(prf.item(0).right)
    
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                Clean Run
------------------------------------------------------------------------------"""

# Clean test of coimplication intro and elim by definitiion

testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[1][prf.statementindex])", str(Necessary(A))),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    ("prf.lines[1][prf.typeindex]", t.linetype_premise),
    #
    ("str(prf.lines[2][prf.statementindex])", str(A)),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", "Necessary Elim"),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    ("prf.lines[2][prf.typeindex]", t.linetype_rule),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_item_clean_2(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    prf.goal(Implies(Or(A, B), And(A, B)))
    prf.premise(Necessary(A))
    prf.rule('nec elim', [prf.item(1).wff], [1])
    
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                Clean Run
------------------------------------------------------------------------------"""

# Clean test of coimplication intro and elim by definitiion

testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[1][prf.statementindex])", str(Necessary(A))),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    ("prf.lines[1][prf.typeindex]", t.linetype_premise),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Necessary(B))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    ("prf.lines[2][prf.typeindex]", t.linetype_premise),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_item_clean_3(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    prf.goal(And(Necessary(A), Necessary(B)))
    prf.premise(prf.item(0).left)
    prf.premise(prf.item(0).right)
    
    assert eval(input_n) == expected


