# altrea/tf.py

"""Provides functions to construct a proof in propositional logic.

The module contains the following functions:

- `equivalent_elim(first, second, comments)` - Given a biconditional and one of the terms return the other term as a
        new statement.
- `equivalent_intro(blockids, comments)` - Construct a biconditional given two blocks showing
        the implications in both directions.
- `closeblock()` - Closes the current block.
- `addpremise(premise, comments)` - Add a premise to the proof.
- `and_elim(line, comments)` - Adds a new line in the proof for each conjunct in the statement at line number `line`.
- `and_intro(first, second, comments)` - Joins as conjunctions the states at line numbers `first` and `second`
- `or_elim(line, blockids, comments)` - Check the correctness of a disjunction elimination line before adding it to the proof.
- `or_intro(newdisjunct, line, comments)` - The newdisjunct statement and the statement at the line number 
        become a disjunction.
- `explosion(expr, line, comments)` - An arbitrary statement is entered in the proof given a false statement preceding it.
- `implies_elim(first, second, comments)` - From an implication and its antecedent derive the consequent.
- `implies_intro(blockid, comments)` - The command puts an implication as a line in the proof one level below the blockid.
- `not_elim(first, second, comments)` - When two statements are contradictory a false line can be derived.
- `not_intro(blockid, comments)` - When an assumption generates a contradiction, the negation of the assumption
        can be used as a line of the proof in the next lower block.
- `openblock(statement)` - Opens a new block.
- `reit(line, comments)` - A statement that already exists which can be accessed can be reused.
"""

from sympy.logic.boolalg import And, Or, Not, Implies, Equivalent, Xor, Nand, Nor, Xnor
from sympy.core.symbol import Symbol
import sympy

import altrea.exception

class Proof:
    """
    This class contains methods to construct, verify, display, save and retrieve proofs in 
    in truth functional logic.
    """

    columns = ['Statement', 'Level', 'Block', 'Rule', 'Lines', 'Blocks', 'Comment']
    statementindex = 0
    levelindex = 1
    blockidindex = 2
    ruleindex = 3
    linesindex = 4
    blocksindex = 5
    commentindex = 6
    lowestlevel = 0
    complete = 'COMPLETE'
    completemessage = 'The proof is complete.'
    goalname = 'Goal'
    premisename = 'Premise'
    assumptionname = 'Assumption'
    or_introname = 'Or Intro'
    or_elimname = 'Or Elim'
    and_introname = 'And Intro'
    and_elimname = 'And Elim'
    reitname = 'Reiteration'
    implies_introname = 'Implies Intro'
    implies_elimname = 'Implies Elim'
    not_introname = 'Not Intro'
    not_elimname = 'Not Elim'
    indprfname = 'Indirect Proof'
    equivalent_introname = 'Iff Intro'
    equivalent_elimname = 'Iff Elim'
    xor_introname = 'Xor Intro'
    xor_elimname = 'Xor Elim'
    nand_introname = 'Nand Intro'
    nand_elimname = 'Nand Elim'
    nor_introname = 'Nor Intro'
    nor_elimname = 'Nor Elim'
    xnor_introname = 'Xnor Intro'
    xnor_elimname = 'Xnor Elim'
    lem_name = 'LEM'
    demorgan_name = 'DeMorgan'
    explosionname = 'Explosion'
    falsename = sympy.S.false
    warningmessage = 'Warning'

    def __init__(self, 
                 goal: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol, 
                 name: str = '', 
                 comments: str = ''):
        """Create a Proof object with optional premises, but a specific goal.
        
        Parameters:
            goal: The goal to be reached by the proof.
            name: The name assigned to the proof.
            comments: Comments that will go on the proof line associated with the goal.
        """
            
        self.name = name
        self.goal = goal
        self.comments = comments
        self.currentblock = [1]
        self.currentblockid = 0
        self.blocklist = [[self.lowestlevel, self.currentblock]]
        self.blocks = []
        self.level = self.lowestlevel
        self.status = ''
        self.premises = []
        self.lines = [[goal, 0, 0, self.goalname, '', '', self.comments]]

    def checkcomplete(self, statement):
        if statement == self.goal and self.level == self.lowestlevel:
            self.status = self.complete

    def reftwolines(self, first: int, second: int) -> str:
        return ''.join([str(first), ', ', str(second)])
    
    def getlevelblockstatements(self, blockid: int) -> tuple:
        level = self.blocklist[blockid][0]
        assumption = self.lines[self.blocklist[blockid][1][0]][self.statementindex]
        conclusion = self.lines[self.blocklist[blockid][1][1]][self.statementindex]
        return level, assumption, conclusion
    
    def getlevelstatement(self, line: int) -> tuple:
        level = self.lines[line][self.levelindex]
        statement = self.lines[line][self.statementindex]
        return level, statement

    def addstatement(self, 
                     statement: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol, 
                     rule: str, 
                     lines: list = '', 
                     blocks: list = '', 
                     comments: str =''):
        if self.status != self.complete:
            if type(statement) == str:
                raise altrea.exception.StringType(statement)
            else:
                self.checkcomplete(statement)
                if self.status == self.complete:
                    newcomment = self.complete
                else:
                    newcomment = comments
                self.lines.append([
                    statement, 
                    self.level, 
                    self.currentblockid, 
                    rule, 
                    lines, 
                    blocks, 
                    newcomment
                    ]
                )

    """The following functions are those intended to be called by the user."""

    def addpremise(self, 
                   premise: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol, 
                   comments: str = ''):
        """Add a premise to the proof.
        
        Parameters:
            premise: The premise to add to the proof.
            comments: Comments for this line of the proof.

        Exceptions:
            PremiseAtLowestLevel: A premise can only be added at the lowest level of the proof.
            StringType: The premise should not be entered as a string type.
        """

        if self.status != self.complete:
            if type(premise) == str:
                raise altrea.exception.StringType(premise)
            if self.level > 0:
                raise altrea.exception.PremiseAtLowestLevel(premise)
            self.premises.append(premise)
            self.checkcomplete(premise)
            if self.status == self.complete:
                newcomment = self.complete
            else:
                newcomment = comments
            self.lines.append([
                premise, 
                self.level, 
                self.currentblockid, 
                self.premisename, 
                '', 
                '', 
                newcomment
            ])
        
    def and_elim(self, line: int, comments: str = ''):
        """A conjunction is split into its individual conjuncts.
        
        Arguments:
            line: The line number of the conjunction to be split.

        Exceptions:
            NotConjunction: The statement is not a conjunction.
            NoSuchLine: The referenced line does not exist in the proof.
            ScopeError: The referenced statement is not accessible.
        """

        if self.status != self.complete:
            try:
                level, statement = self.getlevelstatement(line)
            except:
                raise altrea.exception.NoSuchLine(line)
            if level > self.level:
                raise altrea.exception.ScopeError(line)
            if type(statement) != And:
                raise altrea.exception.NotConjunction(line, statement)
            else:
                conjuncts = sympy.logic.boolalg.conjuncts(statement)
                for conjunct in conjuncts:
                    self.addstatement(
                        statement=conjunct, 
                            rule=self.and_elimname, 
                            lines=str(line),
                            comments=comments
                        )
    
    def and_intro(self, first: int, second: int, comments: str = ''):
        """The statement at first line number is joined with And to the statement at second
        line number.

        Parameters:
            first: The line number of the first conjunct.
            second: The line number of the second conjunct.

        Exceptions:
            NoSuchLine: The line number is not in the proof.
            ScopeError: The line must be in a level less than or equal to the current level.
        """

        if self.status != self.complete:
            try:
                firstlevel, firstconjunct = self.getlevelstatement(first)
            except:
                raise altrea.exception.NoSuchLine(first)
            if firstlevel > self.level:
                raise altrea.exception.ScopeError(first)
        
            try:
                secondlevel, secondconjunct = self.getlevelstatement(second)
            except:
                raise altrea.exception.NoSuchLine(second)
            if secondlevel > self.level:
                raise altrea.exception.ScopeError(second)
        
            andstatement = And(firstconjunct, secondconjunct)
            self.addstatement(
                statement=andstatement, 
                rule=self.and_introname, 
                lines=self.reftwolines(first, second), 
                comments=comments
            )

    def closeblock(self):
        """Closes the block of statements that the proof is currently in.
        
        Examples:
            >>> from sympy.abc import P, Q
            >>> from altrea.tf import Proof
            >>> from altrea.display import show
            >>> p = Proof(P | ~P)
            >>> p.openblock(P)
            >>> p.or_intro(~P,1)
            >>> p.closeblock()
            >>> p.openblock(~P)
            >>> p.or_intro(P,3)
            >>> p.closeblock()
            >>> p.lem(1,2)
            >>> show(p, latex=0)
                Statement  Level  Block        Rule Lines Blocks   Comment
            Line    P | ~P      0      0        Goal
            1            P      1      1  Assumption
            2       P | ~P      1      1    Or Intro     1
            3           ~P      1      2  Assumption
            4       P | ~P      1      2    Or Intro     3
            5       P | ~P      0      0         LEM         1, 2  COMPLETE

        Exceptions:
            CannotCloseStartingBlock: The lowest block is closed by completing the proof.
        """

        if self.status != self.complete:
            if self.currentblockid == 0:
                raise altrea.exception.CannotCloseStartingBlock()
            self.blocklist[self.currentblockid][1].append(len(self.lines)-1)
            self.level -= 1
            for b in range(len(self.blocklist)-1):
                if self.blocklist[b][0] == self.level and len(self.blocklist[b][1]) == 1:
                    self.currentblockid = b
                    self.currentblock = self.blocklist[b][1]

    def demorgan(self, line: int, comments: str = ''):
        """DeMorgan's rules for not, and and or are automatically constructed given a line number
        for which the rules apply.
        
        Parameters:
            line: The line DeMorgan's rules will be applied to.
            
        There are four scenarios in which to use this rule.  Each are listed below as an example.

        Examples:
            >>> from sympy.abc import A, B
            >>> from altrea.tf import Proof
            >>> from altrea.display import show
            >>> p = Proof(~A | ~B, comments="DeMorgan 1 of 4")
            >>> p.addpremise(~(A & B))
            >>> p.demorgan(1)
            >>> show(p, latex=0)
                 Statement  Level  Block      Rule Lines Blocks          Comment
            Line   ~A | ~B      0      0      Goal               DeMorgan 1 of 4
            1     ~(A & B)      0      0   Premise
            2      ~A | ~B      0      0  DeMorgan     1                COMPLETE

            >>> from sympy.abc import A, B
            >>> from altrea.tf import Proof
            >>> from altrea.display import show
            >>> p = Proof(~A & ~B, comments="DeMorgan 2 of 4")
            >>> p.addpremise(~(A | B))
            >>> p.demorgan(1)
            >>> show(p, latex=0)
                 Statement  Level  Block      Rule Lines Blocks          Comment
            Line   ~A & ~B      0      0      Goal               DeMorgan 2 of 4
            1     ~(A | B)      0      0   Premise
            2      ~A & ~B      0      0  DeMorgan     1                COMPLETE

            >>> from sympy.abc import A, B
            >>> from altrea.tf import Proof
            >>> from altrea.display import show
            >>> p = Proof(~(A & B), comments="DeMorgan 3 of 4")
            >>> p.addpremise(~A | ~B)
            >>> p.demorgan(1)
            >>> show(p, latex=0)
                 Statement  Level  Block      Rule Lines Blocks          Comment
            Line  ~(A & B)      0      0      Goal               DeMorgan 3 of 4
            1      ~A | ~B      0      0   Premise
            2     ~(A & B)      0      0  DeMorgan     1                COMPLETE

            >>> from sympy.abc import A, B
            >>> from altrea.tf import Proof
            >>> from altrea.display import show
            >>> p = Proof(~(A | B), comments="DeMorgan 4 of 4")
            >>> p.addpremise(~A & ~B)
            >>> p.demorgan(1)
            >>> show(p, latex=0)
                 Statement  Level  Block      Rule Lines Blocks          Comment
            Line  ~(A | B)      0      0      Goal               DeMorgan 4 of 4
            1      ~A & ~B      0      0   Premise
            2     ~(A | B)      0      0  DeMorgan     1                COMPLETE

        Exceptions:
            NotDeMorgan: The line could not be used by DeMorgan's rules.
            NoSuchLine: The line does not exist.
            ScopeError: The line is not accessible.
        """

        if self.status != self.complete:
            try:
                level, statement = self.getlevelstatement(line)
            except:
                raise altrea.exception.NoSuchLine(line)
            if level > self.level:
                raise altrea.exception.ScopeError(line)
            if type(statement) == Not:
                if type(statement.args[0]) == And:
                    andstatement = statement.args[0]
                    firstsubstatement = andstatement.args[0]
                    secondsubstatement = andstatement.args[1]
                    final = Or(Not(firstsubstatement), Not(secondsubstatement))
                elif type(statement.args[0]) == Or:
                    orstatement = statement.args[0]
                    firstsubstatement = orstatement.args[0]
                    secondsubstatement = orstatement.args[1]
                    final = And(Not(firstsubstatement), Not(secondsubstatement))
                else:
                    raise altrea.exception.NotDeMorgan(line, statement)
            elif type(statement) == Or:
                firstsubstatement = statement.args[0]
                secondsubstatement = statement.args[1]
                if len(statement.args) == 2:
                    if type(firstsubstatement) == Not and type(secondsubstatement) == Not:
                        final = Not(And(firstsubstatement.args[0], secondsubstatement.args[0]))
                else:
                    raise altrea.exception.NotDeMorgan(line, statement)
            elif type(statement) == And:
                firstsubstatement = statement.args[0]
                secondsubstatement = statement.args[1]
                if len(statement.args) == 2:
                    if type(firstsubstatement) == Not and type(secondsubstatement) == Not:
                        final = Not(Or(firstsubstatement.args[0], secondsubstatement.args[0]))
                else:
                    raise altrea.exception.NotDeMorgan(line, statement)
            else:
                raise altrea.exception.NotDeMorgan(line, statement)
            
            self.checkcomplete(final)
            if self.status == self.complete:
                newcomment = self.complete
            else:
                newcomment = comments
            self.lines.append([
                final, 
                self.level, 
                self.currentblockid, 
                self.demorgan_name, 
                str(line), 
                '', 
                newcomment
            ])

    def doublenegative(self, line: int, comments: str = ''):
        pass
    
    def equivalent_elim(self, first: int, second: int, comments: str = ''):
        """Given an iff statement and a proposition one can derive the other proposition.
        
        Parameters:
            first: A statement containing either a proposition or an iff statement.
            second: A second statement containing either a proposition or an iff statement.
            comments: Comments on this line of the proof.
        
        Exceptions:
            NoSuchLine: The line does not exist in the proof.
            NotEquivalence: The two statements cannot be used in equivalence elimination.
            ScopeError: The line is not accessible.
        """
        if self.status != self.complete:
            try:
                firstlevel, firststatement = self.getlevelstatement(first)
            except:
                raise altrea.exception.NoSuchLine(first)
            if firstlevel > self.level:
                raise altrea.exception.ScopeError(first)
            
            try:
                secondlevel, secondstatement = self.getlevelstatement(second)
            except:
                raise altrea.exception.NoSuchLine(second)
            if secondlevel > self.level:
                raise altrea.exception.ScopeError(first)
            
            if type(firststatement) == Equivalent:
                if firststatement.args[0] == secondstatement:
                    final = firststatement.args[1]
                elif firststatement.args[1] == secondstatement:
                    final = firststatement.args[0]
                else:
                    raise altrea.exception.NotEquivalence(firststatement, secondstatement)
            elif type(secondstatement) == Equivalent:
                if secondstatement.args[0] == firststatement:
                    final = secondstatement.args[1]
                elif secondstatement.args[1] == firststatement:
                    final = secondstatement.args[0]
                else:
                    raise altrea.exception.NotEquivalence(firststatement, secondstatement)
            else:
                raise altrea.exception.NotEquivalence(firststatement, secondstatement)
            
            self.checkcomplete(final)
            if self.status == self.complete:
                newcomment = self.complete
            else:
                newcomment = comments
            self.lines.append([
                final, 
                self.level, 
                self.currentblockid, 
                self.equivalent_elimname, 
                self.reftwolines(first, second), 
                '', 
                newcomment
            ])
                
    def equivalent_intro(self, blockids: list, comments: str = ''):
        pass

    def explosion(self, 
                  expr: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol, 
                  comments: str = ''):
        """An arbitrary statement is entered in the proof given a false statement preceding it.
        
        Parameters:
            expr: The statement to add to the proof.
            line: The line number of the proof containing the statement False.
            comments: A optional comment for this line of the proof.

        Exceptions:
            BlockClosed: A line cannot be added to a closed block.
            NoSuchLine: The referenced line does not exist in the proof.
            NotFalse: The referenced statement is not False.
            StringType: The statement should not be a string.
        """
        
        if self.status != self.complete:
            if type(expr) == str:
                raise altrea.exception.StringType(expr)
            line = len(self.lines) - 1
            if line == 0:
                raise altrea.exception.NoSuchLine(line)
            blockid = self.lines[line][self.blockidindex]
            if len(self.blocklist[blockid][1]) == 2:
                raise altrea.exception.BlockClosed(blockid)
            else:
                level, falsestatement = self.getlevelstatement(line)
                if level != self.level:
                    raise altrea.exception.ScopeError(line)
                if falsestatement != self.falsename:
                    raise altrea.exception.NotFalse(line, falsestatement)
                else:
                    self.addstatement(
                        statement=expr,
                        rule=self.explosionname,
                        lines=line,
                        comments=comments
                    )
            
    def implies_elim(self, first: int, second: int, comments: str = ''):
        """From an implication and its antecedent derive the consequent.
        
        Parameters:
            first: The line number of the first statement.
            second: The line number of the second statement.

        Examples:
            >>> from sympy.abc import A, B
            >>> from altrea.tf import Proof
            >>> from altrea.display import show
            >>> p = Proof(B)
            >>> p.addpremise(A)
            >>> p.addpremise(A >> B)
            >>> p.implies_elim(1,2)
            >>> show(p, latex=0)
                      Statement  Level  Block          Rule Lines Blocks   Comment
            Line              B      0      0          Goal
            1                 A      0      0       Premise
            2     Implies(A, B)      0      0       Premise
            3                 B      0      0  Implies Elim  1, 2         COMPLETE

        Exceptions:
            NotAntecedent: The statement is not the antecedent of the implication.
            NoSuchLine: The referenced line does not exist in the proof.
            NotModusPonens: The two statements cannot be used in implication elimination.
            ScopeError: The referenced statement is not accessible.
        """

        if self.status != self.complete:
            try:
                firstlevel, firststatement = self.getlevelstatement(first)
            except:
                raise altrea.exception.NoSuchLine(first)
            if firstlevel > self.level:
                raise altrea.exception.ScopeError(first)
        
            try:
                secondlevel, secondstatement = self.getlevelstatement(second)
            except:
                raise altrea.exception.NoSuchLine(second)
            if secondlevel > self.level:
                raise altrea.exception.ScopeError(second)
        
            if type(firststatement) == Implies:
                if secondstatement != firststatement.args[0]:
                    raise altrea.exception.NotAntecedent(firststatement, secondstatement)
                else:
                    self.checkcomplete(firststatement.args[1])
                    if self.status == self.complete:
                        newcomment = self.complete
                    else:
                        newcomment = comments
                    self.lines.append([
                        firststatement.args[1], 
                        self.level, 
                        self.currentblockid, 
                        self.implies_elimname, 
                        self.reftwolines(first, second), 
                        '', 
                        newcomment
                        ]
                    )
            elif type(secondstatement) == Implies:
                if firststatement != secondstatement.args[0]:
                    raise altrea.exception.NotAntecedent(secondstatement, firststatement)
                else:
                    self.checkcomplete(secondstatement.args[1])
                    if self.status == self.complete:
                        newcomment = self.complete
                    else:
                        newcomment = comments
                    self.lines.append([
                        secondstatement.args[1], 
                        self.level, 
                        self.currentblockid, 
                        self.implies_elimname, 
                        self.reftwolines(first, second), 
                        '', 
                        newcomment
                        ]
                    )                   
            else:
                raise altrea.exception.NotModusPonens(firststatement, secondstatement)

    def implies_intro(self, blockid: int | str, comments: str = ''):
        """The command puts an implication as a line in the proof one level below the blockid.
        
        Parameters:
            blockid: The block identified by [start, end].
            comments: Comments added to the line.

        Examples:
            >>> p = Proof(P >> (Q >> P))
            >>> p.openblock(P)
            >>> p.openblock(Q)
            >>> p.reit(1)
            >>> p.closeblock()
            >>> p.implies_intro(2)
            >>> p.closeblock()
            >>> p.implies_intro(1)
            >>> show(p, latex=0)
                                  Statement  Level  Block  ... Lines Blocks   Comment
            Line  Implies(P, Implies(Q, P))      0      0  ...
            1                             P      1      1  ...
            2                             Q      2      2  ...
            3                             P      2      2  ...     1
            4                 Implies(Q, P)      1      1  ...            2
            5     Implies(P, Implies(Q, P))      0      0  ...            1  COMPLETE

        Exceptions:
            BlockScopeError: The referenced block id is not accessible.
            NoSuchBlock: The block id does not exist.
        """

        if self.status != self.complete:
            try:
                level, antecedent, consequent = self.getlevelblockstatements(blockid)
            except:
                raise altrea.exception.NoSuchBlock(blockid)
            if level != self.level + 1:
                raise altrea.exception.BlockScopeError(blockid)
            implication = Implies(antecedent, consequent)

            self.checkcomplete(implication)
            if self.status == self.complete:
                newcomment = self.complete
            else:
                newcomment = comments
            self.lines.append(
                [implication, 
                self.level, 
                self.currentblockid, 
                self.implies_introname, 
                '', 
                blockid, 
                newcomment
                ]
            )                   
            
    def lem(self, first: int, second: int, comments: str = ''):
        """Add a line justified by the Law of Excluded Middle (LEM) rule.
        
        Parameters:
            first: The first block id
            second: The second block id
            
        Examples:
            >>> from sympy.abc import P, Q
            >>> from altrea.tf import Proof
            >>> from altrea.display import show
            >>> p = Proof(P | ~P)
            >>> p.openblock(P)
            >>> p.or_intro(~P,1)
            >>> p.closeblock()
            >>> p.openblock(~P)
            >>> p.or_intro(P,3)
            >>> p.closeblock()
            >>> p.lem(1,2)
            >>> show(p, latex=0)
                Statement  Level  Block        Rule Lines Blocks   Comment
            Line    P | ~P      0      0        Goal
            1            P      1      1  Assumption
            2       P | ~P      1      1    Or Intro     1
            3           ~P      1      2  Assumption
            4       P | ~P      1      2    Or Intro     3
            5       P | ~P      0      0         LEM         1, 2  COMPLETE

        Exceptions:
            NotSameLevel: The two blocks are not at the same level.
            NotLemOpposites: The assumption of the first block is not the negation of the assumption
                of the second block.
            NotSameStatements: The conclusions of the two blocks are not the same.
            NoSuchBlock: The block id does not exist.
        """

        if self.status != self.complete:
            try:
                firstlevel, firstassumption, firstconclusion = self.getlevelblockstatements(first)
            except:
                raise altrea.exception.NoSuchBlock(first)
            try:
                secondlevel, secondassumption, secondconclusion = self.getlevelblockstatements(second)
            except:
                raise altrea.exception.NoSuchBlock(second)
            if firstlevel != secondlevel:
                raise altrea.exception.NotSameLevel(firstlevel, secondlevel)
        
            if  firstassumption != Not(secondassumption):
                raise altrea.exception.NotLemOpposites(firstassumption, secondassumption)
            if firstconclusion != secondconclusion:
                raise altrea.exception.NotSameStatements(firstconclusion, secondconclusion)
        
            self.addstatement(
                statement=firstconclusion,
                rule=self.lem_name,
                blocks=self.reftwolines(first, second),
                comments=comments
            )

    def not_elim(self, first: int, second: int, comments: str = ''):
        """When two statements are contradictory a false line can be derived.
        
        Parameters:
            first: The line number of the first statement.
            second: The line number of the second statement.
            comments: An optional comment for this line.

        Exceptions:
            NoSuchLine: The referenced line does not exist in the proof.
            NotContradiction: Two referenced statements are not contradictions.
            ScopeError: The referenced statement is not accessible.                       
        """
        
        if self.status != self.complete:
            try:
                firstlevel, firststatement = self.getlevelstatement(first)
            except:
                raise altrea.exception.NoSuchLine(first)
            if firstlevel > self.level:
                raise altrea.exception.ScopeError(first)
        
            try:
                secondlevel, secondstatement = self.getlevelstatement(second)
            except:
                raise altrea.exception.NoSuchLine(second)
            if secondlevel > self.level:
                raise altrea.exception.ScopeError(second)

            if Not(firststatement) != secondstatement:
                raise altrea.exception.NotContradiction(first, second)
        
            self.addstatement(
                statement=self.falsename, 
                rule=self.not_elimname, 
                lines=self.reftwolines(first, second),
                comments=comments
            )
               
    def not_intro(self, blockid: int | str, comments: str = ''):
        """When an assumption generates a contradiction, the negation of the assumption
        can be used as a line of the proof in the next lower block.
        
        Example:
        
        Parameter:
            blockid: The name of the block containing the assumption and contradiction.

        Exceptions:
            NotFalse: The conclusion statement of the block is not false.
            NoSuchBlock: The referenced does not exist in the proof.
            BlockScopeError: The referenced block is not accessible.
        """

        if self.status != self.complete:
            try:   
                level, assumption, conclusion = self.getlevelblockstatements(blockid)
            except:
                raise altrea.exception.NoSuchBlock(blockid)
            if level != self.level + 1:
                raise altrea.exception.BlockScopeError(blockid)
            if conclusion != self.falsename:
                raise altrea.exception.NotFalse(blockid, conclusion)
            
            self.addstatement(
                statement=Not(assumption), 
                rule=self.not_introname,
                blocks=blockid,
                comments=comments
            )      

    def openblock(self, 
                  statement: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol,
                  comments: str = ''):
        """Opens a uniquely identified block of statements with an assumption.
        
        Examples:
            >>> from sympy.abc import P, Q
            >>> from altrea.tf import Proof
            >>> from altrea.display import show
            >>> p = Proof(P | ~P)
            >>> p.openblock(P)
            >>> p.or_intro(~P,1)
            >>> p.closeblock()
            >>> p.openblock(~P)
            >>> p.or_intro(P,3)
            >>> p.closeblock()
            >>> p.lem(1,2)
            >>> show(p, latex=0)
                Statement  Level  Block        Rule Lines Blocks   Comment
            Line    P | ~P      0      0        Goal
            1            P      1      1  Assumption
            2       P | ~P      1      1    Or Intro     1
            3           ~P      1      2  Assumption
            4       P | ~P      1      2    Or Intro     3
            5       P | ~P      0      0         LEM         1, 2  COMPLETE

        Parameters:
            statement: The assumption that starts the block of derived statements.
        """

        if self.status != self.complete:
            self.level += 1
            nextline = len(self.lines)
            self.currentblock = [nextline]
            self.blocklist.append([self.level, self.currentblock])
            self.currentblockid = len(self.blocklist) - 1

            self.addstatement(
                statement=statement, 
                rule=self.assumptionname,
                comments=comments
            )

    def or_elim(self, line: int, blockids: list, comments: str = ''):
        """Check the correctness of a disjunction elimination line before adding it to the proof.
        
        Exceptions:
            AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
            ConclusionsNotTheSame: The conclusions of blocks are not the same.
            NoSuchLine: The referenced line does not exist in the proof.
            ScopeError: The referenced statement is not accessible.
        """

        if self.status != self.complete:
            level, disjunction = self.getlevelstatement(line)
            if type(disjunction) != Or:
                raise altrea.exception.NotDisjunction(line, disjunction)
            if level != self.level:
                raise altrea.exception.ScopeError(line)
            if len(disjunction.args) != len(blockids):
                raise altrea.exception.BlockDisjuntsNotEqual(disjunction, blockids)
        
            try:
                firstlevel, firstassumption, firstconclusion = self.getlevelblockstatements(blockids[0])
            except:
                raise altrea.exception.NoSuchBlock(blockids[0])
            if firstlevel != self.level + 1:
                raise altrea.exception.BlockScopeError(blockids[0])
        
            try:
                secondlevel, secondassumption, secondconclusion = self.getlevelblockstatements(blockids[1])
            except:
                raise altrea.exception.NoSuchBlock(blockids[1])
            if secondlevel != self.level + 1:
                raise altrea.exception.BlockScopeError(blockids[1])
        
            if firstlevel != secondlevel:
                raise altrea.exception.NotSameLevel(firstlevel, secondlevel)
            if firstconclusion != secondconclusion:
                raise altrea.exception.ConclusionsNotTheSame(firstconclusion, secondconclusion)
        #if disjunction.args[0] != firstassumption and disjunction.args[0] != secondassumption:
        #    raise altrea.exception.
        # make this work for arbitrary disjuncts in one statement

            self.addstatement(
                statement=firstconclusion,
                rule=self.or_elimname,
                blocks=self.reftwolines(blockids[0], blockids[1]), 
                comments=comments
            )
            
    def or_intro(self, 
                  disjunct: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol, 
                  line: int, 
                  comments: str = ''):
        """The newdisjunct statement and the statement at the line number become a disjunction.
        
        Parameters:
            disjunct: A statement that will be used in the disjunction.
            line: The line number of the statement that will be the other disjunct.

        Examples:
            >>> from sympy.abc import P, Q
            >>> from altrea.tf import Proof
            >>> from altrea.display import show
            >>> p = Proof(P | ~P)
            >>> p.openblock(P)
            >>> p.or_intro(~P,1)
            >>> p.closeblock()
            >>> p.openblock(~P)
            >>> p.or_intro(P,3)
            >>> p.closeblock()
            >>> p.lem(1,2)
            >>> show(p, latex=0)
                Statement  Level  Block        Rule Lines Blocks   Comment
            Line    P | ~P      0      0        Goal
            1            P      1      1  Assumption
            2       P | ~P      1      1    Or Intro     1
            3           ~P      1      2  Assumption
            4       P | ~P      1      2    Or Intro     3
            5       P | ~P      0      0         LEM         1, 2  COMPLETE

        Exceptions:
            NoSuchLine: The referenced line does not exist in the proof.
            ScopeError: The referenced statement is not accessible.
            StringType: The statement should not be a string.
        """

        if self.status != self.complete:
            if type(disjunct) == str:
                raise altrea.exception.StringType(disjunct)
            try:
                level, statement = self.getlevelstatement(line)
            except:
                raise altrea.exception.NoSuchLine(line)
            if level > self.level:
                raise altrea.exception.ScopeError(line)
            disjunction = Or(statement, disjunct)
            self.addstatement(
                statement=disjunction, 
                rule=self.or_introname, 
                lines=str(line),
                comments=comments
            )
       
    def reit(self, line: int, comments: str = ''):
        """A statement that already exists which can be accessed can be reused.

        Parameter:
            line: The line number of the statement.

        Example:
            >>> from altrea.tf import Proof
            >>> ex = Proof([A], C >> A, 'Example using openblock')
            >>> ex.openblock(C)
            >>> ex.reit(1)
            >>> ex.closeblock()
            >>> ex.implies_intro('11')
            The proof is complete.

        Exceptions:
            NoSuchLine: The referenced line does not exist in the proof.
            ScopeError: The referenced statement is not accessible.

        """
        
        if self.status != self.complete:
            try:
                level, statement = self.getlevelstatement(line)
            except:
                raise altrea.exception.NoSuchLine(line)
            if level > self.level:
                raise altrea.exception.ScopeError(line)
        
            self.addstatement(
                statement=statement, 
                rule=self.reitname, 
                lines=str(line),
                comments=comments
            )
        
    def xnor_elim(self, line: int, comments: str = ''):
        pass

    def xnor_intro(self, line: int, comments: str = ''):
        pass

    def xor_elim(self, line: int, comments: str = ''):
        pass

    def xor_intro(self, line: int, comments: str = ''):
        pass

    