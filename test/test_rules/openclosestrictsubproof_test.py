"""------------------------------------------------------------------------------
                        OPENSTRICTSUBPROOF CLOSESTRICTSUBPROOF
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import Necessary, Implies, And
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
    #
    ("str(prf.lines[2][prf.statementindex])", str(Necessary(A))),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.reiterate_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_openclosestrictsubproof_clean_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    
    prf.goal(B)
    prf.premise(Necessary(A))
    
    prf.openstrictsubproof()
    prf.reiterate(1)
    prf.closestrictsubproof()

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Clean Run
------------------------------------------------------------------------------"""

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
    #
    ("str(prf.lines[2][prf.statementindex])", str(C)),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_openclosestrictsubproof_clean_2(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    B = prf.proposition("B")
    C = prf.proposition("C")
    prf.setlogic()
    
    prf.goal(B)
    prf.premise(Necessary(A))
    
    prf.openstrictsubproof()
    prf.addhypothesis(C)
    prf.closestrictsubproof()

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Clean Run
------------------------------------------------------------------------------"""

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
    #
    ("str(prf.lines[2][prf.statementindex])", str(Necessary(A))),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.reiterate_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_openclosestrictsubproof_clean_3(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    
    prf.goal(B)
    prf.premise(Necessary(A))
    
    prf.openstrictsubproof()
    prf.reiterate(1)

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Clean Run
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 7),
    #
    ("str(prf.lines[5][prf.statementindex])", str(Implies(B, B))),
    ("prf.lines[5][prf.levelindex]", 3),
    ("prf.lines[5][prf.proofidindex]", 3),
    ("prf.lines[5][prf.ruleindex]", t.implication_intro_name),
    ("prf.lines[5][prf.linesindex]", ""),
    ("prf.lines[5][prf.proofsindex]", "4-4"),
    ("prf.lines[5][prf.commentindex]", ""),
    #
    ("str(prf.lines[6][prf.statementindex])", str(Necessary(Implies(B, B)))),
    ("prf.lines[6][prf.levelindex]", 2),
    ("prf.lines[6][prf.proofidindex]", 2),
    ("prf.lines[6][prf.ruleindex]", t.necessary_intro_name),
    ("prf.lines[6][prf.linesindex]", "5"),
    ("prf.lines[6][prf.proofsindex]", ""),
    ("prf.lines[6][prf.commentindex]", ""),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_openclosestrictsubproof_clean_4(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    
    prf.goal(B)
    prf.premise(Necessary(A))
    
    prf.openstrictsubproof()
    prf.reiterate(1)
    prf.openstrictsubproof()
    prf.addhypothesis(B)
    prf.openstrictsubproof()
    prf.opensubproof()
    prf.hypothesis(B)
    prf.closesubproof()
    prf.implication_intro()
    prf.closestrictsubproof()
    prf.necessary_intro()

    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                stopped_closewrongsubproof
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 4),
    #
    ("str(prf.lines[1][prf.statementindex])", str(Necessary(A))),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", t.premise_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 1),
    ("prf.lines[3][prf.proofidindex]", 1),
    #("prf.lines[3][prf.ruleindex]", t.closestrictsubproof_name),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_closewrongsubproof),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_openclosestrictsubproof_closewrongsubproof_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    
    prf.goal(B)
    prf.premise(Necessary(A))
    
    prf.opensubproof()
    prf.hypothesis(B)
    prf.closestrictsubproof()
    prf.necessary_intro()

    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                stopped_unavailablesubproof
------------------------------------------------------------------------------"""

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
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.necessary_intro_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_unavailablesubproof),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_openclosestrictsubproof_unavailablesubproof_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    
    prf.goal(B)
    prf.premise(Necessary(A))
    
    prf.openstrictsubproof()
    prf.necessary_intro()

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                stopped_unavailablesubproof
------------------------------------------------------------------------------"""

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
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.possibly_elim_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_unavailablesubproof),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_openclosestrictsubproof_unavailablesubproof_2(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    
    prf.goal(B)
    prf.premise(Necessary(A))
    
    prf.openstrictsubproof()
    prf.possibly_elim()

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                stopped_unavailablesubproof
------------------------------------------------------------------------------"""

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
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.premise_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_unavailablesubproof),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_openclosestrictsubproof_unavailablesubproof_3(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    
    prf.goal(B)
    prf.premise(Necessary(A))
    
    prf.openstrictsubproof()
    prf.premise(And(A, B))

    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                stopped_unavailablesubproof
------------------------------------------------------------------------------"""

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
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    #("prf.lines[2][prf.ruleindex]", t.axiom_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_unavailablesubproof),
    #("prf.lines[2][prf.typeindex]", t.linetype_axiom),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_openclosestrictsubproof_unavailablesubproof_4(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    
    prf.goal(B)
    prf.premise(Necessary(A))
    
    prf.openstrictsubproof()
    prf.axiom("lem", [A], [])

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                stopped_unavailablesubproof
------------------------------------------------------------------------------"""

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
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    #("prf.lines[2][prf.ruleindex]", t.axiom_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_unavailablesubproof),
    #("prf.lines[2][prf.typeindex]", t.linetype_axiom),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_openclosestrictsubproof_unavailablesubproof_5(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition("A")
    B = prf.proposition("B")
    prf.setlogic()
    
    prf.goal(B)
    prf.premise(Necessary(A))
    
    prf.openstrictsubproof()
    prf.axiom("lem", [A], [])

    assert eval(input_n) == expected





