"""------------------------------------------------------------------------------
                            If and Only Iff Testing
                             coimplication_intro   coimplication_elim
------------------------------------------------------------------------------"""

import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff, F, T
from altrea.truthfunction import Proof
A = Wff('A')
B = Wff('B')
t = Proof()

"""------------------------------------------------------------------------------
                                    coimplication_elim
                                    Clean Run
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    coimplication_elim
                                  Stopped Run
                                  
                Line Does Not Exist (stopped_nosuchline)
------------------------------------------------------------------------------"""


"""------------------------------------------------------------------------------
                                    coimplication_elim
                                  Stopped Run
                                  
                Line Is Outside Accessible Scope (stopped_linescope)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    coimplication_intro
                                    Clean Run
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    coimplication_intro
                                  Stopped Run
                                  
                    Block Does Not Exist (stopped_nosuchblock)
------------------------------------------------------------------------------"""

"""------------------------------------------------------------------------------
                                    coimplication_intro
                                  Stopped Run
                                  
                Block Is Outside Accessible Scope (stopped_blockscope)
------------------------------------------------------------------------------"""
