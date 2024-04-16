
from sympy.abc import A, B, C, D, E
from altrea.tf import Proof
from altrea.exception import *
from contextlib import contextmanager
import pytest

globalproof = Proof(A)

"""INITIALIZATION TESTS"""

"""Test 1: Are initialization parameters set correctly for a proof?"""

testdata = [
    ("p.name", ''), 
    ("p.goal", A & B),
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
    p = Proof(A & B)
    assert eval(input_n) == expected

"""Test 2: Are the additions of optional values set correctly?"""

testdata = [
    ("p.name", "Some Name"),
    ("p.comments", "Some Comment"),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_init_2(input_n, expected):
    p = Proof(A & B, name="Some Name", comments="Some Comment")
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
    p = Proof(A & B)
    p.addpremise(A, "A comment")
    assert eval(input_n) == expected

"""Test 2: Is the PremiseAtLowestLevel exception raised?"""

@pytest.mark.xfail(raises=PremiseAtLowestLevel)
def test_premise_2():
    p = Proof(A & B)
    p.addpremise(A)
    p.openblock(C)
    with pytest.raises(PremiseAtLowestLevel):
        p.addpremise(C)

"""Test 3: Is the premise entered as a string?"""

@pytest.mark.xfail(raises=StringType)
def test_premise_3():
    p = Proof(A & B)
    
    with pytest.raises(StringType):
        p.addpremise('C')

"""CLOSEBLOCK TESTS"""

"""Test 1: Is the block closed correctly?"""

testdata = [
    ("p.level", 1),
    ("lastlevel", 2),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_closeblock_1(input_n, expected):
    p = Proof(A & B)
    p.openblock(C)
    p.openblock(D)
    lastlevel = p.level
    p.closeblock()
    assert eval(input_n) == expected
    
"""Test 2: Is the CannotCloseStartingBlock raised?"""

@pytest.mark.xfail(raises=CannotCloseStartingBlock)
def test_closeblock_2():
    p = Proof(A & B)
    with pytest.raises(CannotCloseStartingBlock):
        p.closeblock()

"""DEMORGAN TESTS"""

"""Test 1: Derive ~A | ~B from ~(A & B)."""

testdata = [
    ("p.lines[len(p.lines)-1][p.statementindex]", ~A | ~B),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.demorgan_name),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_1(input_n, expected):
    p = Proof(~A | ~B)
    p.addpremise(~(A & B))
    p.demorgan(1)
    assert eval(input_n) == expected

"""Test 2: Derive ~A & ~B from ~(A | B)."""

testdata = [
    ("p.lines[len(p.lines)-1][p.statementindex]", ~A & ~B),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.demorgan_name),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_2(input_n, expected):
    p = Proof(~A & ~B)
    p.addpremise(~(A | B))
    p.demorgan(1)
    assert eval(input_n) == expected

"""Test 3: Derive ~(A & B) from ~A | ~B."""

testdata = [
    ("p.lines[len(p.lines)-1][p.statementindex]", ~(A & B)),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.demorgan_name),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_3(input_n, expected):
    p = Proof(~(A & B))
    p.addpremise(~A | ~B)
    p.demorgan(1)
    assert eval(input_n) == expected

"""Test 4: Derive ~(A | B) from ~A & ~B."""

testdata = [
    ("p.lines[len(p.lines)-1][p.statementindex]", ~(A | B)),
    ("p.lines[len(p.lines)-1][p.ruleindex]", globalproof.demorgan_name),
    ("p.status", globalproof.complete),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_demorgan_4(input_n, expected):
    p = Proof(~(A | B))
    p.addpremise(~A & ~B)
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
    p = Proof(~(A | B))
    p.addpremise(B)
    with pytest.raises(NotDeMorgan):
        p.demorgan(1)
    
"""Test 6: Is NoSuchLine raised?"""

@pytest.mark.xfail(raises=NoSuchLine)
def test_demorgan_6():
    p = Proof(~(A | B))
    p.addpremise(A)
    with pytest.raises(NoSuchLine):
        p.demorgan(2)

"""Test 7: Is ScopeError raised?"""

@pytest.mark.xfail(raises=ScopeError)
def test_demorgan_7():
    p = Proof(~(A | B))
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
    p.addpremise(A >> B)
    p.implies_elim(2,1)
    assert eval(input_n) == expected

