import pytest

from altrea.boolean import Wff, Not, And, Or, Implies, Iff
from altrea.truthfunction import Proof
from altrea.exception import *
A = Wff('A')
B = Wff('B')
globalproof = Proof()

"""NAND TESTS"""

"""Test 1: Does the nand elimination perform correctly?"""


"""Test 1: Does the nand introduction perform correctly?"""

