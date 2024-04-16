# altrea/exception

"""This module contains the following exceptions:

- AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
- BlockNotAvailable: The block is outside the scope of the current block.
- BlockNotClosed: The block cannot be accessed until it is closed.
- ConclusionsNotTheSame: The conclusions of blocks are not the same.
- DisjunctNotFound: The disjunct from the disjunction on the specified line was not found
    as one of the assumptions starting a block.
- NoSuchLine: The referenced line does not exist in the proof.
- NotAntecedent: The statement is not the antecedent of the implication.
- NotAssumption: The referenced statement is not an assumption, the first line of a block.
- NotConjunction: The statement is not a conjunction.
- NotContradiction: Two referenced statements are not contradictions.
- NotDisjunction: The statement is not a disjunction.
- NotFalse: The referenced statement is not False.
- NotLemOpposites: The two statements are not the negations of each other.
- NotSameBlock: Two referenced statements are not from the same block.
- NotSameLevel: The two blocks are not at the same level.
- PremiseBeginsProof: A premise was added after other proof lines besides Premise or Goal.
- ScopeError: The referenced statement is not accessible.
"""

from sympy.logic.boolalg import And, Or, Not, Implies, Equivalent, Xor, Nand, Nor, Xnor
from sympy.core.symbol import Symbol

class AssumptionNotFound(Exception):
    """The assumption from a block does not match a disjunct of the disjunction.
    
    Parameters:
        assumption: The assumption that does not match one of the disjuncts in the disjunction.
        disjunction: The disjunction the containing the available disjuncts.
    """

    def __init__(self, 
                 assumption: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol,
                 disjunction: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol,
                 ):
        self.assumption = assumption
        self.disjunction = disjunction

    def __str__(self):
        return f'The assumption {self.assumption} does not match a disjunct in {self.disjunction}.'

class BlocksDisjunctsNotEqual(Exception):
    """The number of blocks and the number of disjuncts in the statement are not the same.
    
    Parameter:
        blockids: A list of blockids
        disjunction: The disjunction with not enough or too many disjuncts.
    """

    def __init__(
            self, 
            disjunction: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol,
            blockids: list
            ):
        self.blockids = blockids
        self.disjunction = disjunction
    
    def __str__(self):
        return f'The number of disjuncts in {self.disjunction} is not the same as the number of blocks {self.blockids}.'
    
class BlockNotAvailable(Exception):
    """The block is outside the scope of the current block.
    
    Parameter:
        blockid: The name of the block that is not available.
    """

    def __init__(self, blockid: str):
        self.blockid = blockid
    
    def __str__(self):
        return f'The block {self.blockid} is not available.'
    
class BlockNotClosed(Exception):
    """The block cannot be accessed until it is closed.
    
    Parameter:
        blockid: The name of the block that is not closed.
    """

    def __init__(self, blockid: str):
        self.blockid = blockid

    def __str__(self):
        return f'The block {self.block} is unavailable because it has not been closed.'
    
class BlockScopeError(Exception):
    """The referenced block is not accessible to the proof.
    
    Parameter:
        blockid: The name of the block that is accessible.
    """

    def __init__(self, blockid: str):
        self.blockid = blockid

    def __str__(self):
        return f'The block {self.blockid} is not accessible.'
    
class BlockClosed(Exception):
    """A proof line cannot be added to a block that is closed.
    
    Parameter:
        blockid: The name of the block that is not closed.
    """

    def __init__(self, blockid: int):
        self.blockid = blockid

    def __str__(self):
        return f'A proof line cannot be added to a closed block {self.blockid}.'

class BlockNotFound(Exception):
    """The referenced blockid does not exist.
    
    Parameter:
        blockid: The block id that could not be found.
    """

    def __init__(self, blockid: int):
        self.blockid = blockid

    def __str__(self):
        return f'The block id {self.blockid} could not be found.'
    
class CannotCloseStartingBlock(Exception):
    """The starting block of the proof cannot be closed except by completing the proof."""

    def __init__(self):
        pass

    def __str__(self) -> str:
        return f'The starting block of the proof cannot be closed except by completing the proof.'

class ConclusionsNotTheSame(Exception):
    """The conclusions of blocks are not the same.  
        
    Parameters:
        conclusion: The first conclusion to be matched by the others.
        nonmatching: The conclusion that did not match.
    """

    def __init__(self, 
                 conclusion: Not | And | Or | Implies | Equivalent | Symbol, 
                 nonmatching: Not | And | Or | Implies | Equivalent | Symbol
                 ):
        self.conclusion = conclusion
        self.nonmatching = nonmatching

    def __str__(self):
        return f'The conclusion {self.nonmatching} did not match {self.conclusion}.'
    
class DisjunctNotFound(Exception):
    """The disjunct from the disjunction on the specified line was not found
    as one of the assumptions starting a block.
    
    Parameters:
        disjunct: This is the disjunct that was not found.
        disjunction: This is the full disjunction with all disjuncts.
        line: This is the line containing the disjunction.
    """

    def __init__(self, 
                 disjunct: Not | And | Or | Implies | Equivalent | Symbol, 
                 disjunction: Or, 
                 line: int):
        self.disjunct = disjunct
        self.disjunction = disjunction
        self.line = line

    def __str__(self):
        return f'The disjunct {self.disjunct} from the disjunction {self.disjunction} on lin {self.line}\
            was not found as an assumption of any of the referenced blocks.'
    
class NoSuchLine(Exception):
    """The referenced line does not exist in the proof.

    Parameter:
        line: The line number requested by the call.
    """
    def __init__(self, line: int):
        self.line = line

    def __str__(self):
        return f'The referenced line number {self.line} does not exist in the proof.'

class NoSuchBlock(Exception):
    """The referenced block number does not exist in the proof.

    Parameter:
        blockid: The line number requested by the call.
    """
    def __init__(self, blockid: int):
        self.blockid = blockid

    def __str__(self):
        return f'The referenced line number {self.blockid} does not exist in the proof.'
    
class NotAntecedent(Exception):
    """The statement is not the antecedent of the implication.
    
    Parameters:
        antecedent: The statement offered as the antecedent.
        implication: The statement offered as the implication.
    """

    def __init__(self, 
                 antecedent: Not | And | Or | Implies | Equivalent | Symbol, 
                 implication: Not | And | Or | Implies | Equivalent | Symbol
                 ):
        self.antecedent = antecedent
        self.implication = implication

    def __str__(self):
        return f'The statement {self.antecedent} is not the antecedent of the implication {self.implication}.'
    
class NotAssumption(Exception):
    """The statement is not an assumption.

    Parameter:
        line: The line of the statement that is not an assumption.
    """

    def __init__(self, line: int):
        self.line = line

    def __str__(self):
        return f'The original statement {self.statement} does not match the rebuilt one: {self.rebuiltstatement}.'

class NotConjunction(Exception):
    """The statement is not a conjunction.
    
    Parameter:
        line: The line number of the statement in the proof.
        statement: The statement that caused the error.
    """

    def __init__(self, line, statement: Not | And | Or | Implies | Equivalent | Symbol):
        self.line = line
        self.statement = statement

    def __str__(self):
        return f'The statement {self.statement} on line {self.line} is not a conjunction.'
    
class NotContradiction(Exception):
    """Two referenced statements are not contradictions.

    Parameters:
        start: The start line of the alleged contradiction.
        end: The last line of the alleged contradiction.
    """

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __str__(self):
        return f'The statements at lines {self.start} and {self.end} are not contradictions.'

class NotDeMorgan(Exception):
    """The statement cannot be used in a DeMorgan rule.
    
    Parameter:
        statement: The statement that caused the error.
    """

    def __init__(self, line: int, statement: Not | And | Or):
        self.statement = statement

    def __str__(self):
        return f'The statement {self.statement} on line {self.line} cannot be used in a DeMorgan rule.'
       
class NotDisjunction(Exception):
    """The statement is not a disjunction.
    
    Parameter:
        line: The line number of the statement in the proof.
        statement: The statement that caused the error.
    """

    def __init__(self, line: int, statement: Not | And | Or | Implies | Equivalent | Symbol):
        self.line = line
        self.statement = statement

    def __str__(self):
        return f'The statement {self.statement} on line {self.line} is not a disjunction.'

class NotFalse(Exception):
    """The referenced statement is not False.

    Parameters:
        line: The number of the line claimed to be False.
        statement: The startment on the line.
    """

    def __init__(self, line: int, statement: Not | And | Or | Implies | Equivalent | Symbol):
        self.line = line
        self.statement = statement

    def __str__(self):
        return f'The line {self.line} contains {self.statement} which is not False.'

class NotModusPonens(Exception):
    """The two statements cannot be used for implication elimination or modus ponens.

    Parameters:
        line: The number of the line claimed to be False.
        statement: The startment on the line.
    """

    def __init__(self, 
                 firststatement: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol,  
                 secondstatement: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol):
        self.firststatement = firststatement
        self.secondstatement = secondstatement

    def __str__(self):
        return f'The two statements {self.firststatement} and {self.secondstatement} cannot be used in implication elimination.'

class NotSameBlock(Exception):
    """Two referenced statements are not from the same block.

    Parameter:
        start: The start line number of the block.
        startblock: The name of the block the start line is in.
        end: The last line number of the block.
        endblock: The name of the block the end line is in.
    """

    def __init__(self, start: int, startblock: list, end: int, endblock: list):
        self.start = start
        self.startblock = startblock
        self.end = end
        self.endblock = endblock

    def __str__(self):
        return f'The statement at line {self.start} is in block {self.startblock} \
            but the statement in lin {self.end} is in block {self.endblock}.'
    
class NotSameLevel(Exception):
    """The two levels are not the same.
    
    Parameter:
        firstlevel: The first level value.
        secondlevel: The second level value. 
    """
    
    def __init__(self, firstlevel: int, secondlevel: int):
        self.firstlevel = firstlevel
        self.secondlevel = secondlevel

    def __str__(self):
        return f'The block {self.firstlevel} is not at the same level as the second block {self.secondlevel}.'

class NotLemOpposites(Exception):
    """The two statements are not the negations of each other.
    
    Parameter:
        firststatement: The first statement.
        secondstatement: The second statement. 
    """
    
    def __init__(self, firststatement: int, secondstatement: int):
        self.firststatement = firststatement
        self.secondstatement = secondstatement

    def __str__(self):
        return f'The statement {self.firststatement} is not the negation of the second {self.secondstatement}.'

class NotSameStatements(Exception):
    """The two statements are not the same.
    
    Parameter:
        firststatement: The first statement.
        secondstatement: The second statement. 
    """
    
    def __init__(self, firststatement: int, secondstatement: int):
        self.firststatement = firststatement
        self.secondstatement = secondstatement

    def __str__(self):
        return f'The statement {self.firststatement} is not the same as the second {self.secondstatement}.'
    
class PremiseAtLowestLevel(Exception):
    """A premise can only be added at the lowest level of the proof.
    
    Parameter:
        premise: The premise that was added after other statements besides Premise were added.
    """

    def __init__(self, premise: Not | And | Or | Implies | Equivalent | Symbol):
        self.premise = premise
    
    def __str__(self):
        return f'The premise {self.premise} was added after proof lines besides Premise or Goal were added.'
    
class ScopeError(Exception):
    """The referenced statement is not accessible.

    Parameters:
        line: The line number requested by the call.
        linelevel: The level of the line based upon how many open blocks there are.
        currentlevel: The current level of the proof.
    """

    def __init__(self, lineblock: int):
        self.lineblock = lineblock

    def __str__(self):
        return f'A referenced line or block {self.lineblock} is not available for use.  Perhaps you need to close a block.'

class StringType(Exception):
    """The expression is of string type not a sympy boolean type.

    Parameters:
        expr: The expression that should be a boolean type.
    """

    def __init__(self, expr: str):
        self.expr = expr

    def __str__(self):
        return f'The expression {self.expr} is of string type not sympy boolean type. Try writing it without quotes.'