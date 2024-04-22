# altrea/newtf.py

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

    columns = ['Statement', 'Level', 'Block', 'Rule', 'Lines', 'Blocks', 'Comment']
    statementindex = 0
    levelindex = 1
    blockidindex = 2
    ruleindex = 3
    linesindex = 4
    blocksindex = 5
    commentindex = 6
    lowestlevel = 0
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
    stopped_blockscope = 'Referenced block is out of scope.'
    stopped_closezeroblock = 'The lowest 0 block cannot be closed.'
    stopped_linescope = 'Reference line is out of scope.'
    stopped_nosuchline = 'The referenced line does not exist.'
    stopped_nosuchblock = 'The referenced block does not exist.'
    stopped_notconjunction = 'The referenced line is not a conjunction.'
    stopped_notcontradiction = 'The referenced lines are not contradictory.'
    stopped_notdemorgan = 'The referenced line is not a DeMorgan statement.'
    stopped_notfalse = 'The referenced line is not false.'
    stopped_string = 'String input is not recognized.'
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

    def __init__(self, logic: str = 'C', name: str = None):
        """Create a Proof object with optional premises, but a specific goal.
        
        Parameters:
            goal: The goal to be reached by the proof.
            name: The name assigned to the proof.
            logic: The logic that will constrain the proof.
        """
            
        self.name = name
        self.goals = []
        self.goalswff = []
        self.goals_string = ''
        self.goals_latex = ''
        self.derivedgoals = []
        self.comments = ''
        self.logic = logic
        self.currentblock = [1]
        self.currentblockid = 0
        self.blocklist = [[self.lowestlevel, self.currentblock]]
        self.blocks = []
        self.level = self.lowestlevel
        self.status = ''
        self.stoppedmessage = ''
        self.premises = []
        self.lines = [['', 0, 0, self.goalname, '', '', '']]

    """SUPPORT FUNCTIONS"""

    def checkcomplete(self):
        """Check if the goal has been found and the proof is over."""

        return self.status == self.complete or self.status == self.stopped
   
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

        newcomment = comments
        if self.level == 0:
            if str(statement) in self.goals:
                if str(statement) not in self.derivedgoals:
                    self.derivedgoals.append(str(statement))
                    if len(self.derivedgoals) < len(self.goals):
                        newcomment = self.partialcompletion
                    else:
                        self.status = self.complete
                        if comments == '':
                            newcomment = self.complete
                        else:
                            newcomment = ''.join([newcomment, self.comments_connector, comments])

        if self.status == self.stopped:
            if comments == '':
                newcomment = ''.join([self.stopped, self.stopped_connector, self.stoppedmessage])
            else:
                newcomment = ''.join([self.stopped, self.stopped_connector, self.stoppedmessage, self.comments_connector, comments])

        if self.logic not in self.availablelogics.get(rulename):
            newcomment = ''.join(['Rule ', rulename, ' violates ', self.logic])
        return newcomment

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

    def reftwolines(self, first: int, second: int) -> str:
        """Join two integers representing line ids or block ids as strings together."""

        return ''.join([str(first), ', ', str(second)])
    
    def stopproof(self, message: str, statement, rule: str, lines: str, blocks: str):
        self.status = self.stopped
        if rule == self.goalname:
            self.lines[0][self.commentindex] = ''.join([self.stopped, self.stopped_connector, message])
        else:
            self.stoppedmessage = ''.join([self.stopped, self.stopped_connector, message])
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
 
    """BASIC RULES"""

    def addgoal(self,
                goal: And | Or | Not | Implies | Iff | Wff | F | T, 
                comments: str = ''):
        """Add a goal to the proof.
        
        Parameters:
            goal: The goal to add to the proof.
            comments: Comments for this line of the proof.
        """

        if not self.checkcomplete():
            if type(goal) == str:
                self.stopproof(self.stopped_string, goal, self.goalname, 0, 0)
            else:
                self.goals.append(str(goal))
                self.goalswff.append(goal)
                if self.goals_string == '':
                    self.goals_string = str(goal)
                else:
                    self.goals_string = ''.join([', ',str(goal)])
                if self.goals_latex == '':
                    self.goals_latex = goal.latex()
                else:
                    self.goals_latex = ''.join([', ',goal.latex()]) 
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
            if type(premise) == str:
                self.stopproof(self.stopped_string, premise, self.premisename, '', '')
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
        """

        if not self.checkcomplete():
            if len(self.lines) <= line:
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.and_elimname, str(line), '')
            else:
                level, statement = self.getlevelstatement(line)
                if level > self.level:
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.and_elimname, str(line), '')
                elif type(statement) != And:
                    self.stopproof(self.stopped_notconjunction, self.blankstatement, self.and_elimname, str(line), '')
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

        if not self.checkcomplete():
            if len(self.lines) <= first:
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.and_introname, str(first), '')
            else:
                firstlevel, firstconjunct = self.getlevelstatement(first)
                if firstlevel > self.level:
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.and_introname, str(first), '')
                elif len(self.lines) <= second:
                    self.stopproof(self.stopped_nosuchline, self.blankstatement, self.and_introname, str(second), '')
                else:
                    secondlevel, secondconjunct = self.getlevelstatement(second)
                    if secondlevel > self.level:
                        self.stopproof(self.stopped_linescope, self.blankstatement, self.and_introname, str(second), '')
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

        if not self.checkcomplete():
            if self.currentblockid == 0:
                self.stopproof(self.stopped_closezeroblock, self.blankstatement, self.closeblockname, '', '')
            else:
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

        if not self.checkcomplete():
            if len(self.lines) <= line:
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.demorgan_name, str(line), '')
            else:
                level, statement = self.getlevelstatement(line)
                if level > self.level:
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.demorgan_name, str(line), '')
                elif type(statement) == Not:
                    if type(statement.negated) == And:
                        andstatement = statement.negated
                        firstsubstatement = andstatement.left
                        secondsubstatement = andstatement.right
                        final = Or(Not(firstsubstatement), Not(secondsubstatement))
                    elif type(statement.negated) == Or:
                        orstatement = statement.negated
                        firstsubstatement = orstatement.left
                        secondsubstatement = orstatement.right
                        final = And(Not(firstsubstatement), Not(secondsubstatement))
                    else:
                        self.stopproof(self.stopped_notdemorgan, self.blankstatement, self.demorgan_name, str(line), '')
                elif type(statement) == Or:
                    firstsubstatement = statement.left
                    secondsubstatement = statement.right               
                    if type(firstsubstatement) == Not and type(secondsubstatement) == Not:
                        final = Not(And(firstsubstatement.negated, secondsubstatement.negated))
                    else:
                        self.stopproof(self.stopped_notdemorgan, self.blankstatement, self.demorgan_name, str(line), '')
                elif type(statement) == And:
                    firstsubstatement = statement.left
                    secondsubstatement = statement.right
                    if type(firstsubstatement) == Not and type(secondsubstatement) == Not:
                        final = Not(Or(firstsubstatement.negated, secondsubstatement.negated))
                    else:
                        self.stopproof(self.stopped_notdemorgan, self.blankstatement, self.demorgan_name, str(line), '')
                else:
                    self.stopproof(self.stopped_notdemorgan, self.blankstatement, self.demorgan_name, str(line), '')
            
                newcomment = self.availablecomplete('demorgan', final, comments)
                self.lines.append(
                    [
                        final, 
                        self.level, 
                        self.currentblockid, 
                        self.demorgan_name, 
                        str(line), 
                        '', 
                        newcomment
                    ]
                )

    def dn_intro(self, line: int, comments: str = ''):
        '''This rule adds a double negation to the statement referenced by the line number
        
        Parameters:
            line: The line number containing the statement.
            comments: User comments on this line.

        Exception:
            NoSuchLine: The line is not in the proof.
            ScopeError: The refernced line is not accessible.
        '''

        if not self.checkcomplete():
            try:
                level, statement = self.getlevelstatement(line)
            except:
                raise altrea.exception.NoSuchLine(line)
            if level > self.level:
                raise altrea.exception.ScopeError(line)
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

        Exception:
            NoSuchLine: The line is not in the proof.
            NotDoubleNegation: The referenced line is not a double negation statement.
            ScopeError: The refernced line is not accessible.
        '''

        if not self.checkcomplete():
            try:
                level, statement = self.getlevelstatement(line)
            except:
                raise altrea.exception.NoSuchLine(line)
            if level > self.level:
                raise altrea.exception.ScopeError(line)
            if type(statement) == Not and type(statement.negated) == Not:
                newstatement = statement.negated.negated
            else:
                raise altrea.exception.NotDoubleNegation(line, statement)
            
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

    def explosion(self, 
                  statement: And | Or | Not | Implies | Iff | Wff | F | T, 
                  comments: str = ''):
        """An arbitrary statement is entered in the proof given a false statement immediately preceding it.
        
        Parameters:
            expr: The statement to add to the proof.
            statement: The new statment to insert.
            comments: A optional comment for this line of the proof.

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

        Exceptions:
            BlockClosed: A line cannot be added to a closed block.
            NoSuchLine: The referenced line does not exist in the proof.
            NotFalse: The referenced statement is not False.
        """
        
        if not self.checkcomplete():
            if type(statement) == str:
                self.stopproof(self.stopped_string, statement, self.explosionname, '', '')
            else:
                line = len(self.lines) - 1
                if line == 0:
                    raise altrea.exception.NoSuchLine(line)
                blockid = self.lines[line][self.blockidindex]
                if len(self.blocklist[blockid][1]) == 2:
                    raise altrea.exception.BlockClosed(blockid)
                else:
                    level, falsestatement = self.getlevelstatement(line)
                    if level != self.level or blockid != self.currentblockid:
                        raise altrea.exception.ScopeError(line)
                    if falsestatement != self.falsename:
                        raise altrea.exception.NotFalse(line, falsestatement)
                    else:
                        newcomment = self.availablecomplete('explosion', statement, comments)
                        self.lines.append(
                            [
                                statement, 
                                self.level, 
                                self.currentblockid, 
                                self.explosionname, 
                                line, 
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
        
        Exceptions:
            NoSuchLine: The line does not exist in the proof.
            NotEquivalence: The two statements cannot be used in equivalence elimination.
            ScopeError: The line is not accessible.
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

        Exceptions:
            NoSuchBlock: The block referred to does not exist.
            NotSameLevel: The blocks are not at the same level.
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

        Exceptions:
            NotAntecedent: The statement is not the antecedent of the implication.
            NoSuchLine: The referenced line does not exist in the proof.
            NotModusPonens: The two statements cannot be used in implication elimination.
            ScopeError: The referenced statement is not accessible.
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
                raise altrea.exception.ScopeError(second)
        
            if type(firststatement) == Implies:
                if secondstatement != firststatement.left:
                    raise altrea.exception.NotAntecedent(firststatement, secondstatement)
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
                    raise altrea.exception.NotAntecedent(secondstatement, firststatement)
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

        if not self.checkcomplete():
            try:
                level, antecedent, consequent = self.getlevelblockstatements(blockid)
            except:
                raise altrea.exception.NoSuchBlock(blockid)
            if level != self.level + 1:
                raise altrea.exception.BlockScopeError(blockid)
            implication = Implies(antecedent, consequent)

            newcomment = self.availablecomplete('implies_intro', implication, comments)
            self.lines.append(
                [
                    implication, 
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
            NotLemOpposites: The assumption of the first block is not the negation of the assumption
                of the second block.
            NotSameLevel: The two blocks are not at the same level.
            NotSameStatements: The conclusions of the two blocks are not the same.
            NoSuchBlock: The block id does not exist.
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
        
            if  type(firstassumption) == Not and firstassumption.negated.equals(secondassumption):
                final = firstconclusion       
            elif type(secondassumption) == Not and secondassumption.negated.equals(firstassumption):
                final = firstconclusion
            else:
                raise altrea.exception.NotLemOpposites(firstassumption, secondassumption)
            if not firstconclusion.equals(secondconclusion):
                raise altrea.exception.NotSameStatements(firstconclusion, secondconclusion)

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

        Exceptions:
            NoSuchLine: The referenced line does not exist in the proof.
            ScopeError: The referenced statement is not accessible.                       
        """
        
        if not self.checkcomplete():
            if (len(self.lines) <= first) or (len(self.lines) <= second):
                if len(self.lines) <= first:
                    self.stopproof(self.stopped_nosuchline, self.blankstatement, self.not_elimname, str(first), '')
                else:
                    self.stopproof(self.stopped_nosuchline, self.blankstatement, self.not_elimname, str(second), '')
            else:
                firstlevel, firststatement = self.getlevelstatement(first)
                secondlevel, secondstatement = self.getlevelstatement(second)
                if not Not(firststatement).equals(secondstatement) and not Not(secondstatement).equals(firststatement):
                    self.stopproof(self.stopped_notcontradiction, self.blankstatement, self.not_elimname, self.reftwolines(first, second), '')
                elif firstlevel > self.level:
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.not_elimname, str(first), '')
                elif secondlevel > self.level:
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.not_elimname, str(second), '')
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
                self.stopproof(self.stopped_string, statement, self.assumptionname, '', '')
            else:
                self.level += 1
                nextline = len(self.lines)
                self.currentblock = [nextline]
                self.blocklist.append([self.level, self.currentblock])
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
        
        Exceptions:
            AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
            ConclusionsNotTheSame: The conclusions of blocks are not the same.
            NoSuchLine: The referenced line does not exist in the proof.
            ScopeError: The referenced statement is not accessible.
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
                self.stopproof(self.stopped_string, left, self.or_introname, str(line), '')
            elif type(right) == str:
                self.stopproof(self.stopped_string, right, self.or_introname, str(line), '')
            else:
                try:
                    level, statement = self.getlevelstatement(line)
                except:
                    raise altrea.exception.NoSuchLine(line)
                if level > self.level:
                 raise altrea.exception.ScopeError(line)
            
                if left is None and right is None:
                    raise altrea.exception.NoValuePassed('or_intro')
                elif left is None:
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
        
        if not self.checkcomplete():
            try:
                level, statement = self.getlevelstatement(line)
            except:
                raise altrea.exception.NoSuchLine(line)
            if level > self.level:
                raise altrea.exception.ScopeError(line)
        
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
    