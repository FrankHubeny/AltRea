"""------------------------------------------------------------------------------
                                DATABASE SET OF TESTS
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, Proposition, Falsehood, Truth
from altrea.rules import Proof
import altrea.data

t = Proof()
A = t.proposition('A')
B = t.proposition('B')
C = t.proposition('C')
D = t.proposition('D')
E = t.proposition('E')

logicname = '_test_'
logicdisplay = '_testdisplay_'
logicdescription = '_testdescription_'

connectors = [
    (logicname, 'And', 'Conjunction'), 
    (logicname, 'Or', 'Disjunction'), 
]
intelimrules = [
    (logicname, t.conjunction_elim_tag, 'self.conjunction_elim_name'),
    (logicname, t.conjunction_intro_tag, 'self.conjunction_intro_name'),
    (logicname, t.disjunction_elim_tag, 'self.disjunction_elim_name'),
    (logicname, t.disjunction_intro_tag, 'self.disjunction_intro_name'),

]
definitions = [
    (logicname, 'not_from_notnot', 'ConclusionPremises(Not({0}), [{0}])', 'Not From Not Not', 'Not Is the Same As What It Negates'),
    #(logicname, 'notnot_from_not', 'ConclusionPremises({0}, [Not({0})])', 'Not Not From Not', 'Not Is the Same As What It Negates'),
]
axioms = [                 
    (logicname, 'explosion', 'ConclusionPremises({1}, [{0}, Not({0})])', 'Explosion', 'From a Contradiction Derive Anything'),
    #(logicname, 'contradiction', 'ConclusionPremises(And({0}, Not({0})), [])', 'Contradiction', 'All Contradictions Are True'),
]


"""------------------------------------------------------------------------------
                                ADD LOGIC
------------------------------------------------------------------------------"""

# clean construction
altrea.data.addlogic(logicname, logicdisplay, logicdescription, connectors, intelimrules, definitions, axioms)

"""------------------------------------------------------------------------------
                                SETLOGIC
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ('len(prf.lines)', 1),
    #
    ("str(prf.lines[0][prf.statementindex])", t.blankstatement),
    ("prf.lines[0][prf.levelindex]", 0),
    ("prf.lines[0][prf.proofidindex]", 0),
    ("prf.lines[0][prf.ruleindex]", ""),
    ("prf.lines[0][prf.linesindex]", ""),
    ("prf.lines[0][prf.proofsindex]", ""),
    ("prf.lines[0][prf.commentindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_setlogic_clean_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    prf.setlogic(logicname)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_logicalreadydefined
------------------------------------------------------------------------------"""

# Error logic already defined
testdata = [
    ('len(prf.lines)', 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", "Set Logic"),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_logicalreadydefined),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_setlogic_logicalreadydefined_1(input_n, expected):
    prf = Proof()
    A = Wff('A')
    prf.setlogic(logicname)
    prf.setlogic(logicname)
    prf.goal(A)
    prf.setlogic()
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_logicalreadydefined
------------------------------------------------------------------------------"""

# Error logic already defined, but run with the empty logic
testdata = [
    ('len(prf.lines)', 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", "Set Logic"),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_logicalreadydefined),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_setlogic_logicalreadydefined_2(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    prf.setlogic(logicname)
    prf.setlogic()
    prf.goal(A)
    prf.setlogic()
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_logicnotfound
------------------------------------------------------------------------------"""

# Error logic already defined, but run with the empty logic
testdata = [
    ('len(prf.lines)', 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", "Set Logic"),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_logicnotfound),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_setlogic_logicnotfound_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    prf.setlogic('Hi')
    prf.goal(A)
    prf.setlogic()
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                SAVEAXIOM/AXIOM
                                with database
------------------------------------------------------------------------------"""

# Clean run saving and using an axiom with a database.

testdata = [
    ('len(prf.lines)', 2),
    #
    ("str(prf.lines[1][prf.statementindex])", str(And(A, Not(A)))),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", "Contradiction"),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", "test comment"),
    ("prf.lines[1][prf.typeindex]", t.linetype_axiom),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_axiom_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    prf.setlogic(logicname)
    prf.saveaxiom('contradiction', 'Contradiction', 'All Contradictions Are True', And(C, Not(C)), [])
    prf.goal(A)
    prf.axiom('contradiction', [A], comment='test comment')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                SAVEPROOF
------------------------------------------------------------------------------"""
# Clean run of saveproof.

testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", str(B)),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.conjunction_elim_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.complete),
    ("prf.lines[2][prf.typeindex]", t.linetype_transformationrule),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_saveproof_1(input_n, expected):
    prf = Proof('testproof', 'Special', 'Trivial Proof')
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.saveaxiom('contradiction', 'Contradiction', 'All Contradictions Are True', And(D, Not(D)), [])
    prf.axiom('contradiction', [B], [])
    prf.goal(B)
    prf.conjunction_elim(1, side='left')
    prf.saveproof()
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                SAVEPROOF
------------------------------------------------------------------------------"""

# Clean run of saveproof with premises.

testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", str(B)),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", t.implication_elim_name),
    ("prf.lines[3][prf.linesindex]", "1, 2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.complete),
    ("prf.lines[3][prf.typeindex]", t.linetype_transformationrule),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_saveproof_withpremises_1(input_n, expected):
    prf = Proof('modusponens', 'Modus Ponens', 'A saved proof with premises.')
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.goal(B)
    prf.premise(A)
    prf.premise(Implies(A, B))
    prf.implication_elim(1, 2)
    prf.saveproof()
    prf.saveproof()
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                names required
------------------------------------------------------------------------------"""

# Error: no name for proof enetered

testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", str(B)),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.conjunction_elim_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.complete),
    ("prf.lines[2][prf.typeindex]", t.linetype_transformationrule),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_saveproof_noname_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.saveaxiom('contradiction', 'Contradiction', 'All Contradictions Are True', And(D, Not(D)), [])
    prf.axiom('contradiction', [B], [])
    prf.goal(B)
    prf.conjunction_elim(1, side='left')
    prf.saveproof()
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                notcomplete
------------------------------------------------------------------------------"""

# Error: the proof is not complete

testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.saveproof_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_notcomplete),
    ("prf.lines[2][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_saveproof_notcomplete_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.saveaxiom('contradiction', 'Contradiction', 'All Contradictions Are True', And(D, Not(D)), [])
    prf.axiom('contradiction', [B], [])
    prf.goal(B)
    prf.saveproof()
    prf.conjunction_elim(1, side='left')
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                USEPROOF
------------------------------------------------------------------------------"""

# Clean run using the proof saved above.

testdata = [
    ('len(prf.lines)', 2),
    #
    ("str(prf.lines[1][prf.statementindex])", str(B)),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", "Special"),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", "test comment"),
    ("prf.lines[1][prf.typeindex]", t.linetype_savedproof),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_useproof_clean_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.goal(And(A, B))
    prf.useproof('testproof', [B], comment='test comment')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                USEPROOF
------------------------------------------------------------------------------"""

# Clean run using the proof saved above with premises.

testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", str(B)),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", "Modus Ponens"),
    ("prf.lines[3][prf.linesindex]", "1, 2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.complete),
    ("prf.lines[3][prf.typeindex]", t.linetype_savedproof),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_useproof_withpremises_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.goal(B)
    prf.premise(A)
    prf.premise(Implies(A, B))
    prf.useproof('modusponens', [A, B], [1, 2])
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                USEPROOF
                                stopped_notenoughsubs
------------------------------------------------------------------------------"""

# Clean run using the proof saved above with premises.

testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", "Modus Ponens"),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_notenoughsubs),
    ("prf.lines[3][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_useproof_notenoughsubs_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.goal(B)
    prf.premise(A)
    prf.premise(Implies(A, B))
    prf.useproof('modusponens', [A], [1, 2])
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_nosavedproof
------------------------------------------------------------------------------"""

# Error: no saved proof by that name

testdata = [
    ('len(prf.lines)', 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", "testpro"),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_nosavedproof),
    ("prf.lines[1][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_useproof_nosuchproof_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.goal(And(A, B))
    prf.useproof('testpro', [B])
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_premisesdontmatch
------------------------------------------------------------------------------"""

# Error: premises don't match

testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", "Modus Ponens"),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_premisesdontmatch),
    ("prf.lines[3][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_useproof_premisesdontmatch_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.goal(B)
    prf.premise(A)
    prf.premise(Implies(A, B))
    prf.useproof('modusponens', [A, B], [1, ])
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_nosubs
------------------------------------------------------------------------------"""

# Error: no substitution values

testdata = [
    ('len(prf.lines)', 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", "Special"),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_nosubs),
    ("prf.lines[1][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_useproof_nosubs_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.goal(And(A, B))
    prf.useproof('testproof', [])
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_notwff
------------------------------------------------------------------------------"""

# Error: substitution value was not an object

testdata = [
    ('len(prf.lines)', 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", "Special"),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_notwff),
    ("prf.lines[1][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_useproof_nosubs_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.goal(And(A, B))
    prf.useproof('testproof', [1])
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_notinteger
------------------------------------------------------------------------------"""

# Error: line number is not an integer

testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", "Modus Ponens"),
    ("prf.lines[3][prf.linesindex]", "1.3"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_notinteger),
    ("prf.lines[3][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_saveproof_notintegerh_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.goal(B)
    prf.premise(A)
    prf.premise(Implies(A, B))
    prf.useproof('modusponens', [A, B], [1, 1.3])
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_nosuchline
------------------------------------------------------------------------------"""

# Error: No such line.

testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", "Modus Ponens"),
    ("prf.lines[3][prf.linesindex]", "4"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_nosuchline),
    ("prf.lines[3][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_saveproof_notintegerh_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.goal(B)
    prf.premise(A)
    prf.premise(Implies(A, B))
    prf.useproof('modusponens', [A, B], [1, 4])
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_linescope
------------------------------------------------------------------------------"""

# Error: Line out of scope.

testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    ("prf.lines[4][prf.ruleindex]", "Modus Ponens"),
    ("prf.lines[4][prf.linesindex]", "1"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_linescope),
    ("prf.lines[4][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_saveproof_notintegerh_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.goal(B)
    prf.hypothesis(A)
    prf.implication_intro()
    prf.premise(Implies(A, B))
    prf.useproof('modusponens', [A, B], [1, 4])
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                REMOVEPROOF
------------------------------------------------------------------------------"""

testdata = [
    ('len(prf.lines)', 4),
    #
    ("str(prf.lines[3][prf.statementindex])", t.blankstatement),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    ("prf.lines[3][prf.ruleindex]", "modusponens"),
    ("prf.lines[3][prf.linesindex]", ""),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_nosavedproof),
    ("prf.lines[3][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_saveproof_removeproof_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.removeproof('modusponens')
    prf.goal(B)
    prf.premise(A)
    prf.premise(Implies(A, B))
    prf.useproof('modusponens', [A, B], [1, 2])
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                SAVEDEFINITION
------------------------------------------------------------------------------"""

# Clean run saving and using a definition.

testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", str(A)),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", "Same"),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.complete + t.dash_connector + "test comment"),
    ("prf.lines[2][prf.typeindex]", t.linetype_definition),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_savedefinition_clean_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.savedefinition(name='same', displayname='Same', description='One Letter Is Same As Other', conclusion=A, premise=[B])
    prf.goal(A)
    prf.premise(B)
    prf.definition('same', [B, A], [1], comment='test comment')
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                DEFINITION
                            stopped_nosuchdefinition
------------------------------------------------------------------------------"""

# Error: bad name

testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", "sam"),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_nosuchdefinition),
    ("prf.lines[2][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_usedefinition_nosuchdefinition_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.savedefinition(name='same', displayname='Same', description='One Letter Is Same As Other', conclusion=A, premise=[B])
    prf.goal(A)
    prf.premise(B)
    prf.definition('sam', [B, A], [1])
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                DEFINITION
                                stopped_premisesdontmatch
------------------------------------------------------------------------------"""

# Error: premises dont match

testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", "Same"),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_premisesdontmatch),
    ("prf.lines[2][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_usedefinition_premisesdontmatch_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.savedefinition(name='same', displayname='Same', description='One Letter Is Same As Other', conclusion=A, premise=[B])
    prf.goal(A)
    prf.premise(B)
    prf.definition('same', [B, A], [])
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                DEFINITION
                                stopped_notenoughsubs
------------------------------------------------------------------------------"""

# Error: premises dont match

testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", "Same"),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_notenoughsubs),
    ("prf.lines[2][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_usedefinition_notenoughsubs_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.savedefinition(name='same', displayname='Same', description='One Letter Is Same As Other', conclusion=A, premise=[B])
    prf.goal(A)
    prf.premise(B)
    prf.definition('same', [B], [1])
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                DEFINITION
                                stopped_notwff
------------------------------------------------------------------------------"""

# Error: substitution value is not a wff

testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", "Same"),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_notwff),
    ("prf.lines[2][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_usedefinition_notwff_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.savedefinition(name='same', displayname='Same', description='One Letter Is Same As Other', conclusion=A, premise=[B])
    prf.goal(A)
    prf.premise(B)
    prf.definition('same', [B, 'A'], [1])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                DEFINITION
                                Not Integers
------------------------------------------------------------------------------"""

# Error: not integer

testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", "Same"),
    ("prf.lines[2][prf.linesindex]", "1.1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_notinteger),
    ("prf.lines[2][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_usedefinition_notinteger_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.savedefinition(name='same', displayname='Same', description='One Letter Is Same As Other', conclusion=A, premise=[B])
    prf.goal(A)
    prf.premise(B)
    prf.definition('same', [B, A], [1.1])
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                REMOVEDEFINITION
------------------------------------------------------------------------------"""

# Error: not integer

testdata = [
    ('len(prf.lines)', 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", "same"),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_nosuchdefinition),
    ("prf.lines[2][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_usedefinition_nosuchdefinition_2(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    C = prf.proposition('C')
    D = prf.proposition('D')
    E = prf.proposition('E')
    prf.setlogic(logicname)
    prf.removedefinition(name='same')
    prf.goal(A)
    prf.premise(B)
    prf.definition('same', [B, A], [1])
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                REMOVEAXIOM
------------------------------------------------------------------------------"""

# Clean run saving and using an axiom with a database.

testdata = [
    ('len(prf.lines)', 2),
    #
    ("str(prf.lines[1][prf.statementindex])", t.blankstatement),
    ("prf.lines[1][prf.levelindex]", 0),
    ("prf.lines[1][prf.proofidindex]", 0),
    ("prf.lines[1][prf.ruleindex]", "contradiction"),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_nosuchaxiom),
    ("prf.lines[1][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_database_axiom_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    prf.setlogic(logicname)
    prf.removeaxiom('contradiction')
    prf.goal(A)
    prf.axiom('contradiction', [A])
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                DELETELOGIC
------------------------------------------------------------------------------"""

#altrea.data.deletelogic(logicname)
