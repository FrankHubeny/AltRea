"""------------------------------------------------------------------------------
                                DEFINITION
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import And, Implies, Iff
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
    ('len(prf.lines)', 6),
    #
    ("str(prf.lines[3][prf.statementindex])", str(And(Implies(A, B), Implies(B, A)))),
    ("prf.lines[3][prf.levelindex]", 0),
    ("prf.lines[3][prf.proofidindex]", 0),
    #("prf.lines[3][prf.ruleindex]", t.conjunction_intro_name),
    ("prf.lines[3][prf.linesindex]", "1, 2"),
    ("prf.lines[3][prf.proofsindex]", ""),
    ("prf.lines[3][prf.commentindex]", ""),
    ("prf.lines[3][prf.typeindex]", t.linetype_rule),
    #
    ("str(prf.lines[4][prf.statementindex])", str(Iff(A, B))),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    #("prf.lines[4][prf.ruleindex]", "Iff Intro"),
    ("prf.lines[4][prf.linesindex]", "3"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", ""),
    ("prf.lines[4][prf.typeindex]", t.linetype_definition),
    #
    ("str(prf.lines[5][prf.statementindex])", str(And(Implies(A, B), Implies(B, A)))),
    ("prf.lines[5][prf.levelindex]", 0),
    ("prf.lines[5][prf.proofidindex]", 0),
    #("prf.lines[5][prf.ruleindex]", "Iff Elim"),
    ("prf.lines[5][prf.linesindex]", "4"),
    ("prf.lines[5][prf.proofsindex]", ""),
    ("prf.lines[5][prf.commentindex]", ""),
    ("prf.lines[5][prf.typeindex]", t.linetype_definition),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_definition_iff_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    prf.goal(B)
    prf.premise(Implies(A, B))
    prf.premise(Implies(B, A))
    prf.rule("conj intro", [prf.item(1), prf.item(2)], [1, 2])
    prf.definition('iff intro', [A, B], [3])
    prf.definition('iff elim', [A, B], [4])
    
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                        Restricted True Stopped No Definitions
------------------------------------------------------------------------------"""

# Clean test of coimplication intro and elim by definitiion

testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    #("prf.lines[4][prf.ruleindex]", "iff intro"),
    ("prf.lines[4][prf.linesindex]", ""),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_nosuchdefinition),
    ("prf.lines[4][prf.typeindex]", ""),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_definition_restricted_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    prf.goal(B)
    prf.premise(Implies(A, B))
    prf.premise(Implies(B, A))
    prf.rule("conj intro", [prf.item(1), prf.item(2)], [1, 2])
    prf.definition('iff intro', [A, B], [3])
    prf.definition('iff elim', [A, B], [4])
    
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_premisesdontmatch
------------------------------------------------------------------------------"""

# Error: The premises do not match the identified lines.

testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    #("prf.lines[4][prf.ruleindex]", "Iff Intro"),
    ("prf.lines[4][prf.linesindex]", ""),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_premisesdontmatch),
    ("prf.lines[4][prf.typeindex]", ""),
    #
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_definition_premisesdontmatch_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    prf.setrestricted(False)
    prf.goal(B)
    prf.premise(Implies(A, B))
    prf.premise(Implies(B, A))
    prf.rule("conj intro", [prf.item(1), prf.item(2)], [1, 2])
    prf.definition('iff intro', [B, A], [3])
    
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  Stopped Run
                            stopped_premiseslengthsdontmatch
------------------------------------------------------------------------------"""

# Error: The premises do not match the identified lines.

testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    #("prf.lines[4][prf.ruleindex]", "Iff Intro"),
    ("prf.lines[4][prf.linesindex]", ""),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_premiseslengthsdontmatch),
    ("prf.lines[4][prf.typeindex]", ""),
    #
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_definition_premiseslengthsdontmatch_2(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    prf.setrestricted(False)
    prf.goal(B)
    prf.premise(Implies(A, B))
    prf.premise(Implies(B, A))
    prf.rule("conj intro", [prf.item(1), prf.item(2)], [1, 2])
    prf.definition('iff intro', [A, B], [])
    
    assert eval(input_n) == expected



"""------------------------------------------------------------------------------
                                stopped_nosubs
------------------------------------------------------------------------------"""


# Error: No substitutes were entered.

testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    #("prf.lines[4][prf.ruleindex]", "Iff Intro"),
    ("prf.lines[4][prf.linesindex]", ""),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_nosubs),
    ("prf.lines[4][prf.typeindex]", ""),
    #
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_definition_nosubs_1(input_n, expected):
    prf = Proof()
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    prf.setrestricted(False)
    prf.goal(B)
    prf.premise(Implies(A, B))
    prf.premise(Implies(B, A))
    prf.rule("conj intro", [prf.item(1), prf.item(2)], [1, 2])
    prf.definition('iff intro', [], [3])
    
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                stopped_notwff
------------------------------------------------------------------------------"""

# Error: Strings were used as substitution values.

testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    #("prf.lines[4][prf.ruleindex]", "Iff Intro"),
    ("prf.lines[4][prf.linesindex]", ""),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_notwff),
    ("prf.lines[4][prf.typeindex]", ""),
    #
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_definition_notwff_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    prf.goal(B)
    prf.premise(Implies(A, B))
    prf.premise(Implies(B, A))
    prf.rule("conj intro", [prf.item(1), prf.item(2)], [1, 2])
    prf.definition('iff intro', ['A', 'B'], [3])
    
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                                stopped_notinteger
------------------------------------------------------------------------------"""

# Error: A line number is not an integer.

testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
   # ("prf.lines[4][prf.ruleindex]", "Iff Intro"),
    ("prf.lines[4][prf.linesindex]", "-3.14"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_notinteger),
    ("prf.lines[4][prf.typeindex]", ""),
    #
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_definition_notinteger_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    prf.goal(B)
    prf.premise(Implies(A, B))
    prf.premise(Implies(B, A))
    prf.rule("conj intro", [prf.item(1), prf.item(2)], [1, 2])
    prf.definition('iff intro', [A, B], [-3.14])
    
    assert eval(input_n) == expected

    
"""------------------------------------------------------------------------------
                               stopped_nosuchline
------------------------------------------------------------------------------"""

# Error: The integer is not a previous line of the proof.

testdata = [
    ('len(prf.lines)', 5),
    #
    ("str(prf.lines[4][prf.statementindex])", t.blankstatement),
    ("prf.lines[4][prf.levelindex]", 0),
    ("prf.lines[4][prf.proofidindex]", 0),
    #("prf.lines[4][prf.ruleindex]", "Iff Intro"),
    ("prf.lines[4][prf.linesindex]", "4"),
    ("prf.lines[4][prf.proofsindex]", ""),
    ("prf.lines[4][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_nosuchline),
    ("prf.lines[4][prf.typeindex]", ""),
    #
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_definition_nosuchline_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    prf.goal(B)
    prf.premise(Implies(A, B))
    prf.premise(Implies(B, A))
    prf.rule("conj intro", [prf.item(1), prf.item(2)], [1, 2])
    prf.definition('iff intro', [A, B], [4])
    
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                               stopped_linescope
------------------------------------------------------------------------------"""

# Error: The refereneced line is out of scope.

testdata = [
    ('len(prf.lines)', 6),
    #
    ("str(prf.lines[5][prf.statementindex])", t.blankstatement),
    ("prf.lines[5][prf.levelindex]", 0),
    ("prf.lines[5][prf.proofidindex]", 0),
    #("prf.lines[5][prf.ruleindex]", "Iff Intro"),
    ("prf.lines[5][prf.linesindex]", "3"),
    ("prf.lines[5][prf.proofsindex]", ""),
    ("prf.lines[5][prf.commentindex]", t.stopped + t.colon_connector + t.stopped_linescope),
    ("prf.lines[5][prf.typeindex]", ""),
    #
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_definition_linescope_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    A = prf.proposition('A')
    B = prf.proposition('B')
    prf.setlogic()
    
    prf.goal(B)
    
    prf.opensubproof()
    prf.hypothesis(Implies(A, B))
    prf.hypothesis(Implies(B, A))
    prf.rule("conj intro", [prf.item(1), prf.item(2)], [1, 2])
    prf.closesubproof()
    prf.implication_intro()
    prf.definition('iff intro', [A, B], [3])
    
    assert eval(input_n) == expected


    
    