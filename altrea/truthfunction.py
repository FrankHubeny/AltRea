# altrea/truthfunction.py

"""The module provides functions to construct a proof in propositional logic.

The module contains three groups of functions: 

- Supporting functions called by other functions for routine procesing.
- Basic rules for the list of logical operators that one accepts for the logic.
- Derived rules which are short cuts for a proof using basic rules.

The following methods support other functions.  They are not intended to be called by the user directly.

- `checkavailable(rulename, comments)` - Based on the logic specified check if a warning comment 
should be posted for the proof line overwriting any comments provided by the user.
- `checkcompleteorstopped(statement)` - Mark the proof completed if the statement equals the goal.
- `getlevelblockstatements(blockid)` - Get the level, hypothesis statement and conclusion statement for the blockid.
- `getlevelstatement(line)` - Get the level and statement for the line id.
- `reftwolines(first, second)` - Join thw integers together into a string to record as set of lines or blocks.

The following are basic rules which the user may call after initializing a Proof.  Depending on
which logical operators one has, the basic list may include only a subset of this list.

- `addpremise` - ['C', 'CI', 'CO', 'I'] Add a premise
- `conjunction_elim` - ['C', 'CI', 'CO', 'I'] Conjunction Elimination
- `conjunction_intro` - ['C', 'CI', 'CO', 'I'] Conjunction Introduction
- `explosion` - ['C', 'CI', 'CO', 'I'] Explosion
- `coimplication_elim` - ['C', 'CI', 'CO', 'I'] Equivalence Elimination
- `coimplication_intro` - ['C', 'CI', 'CO', 'I'] Equivalence Introduction
- `implication_elim` - ['C', 'CI', 'CO', 'I'] Implication Elimination
- `implication_intro` - ['C', 'CI', 'CO', 'I'] Implication Introduction
- `lem` - ['C', 'CI', 'CO', 'I'] Law of Excluded Middle
- `negation_elim` - ['C', 'CI', 'CO', 'I'] Negation Elimination
- `negation_intro` - ['C', 'CI', 'CO', 'I'] Negation Introduction
- `hypothesis` - ['C', 'CI', 'CO', 'I'] Open a block with an hypothesis
- `disjunction_elim` - ['C', 'CI', 'CO', 'I'] Disjunction Elimination
- `disjunction_intro` - ['C', 'CI', 'CO', 'I'] Disjunction Introduction
- `reiterate` - ['C', 'CI', 'CO', 'I'] reiterateeration

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

    #columns = ['Statement', 'Level', 'Proof', 'Rule', 'Lines', 'Proofs', 'Comment']
    statementindex = 0
    levelindex = 1
    proofidindex = 2
    ruleindex = 3
    linesindex = 4
    proofsindex = 5
    commentindex = 6
    #lasthypothesisindex = 7
    lowestlevel = 0
    acceptedtypes = [And, Or, Not, Implies, Iff, Wff, F, T],
    falsename = F()
    goal_name = 'GOAL'
    premise_name = 'Premise'
    premise_tag = 'P'
    hypothesis_name = 'Hypothesis'
    hypothesis_tag = 'H'
    disjunction_intro_name = 'Disjunction Intro'
    disjunction_intro_tag = 'DI'
    disjunction_elim_name = 'Disjunction Elim'
    disjunction_elim_tag = 'DE'
    conjunction_intro_name = 'Conjunction Intro'
    conjunction_intro_tag = 'CI'
    conjunction_elim_name = 'Conjunction Elim'
    conjunction_elim_tag = 'CE'
    reiterate_name = 'Reiteration'
    reiterate_tag = 'R'
    implication_intro_name = 'Implication Intro'
    implication_intro_tag = 'II'
    implication_elim_name = 'Implication Elim'
    implication_elim_tag = 'IE'
    negation_intro_name = 'Negation Intro'
    negation_intro_tag = 'NI'
    negation_elim_name = 'Negation Elim'
    negation_elim_tag = 'NE'
    indirectproof_name = 'Indirect Proof'
    coimplication_intro_name = 'Coimplication Intro'
    coimplication_intro_tag = 'CII'
    coimplication_elim_name = 'Coimplication Elim'
    coimplication_elim_tag = 'CIE'
    xor_intro_name = 'Xor Intro'
    xor_intro_tag = 'XOI'
    xor_elim_name = 'Xor Elim'
    xor_elim_tag = 'XOE'
    nand_intro_name = 'Nand Intro'
    nand_intro_tag = 'NAI'
    nand_elim_name = 'Nand Elim'
    nand_elim_tag = 'NAE'
    nor_intro_name = 'Nor Intro'
    nor_intro_tag = 'NOI'
    nor_elim_name = 'Nor Elim'
    nor_elim_tag = 'NOE'
    xnor_intro_name = 'Xnor Intro'
    xnor_intro_tag = 'XNI'
    xnor_elim_name = 'Xnor Elim'
    xnor_elim_tag = 'XNE'
    lem_name = 'LEM'
    lem_tag = 'LEM'
    doublenegation_intro_name = 'Double Negation Intro'
    doublenegation_intro_tag = 'DNI'
    doublenegation_elim_name = 'Double Negation Elim'
    doublenegation_elim_tag = 'DNE'
    demorgan_name = 'DeMorgan'
    explosion_name = 'Explosion'
    explosion_tag = 'X'
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
    stopped_linescope = 'Reference item is out of scope.'
    stopped_nogoal = 'The proof does not yet have a goal.'
    stopped_nosuchline = 'The referenced line does not exist.'
    stopped_nosuchblock = 'The referenced block does not exist.'
    stopped_notantecedent = 'One statement is not the antecedent of the other.'
    stopped_notconjunction = 'The referenced item is not a conjunction.'
    stopped_notcontradiction = 'The referenced itemss are not contradictory.'
    stopped_notdemorgan = 'The referenced item is not a DeMorgan statement.'
    stopped_notdoublenegation = 'The referenced line is not a double negation.'
    stopped_notfalse = 'The referenced item is not false.'
    stopped_notimplication = 'The referenced item is not an implication.'
    stopped_notsameconclusion = 'The two conclusions are not the same.'
    stopped_notsamestatement = 'The referenced items are not the same.'
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
        'I': 'Intuitionist Propositional Logic',
        'MC': 'Metamath Classical Logic',
        'MI': 'Metamath Intuitionist Logic',
        'MNF': 'Metamath New Foundations Logic',
    }
    availablelogics = {
        'addpremise': ['C', 'CI', 'CO', 'I'],
        'addgoal': ['C', 'CI', 'CO', 'I'],
        'conjunction_elim': ['C', 'CI', 'CO', 'I'],
        'conjunction_intro': ['C', 'CI', 'CO', 'I'],
        'closeblock': ['C', 'CI', 'CO', 'I'],
        'demorgan': ['C', 'CI', 'CO', 'I'],
        'doublenegation_elim': ['C', 'CI', 'CO', 'I'],
        'doublenegation_intro': ['C', 'CI', 'CO', 'I'],
        'explosion': ['C', 'CI', 'CO', 'I'],
        'coimplication_elim': ['C', 'CI', 'CO', 'I'],
        'coimplication_intro': ['C', 'CI', 'CO', 'I'],
        'implication_elim': ['C', 'CI', 'CO', 'I'],
        'implication_intro': ['C', 'CI', 'CO', 'I'],
        'lem': ['C', 'CI', 'CO', 'I'],
        'negation_elim': ['C', 'CI', 'CO', 'I'],
        'nconjunction_intro': ['C', 'CI', 'CO', 'I'],
        'nconjunction_elim': ['C', 'CI', 'CO', 'I'],
        'ndisjunction_intro': ['C', 'CI', 'CO', 'I'],
        'negation_elim': ['C', 'CI', 'CO', 'I'],
        'negation_intro': ['C', 'CI', 'CO', 'I'],
        'hypothesis': ['C', 'CI', 'CO', 'I'],
        'disjunction_elim': ['C', 'CI', 'CO', 'I'],
        'disjunction_intro': ['C', 'CI', 'CO', 'I'],
        'reiterate': ['C', 'CI', 'CO', 'I'],
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
        self.currentproof = [1]
        self.currentproofid = 0
        self.proofdata = [[self.name, self.logic]]
        self.prooflist = [[self.lowestlevel, self.currentproof, self.parentproofid, []]]
        self.level = self.lowestlevel
        self.status = ''
        self.premises = []
        if self.logic in self.logicdictionary:
            self.lines = [['', 0, 0, '', '', '', '']]
        else:
            self.status = self.stopped
            self.lines = [['', 0, 0, '', '', '', ''.join([self.stopped, self.stopped_connector, self.stopped_undefinedlogic])]]

    """SUPPORT FUNCTIONS"""

    def checkcompleteorstopped(self):
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

        return blockid >= 0 and blockid < len(self.prooflist)
    
    def checkblockclosed(self, blockid: int):
        """Check if the blockid represents a closed block."""

        return len([blockid][1]) == 2
    
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
                        self.prooflist[0][1].append(len(self.lines)-1)
                        newcomment = self.complete
        if comments == '':
            return newcomment
        else:
            if newcomment == '':
                return comments
            else:
                return ''.join([newcomment, self.comments_connector, comments])

    def getcurrentitemid(self):
        """Returns the number of the current item of the proof."""

        return len(self.lines)
    
    def getlevelblockstatements(self, blockid: int) -> tuple:
        """Given a block id, return the level the block is in and the hypothesis and conclusion statements."""

        level = self.prooflist[blockid][0]
        hypothesis = self.lines[self.prooflist[blockid][1][0]][self.statementindex]
        conclusion = self.lines[self.prooflist[blockid][1][1]][self.statementindex]
        return level, hypothesis, conclusion
    
    def getlevelstatement(self, line: int) -> tuple:
        """Given a line id, return the level and the statement on that line."""

        level = self.lines[line][self.levelindex]
        statement = self.lines[line][self.statementindex]
        return level, statement
    

    def getparentproofid(self, proofid: int) -> int:
        """Returns the parent proof id of a given proof."""
    
        return self.prooflist[proofid][2]
    
    def getproof(self, proofid: int) -> tuple:
        """Returns the leve, hypothesis statement, conclusion statement and parent proof id."""

        level = self.prooflist[proofid][0]
        hypothesis = self.lines[self.prooflist[proofid][3][0]][self.statementindex]
        if len(self.prooflist[proofid][3]) > 1:
            for i in range(len(self.prooflist[proofid][3])):
                if i > 0:
                    hypothesis = And(hypothesis, self.lines[self.prooflist[proofid][3][i]][self.statementindex])
        conclusion = self.lines[self.prooflist[proofid][1][1]][self.statementindex]
        parentproofid = self.prooflist[proofid][2]
        return level, hypothesis, conclusion, parentproofid
    

    def reftwolines(self, first: int, second: int) -> str:
        """Join two integers representing line ids or block ids as strings together."""

        return ''.join([str(first), ', ', str(second)])
    
    def refproof(self, proofid: int):
        """Formats a proof used in a proof."""

        proof = self.prooflist[proofid][1]
        return ''.join([str(proof[0]), '-', str(proof[1])])
    
    def stopproof(self, message: str, statement, rule: str, lines: str, blocks: str, comments: str = ''):
        self.status = self.stopped
        stoppedmessage = ''
        if rule == self.goal_name:
            if comments == '':
                self.lines[0][self.commentindex] = ''.join([self.stopped, self.stopped_connector, message])
            else:
                self.lines[0][self.commentindex] = ''.join([self.stopped, self.stopped_connector, message, self.comments_connector, comments])
        else:
            if comments == '':
                stoppedmessage = ''.join([self.stopped, self.stopped_connector, message])
            else:
                stoppedmessage = ''.join([self.stopped, self.stopped_connector, message, self.comments_connector, comments])
            self.lines.append(
                [
                    statement, 
                    self.level, 
                    self.currentproofid, 
                    rule, 
                    lines, 
                    blocks, 
                    stoppedmessage
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

        # Look for errors
        if not self.checkcompleteorstopped():
            #if type(goal) == str:
            if self.checkstring(goal):
                self.stopproof(self.stopped_string, goal, self.goal_name, 0, 0, comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
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
            self.lines[0][self.ruleindex] = self.goal_name
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

        # Look for errors
        if not self.checkcompleteorstopped():
            #if type(premise) == str:
            if self.checkstring(premise):
                self.stopproof(self.stopped_string, premise, self.premise_name, '', '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.premise_name, '', '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            self.premises.append(premise)
            newcomment = self.availablecomplete('addpremise', premise, comments)
            self.lines.append(
                [
                    premise, 
                    0, 
                    self.currentproofid, 
                    self.premise_name, 
                    '', 
                    '', 
                    newcomment
                ]
            )
            self.proofdata.append([self.premise_tag, premise.pattern()])
        
    def conjunction_elim(self, line: int, comments: str = ''):
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
            >>> p.conjunction_elim(1)
            >>> show(p, latex=0)
              Statement  Level  Block      Rule Lines Blocks             Comment
            C      A, B      0      0      Goal                        one - two
            1     A & B      0      0   Premise
            2         A      0      0  And Elim     1         PARTIAL COMPLETION
            3         B      0      0  And Elim     1                   COMPLETE

            Most rules have a scope limited to the level they are on.  They cannot 
            reference lines from a block above them nor from a line at a level
            below them.  However, they can reiterateerate those statements from a lower level
            to make them available for use on the current level.  Consider the following
            stopped attempt to derive C >> (A & B) from the premise A & B.


        """

        # Look for errors
        if not self.checkcompleteorstopped():
            if not self.checkline(line):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.conjunction_elim_name, str(line), '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.premise_name, '', '', comments)
            else:
                level, statement = self.getlevelstatement(line)
                if not self.checkcurrentlevel(level):
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.conjunction_elim_name, str(line), '', comments)
                elif type(statement) != And:
                    self.stopproof(self.stopped_notconjunction, self.blankstatement, self.conjunction_elim_name, str(line), '', comments)

        # If no errors, perform the task
        if not self.checkcompleteorstopped():
            for conjunct in [statement.left, statement.right]:
                newcomment = self.availablecomplete('conjunction_elim', conjunct, comments)
                self.lines.append(
                    [
                        conjunct, 
                        self.level, 
                        self.currentproofid, 
                        self.conjunction_elim_name, 
                        str(line), 
                        '',
                        newcomment
                    ]
                )   
                self.proofdata.append([self.conjunction_elim_tag, conjunct.pattern()])
                if self.status == self.complete:
                    break              
                
    def conjunction_intro(self, first: int, second: int, comments: str = ''):
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
            >>> p.conjunction_intro(1, 2)
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
            >>> p.conjunction_intro(1, 1, 'Obvious result')
            >>> show(p, latex=0)
              Statement  Level  Block       Rule Lines Blocks                    Comment
            C     A & A      0      0       Goal
            1         A      0      0    Premise
            2     A & A      0      0  And Intro  1, 1         COMPLETE - Obvious result

            In the previous examples all of the statements were on level 0, the same level.
            Both the and_into and conjunction_elim require that the statenents they use be on the 
            same level as the current level.  However, one can use statements from a
            lower level by reiterateerating then using the reiterate rule.  Here is an example of that.
        """

        # Look for errors
        if not self.checkcompleteorstopped():
            if not self.checkline(first):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.conjunction_intro_name, str(first), '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.conjunction_elim_name, '', '', comments)
            else:
                firstlevel, firstconjunct = self.getlevelstatement(first)
                if not self.checkcurrentlevel(firstlevel):  
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.conjunction_intro_name, str(first), '', comments)
                elif not self.checkline(second):
                    self.stopproof(self.stopped_nosuchline, self.blankstatement, self.conjunction_intro_name, str(second), '', comments)
                else:
                    secondlevel, secondconjunct = self.getlevelstatement(second)
                    if not self.checkcurrentlevel(secondlevel):  
                        self.stopproof(self.stopped_linescope, self.blankstatement, self.conjunction_intro_name, str(second), '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            andstatement = And(firstconjunct, secondconjunct)
            newcomment = self.availablecomplete('conjunction_intro', andstatement, comments)
            self.lines.append(
                [
                    andstatement, 
                    self.level, 
                    self.currentproofid, 
                    self.conjunction_intro_name, 
                    self.reftwolines(first, second), 
                    '',
                    newcomment
                ]
            ) 
            self.proofdata.append([self.conjunction_intro_tag, andstatement.pattern()])                

    def addhypothesis(self,
                      hypothesis: And | Or | Not | Implies | Iff | Wff | F | T,
                      comments: str = ''):
        """Adds to the currently opened subproof an hypothesis.
        
        Parameters:
            hypothesis: The hypothesis that will be added.
            comments: Options comments entered by the user.
            
        Examples:
        
        """

        # Look for errors
        if not self.checkcompleteorstopped():
            if type(hypothesis) == str:
            #if self.checkstring(statement):
                self.stopproof(self.stopped_string, self.blankstatement, self.hypothesis_name, '', '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.hypothesis_name, '', '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            nextline = len(self.lines)
            self.prooflist[self.currentproofid][3].append(nextline)
            newcomment = self.availablecomplete('hypothesis', hypothesis, comments)
            self.lines.append(
                [
                    hypothesis, 
                    self.level, 
                    self.currentproofid, 
                    self.hypothesis_name, 
                    '', 
                    '',
                    newcomment
                ]
            )
            self.proofdata.append([self.hypothesis_tag, hypothesis.pattern()])                 


    def hypothesis(self, 
                   hypothesis: And | Or | Not | Implies | Iff | Wff | F | T,
                   comments: str = ''):
        """Opens a uniquely identified subproof of items with an hypothesis.
        
        Examples:

        Parameters:
            statement: The hypothesis that starts the block of derived statements.
        """

        # Look for errors
        if not self.checkcompleteorstopped():
            if type(hypothesis) == str:
            #if self.checkstring(statement):
                self.stopproof(self.stopped_string, self.blankstatement, self.hypothesis_name, '', '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.hypothesis_name, '', '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            parentproofid = self.currentproofid
            self.level += 1
            nextline = len(self.lines)
            self.currentproof = [nextline]
            self.currenthypotheses = [nextline]
            self.prooflist.append([self.level, self.currentproof, parentproofid, self.currenthypotheses])
            self.currentproofid = len(self.prooflist) - 1
            newcomment = self.availablecomplete('hypothesis', hypothesis, comments)
            self.lines.append(
                [
                    hypothesis, 
                    self.level, 
                    self.currentproofid, 
                    self.hypothesis_name, 
                    '', 
                    '',
                    newcomment
                ]
            )             
            self.proofdata.append([self.hypothesis_tag, hypothesis.pattern()])    

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

        # Look for errors
        if not self.checkcompleteorstopped():
            if not self.checkline(line):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.demorgan_name, str(line), '', comments)
            else:
                level, statement = self.getlevelstatement(line)
                if not self.checkcurrentlevel(level):  
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.demorgan_name, str(line), '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            if type(statement) == Not:
                if type(statement.negated) == And:
                    andstatement = statement.negated
                    firstsubstatement = andstatement.left
                    secondsubstatement = andstatement.right
                    final = Or(Not(firstsubstatement), Not(secondsubstatement))
                    newcomment = self.availablecomplete('demorgan', final, comments)
                    self.lines.append([final, self.level, self.currentproofid, self.demorgan_name, str(line), '', newcomment])
                elif type(statement.negated) == Or:
                    orstatement = statement.negated
                    firstsubstatement = orstatement.left
                    secondsubstatement = orstatement.right
                    final = And(Not(firstsubstatement), Not(secondsubstatement))
                    newcomment = self.availablecomplete('demorgan', final, comments)
                    self.lines.append([final, self.level, self.currentproofid, self.demorgan_name, str(line), '', newcomment])
                else:
                    self.stopproof(self.stopped_notdemorgan, self.blankstatement, self.demorgan_name, str(line), '', comments)
            elif type(statement) == Or:
                firstsubstatement = statement.left
                secondsubstatement = statement.right               
                if type(firstsubstatement) == Not and type(secondsubstatement) == Not:
                    final = Not(And(firstsubstatement.negated, secondsubstatement.negated))
                    newcomment = self.availablecomplete('demorgan', final, comments)
                    self.lines.append([final, self.level, self.currentproofid, self.demorgan_name, str(line), '', newcomment])
                else:
                    self.stopproof(self.stopped_notdemorgan, self.blankstatement, self.demorgan_name, str(line), '', comments)
            elif type(statement) == And:
                firstsubstatement = statement.left
                secondsubstatement = statement.right
                if type(firstsubstatement) == Not and type(secondsubstatement) == Not:
                    final = Not(Or(firstsubstatement.negated, secondsubstatement.negated))
                    newcomment = self.availablecomplete('demorgan', final, comments)
                    self.lines.append([final, self.level, self.currentproofid, self.demorgan_name, str(line), '', newcomment])
                else:
                    self.stopproof(self.stopped_notdemorgan, self.blankstatement, self.demorgan_name, str(line), '', comments)
            else:
                self.stopproof(self.stopped_notdemorgan, self.blankstatement, self.demorgan_name, str(line), '')

    def doublenegation_intro(self, line: int, comments: str = ''):
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
            >>> p.doublenegation_intro(1, comments='double negative works')
            >>> show(p, latex=0)
              Statement  Level  Block  ... Lines Blocks                           Comment
            C       ~~A      0      0  ...                           double negative goal
            1         A      0      0  ...                    make this a double negative
            2       ~~A      0      0  ...     1         COMPLETE - double negative works

        '''

        # Look for errors
        if not self.checkcompleteorstopped():
            if not self.checkline(line):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.doublenegation_intro_name, str(line), '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.doublenegation_intro_name, '', '', comments)
            else:
                level, statement = self.getlevelstatement(line)
                if not self.checkcurrentlevel(level): #not self.checklinescope(level):
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.doublenegation_intro_name, str(line), '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            newstatement = Not(Not(statement))
            newcomment = self.availablecomplete('doublenegation_intro', newstatement, comments)
            self.lines.append(
                [
                    newstatement, 
                    self.level, 
                    self.currentproofid, 
                    self.doublenegation_intro_name, 
                    str(line), 
                    '', 
                    newcomment
                ]
            )
            self.proofdata.append([self.doublenegation_intro_tag, newstatement.pattern()])

    def doublenegation_elim(self, line: int, comments: str = ''):
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
            >>> p.doublenegation_intro(1, comments="hmm, I'm going in the wrong direction")
            >>> p.doublenegation_elim(2)
            >>> p.doublenegation_elim(3, comments="that's better!")
            >>> show(p, latex=0)
              Statement  Level  Block  ... Lines Blocks                                Comment
            C         A      0      0  ...                                         derive this
            1       ~~A      0      0  ...                                           from this
            2     ~~~~A      0      0  ...     1         hmm, I'm going in the wrong direction
            3       ~~A      0      0  ...     2
            4         A      0      0  ...     3                     COMPLETE - that's better!
        '''

        # Look for errors
        if not self.checkcompleteorstopped():
            if not self.checkline(line):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.doublenegation_elim_name, str(line), '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.doublenegation_elim_name, '', '', comments)
            else:
                level, statement = self.getlevelstatement(line)
                if not self.checkcurrentlevel(level): #not self.checklinescope(level):
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.doublenegation_elim_name, str(line), '', comments)
                elif type(statement) != Not:
                    self.stopproof(self.stopped_notdoublenegation, self.blankstatement, self.doublenegation_elim_name, str(line), '', comments)
                elif type(statement.negated) != Not:
                    self.stopproof(self.stopped_notdoublenegation, self.blankstatement, self.doublenegation_elim_name, str(line), '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            newstatement = statement.negated.negated
            newcomment = self.availablecomplete('doublenegation_elim', newstatement, comments)
            self.lines.append(
                [
                    newstatement, 
                    self.level, 
                    self.currentproofid, 
                    self.doublenegation_elim_name, 
                    str(line), 
                    '', 
                    newcomment
                ]
            )
            self.proofdata.append([self.doublenegation_elim_tag, newstatement.pattern()])

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
            >>> p.negation_elim(1, 2)
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
            >>> # p.negation_elim(1, 2)
            >>> p.explosion(And(A, B))
            >>> show(p, latex=0)
              Statement  Level  ...  Blocks                                     Comment
            C     A & B      0  ...
            1         A      0  ...
            2        ~A      0  ...
            3                0  ...          STOPPED: The referenced line is not false.
        """
        
        # Look for errors
        if not self.checkcompleteorstopped():
            if self.checkstring(statement):
                self.stopproof(self.stopped_string, statement, self.explosion_name, '', '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.explosion_name, '', '', comments)
            else:
                line = len(self.lines) - 1
                blockid = self.lines[line][self.proofidindex]
                if line == 0:
                    self.stopproof(self.stopped_nosuchline, self.blankstatement, self.explosion_name, str(line), '', comments)
                else:
                    level, falsestatement = self.getlevelstatement(line)
                    if level != self.level or blockid != self.currentproofid:
                        self.stopproof(self.stopped_blockscope, self.blankstatement, self.explosion_name, str(line), '', comments)
                    elif falsestatement != self.falsename:
                        self.stopproof(self.stopped_notfalse, self.blankstatement, self.explosion_name, str(line), '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            newcomment = self.availablecomplete('explosion', statement, comments)
            self.lines.append(
                [
                    statement, 
                    self.level, 
                    self.currentproofid, 
                    self.explosion_name, 
                    str(line), 
                    '',
                    newcomment
                ]
            ) 
            self.proofdata.append([self.explosion_tag, statement.pattern()])                
    
    def coimplication_elim(self, first: int, second: int, comments: str = ''):
        """Given an iff statement and a proposition one can derive the other proposition.
        
        Parameters:
            first: A statement containing either a proposition or an iff statement.
            second: A second statement containing either a proposition or an iff statement.
            comments: Comments on this line of the proof.
        
        Examples:

        """

        # Look for errors
        if not self.checkcompleteorstopped():
            if not self.checkline(first):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.coimplication_elim_name, '', '', comments)
            else:
                firstlevel, firststatement = self.getlevelstatement(first)
                if not self.checkcurrentlevel(firstlevel): 
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.coimplication_elim_name, '', '', comments)
                else:
                    if not self.checkline(second):
                        self.stopproof(self.stopped_nosuchline, self.blankstatement, self.coimplication_elim_name, '', '', comments)
                    else:
                        secondlevel, secondstatement = self.getlevelstatement(second)
                        if not self.checkcurrentlevel(secondlevel): 
                            self.stopproof(self.stopped_linescope, self.blankstatement, self.coimplication_elim_name, '', '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():      
            if type(firststatement) == Iff:
                if secondstatement != firststatement.left:
                    self.stopproof(self.stopped_notantecedent, self.blankstatement, self.coimplication_elim_name, '', '', comments)
                else:
                    newcomment = self.availablecomplete('coimplication_elim', firststatement.right, comments)
                    self.lines.append(
                        [
                            firststatement.right, 
                            self.level, 
                            self.currentproofid, 
                            self.coimplication_elim_name, 
                            self.reftwolines(first, second), 
                            '', 
                            newcomment
                        ]
                    )
                    self.proofdata.append([self.coimplication_elim_tag, firststatement.right.pattern()])
            elif type(secondstatement) == Iff:
                if firststatement != secondstatement.left:
                    self.stopproof(self.stopped_notantecedent, self.blankstatement, self.coimplication_elim_name, '', '', comments)
                else:
                    newcomment = self.availablecomplete('coimplication_elim', secondstatement.right, comments)
                    self.lines.append(
                        [
                            secondstatement.right, 
                            self.level, 
                            self.currentproofid, 
                            self.coimplication_elim_name, 
                            self.reftwolines(first, second), 
                            '', 
                            newcomment
                        ]
                    ) 
                    self.proofdata.append([self.coimplication_elim_tag, secondstatement.right.pattern()])                  
            else:
                self.stopproof(self.stopped_notantecedent, self.blankstatement, self.coimplication_elim_name, '', '', comments)
                
    def coimplication_intro(self, first: int, second: int, comments: str = ''):
        """Derive a live using the if and only if symbol.
        
        Parameters:
            first: The first item number to obtain an implication going in one direction.
            second: The second item number to obtain an implication going in the other direction.
            comments: Comments entered by the user for this line.

        Examples:
        """

        # Look for errors
        if not self.checkcompleteorstopped():
            if not self.checkline(first):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.coimplication_intro_name, '', '', comments)
            else:
                firstlevel, firststatement = self.getlevelstatement(first)
                if not self.checkcurrentlevel(firstlevel): 
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.coimplication_intro_name, '', '', comments)
                elif not self.checkline(second):
                    self.stopproof(self.stopped_nosuchline, self.blankstatement, self.coimplication_intro_name, '', '', comments)
                else:
                    secondlevel, secondstatement = self.getlevelstatement(second)
                    if not self.checkcurrentlevel(secondlevel): 
                        self.stopproof(self.stopped_linescope, self.blankstatement, self.coimplication_intro_name, '', '', comments)
                    elif type(firststatement) != Implies:
                        self.stopproof(self.stopped_notimplication, self.blankstatement, self.coimplication_intro_name, '', '', comments)
                    elif type(secondstatement) != Implies:
                        self.stopproof(self.stopped_notimplication, self.blankstatement, self.coimplication_intro_name, '', '', comments)
                    elif firststatement.left != secondstatement.right:
                        self.stopproof(self.stopped_notsamestatement, self.blankstatement, self.coimplication_intro_name, '', '', comments)
                    elif firststatement.right != secondstatement.left:
                        self.stopproof(self.stopped_notsamestatement, self.blankstatement, self.coimplication_intro_name, '', '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            newstatement = Iff(firststatement.left, firststatement.right)
            newcomment = self.availablecomplete('coimplication_intro', newstatement, comments)
            self.lines.append(
                [
                    newstatement, 
                    self.level, 
                    self.currentproofid, 
                    self.coimplication_intro_name, 
                    '',
                    self.reftwolines(first, second), 
                    newcomment
                ]
            )   
            self.proofdata.append([self.coimplication_intro_tag, newstatement.pattern()])        
           
    def implication_elim(self, first: int, second: int, comments: str = ''):
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
            >>> p.implication_elim(1,2)
            >>> show(p, latex=0)
                      Statement  Level  Block          Rule Lines Blocks   Comment
            Line              B      0      0          Goal
            1                 A      0      0       Premise
            2     Implies(A, B)      0      0       Premise
            3                 B      0      0  Implies Elim  1, 2         COMPLETE

        """

        # Look for errors
        if not self.checkcompleteorstopped():
            if not self.checkline(first):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.implication_elim_name, '', '', comments)
            else:
                firstlevel, firststatement = self.getlevelstatement(first)
                if not self.checkcurrentlevel(firstlevel): 
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.implication_elim_name, '', '', comments)
                else:
                    if not self.checkline(second):
                        self.stopproof(self.stopped_nosuchline, self.blankstatement, self.implication_elim_name, '', '', comments)
                    else:
                        secondlevel, secondstatement = self.getlevelstatement(second)
                        if not self.checkcurrentlevel(secondlevel): 
                            self.stopproof(self.stopped_linescope, self.blankstatement, self.implication_elim_name, '', '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():      
            if type(firststatement) == Implies:
                if secondstatement != firststatement.left:
                    self.stopproof(self.stopped_notantecedent, self.blankstatement, self.implication_elim_name, '', '', comments)
                else:
                    newcomment = self.availablecomplete('implication_elim', firststatement.right, comments)
                    self.lines.append(
                        [
                            firststatement.right, 
                            self.level, 
                            self.currentproofid, 
                            self.implication_elim_name, 
                            self.reftwolines(first, second), 
                            '', 
                            newcomment
                        ]
                    )
                    self.proofdata.append([self.implication_elim_tag, firststatement.right.pattern()])
            elif type(secondstatement) == Implies:
                if firststatement != secondstatement.left:
                    self.stopproof(self.stopped_notantecedent, self.blankstatement, self.implication_elim_name, '', '', comments)
                else:
                    newcomment = self.availablecomplete('implication_elim', secondstatement.right, comments)
                    self.lines.append(
                        [
                            secondstatement.right, 
                            self.level, 
                            self.currentproofid, 
                            self.implication_elim_name, 
                            self.reftwolines(first, second), 
                            '', 
                            newcomment
                        ]
                    ) 
                    self.proofdata.append([self.implication_elim_tag, secondstatement.right.pattern()])                  
            else:
                self.stopproof(self.stopped_notantecedent, self.blankstatement, self.implication_elim_name, '', '', comments)

    def implication_intro(self, comments: str = ''):
        """This is the implication introduction rule.
        
        Parameters:
            comments: Optional comments the user wishes to enter.  Also a place where AltRea may display in addition
                stopped and completion messages.
                
        Examples:
        
            >>> from altrea.boolean import Wff, Implies
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import show, fitch
            >>> P = Wff('P')
            >>> p = Proof()
            >>> p.addgoal(Implies(P, P))
            >>> p.hypothesis(P)
            >>> p.imp_int()
            >>> fitch(p, latex=0)
              Proposition          Rule   Comment
            0      P -> P          GOAL
            1        P  |           hyp
            2      P -> P  1-1, imp int  COMPLETE
        """

        # Look for errors
        if not self.checkcompleteorstopped():
            if self.currentproofid == 0:
                self.stopproof(self.stopped_closezeroblock, self.blankstatement, self.implication_intro_name, '', '')

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            proofid = self.currentproofid
            self.prooflist[proofid][1].append(len(self.lines)-1)
            self.level -= 1
            level, antecedent, consequent, parentproofid = self.getproof(proofid)
            self.currentproofid = parentproofid
            self.currentproof = self.prooflist[parentproofid][1]
            implication = Implies(antecedent, consequent)
            newcomment = self.availablecomplete('implication_intro', implication, comments)
            self.lines.append(
                [
                    implication, 
                    self.level, 
                    self.currentproofid, 
                    self.implication_intro_name, 
                    '', 
                    self.refproof(proofid), 
                    newcomment
                ]
            )        
            self.proofdata.append([self.implication_intro_tag, implication.pattern()])           
            
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
            >>> p.hypothesis(P)
            >>> p.disjunction_intro(~P,1)
            >>> p.closeblock()
            >>> p.hypothesis(~P)
            >>> p.disjunction_intro(P,3)
            >>> p.closeblock()
            >>> p.lem(1,2)
            >>> show(p, latex=0)
                Statement  Level  Block        Rule Lines Blocks   Comment
            Line    P | ~P      0      0        Goal
            1            P      1      1  hypothesis
            2       P | ~P      1      1    Or Intro     1
            3           ~P      1      2  hypothesis
            4       P | ~P      1      2    Or Intro     3
            5       P | ~P      0      0         LEM         1, 2  COMPLETE

        """

        # Look for errors
        if not self.checkcompleteorstopped():
            if not self.checkblockid(first):
                self.stopproof(self.stopped_nosuchblock, self.blankstatement, self.lem_name, '', '', comments)
            else:
                firstlevel, firsthypothesis, firstconclusion = self.getlevelblockstatements(first)
                if not self.checkblockid(second):
                    self.stopproof(self.stopped_nosuchblock, self.blankstatement, self.lem_name, '', '', comments)
                else:
                    secondlevel, secondhypothesis, secondconclusion = self.getlevelblockstatements(second)           
                    if firstlevel != secondlevel:
                        self.stopproof(self.stopped_notsamelevel, self.blankstatement, self.lem_name, '', '', comments)
                    else:     
                        if  type(firsthypothesis) == Not and firsthypothesis.negated.equals(secondhypothesis):
                            final = firstconclusion       
                        elif type(secondhypothesis) == Not and secondhypothesis.negated.equals(firsthypothesis):
                            final = firstconclusion   
                        else:
                            self.stopproof(self.stopped_notlem, self.blankstatement, self.lem_name, '', '', comments)
                        if not self.checkcompleteorstopped():
                            if not firstconclusion.equals(secondconclusion):
                                self.stopproof(self.stopped_notsameconclusion, self.blankstatement, self.lem_name, '', '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            newcomment = self.availablecomplete('lem', final, comments)
            self.lines.append(
                [
                    final, 
                    self.level, 
                    self.currentproofid, 
                    self.lem_name, 
                    '', 
                    self.reftwolines(first, second),
                    newcomment
                ]
            ) 
            self.proofdata.append([self.lem_tag, final.pattern()])                

    def nconjunction_elim(self, first: int, second: int, comments: str = ''):
        pass

    def nconjunction_intro(self, first: int, second: int, comments: str = ''):
        pass

    def ndisjunction_elim(self, first: int, second: int, comments: str = ''):
        pass

    def ndisjunction_intro(self, first: int, second: int, comments: str = ''):
        pass

    def negation_elim(self, first: int, second: int, comments: str = ''):
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
            >>> p.negation_elim(1, 2)
            >>> p.explosion(And(A, B), 3)
            >>> show(p, latex=0)
              Statement  Level  Block       Rule Lines Blocks   Comment
            C     A & B      0      0       Goal
            1         A      0      0    Premise
            2        ~A      0      0    Premise
            3         X      0      0   Not Elim  1, 2
            4     A & B      0      0  Explosion     3         COMPLETE                 
        """
        
        # Look for errors
        if not self.checkcompleteorstopped():
            if not self.checkline(first):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.negation_elim_name, str(first), '', comments)
            elif not self.checkline(second):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.negation_elim_name, str(second), '', comments)
            else:
                firstlevel, firststatement = self.getlevelstatement(first)
                secondlevel, secondstatement = self.getlevelstatement(second)
                if not self.checkcurrentlevel(firstlevel):
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.negation_elim_name, '', '', comments)
                elif not self.checkcurrentlevel(secondlevel):
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.negation_elim_name, '', '', comments)
                else:
                    if not Not(firststatement).equals(secondstatement) and not Not(secondstatement).equals(firststatement):
                        self.stopproof(self.stopped_notcontradiction, self.blankstatement, self.negation_elim_name, self.reftwolines(first, second), '', comments)
                    elif firstlevel > self.level:
                        self.stopproof(self.stopped_linescope, self.blankstatement, self.negation_elim_name, str(first), '', comments)
                    elif secondlevel > self.level:
                        self.stopproof(self.stopped_linescope, self.blankstatement, self.negation_elim_name, str(second), '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            newcomment = self.availablecomplete('negation_elim', self.falsename, comments)
            self.lines.append(
                [
                    self.falsename, 
                    self.level, 
                    self.currentproofid, 
                    self.negation_elim_name, 
                    self.reftwolines(first, second), 
                    '',
                    newcomment
                ]
            )            
            self.proofdata.append([self.negation_elim_tag, self.falsename.pattern()])     

    def negation_intro(self, comments: str = ''):
        if not self.checkcompleteorstopped():
            if self.currentproofid == 0:
                self.stopproof(self.stopped_closezeroblock, self.blankstatement, self.closeblockname, '', '')
            else:
                proofid = self.currentproofid
                level, antecedent, consequent, parentproofid = self.getproof(proofid)
                self.prooflist[proofid][1].append(len(self.lines)-1)
                self.level -= 1
                self.currentproofid = parentproofid
                self.currentproof = self.prooflist[parentproofid][1]
                negation = Not(antecedent)
                newcomment = self.availablecomplete('negation_intro', negation, comments)
                self.lines.append(
                    [
                        negation, 
                        self.level, 
                        self.currentproofid, 
                        self.negation_intro_name, 
                        '', 
                        self.refproof(proofid), 
                        newcomment
                    ]
                )  
                self.proofdata.append([self.negation_intro_tag, negation.pattern()])                 

    def disjunction_elim(self, line: int, blockids: list, comments: str = ''):
        """Check the correctness of a disjunction elimination line before adding it to the proof.
        

        """

        if not self.checkcompleteorstopped():
            level, disjunction = self.getlevelstatement(line)
            if type(disjunction) != Or:
                raise altrea.exception.NotDisjunction(line, disjunction)
            if level != self.level:
                raise altrea.exception.ScopeError(line)
            if len(disjunction.args) != len(blockids):
                raise altrea.exception.BlockDisjuntsNotEqual(disjunction, blockids)
        
            try:
                firstlevel, firsthypothesis, firstconclusion = self.getlevelblockstatements(blockids[0])
            except:
                raise altrea.exception.NoSuchBlock(blockids[0])
            if firstlevel != self.level + 1:
                raise altrea.exception.BlockScopeError(blockids[0])
        
            try:
                secondlevel, secondhypothesis, secondconclusion = self.getlevelblockstatements(blockids[1])
            except:
                raise altrea.exception.NoSuchBlock(blockids[1])
            if secondlevel != self.level + 1:
                raise altrea.exception.BlockScopeError(blockids[1])
        
            if firstlevel != secondlevel:
                raise altrea.exception.NotSameLevel(firstlevel, secondlevel)
            if firstconclusion != secondconclusion:
                raise altrea.exception.ConclusionsNotTheSame(firstconclusion, secondconclusion)

            newcomment = self.availablecomplete('disjunction_elim', firstconclusion, comments)
            self.lines.append(
                [
                    firstconclusion, 
                    self.level, 
                    self.currentproofid, 
                    self.disjunction_elim_name, 
                    '', 
                    self.reftwolines(blockids[0], blockids[1]),
                    newcomment
                ]
            )    
            self.proofdata.append([self.disjunction_elim_tag, firstconclusion.pattern()])             

    def disjunction_intro(self, 
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
            >>> p.hypothesis(P)
            >>> p.disjunction_intro(~P,1)
            >>> p.closeblock()
            >>> p.hypothesis(~P)
            >>> p.disjunction_intro(P,3)
            >>> p.closeblock()
            >>> p.lem(1,2)
            >>> show(p, latex=0)
                Statement  Level  Block        Rule Lines Blocks   Comment
            Line    P | ~P      0      0        Goal
            1            P      1      1  hypothesis
            2       P | ~P      1      1    Or Intro     1
            3           ~P      1      2  hypothesis
            4       P | ~P      1      2    Or Intro     3
            5       P | ~P      0      0         LEM         1, 2  COMPLETE

        Exceptions:
            NoSuchLine: The referenced line does not exist in the proof.
            NoValuePassed: 
            ScopeError: The referenced statement is not accessible.
        """

        # Look for errors
        if not self.checkcompleteorstopped():
            if type(left) == str:
            #if self.checkstring(left):
                self.stopproof(self.stopped_string, self.blankstatement, self.disjunction_intro_name, str(line), '', comments)
            elif type(right) == str:
            #elif self.checkstring(right):
                self.stopproof(self.stopped_string, self.blankstatement, self.disjunction_intro_name, str(line), '', comments)
            elif not self.checkline(line):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.disjunction_intro_name, str(line), '', comments)
            else:
                level, statement = self.getlevelstatement(line)
                if not self.checkcurrentlevel(level): #not self.checklinescope(level): #level > self.level:
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.disjunction_intro_name, str(line), '', comments)
                elif left is None and right is None:
                    self.stopproof(self.stopped_novaluepassed, self.blankstatement, self.disjunction_intro_name, str(line), '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            if left is None:
                disjunction = Or(statement, right)
            elif right is None:
                disjunction = Or(left, statement)
            newcomment = self.availablecomplete('disjunction_intro', disjunction, comments)
            self.lines.append(
                [
                    disjunction, 
                    self.level, 
                    self.currentproofid, 
                    self.disjunction_intro_name, 
                    str(line), 
                    '',
                    newcomment
                ]
            )          
            self.proofdata.append([self.disjunction_intro_tag, disjunction.pattern()])       
       
    def reiterate(self, line: int, comments: str = ''):
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
            >>> p.hypothesis(A)
            >>> p.reiterate(1)
            >>> show(p, latex=0)
              Statement  Level  Block         Rule Lines Blocks Comment
            C    A -> B      0      0         Goal
            1         B      0      0      Premise
            2         A      1      1   hypothesis
            3         B      1      1  reiterateeration     1
        """
        
        # Look for errors
        if not self.checkcompleteorstopped():
            if not self.checkline(line):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.reiterate_name, str(line), '', comments)
            else:
                level, statement = self.getlevelstatement(line)
                if level >= self.level: # Special scope check for reiterate
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.reiterate_name, str(line), '', comments)
                else:
                    found = False
                    for i in self.lines:
                        if i[self.statementindex] == statement and i[self.levelindex] == self.level:
                            found = True
                            break
                    if found:
                        self.stopproof(self.stopped_alreadyavailable, self.blankstatement, self.reiterate_name, str(line), '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            newcomment = self.availablecomplete('reiterate', statement, comments)
            self.lines.append(
                [
                    statement, 
                    self.level, 
                    self.currentproofid, 
                    self.reiterate_name, 
                    str(line), 
                    '',
                    newcomment
                ]
            )  
            self.proofdata.append([self.reiterate_tag, statement.pattern()])               
    