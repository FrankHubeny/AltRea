# altrea/truthfunction.py

"""The module provides functions to construct a proof in propositional logic.

The module contains thhree groups of functions: 

- Supporting functions called by other functions for routine procesing.
- Basic rules for the list of logical operators that one accepts for the logic.
- Derived rules which are short cuts for a proof using basic rules.

The following methods support other functions.  They are not intended to be called by the user directly.

- `checkavailable(rulename, comments)` - Based on the logic specified check if a warning comment 
should be posted for the proof line overwriting any comments provided by the user.
- `checkcomplete(statement)` - Mark the proof completed if the statement equals the goal.
- `getlevelblockstatements(blockid)` - Get the level, assumption statement and conclusion statement for the blockid.
- `getlevelstatement(line)` - Get the level and statement for the line id.
- `reftwolines(first, second)` - Join thw integers together into a string to record as set of lines or blocks.

The following are basic rules which the user may call after initializing a Proof.  Depending on
which logical operators one has, the basic list may include only a subset of this list.

- `addpremise` - ['C', 'CI', 'CO', 'I'] Add a premise
- `and_elim` - ['C', 'CI', 'CO', 'I'] Conjunction Elimination
- `and_intro` - ['C', 'CI', 'CO', 'I'] Conjunction Introduction
- `explosion` - ['C', 'CI', 'CO', 'I'] Explosion
- `iff_elim` - ['C', 'CI', 'CO', 'I'] Equivalence Elimination
- `iff_intro` - ['C', 'CI', 'CO', 'I'] Equivalence Introduction
- `implies_elim` - ['C', 'CI', 'CO', 'I'] Implication Elimination
- `implies_intro` - ['C', 'CI', 'CO', 'I'] Implication Introduction
- `lem` - ['C', 'CI', 'CO', 'I'] Law of Excluded Middle
- `not_elim` - ['C', 'CI', 'CO', 'I'] Negation Elimination
- `not_intro` - ['C', 'CI', 'CO', 'I'] Negation Introduction
- `openblock` - ['C', 'CI', 'CO', 'I'] Open a block with an assumption
- `or_elim` - ['C', 'CI', 'CO', 'I'] Disjunction Elimination
- `or_intro` - ['C', 'CI', 'CO', 'I'] Disjunction Introduction
- `reit` - ['C', 'CI', 'CO', 'I'] Reiteration

The following are derived rules which the user may call after initializing a Proof.
One of the examples associated with each rule shows the derivation of this rule from those above.

- `demorgan` - ['C', 'CI', 'CO', 'I'] DeMorgan's Rules
- `doublenegation` - ['C', 'CI', 'CO', 'I'] Double Negation (both introduction and elimination)

The entire AltRea software is designed to be simple to read so that those who are skeptical
about a proof's accuracy do not receive additional doubt coming from the software constructing
the proof.  The display module uses pandas, but the rules use only basic python code coming
from the altrea.boolean.py, altrea.exception.py and altrea.truthfunction.py files.

Anyone finding an issue with the code, whether a python programmer, a user or a logician
question some implementation may raise raise the issue in GitHub.

It is also designed to help those learning python.  If you created a virtual environment
which you like should, you can find this software in your virtual directory under Lib/altrea.  You are
welcome and encouraged to copy these files to a local directory under a new name, say, "myaltrea".
Then import from these files rather than the altrea files to experiment with using python. 

Examples:
    >>> from myaltrea.boolean import And, Or, Not, Implies, Iff, Wff
    >>> import myaltrea.exception


"""

from altrea.boolean import And, Or, Not, Implies, Iff, Wff, F, T
import altrea.exception

class Proof:
    """
    This class contains methods to construct and verify proofs in 
    in various truth functional logics.
    """

    columns = ['Statement', 'Level', 'Proof', 'Rule', 'Lines', 'Proofs', 'Comment']
    statementindex = 0
    levelindex = 1
    blockidindex = 2
    ruleindex = 3
    linesindex = 4
    blocksindex = 5
    commentindex = 6
    lowestlevel = 0
    acceptedtypes = [And, Or, Not, Implies, Iff, Wff, F, T],
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
    dn_introname = 'DN Intro'
    dn_elimname = 'DN Elim'
    demorgan_name = 'DeMorgan'
    explosionname = 'Explosion'
    closeblockname = 'Close Block'
    falsename = F()
    blankstatement = ''
    complete = 'COMPLETE'
    partialcompletion = 'PARTIAL COMPLETION'
    stopped = 'STOPPED'
    comments_connector = ' - '
    stopped_connector = ': '
    stopped_alreadyavailable = 'The statement is already available at the current level.'
    stopped_blockclosed = 'Referenced block is closed.'
    stopped_blocknotclosed = 'Referenced block is not closed.'
    stopped_blockscope = 'Referenced block is out of scope.'
    stopped_closezeroblock = 'The lowest 0 block cannot be closed.'
    stopped_notlem = 'The blocks will not work with LEM rule.'
    stopped_linescope = 'Reference line is out of scope.'
    stopped_nogoal = 'The proof does not yet have a goal.'
    stopped_nosuchline = 'The referenced line does not exist.'
    stopped_nosuchblock = 'The referenced block does not exist.'
    stopped_notantecedent = 'One statement is not the antecedent of the other.'
    stopped_notconjunction = 'The referenced line is not a conjunction.'
    stopped_notcontradiction = 'The referenced lines are not contradictory.'
    stopped_notdemorgan = 'The referenced line is not a DeMorgan statement.'
    stopped_notdoublenegation = 'The referenced line is not a double negation.'
    stopped_notfalse = 'The referenced line is not false.'
    stopped_notsameconclusion = 'The two conclusions are not the same.'
    stopped_notsamelevel = 'The two blocks are not at the same level.'
    stopped_novaluepassed = 'No value was passed to the function.'
    stopped_string = 'Input is not a Wff derived object.'
    stopped_undefinedlogic = 'This logic has not been defined.'
    connectors = {
        'C': ['$\\wedge$', '$\\vee$', '$\\lnot$', '$\\rightarrow$', '$\\leftrightarrow$'],
        'CI': ['$\\wedge$', '$\\vee$', '$\\lnot$', '$\\rightarrow$', '$\\leftrightarrow$'],
        'CO': ['$\\wedge$', '$\\vee$', '$\\lnot$', '$\\rightarrow$', '$\\leftrightarrow$'],
        'I': ['$\\wedge$', '$\\vee$', '$\\lnot$', '$\\rightarrow$', '$\\leftrightarrow$'],
    }
    logicdictionary = {
        'C': 'Classical Propositional Logic',
        'CI': 'Classical Implicational Propostional Logic',
        'CO': 'Classical And-Or-Not Propositional Logic',
        'I': 'Intuitionist Propositional Logic'
    }
    availablelogics = {
        'addpremise': ['C', 'CI', 'CO', 'I'],
        'addgoal': ['C', 'CI', 'CO', 'I'],
        'and_elim': ['C', 'CI', 'CO', 'I'],
        'and_intro': ['C', 'CI', 'CO', 'I'],
        'closeblock': ['C', 'CI', 'CO', 'I'],
        'demorgan': ['C', 'CI', 'CO', 'I'],
        'dn_elim': ['C', 'CI', 'CO', 'I'],
        'dn_intro': ['C', 'CI', 'CO', 'I'],
        'explosion': ['C', 'CI', 'CO', 'I'],
        'iff_elim': ['C', 'CI', 'CO', 'I'],
        'iff_intro': ['C', 'CI', 'CO', 'I'],
        'implies_elim': ['C', 'CI', 'CO', 'I'],
        'implies_intro': ['C', 'CI', 'CO', 'I'],
        'lem': ['C', 'CI', 'CO', 'I'],
        'not_elim': ['C', 'CI', 'CO', 'I'],
        'nand_intro': ['C', 'CI', 'CO', 'I'],
        'nand_elim': ['C', 'CI', 'CO', 'I'],
        'nor_intro': ['C', 'CI', 'CO', 'I'],
        'not_elim': ['C', 'CI', 'CO', 'I'],
        'not_intro': ['C', 'CI', 'CO', 'I'],
        'openblock': ['C', 'CI', 'CO', 'I'],
        'or_elim': ['C', 'CI', 'CO', 'I'],
        'or_intro': ['C', 'CI', 'CO', 'I'],
        'reit': ['C', 'CI', 'CO', 'I'],
    }

    def __init__(self, logic: str = 'C', name: str = ''):
        """Create a Proof object with optional premises, but a specific goal.
        
        Parameters:
            goal: The goal to be reached by the proof.
            name: The name assigned to the proof.
            logic: The logic that will constrain the proof.
        """
            
        self.name = name
        self.goals = []
        self.goals_string = ''
        self.goals_latex = ''
        self.derivedgoals = []
        self.comments = ''
        self.logic = logic
        self.parentproofid = 0
        self.currentblock = [1]
        self.currentblockid = 0
        self.blocklist = [[self.lowestlevel, self.currentblock, self.parentproofid]]
        self.blocks = []
        self.level = self.lowestlevel
        self.status = ''
        self.stoppedmessage = ''
        self.premises = []
        if self.logic in self.logicdictionary:
            self.lines = [['', 0, 0, self.goalname, '', '', '']]
        else:
            self.status = self.stopped
            self.lines = [['', 0, 0, self.goalname, '', '', ''.join([self.stopped, self.stopped_connector, self.stopped_undefinedlogic])]]

    """SUPPORT FUNCTIONS"""

    def checkcomplete(self):
        """Check if the goal has been found and the proof is over."""

        return self.status == self.complete or self.status == self.stopped
    
    def checkhasgoal(self):
        """Check if the proof has at least one goal."""

        return len(self.goals) > 0
    
    def checkline(self, line: int):
        """Check if the line is an integer within the range of the proof lines."""

        if type(line) == int:
            return len(self.lines) > line and line > 0
        else:
            return False
        
    def checklinescope(self, level: int):
        """Check is the line can be accessed by the current line."""

        return level <= self.level 
    
    def checkblockid(self, blockid: int):
        """Check if the blockid is an actual block."""

        # found = False
        # for i in self.blocklist:
        #     if i[0] == blockid:
        #         found = True
        #         break
        return blockid >= 0 and blockid < len(self.blocklist)
    
    def checkblockclosed(self, blockid: int):
        """Check if the blockid represents a closed block."""

        # closed = False
        # for i in self.blocklist:
        #     if i[0] == blockid and len(i[1]) == 2:
        #         closed = True
        #         break
        return len(self.blocklist[blockid][1]) == 2
    
    def checkblockscope(self, level: int):
        """Check if the block can be accessed from the current level."""

        return level == self.level + 1

    def checkcurrentlevel(self, level: int):
        """Check that the level of a statement one plans to use is at the current level."""

        return level == self.level
    
    def checkstring(self, wff: And | Or | Not | Implies | Iff | Wff | F | T):
        #return (type(wff) not in self.acceptedtypes) # or (type(wff) == None)
        return type(wff) == str
    
    def checkacceptedtype(self, statement):

        return type(statement) in self.acceptedtypes
   
    def availablecomplete(self, 
                          rulename: str, 
                          statement:  And | Or | Not | Implies | Iff | Wff | F | T = None, 
                          comments: str = ''):
        """Check if the user's declared logic can use this rule.  If not, leave a message for the user.
        Also check if the proof is complete and if so leave a message that the proof is finished.
        
        Parameters:
            rulename: The function name representing the rule where this is called.
            comments: Any comments the user has provided which may be overwritten.
        """

        newcomment = self.status
        if self.level == 0:
            if str(statement) in self.goals:
                if str(statement) not in self.derivedgoals:
                    self.derivedgoals.append(str(statement))
                    if len(self.derivedgoals) < len(self.goals):
                        newcomment = self.partialcompletion
                    else:
                        self.status = self.complete
                        self.blocklist[0][1].append(len(self.lines)-1)
                        newcomment = self.complete
        if comments == '':
            return newcomment
        else:
            if newcomment == '':
                return comments
            else:
                return ''.join([newcomment, self.comments_connector, comments])

    def getlevelblockstatements(self, blockid: int) -> tuple:
        """Given a block id, return the level the block is in and the assumption and conclusion statements."""

        level = self.blocklist[blockid][0]
        assumption = self.lines[self.blocklist[blockid][1][0]][self.statementindex]
        conclusion = self.lines[self.blocklist[blockid][1][1]][self.statementindex]
        return level, assumption, conclusion
    
    def getlevelstatement(self, line: int) -> tuple:
        """Given a line id, return the level and the statement on that line."""

        level = self.lines[line][self.levelindex]
        statement = self.lines[line][self.statementindex]
        return level, statement
    
    def getproof(self, proofid: int) -> tuple:
        """Returns the leve, assumption statement, conclusion statement and parent proof id."""

        level = self.blocklist[proofid][0]
        assumption = self.lines[self.blocklist[proofid][1][0]][self.statementindex]
        conclusion = self.lines[self.blocklist[proofid][1][1]][self.statementindex]
        parentproofid = self.blocklist[proofid][2]
        return level, assumption, conclusion, parentproofid
    
    def getparentproofid(self, proofid: int) -> int:
        """Returns the parent proof id of a given proof."""
    
        return self.blocklist[proofid][2]

    def reftwolines(self, first: int, second: int) -> str:
        """Join two integers representing line ids or block ids as strings together."""

        return ''.join([str(first), ', ', str(second)])
    
    def refproof(self, proofid: int):
        """Formats a proof used in a proof."""

        proof = self.blocklist[proofid][1]
        return ''.join([str(proof[0]), '-', str(proof[1])])
    
    def stopproof(self, message: str, statement, rule: str, lines: str, blocks: str, comments: str = ''):
        self.status = self.stopped
        if rule == self.goalname:
            if comments == '':
                self.lines[0][self.commentindex] = ''.join([self.stopped, self.stopped_connector, message])
            else:
                self.lines[0][self.commentindex] = ''.join([self.stopped, self.stopped_connector, message, self.comments_connector, comments])
        else:
            if comments == '':
                self.stoppedmessage = ''.join([self.stopped, self.stopped_connector, message])
            else:
                self.stoppedmessage = ''.join([self.stopped, self.stopped_connector, message, self.comments_connector, comments])
            self.lines.append(
                [
                    statement, 
                    self.level, 
                    self.currentblockid, 
                    rule, 
                    lines, 
                    blocks, 
                   self.stoppedmessage
                ]
            )
 
    """BASIC CLASSICAL RULES"""

    def addgoal(self,
                goal: And | Or | Not | Implies | Iff | Wff | F | T, 
                comments: str = ''):
        """Add a goal to the proof.
        
        Parameters:
            goal: The goal to add to the proof.
            comments: Comments for this line of the proof.

        Examples:

            Once one has a Proof object one has to add a goal to it.  Without a goal attempting to
            add any other line will stop the proof.  Below is an example of a proof and
            a disply using latex for the statements.  Note the $C$ in the first line.  This
            would display well in environments that can display latex.  Note also how a comment
            can be added to the goal.

            What is passed to addgoal is not a string, but an instantiated Wff (well-formed formula).
            An error is returned is a string is passed.

            >>> from altrea.boolean import Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import show
            >>> C = Wff('C')
            >>> p = Proof()
            >>> p.addgoal(C, 'My Comment')
            >>> show(p, latex=1)
              Statement  Level  Block  Rule Lines Blocks     Comment
            C       $C$      0      0  Goal               My Comment

        See Also:
            Proof, Wff
        """

        if not self.checkcomplete():
            #if type(goal) == str:
            if self.checkstring(goal):
                self.stopproof(self.stopped_string, goal, self.goalname, 0, 0, comments)
            else:
                self.goals.append(str(goal))
                if self.goals_string == '':
                    self.goals_string = str(goal)
                else:
                    self.goals_string += ''.join([', ',str(goal)])
                if self.goals_latex == '':
                    self.goals_latex = goal.latex()
                else:
                    self.goals_latex += ''.join([', ',goal.latex()]) 
                self.lines[0][self.statementindex] = self.goals_string
                if self.lines[0][self.commentindex] == '':
                    self.lines[0][self.commentindex] = comments
                elif comments != '':
                    self.lines[0][self.commentindex] += ''.join([self.comments_connector, comments])

    def addpremise(self, 
                   premise: And | Or | Not | Implies | Iff | Wff | F | T, 
                   comments: str = ''):
        """Add a premise to the proof.
        
        Parameters:
            premise: The premise to add to the proof.
            comments: Comments for this line of the proof.
        """

        if not self.checkcomplete():
            #if type(premise) == str:
            if self.checkstring(premise):
                self.stopproof(self.stopped_string, premise, self.premisename, '', '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.premisename, '', '', comments)
            else:
                self.premises.append(premise)
                newcomment = self.availablecomplete('addpremise', premise, comments)
                self.lines.append(
                    [
                        premise, 
                        0, 
                        self.currentblockid, 
                        self.premisename, 
                        '', 
                        '', 
                        newcomment
                    ]
                )
        
    def and_elim(self, line: int, comments: str = ''):
        """A conjunction is split into its individual conjuncts.
        
        Parameters:
            line: The line number of the conjunction to be split.
            comments: Optional user comments for the line.

        Examples:
            The first example provides a proof that from the statement A & B one can derive 
            two statements, A and B. 
            
            The starting point for the proof are named well-formed forumulas (Wff).  Although this
            looks like a string 'A', the Wff('A') contains metadata associated with it.
            From them more complicated well-formed formulas such as "And(A, B)" can be
            formed.  Note that this formula is not the string 'A & B' although
            it is displayed as such in the proof.  If one used "show(p, latex=1)" one
            would see a latex display of the same well-formed formula.
            
            It is somewhat unusual that there are two goals, but this rule produces two
            statements, one for each conjunct on lines 2 and 3 of the proof.  In the first
            line with the "Goal" Rule they are separated by a comma.  An optional comment
            appears for each goal which is visible in the Comment column separated by a " - ".

            The comments on lines 2 and 3, "PARTIAL COMPLETION" and "COMPLETE" were generated
            by AltRea.  This comment column can be used both by the user and AltRea to
            provide a message about the proof.

            >>> from altrea.boolean import And, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import show
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> p = Proof()
            >>> p.addgoal(A, 'one')
            >>> p.addgoal(B, 'two')
            >>> p.addpremise(And(A, B))
            >>> p.and_elim(1)
            >>> show(p, latex=0)
              Statement  Level  Block      Rule Lines Blocks             Comment
            C      A, B      0      0      Goal                        one - two
            1     A & B      0      0   Premise
            2         A      0      0  And Elim     1         PARTIAL COMPLETION
            3         B      0      0  And Elim     1                   COMPLETE

            Most rules have a scope limited to the level they are on.  They cannot 
            reference lines from a block above them nor from a line at a level
            below them.  However, they can reiterate those statements from a lower level
            to make them available for use on the current level.  Consider the following
            stopped attempt to derive C >> (A & B) from the premise A & B.


        """

        if not self.checkcomplete():
            if not self.checkline(line):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.and_elimname, str(line), '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.premisename, '', '', comments)
            else:
                level, statement = self.getlevelstatement(line)
                if not self.checkcurrentlevel(level):
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.and_elimname, str(line), '', comments)
                #if not self.checklinescope(level):
                #    self.stopproof(self.stopped_linescope, self.blankstatement, self.and_elimname, str(line), '', comments)
                elif type(statement) != And:
                    self.stopproof(self.stopped_notconjunction, self.blankstatement, self.and_elimname, str(line), '', comments)
                else:
                    for conjunct in [statement.left, statement.right]:
                        newcomment = self.availablecomplete('and_elim', conjunct, comments)
                        self.lines.append(
                            [
                                conjunct, 
                                self.level, 
                                self.currentblockid, 
                                self.and_elimname, 
                                str(line), 
                                '',
                                newcomment
                            ]
                        )   
                        if self.status == self.complete:
                            break              
                
    def and_intro(self, first: int, second: int, comments: str = ''):
        """The statement at first line number is joined with And to the statement at second
        line number.

        Parameters:
            first: The line number of the first conjunct.
            second: The line number of the second conjunct.
            comments: Optional comments that a user may enter.

        Exception:
            Start with two named well-formed formulas (Wff), "A" and "B" one can start a proof p.
            This example will derive from those two statements given as premises in line 1 and 2
            the statement displayed as "A & B" on line 3.  The comment on line 3 shows that
            the proof is complete.  Also on line 3 is information on the lines (1 and 2) that were
            referenced to justify the presence in the proof.

            >>> from altrea.boolean import And, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import show
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> p = Proof()
            >>> p.addgoal(And(A, B))
            >>> p.addpremise(A)
            >>> p.addpremise(B)
            >>> p.and_intro(1, 2)
            >>> show(p, latex=0)
              Statement  Level  Block       Rule Lines Blocks   Comment
            C     A & B      0      0       Goal
            1         A      0      0    Premise
            2         B      0      0    Premise
            3     A & B      0      0  And Intro  1, 2         COMPLETE

            This example shows an obvious result along with how a comment can be entered by the user.  

            >>> from altrea.boolean import And, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import show
            >>> A = Wff('A')
            >>> p = Proof()
            >>> p.addgoal(And(A, A))
            >>> p.addpremise(A)
            >>> p.and_intro(1, 1, 'Obvious result')
            >>> show(p, latex=0)
              Statement  Level  Block       Rule Lines Blocks                    Comment
            C     A & A      0      0       Goal
            1         A      0      0    Premise
            2     A & A      0      0  And Intro  1, 1         COMPLETE - Obvious result

            In the previous examples all of the statements were on level 0, the same level.
            Both the and_into and and_elim require that the statenents they use be on the 
            same level as the current level.  However, one can use statements from a
            lower level by reiterating then using the reit rule.  Here is an example of that.
        """

        if not self.checkcomplete():
            if not self.checkline(first):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.and_introname, str(first), '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.and_elimname, '', '', comments)
            else:
                firstlevel, firstconjunct = self.getlevelstatement(first)
                if not self.checkcurrentlevel(firstlevel):  
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.and_introname, str(first), '', comments)
                elif not self.checkline(second):
                    self.stopproof(self.stopped_nosuchline, self.blankstatement, self.and_introname, str(second), '', comments)
                else:
                    secondlevel, secondconjunct = self.getlevelstatement(second)
                    if not self.checkcurrentlevel(secondlevel):  
                        self.stopproof(self.stopped_linescope, self.blankstatement, self.and_introname, str(second), '', comments)
                    else:
                        andstatement = And(firstconjunct, secondconjunct)
                        newcomment = self.availablecomplete('and_intro', andstatement, comments)
                        self.lines.append(
                            [
                                andstatement, 
                                self.level, 
                                self.currentblockid, 
                                self.and_introname, 
                                self.reftwolines(first, second), 
                                '',
                                newcomment
                            ]
                        )                 

    # def closeblock(self):
    #     """Closes the block of statements that the proof is currently in.
        
    #     Examples:
    #         >>> from sympy.abc import P, Q
    #         >>> from altrea.tf import Proof
    #         >>> from altrea.display import show
    #         >>> p = Proof(P | ~P)
    #         >>> p.openblock(P)
    #         >>> p.or_intro(~P,1)
    #         >>> p.closeblock()
    #         >>> p.openblock(~P)
    #         >>> p.or_intro(P,3)
    #         >>> p.closeblock()
    #         >>> p.lem(1,2)
    #         >>> show(p, latex=0)
    #             Statement  Level  Block        Rule Lines Blocks   Comment
    #         Line    P | ~P      0      0        Goal
    #         1            P      1      1  Assumption
    #         2       P | ~P      1      1    Or Intro     1
    #         3           ~P      1      2  Assumption
    #         4       P | ~P      1      2    Or Intro     3
    #         5       P | ~P      0      0         LEM         1, 2  COMPLETE

    #     Exceptions:
    #         CannotCloseStartingBlock: The lowest block is closed by completing the proof.
    #     """

    #     if not self.checkcomplete():
    #         if self.currentblockid == 0:
    #             self.stopproof(self.stopped_closezeroblock, self.blankstatement, self.closeblockname, '', '')
    #         else:
    #             self.blocklist[self.currentblockid][1].append(len(self.lines)-1)
    #             self.level -= 1
    #             for b in range(len(self.blocklist)-1):
    #                 if self.blocklist[b][0] == self.level and len(self.blocklist[b][1]) == 1:
    #                     self.currentblockid = b
    #                     self.currentblock = self.blocklist[b][1]

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

        """

        if not self.checkcomplete():
            if not self.checkline(line):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.demorgan_name, str(line), '', comments)
            #elif not self.checkhasgoal():
            #    self.stopproof(self.stopped_nogoal, self.blankstatement, self.demorgan_name, '', '', comments)
            else:
                level, statement = self.getlevelstatement(line)
                if not self.checkcurrentlevel(level):  #not self.checklinescope(level):
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.demorgan_name, str(line), '', comments)
                else:
                    if type(statement) == Not:
                        if type(statement.negated) == And:
                            andstatement = statement.negated
                            firstsubstatement = andstatement.left
                            secondsubstatement = andstatement.right
                            final = Or(Not(firstsubstatement), Not(secondsubstatement))
                            newcomment = self.availablecomplete('demorgan', final, comments)
                            self.lines.append([final, self.level, self.currentblockid, self.demorgan_name, str(line), '', newcomment])
                        elif type(statement.negated) == Or:
                            orstatement = statement.negated
                            firstsubstatement = orstatement.left
                            secondsubstatement = orstatement.right
                            final = And(Not(firstsubstatement), Not(secondsubstatement))
                            newcomment = self.availablecomplete('demorgan', final, comments)
                            self.lines.append([final, self.level, self.currentblockid, self.demorgan_name, str(line), '', newcomment])
                        else:
                            self.stopproof(self.stopped_notdemorgan, self.blankstatement, self.demorgan_name, str(line), '', comments)
                    elif type(statement) == Or:
                        firstsubstatement = statement.left
                        secondsubstatement = statement.right               
                        if type(firstsubstatement) == Not and type(secondsubstatement) == Not:
                            final = Not(And(firstsubstatement.negated, secondsubstatement.negated))
                            newcomment = self.availablecomplete('demorgan', final, comments)
                            self.lines.append([final, self.level, self.currentblockid, self.demorgan_name, str(line), '', newcomment])
                        else:
                            self.stopproof(self.stopped_notdemorgan, self.blankstatement, self.demorgan_name, str(line), '', comments)
                    elif type(statement) == And:
                        firstsubstatement = statement.left
                        secondsubstatement = statement.right
                        if type(firstsubstatement) == Not and type(secondsubstatement) == Not:
                            final = Not(Or(firstsubstatement.negated, secondsubstatement.negated))
                            newcomment = self.availablecomplete('demorgan', final, comments)
                            self.lines.append([final, self.level, self.currentblockid, self.demorgan_name, str(line), '', newcomment])
                        else:
                            self.stopproof(self.stopped_notdemorgan, self.blankstatement, self.demorgan_name, str(line), '', comments)
                    else:
                        self.stopproof(self.stopped_notdemorgan, self.blankstatement, self.demorgan_name, str(line), '')

    def dn_intro(self, line: int, comments: str = ''):
        '''This rule adds a double negation to the statement referenced by the line number
        
        Parameters:
            line: The line number containing the statement.
            comments: User comments on this line.

        Examples:
            In the following example a well-formed formula A = Wff('A') is turned into a double negative.
            Note how comments can be added to the code and the COMPLETE result displayed with the
            user entered comments.

            >>> from altrea.boolean import Not, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import show
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> p = Proof()
            >>> p.addgoal(Not(Not(A)), comments='double negative goal')
            >>> p.addpremise(A, comments='make this a double negative')
            >>> p.dn_intro(1, comments='double negative works')
            >>> show(p, latex=0)
              Statement  Level  Block  ... Lines Blocks                           Comment
            C       ~~A      0      0  ...                           double negative goal
            1         A      0      0  ...                    make this a double negative
            2       ~~A      0      0  ...     1         COMPLETE - double negative works

        '''

        if not self.checkcomplete():
            if not self.checkline(line):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.dn_introname, str(line), '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.dn_introname, '', '', comments)
            else:
                level, statement = self.getlevelstatement(line)
                if not self.checkcurrentlevel(level): #not self.checklinescope(level):
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.dn_introname, str(line), '', comments)
                else:
                    newstatement = Not(Not(statement))
                    newcomment = self.availablecomplete('dn_intro', newstatement, comments)
                    self.lines.append(
                        [
                            newstatement, 
                            self.level, 
                            self.currentblockid, 
                            self.dn_introname, 
                            str(line), 
                            '', 
                            newcomment
                        ]
                    )

    def dn_elim(self, line: int, comments: str = ''):
        '''This rule removes a double negation from a statement.
        
        Parameters:
            line: The line number containing the double negation.
            comments: User comments on this line.

        Examples:

            >>> from altrea.boolean import Not, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import show
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> p = Proof()
            >>> p.addgoal(A, comments='derive this')
            >>> p.addpremise(Not(Not(A)), comments='from this')
            >>> p.dn_intro(1, comments="hmm, I'm going in the wrong direction")
            >>> p.dn_elim(2)
            >>> p.dn_elim(3, comments="that's better!")
            >>> show(p, latex=0)
              Statement  Level  Block  ... Lines Blocks                                Comment
            C         A      0      0  ...                                         derive this
            1       ~~A      0      0  ...                                           from this
            2     ~~~~A      0      0  ...     1         hmm, I'm going in the wrong direction
            3       ~~A      0      0  ...     2
            4         A      0      0  ...     3                     COMPLETE - that's better!
        '''

        if not self.checkcomplete():
            if not self.checkline(line):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.dn_elimname, str(line), '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.dn_elimname, '', '', comments)
            else:
                level, statement = self.getlevelstatement(line)
                if not self.checkcurrentlevel(level): #not self.checklinescope(level):
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.dn_elimname, str(line), '', comments)
                elif type(statement) == Not and type(statement.negated) == Not:
                    newstatement = statement.negated.negated
                    newcomment = self.availablecomplete('dn_elim', newstatement, comments)
                    self.lines.append(
                        [
                            newstatement, 
                            self.level, 
                            self.currentblockid, 
                            self.dn_elimname, 
                            str(line), 
                            '', 
                            newcomment
                        ]
                    )
                else:
                    self.stopproof(self.stopped_notdoublenegation, self.blankstatement, self.dn_elimname, str(line), '', comments)


    def explosion(self, 
                  statement: And | Or | Not | Implies | Iff | Wff | F | T, 
                  comments: str = ''):
        """An arbitrary statement is entered in the proof given a false statement immediately preceding it.
        
        Parameters:
            expr: The statement to add to the proof.
            statement: The new statment to insert.
            comments: A optional comment for this line of the proof.

        Examples:
            In this example the premises are contradictory and so we can derive anything.  In particular,
            we can derive the goal, whatever goal we want.  

            If our logic is inconsistent then we can come up with a contradiction such as the one on lines
            1 and 2.  Then all well-formed formulas are true.  

            >>> from altrea.boolean import And, Not, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import show
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> p = Proof(And(A, B))
            >>> p.addpremise(A)
            >>> p.addpremise(Not(A))
            >>> p.not_elim(1, 2)
            >>> p.explosion(And(A, B), 3)
            >>> show(p, latex=0)
              Statement  Level  Block       Rule Lines Blocks   Comment
            C     A & B      0      0       Goal
            1         A      0      0    Premise
            2        ~A      0      0    Premise
            3         X      0      0   Not Elim  1, 2
            4     A & B      0      0  Explosion     3         COMPLETE

            Errors are returned as STOPPED messages.  Here is an error noting that the previous
            statement is not a contradiction.  To get that contradiction one need to first have a 
            Not Elim line on two lines which are contradictory.

            >>> from altrea.boolean import Not, And, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import show
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> p = Proof()
            >>> p.addgoal(And(A, B))
            >>> p.addpremise(A)
            >>> p.addpremise(Not(A))
            >>> # p.not_elim(1, 2)
            >>> p.explosion(And(A, B))
            >>> show(p, latex=0)
              Statement  Level  ...  Blocks                                     Comment
            C     A & B      0  ...
            1         A      0  ...
            2        ~A      0  ...
            3                0  ...          STOPPED: The referenced line is not false.
        """
        
        if not self.checkcomplete():
            if self.checkstring(statement):
            #if not self.checkacceptedtype(statement):
                self.stopproof(self.stopped_string, statement, self.explosionname, '', '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.explosionname, '', '', comments)
            else:
                line = len(self.lines) - 1
                blockid = self.lines[line][self.blockidindex]
                if line == 0:
                    self.stopproof(self.stopped_nosuchline, self.blankstatement, self.explosionname, str(line), '', comments)
                #elif len(self.blocklist[blockid][1]) == 2:
                #    self.stopproof(self.stopped_blockclosed, self.blankstatement, self.explosionname, str(line), '', comments)
                else:
                    level, falsestatement = self.getlevelstatement(line)
                    if level != self.level or blockid != self.currentblockid:
                        self.stopproof(self.stopped_blockscope, self.blankstatement, self.explosionname, str(line), '', comments)
                    elif falsestatement != self.falsename:
                        self.stopproof(self.stopped_notfalse, self.blankstatement, self.explosionname, str(line), '', comments)
                    else:
                        newcomment = self.availablecomplete('explosion', statement, comments)
                        self.lines.append(
                            [
                                statement, 
                                self.level, 
                                self.currentblockid, 
                                self.explosionname, 
                                str(line), 
                                '',
                                newcomment
                            ]
                        )                 
    
    def iff_elim(self, first: int, second: int, comments: str = ''):
        """Given an iff statement and a proposition one can derive the other proposition.
        
        Parameters:
            first: A statement containing either a proposition or an iff statement.
            second: A second statement containing either a proposition or an iff statement.
            comments: Comments on this line of the proof.
        
        Examples:

        """
        if not self.checkcomplete():
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
            
            if type(firststatement) == Iff:
                if firststatement.args[0] == secondstatement:
                    final = firststatement.args[1]
                elif firststatement.args[1] == secondstatement:
                    final = firststatement.args[0]
                else:
                    raise altrea.exception.NotEquivalence(firststatement, secondstatement)
            elif type(secondstatement) == Iff:
                if secondstatement.args[0] == firststatement:
                    final = secondstatement.args[1]
                elif secondstatement.args[1] == firststatement:
                    final = secondstatement.args[0]
                else:
                    raise altrea.exception.NotEquivalence(firststatement, secondstatement)
            else:
                raise altrea.exception.NotEquivalence(firststatement, secondstatement)
            
            newcomment = self.availablecomplete('iff_elim', final, comments)
            self.lines.append([
                final, 
                self.level, 
                self.currentblockid, 
                self.equivalent_elimname, 
                self.reftwolines(first, second), 
                '', 
                newcomment
            ])
                
    def iff_intro(self, first: int, second: int, comments: str = ''):
        """Derive a live using the if and only if symbol.
        
        Parameters:
            first: The first block to obtain an implication going in one direction.
            second: The second block to obtain an implication going in the other direction.
            comments: Comments entered by the user for this line.

        Examples:
        """

        if not self.checkcomplete():
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
        
            if  firstassumption != secondconclusion:
                raise altrea.exception.NotSameStatements(firstassumption, secondconclusion)
            if firstconclusion != secondassumption:
                raise altrea.exception.NotSameStatements(firstconclusion, secondassumption)
            newstatement = Iff(firstassumption, firstconclusion)
            newcomment = self.availablecomplete('iff_intro', newstatement, comments)
            self.lines.append(
                [
                    newstatement, 
                    self.level, 
                    self.currentblockid, 
                    self.equivalent_introname, 
                    '',
                    self.reftwolines(first, second), 
                    newcomment
                ]
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

        """

        if not self.checkcomplete():
            if not self.checkline(first):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.implies_elimname, '', '', comments)
            else:
                firstlevel, firststatement = self.getlevelstatement(first)
                if not self.checkcurrentlevel(firstlevel): #not self.checklinescope(firstlevel):
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.implies_elimname, '', '', comments)
                else:
                    if not self.checkline(second):
                        self.stopproof(self.stopped_nosuchline, self.blankstatement, self.implies_elimname, '', '', comments)
                    else:
                        secondlevel, secondstatement = self.getlevelstatement(second)
                        if not self.checkcurrentlevel(secondlevel): #not self.checklinescope(secondlevel):
                            self.stopproof(self.stopped_linescope, self.blankstatement, self.implies_elimname, '', '', comments)
                        else:       
                            if type(firststatement) == Implies:
                                if secondstatement != firststatement.left:
                                    self.stopproof(self.stopped_notantecedent, self.blankstatement, self.implies_elimname, '', '', comments)
                                else:
                                    newcomment = self.availablecomplete('implies_elim', firststatement.right, comments)
                                    self.lines.append(
                                        [
                                            firststatement.right, 
                                            self.level, 
                                            self.currentblockid, 
                                            self.implies_elimname, 
                                            self.reftwolines(first, second), 
                                            '', 
                                            newcomment
                                        ]
                                    )
                            elif type(secondstatement) == Implies:
                                if firststatement != secondstatement.left:
                                    self.stopproof(self.stopped_notantecedent, self.blankstatement, self.implies_elimname, '', '', comments)
                                else:
                                    newcomment = self.availablecomplete('implies_elim', secondstatement.right, comments)
                                    self.lines.append(
                                        [
                                            secondstatement.right, 
                                            self.level, 
                                            self.currentblockid, 
                                            self.implies_elimname, 
                                            self.reftwolines(first, second), 
                                            '', 
                                            newcomment
                                        ]
                                    )                   
                            else:
                                self.stopproof(self.stopped_notantecedent, self.blankstatement, self.implies_elimname, '', '', comments)

    def imp_int(self, comments: str = ''):
        if not self.checkcomplete():
            if self.currentblockid == 0:
                self.stopproof(self.stopped_closezeroblock, self.blankstatement, self.closeblockname, '', '')
            else:
                proofid = self.currentblockid
                self.blocklist[proofid][1].append(len(self.lines)-1)
                self.level -= 1
                level, antecedent, consequent, parentproofid = self.getproof(proofid)
                self.currentblockid = parentproofid
                self.currentblock = self.blocklist[parentproofid][1]
                # for b in range(len(self.blocklist)-1):
                #     if self.blocklist[b][0] == self.level and len(self.blocklist[b][1]) == 1:
                #         self.currentblockid = b
                #         self.currentblock = self.blocklist[b][1]
                
                implication = Implies(antecedent, consequent)
                newcomment = self.availablecomplete('implies_intro', implication, comments)
                self.lines.append(
                    [
                        implication, 
                        self.level, 
                        self.currentblockid, 
                        self.implies_introname, 
                        '', 
                        self.refproof(proofid), 
                        newcomment
                    ]
                )                   

    def implies_intro(self, blockid: int | str, comments: str = ''):
        """The command puts an implication as a line in the proof one level below the blockid.
        
        Parameters:
            blockid: The block identified by [start, end].
            comments: Comments added to the line.

        Examples:
            The following example shows how one can derive P >> P without any premise.  A block is opened
            with the assumption P and then the block is closed.  With the closure of the block the last
            line becomes the conclusion.  Since there is only one line in this block the antecedent
            and the consequent are the same.

            >>> from altrea.boolean import Wff, Implies
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import show
            >>> P = Wff('P')
            >>> p = Proof()
            >>> p.addgoal(Implies(P, P))
            >>> p.openblock(P)
            >>> p.closeblock()
            >>> p.implies_intro(1)
            >>> show(p, latex=0)
              Statement  Level  Block           Rule Lines Blocks   Comment
            C    P -> P      0      0           Goal
            1         P      1      1     Assumption
            2    P -> P      0      0  Implies Intro            1  COMPLETE

            The following example is similar to the P >> P example except now there is a new well-formed-formula, Q,
            involved.  

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

        """

        if not self.checkcomplete():
            if not self.checkblockid(blockid):
                self.stopproof(self.stopped_nosuchblock, self.blankstatement, self.implies_introname, '', '', comments)
            elif not self.checkblockclosed(blockid):
                self.stopproof(self.stopped_blocknotclosed, self.blankstatement, self.implies_introname, '', '', comments)
            else:
                level, antecedent, consequent = self.getlevelblockstatements(blockid)
                if not self.checkblockscope(level):  #level != self.level + 1:
                    self.stopproof(self.stopped_blockscope, self.blankstatement, self.implies_introname, '', '', comments)
                else:
                    implication = Implies(antecedent, consequent)
                    newcomment = self.availablecomplete('implies_intro', implication, comments)
                    self.lines.append(
                        [
                            implication, 
                            self.level, 
                            self.currentblockid, 
                            self.implies_introname, 
                            '', 
                            str(blockid), 
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
            NotLemOpposites: The assumption of the first block is not the negation of the assumption
                of the second block.
            NotSameLevel: The two blocks are not at the same level.
            NotSameStatements: The conclusions of the two blocks are not the same.
            NoSuchBlock: The block id does not exist.
        """

        if not self.checkcomplete():
            if not self.checkblockid(first):
                self.stopproof(self.stopped_nosuchblock, self.blankstatement, self.lem_name, '', '', comments)
            else:
                firstlevel, firstassumption, firstconclusion = self.getlevelblockstatements(first)
                if not self.checkblockid(second):
                    self.stopproof(self.stopped_nosuchblock, self.blankstatement, self.lem_name, '', '', comments)
                else:
                    secondlevel, secondassumption, secondconclusion = self.getlevelblockstatements(second)           
                    if firstlevel != secondlevel:
                        self.stopproof(self.stopped_notsamelevel, self.blankstatement, self.lem_name, '', '', comments)
                    else:     
                        if  type(firstassumption) == Not and firstassumption.negated.equals(secondassumption):
                            final = firstconclusion       
                        elif type(secondassumption) == Not and secondassumption.negated.equals(firstassumption):
                            final = firstconclusion   
                        else:
                            self.stopproof(self.stopped_notlem, self.blankstatement, self.lem_name, '', '', comments)
                        if not self.checkcomplete():
                            if not firstconclusion.equals(secondconclusion):
                                self.stopproof(self.stopped_notsameconclusion, self.blankstatement, self.lem_name, '', '', comments)
                            else:
                                newcomment = self.availablecomplete('lem', final, comments)
                                self.lines.append(
                                    [
                                        final, 
                                        self.level, 
                                        self.currentblockid, 
                                        self.lem_name, 
                                        '', 
                                        self.reftwolines(first, second),
                                        newcomment
                                    ]
                                )                 

    def nand_elim(self, first: int, second: int, comments: str = ''):
        pass

    def nand_intro(self, first: int, second: int, comments: str = ''):
        pass

    def nor_elim(self, first: int, second: int, comments: str = ''):
        pass

    def nor_intro(self, first: int, second: int, comments: str = ''):
        pass

    def not_elim(self, first: int, second: int, comments: str = ''):
        """When two statements are contradictory a false line can be derived.
        
        Parameters:
            first: The line number of the first statement.
            second: The line number of the second statement.
            comments: An optional comment for this line.

        Examples:
            >>> from altrea.boolean import And, Not, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import show
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> p = Proof(And(A, B))
            >>> p.addpremise(A)
            >>> p.addpremise(Not(A))
            >>> p.not_elim(1, 2)
            >>> p.explosion(And(A, B), 3)
            >>> show(p, latex=0)
              Statement  Level  Block       Rule Lines Blocks   Comment
            C     A & B      0      0       Goal
            1         A      0      0    Premise
            2        ~A      0      0    Premise
            3         X      0      0   Not Elim  1, 2
            4     A & B      0      0  Explosion     3         COMPLETE                 
        """
        
        if not self.checkcomplete():
            # if (len(self.lines) <= first) or (len(self.lines) <= second):
            #     if len(self.lines) <= first:
            #         self.stopproof(self.stopped_nosuchline, self.blankstatement, self.not_elimname, str(first), '', comments)
            #     else:
            #         self.stopproof(self.stopped_nosuchline, self.blankstatement, self.not_elimname, str(second), '', comments)
            if not self.checkline(first):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.not_elimname, str(first), '', comments)
            elif not self.checkline(second):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.not_elimname, str(second), '', comments)
            else:
                firstlevel, firststatement = self.getlevelstatement(first)
                secondlevel, secondstatement = self.getlevelstatement(second)
                if not self.checkcurrentlevel(firstlevel):
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.not_elimname, '', '', comments)
                elif not self.checkcurrentlevel(secondlevel):
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.not_elimname, '', '', comments)
                else:
                    if not Not(firststatement).equals(secondstatement) and not Not(secondstatement).equals(firststatement):
                        self.stopproof(self.stopped_notcontradiction, self.blankstatement, self.not_elimname, self.reftwolines(first, second), '', comments)
                    elif firstlevel > self.level:
                        self.stopproof(self.stopped_linescope, self.blankstatement, self.not_elimname, str(first), '', comments)
                    elif secondlevel > self.level:
                        self.stopproof(self.stopped_linescope, self.blankstatement, self.not_elimname, str(second), '', comments)
                    else:
                        newcomment = self.availablecomplete('not_elim', self.falsename, comments)
                        self.lines.append(
                            [
                                self.falsename, 
                                self.level, 
                                self.currentblockid, 
                                self.not_elimname, 
                                self.reftwolines(first, second), 
                                '',
                                newcomment
                            ]
                        )                 

    def neg_int(self, comments: str = ''):
        if not self.checkcomplete():
            if self.currentblockid == 0:
                self.stopproof(self.stopped_closezeroblock, self.blankstatement, self.closeblockname, '', '')
            else:
                proofid = self.currentblockid
                level, antecedent, consequent, parentproofid = self.getproof(proofid)
                self.blocklist[proofid][1].append(len(self.lines)-1)
                self.level -= 1
                self.currentblockid = parentproofid
                self.currentblock = self.blocklist[parentproofid][1]
                # for b in range(len(self.blocklist)-1):
                #     if self.blocklist[b][0] == self.level and len(self.blocklist[b][1]) == 1:
                #         self.currentblockid = b
                #         self.currentblock = self.blocklist[b][1]
                negation = Not(antecedent)
                newcomment = self.availablecomplete('not_intro', negation, comments)
                self.lines.append(
                    [
                        negation, 
                        self.level, 
                        self.currentblockid, 
                        self.not_introname, 
                        '', 
                        self.refproof(proofid), 
                        newcomment
                    ]
                )                   

    def not_intro(self, blockid: int | str, comments: str = ''):
        """When an assumption generates a contradiction, the negation of the assumption
        can be used as a line of the proof in the next lower block.
        
        Example:
        
        Parameter:
            blockid: The name of the block containing the assumption and contradiction.

        """

        if not self.checkcomplete():
            try:   
                level, assumption, conclusion = self.getlevelblockstatements(blockid)
            except:
                raise altrea.exception.NoSuchBlock(blockid)
            if level != self.level + 1:
                raise altrea.exception.BlockScopeError(blockid)
            if not conclusion.equals(self.falsename):
                raise altrea.exception.NotFalse(blockid, conclusion)       
            statement = Not(assumption)
            newcomment = self.availablecomplete('not_intro', statement, comments)
            self.lines.append(
                [
                    statement, 
                    self.level, 
                    self.currentblockid, 
                    self.not_introname, 
                    '', 
                    str(blockid),
                    newcomment
                ]
            )                 

    def openblock(self, 
                  statement: And | Or | Not | Implies | Iff | Wff | F | T,
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

        if not self.checkcomplete():
            if type(statement) == str:
            #if self.checkstring(statement):
                self.stopproof(self.stopped_string, self.blankstatement, self.assumptionname, '', '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.assumptionname, '', '', comments)
            else:
                parentproofid = self.currentblockid
                self.level += 1
                nextline = len(self.lines)
                self.currentblock = [nextline]
                self.blocklist.append([self.level, self.currentblock, parentproofid])
                self.currentblockid = len(self.blocklist) - 1

                newcomment = self.availablecomplete('openblock', statement, comments)
                self.lines.append(
                    [
                        statement, 
                        self.level, 
                        self.currentblockid, 
                        self.assumptionname, 
                        '', 
                        '',
                        newcomment
                    ]
                )                 

    def or_elim(self, line: int, blockids: list, comments: str = ''):
        """Check the correctness of a disjunction elimination line before adding it to the proof.
        

        """

        if not self.checkcomplete():
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

            newcomment = self.availablecomplete('or_elim', firstconclusion, comments)
            self.lines.append(
                [
                    firstconclusion, 
                    self.level, 
                    self.currentblockid, 
                    self.or_elimname, 
                    '', 
                    self.reftwolines(blockids[0], blockids[1]),
                    newcomment
                ]
            )                 

    def or_intro(self, 
                 line: int,
                 left: And | Or | Not | Implies | Iff | Wff | F | T = None,
                 right: And | Or | Not | Implies | Iff | Wff | F | T = None,   
                 comments: str = ''):
        """The newdisjunct statement and the statement at the line number become a disjunction.
        
        Parameters:
            line: The line number of the statement that will be the other disjunct.
            left: A statement that will be used in the disjunction on the left side of the one
                referenced by the line.
            right: A state that will be used in the disjunction on the right side of the one
                referenced by the line.
 

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
            NoValuePassed: 
            ScopeError: The referenced statement is not accessible.
        """

        if not self.checkcomplete():
            if type(left) == str:
            #if self.checkstring(left):
                self.stopproof(self.stopped_string, self.blankstatement, self.or_introname, str(line), '', comments)
            elif type(right) == str:
            #elif self.checkstring(right):
                self.stopproof(self.stopped_string, self.blankstatement, self.or_introname, str(line), '', comments)
            else:
                if not self.checkline(line):
                    self.stopproof(self.stopped_nosuchline, self.blankstatement, self.or_introname, str(line), '', comments)
                else:
                    level, statement = self.getlevelstatement(line)
                    if not self.checkcurrentlevel(level): #not self.checklinescope(level): #level > self.level:
                        self.stopproof(self.stopped_linescope, self.blankstatement, self.or_introname, str(line), '', comments)
                    else:
            
                        if left is None and right is None:
                            self.stopproof(self.stopped_novaluepassed, self.blankstatement, self.or_introname, str(line), '', comments)
                        else:
                            if left is None:
                                disjunction = Or(statement, right)
                            elif right is None:
                                disjunction = Or(left, statement)
                            newcomment = self.availablecomplete('or_intro', disjunction, comments)
                            self.lines.append(
                                [
                                    disjunction, 
                                    self.level, 
                                    self.currentblockid, 
                                    self.or_introname, 
                                    str(line), 
                                    '',
                                    newcomment
                                ]
                            )                 
       
    def reit(self, line: int, comments: str = ''):
        """A statement that already exists which can be accessed can be reused.

        Parameter:
            line: The line number of the statement.

        Example:
            >>> from altrea.boolean import And, Or, Not, Wff, F, Implies
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import show
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> p = Proof()
            >>> p.addgoal(Implies(A, B))
            >>> p.addpremise(B)
            >>> p.openblock(A)
            >>> p.reit(1)
            >>> show(p, latex=0)
              Statement  Level  Block         Rule Lines Blocks Comment
            C    A -> B      0      0         Goal
            1         B      0      0      Premise
            2         A      1      1   Assumption
            3         B      1      1  Reiteration     1
        """
        
        if not self.checkcomplete():
            if not self.checkline(line):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.reitname, str(line), '', comments)
            else:
                level, statement = self.getlevelstatement(line)
                if level >= self.level: #not self.checklinescope(level): #level > self.level:
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.reitname, str(line), '', comments)
                else:
                    found = False
                    for i in self.lines:
                        if i[self.statementindex] == statement and i[self.levelindex] == self.level:
                            found = True
                            break
                    if found:
                        self.stopproof(self.stopped_alreadyavailable, self.blankstatement, self.reitname, str(line), '', comments)
                    else:
                        newcomment = self.availablecomplete('reit', statement, comments)
                        self.lines.append(
                            [
                                statement, 
                                self.level, 
                                self.currentblockid, 
                                self.reitname, 
                                str(line), 
                                '',
                                newcomment
                            ]
                        )                 
    