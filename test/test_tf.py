
from altrea.boolean import Wff, Not, And, Or, Implies, Iff, A, B, C, D, E
from altrea.truthfunction import Proof
from altrea.exception import *

import pytest

globalproof = Proof(A)

"""INITIALIZATION TESTS"""

"""Test 1: Are initialization parameters set correctly for a proof?"""

testdata = [
    ("p.name", ''), 
    #("p.goal", 'A & B'),
    ("p.blocklist", [ [0,[1]] ]),
    ("p.blocks", []),
    ("p.premises", []),
    ("p.status", ''),
    ("p.comments", ''),
    ("len(p.lines)", 1),
    #pytest.param("p.blocklist", [[0,1]], marks=pytest.mark.xfail),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_init_1(input_n, expected):
    p = Proof(And(A, B))
    assert eval(input_n) == expected

"""Test 2: Are the additions of optional values set correctly?"""

testdata = [
    ("p.name", "Some Name"),
    ("p.comments", "Some Comment"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_init_2(input_n, expected):
    p = Proof(And(A, B), name="Some Name", comments="Some Comment")
    assert eval(input_n) == expected

"""PREMISE TESTS"""

"""Test 1: Is a premise entered correctly?"""

testdata = [
    ("len(p.lines)", 2),
    ("p.lines[1][0]", A),
    ("p.lines[1][p.ruleindex]", globalproof.premisename),
    ("p.lines[1][p.commentindex]", "A comment"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_premise_1(input_n, expected):
    p = Proof(And(A, B))
    p.addpremise(A, "A comment")
    assert eval(input_n) == expected

"""Test 2: Is the PremiseAtLowestLevel exception raised?"""

@pytest.mark.xfail(raises=PremiseAtLowestLevel)
def test_premise_2():
    p = Proof(And(A, B))
    p.addpremise(A)
    p.openblock(C)
    with pytest.raises(PremiseAtLowestLevel):
        p.addpremise(C)

"""Test 3: Is the premise entered as a string?"""

@pytest.mark.xfail(raises=StringType)
def test_premise_3():
    p = Proof(And(A, B))
    
    with pytest.raises(StringType):
        p.addpremise('C')

"""CLOSEBLOCK TESTS"""

"""Test 1: Is the block closed correctly?"""

testdata = [
    ("p.level", 0),
    ("level1", 2),
    ("level2", 1),
    ("level3", 0),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_closeblock_1(input_n, expected):
    p = Proof(And(A, B))
    p.openblock(C)
    p.openblock(D)
    level1 = p.level
    p.closeblock()
    level2 = p.level
    blocklist = p.blocklist[1:]
    p.closeblock()
    level3 = p.level
    assert eval(input_n) == expected
    
"""Test 2: Is the CannotCloseStartingBlock raised?"""

@pytest.mark.xfail(raises=CannotCloseStartingBlock)
def test_closeblock_2():
    p = Proof(And(A, B))
    with pytest.raises(CannotCloseStartingBlock):
        p.closeblock()

"""DEMORGAN TESTS"""

"""Test 1: Derive ~A | ~B from ~(A & B)."""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Or(Not(A), Not(B)))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.demorgan_name),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_1(input_n, expected):
    p = Proof(Or(Not(A), Not(B)))
    p.addpremise(Not(And(A, B)))
    p.demorgan(1)
    assert eval(input_n) == expected

"""Test 2: Derive ~A & ~B from ~(A | B)."""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(And(Not(A), Not(B)))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.demorgan_name),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_2(input_n, expected):
    p = Proof(And(Not(A), Not(B)))
    p.addpremise(Not(Or(A, B)))
    p.demorgan(1)
    assert eval(input_n) == expected

"""Test 3: Derive ~(A & B) from ~A | ~B."""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Not(And(A, B)))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.demorgan_name),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_3(input_n, expected):
    p = Proof(Not(And(A, B)))
    p.addpremise(Or(Not(A), Not(B)))
    p.demorgan(1)
    assert eval(input_n) == expected

"""Test 4: Derive ~(A | B) from ~A & ~B."""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Not(Or(A, B)))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.demorgan_name),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_4(input_n, expected):
    p = Proof(Not(Or(A, B)))
    p.addpremise(And(Not(A), Not(B)))
    p.demorgan(1)
    assert eval(input_n) == expected

"""Demorgan Error checking.
            
- NotDeMorgan: The line could not be used by DeMorgan's rules.
- NoSuchLine: The line does not exist.
- ScopeError: The line is not accessible.
"""

"""Test 5: Is NotDeMorgan raised?"""

@pytest.mark.xfail(raises=NotDeMorgan)
def test_demorgan_5():
    p = Proof(Not(Or(A, B)))
    p.addpremise(B)
    with pytest.raises(NotDeMorgan):
        p.demorgan(1)
    
"""Test 6: Is NoSuchLine raised?"""

@pytest.mark.xfail(raises=NoSuchLine)
def test_demorgan_6():
    p = Proof(Not(Or(A, B)))
    p.addpremise(A)
    with pytest.raises(NoSuchLine):
        p.demorgan(2)

"""Test 7: Is ScopeError raised?"""

@pytest.mark.xfail(raises=ScopeError)
def test_demorgan_7():
    p = Proof(Not(Or(A, B)))
    p.openblock(A)
    p.closeblock()
    with pytest.raises(ScopeError):
        p.demorgan(1)

"""IMPLIES TESTS"""

"""Test 1: Does the elimination rule work correctly?"""

testdata = [
    ("p.lines[len(p.lines)-1][p.statementindex]", B),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.implies_elimname),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_implies_elim_1(input_n, expected):
    p = Proof(B)
    p.addpremise(A)
    p.addpremise(Implies(A, B))
    p.implies_elim(2,1)
    assert eval(input_n) == expected

"""Test 2: Does the introduction rule work correctly?"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Implies(B, A))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.implies_introname),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_implies_intro_1(input_n, expected):
    p = Proof(Implies(B, A))
    p.addpremise(A)
    p.openblock(B)
    p.reit(1)
    p.closeblock()
    p.implies_intro(1)
    assert eval(input_n) == expected

"""Implies Elim Error checking.

- NotAntecedent: The line without the Implies type could not be an antecedent.
- NotModusPonens: The lines could not be used by the implies eliminate rule.
- NoSuchLine: The line does not exist.
- ScopeError: The line is not accessible.
"""

@pytest.mark.xfail(raises=NotAntecedent)
def test_implies_elim_2():
    p = Proof(B)
    p.addpremise(C)
    p.addpremise(Implies(A, B))
    with pytest.raises(NotAntecedent):
        p.implies_elim(1,2)

@pytest.mark.xfail(raises=NotModusPonens)
def test_implies_elim_3():
    p = Proof(B)
    p.addpremise(C)
    p.addpremise(Or(A, B))
    with pytest.raises(NotModusPonens):
        p.implies_elim(1,2)

@pytest.mark.xfail(raises=NoSuchLine)
def test_implies_elim_4():
    p = Proof(B)
    p.addpremise(C)
    p.addpremise(Or(A, B))
    with pytest.raises(NoSuchLine):
        p.implies_elim(1,3)

@pytest.mark.xfail(raises=ScopeError)
def test_implies_elim_5():
    p = Proof(Not(Or(A, B)))
    p.addpremise(Implies(A, B))
    p.openblock(A)
    p.closeblock()
    with pytest.raises(ScopeError):
        p.implies_elim(1,2)

"""Implies Intro Error checking.

- NoSuchBlock: The line does not exist.
- BlockScopeError: The line is not accessible.
"""

@pytest.mark.xfail(raises=NoSuchBlock)
def test_implies_intro_2():
    p = Proof(Implies(B, A))
    p.addpremise(A)
    p.openblock(B)
    p.reit(1)
    p.closeblock()
    with pytest.raises(NoSuchBlock):
        p.implies_intro(3)

@pytest.mark.xfail(raises=BlockScopeError)
def test_implies_intro_3():
    p = Proof(Implies(B, A))
    p.addpremise(B)
    p.openblock(C)
    p.openblock(A)
    p.closeblock()
    p.closeblock()
    with pytest.raises(BlockScopeError):
        p.implies_intro(2)

"""This test addressing a formatting issue.  The table returns True rather than A >> A."""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Implies(A, A))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.implies_introname),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_intro_4(input_n, expected):
    p = Proof(Implies(A, A))
    p.openblock(A)
    p.closeblock()
    p.implies_intro(1)
    assert eval(input_n) == expected

"""LEM TESTS"""

"""Test 1: Does the LEM rule work correctly?"""

testdata = [
    ("str(p.lines[len(p.lines)-1][p.statementindex])", str(Or(A, Not(A)))),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.lem_name),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_lem_1(input_n, expected):
    p = Proof(Or(A, Not(A)))
    p.openblock(A)
    p.or_intro(1, right=Not(A))
    p.closeblock()
    p.openblock(Not(A))
    p.or_intro(3, left=A)
    p.closeblock()
    p.lem(1,2)
    assert eval(input_n) == expected
