"""------------------------------------------------------------------------------
                                SUBSTITUTION
------------------------------------------------------------------------------"""

import pytest

from altrea.wffs import Not
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

# Clean test substituting one letter for another.

testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[2][prf.statementindex])", str(Not(B))),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.substitution_name),
    ("prf.lines[2][prf.linesindex]", "1"),
    ("prf.lines[2][prf.proofsindex]", ""),
    ("prf.lines[2][prf.commentindex]", ""),
    ("prf.lines[2][prf.typeindex]", t.linetype_substitution),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_substitution_clean_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    prf.proofrules = prf.rule_axiomatic
    B = prf.proposition("B")
    C = prf.proposition("C")
    prf.setlogic()
    prf.goal(C)
    prf.proofrules = prf.rule_naturaldeduction
    prf.premise(B)
    prf.proofrules = prf.rule_axiomatic
    prf.substitution(1, [B], [Not(B)])
    assert eval(input_n) == expected


"""------------------------------------------------------------------------------
                            stopped_rules
------------------------------------------------------------------------------"""

# Clean test substituting one letter for another.

testdata = [
    ("len(prf.lines)", 3),
    #
    ("str(prf.lines[2][prf.statementindex])", t.blankstatement),
    ("prf.lines[2][prf.levelindex]", 0),
    ("prf.lines[2][prf.proofidindex]", 0),
    ("prf.lines[2][prf.ruleindex]", t.substitution_name),
    ("prf.lines[2][prf.linesindex]", ""),
    ("prf.lines[2][prf.proofsindex]", ""),
    (
        "prf.lines[2][prf.commentindex]",
        t.stopped + t.colon_connector + t.stopped_ruleclass,
    ),
    ("prf.lines[2][prf.typeindex]", ""),
]


@pytest.mark.parametrize("input_n,expected", testdata)
def test_substitution_rules_ruleclass_1(input_n, expected):
    prf = Proof()
    prf.setrestricted(False)
    prf.proofrules = prf.rule_naturaldeduction
    B = prf.proposition("B")
    C = prf.proposition("C")
    prf.setlogic()
    prf.goal(C)
    prf.premise(B)
    prf.substitution(1, [B], [Not(B)])
    assert eval(input_n) == expected
