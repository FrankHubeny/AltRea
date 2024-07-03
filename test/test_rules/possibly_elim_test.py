"""------------------------------------------------------------------------------
                                    POSSIBLY_ELIM
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import Possibly
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
    ("str(prf.lines[1][prf.statementindex])", str(A)),
    ("prf.lines[1][prf.levelindex]", 1),
    ("prf.lines[1][prf.proofidindex]", 1),
    ("prf.lines[1][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Possibly(A))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.possibly_elim_rulename),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", t.complete),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_possibly_elim_clean_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    prf.setlogic()
    
    prf.goal(Possibly(A))
    
    prf.openstrictsubproof()
    prf.hypothesis(A)
    prf.closestrictsubproof()
    prf.possibly_elim()

    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                                Error: ruleclass
------------------------------------------------------------------------------"""

testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[1][prf.statementindex])", str(A)),
    ("prf.lines[1][prf.levelindex]", 1),
    ("prf.lines[1][prf.proofidindex]", 1),
    ("prf.lines[1][prf.ruleindex]", t.hypothesis_name),
    ("prf.lines[1][prf.linesindex]", ""),
    ("prf.lines[1][prf.proofsindex]", ""),
    ("prf.lines[1][prf.commentindex]", ""),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 1),
    ("prf.lines[2][prf.proofidindex]", 1),
    ("prf.lines[2][prf.ruleindex]", t.possibly_elim_name),  # stopped, so name not rulename
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    (
        "prf.lines[2][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_ruleclass,
    ),
    #
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_possibly_elim_ruleclass_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(True)
    A = prf.proposition("A")
    prf.setlogic()
    
    prf.goal(Possibly(A))
    
    prf.openstrictsubproof()
    prf.hypothesis(A)
    prf.proofrules = prf.rule_axiomatic
    prf.possibly_elim()

    assert eval(input_n) == expected
