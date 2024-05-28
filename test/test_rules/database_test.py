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
                                SAVEAXIOM/ADDAXIOM
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                names required
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                ADDDEFINITION
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                names required
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                SAVEPROOF
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                names required
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                USEPROOF
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_nosuchproof
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_premisesdontmatch
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_nosubs
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_notwff
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                                stopped_notinteger
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_nosuchline
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                  Stopped Run
                               stopped_linescope
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                REMOVEDEFINITION
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                REMOVEAXIOM
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                DELETELOGIC
------------------------------------------------------------------------------"""

#altrea.data.deletelogic(logicname)
