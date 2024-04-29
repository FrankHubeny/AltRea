"""------------------------------------------------------------------------------
                                Nor Testing
                            ndisjunction_intro   ndisjunction_elim
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                Ndisjunction_elim
                                Clean Run
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                Ndisjunction_elim
                                Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    Ndisjunction_intro
                                    Clean Run
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    Ndisjunction_intro
                                    Stopped Run
                                  
                    Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    Ndisjunction_intro
                                    Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

