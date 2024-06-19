"""------------------------------------------------------------------------------
                                ENTAILMENT
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