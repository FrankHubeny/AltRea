# altrea/truthfunction.py

"""The module provides functions to construct a proof in propositional logic.

The module contains three groups of functions: 

- Supporting functions called by other functions for routine procesing.
- Basic rules for the list of logical operators that one accepts for the logic.
- Tautologies or axioms that one can add arbitrarily to the proof depending on the chosen logic.

The following methods support other functions.  They are not intended to be called by the user directly.

- `checkavailable(rulename, comments)` - Based on the logic specified check if a warning comment 
should be added to the proof line.
- `checkcompleteorstopped()` - Returns true or false depending on wither the proof is stopped or complete.
- `getlevelstatement(line)` - Get the level and statement for the line id.
- `reflines(*lines)` - Join an arbitrary number of integers together into a string.

The following are basic rules which the user may call after initializing a Proof.  Depending on
which logical operators one has, the basic list may include only a subset of this list.

- `addhypothesis` - Add an hypothesis to an already opened subordinate proof.
- `coimplication_elim` - Equivalence Elimination
- `coimplication_intro` - Equivalence Introduction
- `conjunction_elim` - Conjunction Elimination
- `conjunction_intro` - Conjunction Introduction
- `disjunction_elim` - Disjunction Elimination
- `disjunction_intro` - Disjunction Introduction
- `explosion` - Explosion
- `goal` - Add a goal to the proof
- `hypothesis` - Open a subordinate proof with an hypothesis
- `implication_elim` - Implication Elimination
- `implication_intro` - Implication Introduction
- `negation_elim` - Negation Elimination
- `negation_intro` - Negation Introduction
- `premise` - Add a premise to the proof
- `reiterate` - Reiterate an item from a parent proof to the current proof.

The following procedure along with a dictionary of tautologies and axioms allows one to
add these at any point in the proof without referring to a previous line.  Whether one
can use these depends on the logic one has selected.

- `usetautology` - Use a rule from a dictionary of tautologies, or rules which can be derived in the selected logic without premises.
- `useaxiom` - Use a rule which cannot be derived, but which is assumed to be true in the logic.
- `useproof` - Use a previously derived proof matching first hypotheses before allowing the conclusion to be a line of the proof.

AltRea uses the following.

- `python` - This is for general processing.
- `pandas` - This is for displaying proofs and other displays.
- `sqlite3` - This is for storing and retrieving proofs.

Anyone finding an issue with the code, whether a python programmer, a user or a logician
question some implementation may raise raise the issue in GitHub.

It is also designed to help those learning python.  If you created a virtual environment
which you like should, you can find this software in your virtual directory under Lib/altrea.  You are
welcome and encouraged to copy these files to a local directory under a new name, say, "myaltrea".
Then import from these files rather than the altrea files to experiment with using python. 

Examples:
    >>> from myaltrea.boolean import And, Or, Not, Implies, Iff, Wff
    >>> import myaltrea.rules


"""


from altrea.boolean import And, Or, Not, Implies, Iff, Wff, F, T


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
    stopped_logiccannotuserule = 'The selected logic cannot use this rule.'
    stopped_nogoal = 'The proof does not yet have a goal.'
    stopped_nologic = 'No logic has been declared for the proof.'
    stopped_nosuchline = 'The referenced line does not exist.'
    stopped_nosuchblock = 'The referenced block does not exist.'
    stopped_notantecedent = 'One statement is not the antecedent of the other.'
    stopped_notconjunction = 'The referenced item is not a conjunction.'
    stopped_notcontradiction = 'The referenced itemss are not contradictory.'
    stopped_notdemorgan = 'The referenced item is not a DeMorgan statement.'
    stopped_notdisjunction = 'The referenced item is not a disjunction.'
    stopped_notdoublenegation = 'The referenced line is not a double negation.'
    stopped_notfalse = 'The referenced item is not false.'
    stopped_notimplication = 'The referenced item is not an implication.'
    stopped_notsameconclusion = 'The two conclusions are not the same.'
    stopped_notsamestatement = 'The referenced items are not the same.'
    stopped_notsamelevel = 'The two blocks are not at the same level.'
    stopped_novaluepassed = 'No value was passed to the function.'
    stopped_sidenotselected = 'A side, left or right, must be selected.'
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
        'premise': ['C', 'CI', 'CO', 'I'],
        'goal': ['C', 'CI', 'CO', 'I'],
        'disjunction_elim': ['C', 'CI', 'CO', 'I'],
        'disjunction_intro': ['C', 'CI', 'CO', 'I'],
        'coimplication_elim': ['C', 'CI', 'CO', 'I'],
        'coimplication_intro': ['C', 'CI', 'CO', 'I'],
        'conjunction_elim': ['C', 'CI', 'CO', 'I'],
        'conjunction_intro': ['C', 'CI', 'CO', 'I'],
        'explosion': ['C', 'CI', 'CO', 'I'],
        'implication_elim': ['C', 'CI', 'CO', 'I'],
        'implication_intro': ['C', 'CI', 'CO', 'I'],
        'negation_elim': ['C', 'CI', 'CO', 'I'],
        'negation_intro': ['C', 'CI', 'CO', 'I'],
        'hypothesis': ['C', 'CI', 'CO', 'I'],
        'addhypothesis': ['C', 'CI', 'CO', 'I'],
        'reiterate': ['C', 'CI', 'CO', 'I'],
    }
    axioms = {
        'lem' : ['LEM', ['C',], '', 'Or(1, Not(1))', 1, 'userule("lem", P)'],
    }
    tautologies = {
        'lem' : [],
    }

    def __init__(self, name: str = ''):
        """Create a Proof object with an optional name.
        
        Parameters:
            name: The name assigned to the proof.
        """
            
        self.name = name
        self.goals = []
        self.goals_string = ''
        self.goals_latex = ''
        self.derivedgoals = []
        self.comments = ''
        self.logic = ''
        self.logging = False
        self.parentproofid = 0
        self.currentproof = [1]
        self.currentproofid = 0
        self.proofdata = [[self.name, self.logic]]
        self.prooflist = [[self.lowestlevel, self.currentproof, self.parentproofid, []]]
        self.level = self.lowestlevel
        self.status = ''
        self.premises = []

    """SUPPORT FUNCTIONS NOT INTENTED TO BE DIRECTLY CALLED BY THE USER"""

    def checkcompleteorstopped(self):
        """Check if the goal has been found and the proof is over."""

        return self.status == self.complete or self.status == self.stopped
    
    def checkcurrentlevel(self, level: int):
        """Check that the level of a statement one plans to use is at the current level."""

        return level == self.level
    
    def checkhasgoal(self):
        """Check if the proof has at least one goal."""

        return len(self.goals) > 0
    
    def checkline(self, line: int):
        """Check if the line is an integer within the range of the proof lines."""

        if type(line) == int:
            return len(self.lines) > line and line > 0
        else:
            return False

    def checklogic(self, listoflogics:list):
        """Check if the selected logic is in the string of logics permitted to use the rule or function."""

        return self.logic in listoflogics

    def checkstring(self, wff: And | Or | Not | Implies | Iff | Wff | F | T):
        #return (type(wff) not in self.acceptedtypes) # or (type(wff) == None)
        return type(wff) == str

    def getcurrentitemid(self):
        """Returns the number of the current item of the proof."""

        return len(self.lines)
    
    def getlevelstatement(self, line: int) -> tuple:
        """Given a line id, return the level and the statement on that line."""

        level = self.lines[line][self.levelindex]
        statement = self.lines[line][self.statementindex]
        return level, statement

    def getparentproofid(self, proofid: int) -> int:
        """Returns the parent proof id of a given proof."""
    
        return self.prooflist[proofid][2]
    
    def getproof(self, proofid: int) -> tuple:
        """Returns the level, one or more hypothesis statements conjoined together, the conclusion statement 
        and the parent proof id.
        """

        level = self.prooflist[proofid][0]
        hypothesis = self.lines[self.prooflist[proofid][3][0]][self.statementindex]
        if len(self.prooflist[proofid][3]) > 1:
            for i in range(len(self.prooflist[proofid][3])):
                if i > 0:
                    hypothesis = And(hypothesis, self.lines[self.prooflist[proofid][3][i]][self.statementindex])

        conclusion = self.lines[self.prooflist[proofid][1][1]][self.statementindex]
        parentproofid = self.prooflist[proofid][2]
        return level, hypothesis, conclusion, parentproofid
    
    def iscomplete(self, 
                   rulename: str, 
                   statement:  And | Or | Not | Implies | Iff | Wff | F | T = None, 
                   comments: str = ''):
        """Check if the proof is complete or partially complete and if so leave a message."""

        newcomment = self.status
        if self.level == 0:
            if str(statement) in self.goals:
                if str(statement) not in self.derivedgoals:
                    self.derivedgoals.append(str(statement))
                    if len(self.derivedgoals) < len(self.goals):
                        newcomment = self.partialcompletion
                        if self.logging:
                            print(f'The proof is partially complete.')
                    else:
                        self.status = self.complete
                        self.prooflist[0][1].append(len(self.lines)-1)
                        newcomment = self.complete
                        if self.logging:
                            print(f'The proof is complete.')
        if comments == '':
            return newcomment
        else:
            if newcomment == '':
                return comments
            else:
                return ''.join([newcomment, self.comments_connector, comments])
    
    def reflines(self, *lines):
        """Convert integers to strings and join separated by commas."""

        joined = str(lines[0])
        for i in range(len(lines)):
            if i > 0:
                joined += ''.join([', ', str(lines[i])])
        return joined
    
    def refproof(self, proofid: int):
        """Formats a proof used in a proof."""

        proof = self.prooflist[proofid][1]
        return ''.join([str(proof[0]), '-', str(proof[1])])
    
    def setlogic(self, logic: str):
        """Sets the logic for the proof."""

        self.logic = logic
        if self.logic in self.logicdictionary:
            self.lines = [['', 0, 0, '', '', '', '']]
        else:
            self.status = self.stopped
            self.lines = [['', 0, 0, '', '', '', ''.join([self.stopped, self.stopped_connector, self.stopped_undefinedlogic])]]
        if self.logging:
            print(f'The logic {logic} or {self.logicdictionary.get(logic)} has been set for the proof.')
    
    def stopproof(self, message: str, statement, rule: str, lines: str, blocks: str, comments: str = ''):
        """Logs a status message in the line of a proof that shows no further lines can be added until the error is fixed."""

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
            if self.logging:
                print(stoppedmessage)
 
    """SUPPORT FUNCTIONS CALLABLE BY THE USER"""

    def logging_off(self):
        """This function turns logging off if it has been turned on.
        
        Examples:
            One can turn logging on for only one statement such as in the example below
            by turning it on before the statement and turning it off afterwards.

            >>> from altrea.boolean import Not, And, Or, Implies, Iff, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import showproof
            >>> proof = Proof()
            >>> P = Wff('P')
            >>> Q = Wff('Q')
            >>> proof.setlogic('C')
            >>> proof.goal(Q)
            >>> proof.premise(Implies(P, Q))
            >>> proof.premise(P)
            >>> proof.logging_on()
            Logging has started.
            >>> proof.implication_elim(1,2)
            IMPLICATION_ELIM: The item Q is derived from the implication P > Q and P.
            The proof is complete.
            >>> proof.logging_off()
            Logging has been turned off.
            >>> showproof(proof, latex=0)
                Item                  Reason   Comment
            0      Q                    GOAL
            1  P > Q                 Premise
            2      P                 Premise
            3      Q  1, 2, Implication Elim  COMPLETE
        """

        if self.logging:
            self.logging = False
            print('Logging has been turned off.')

    def logging_on(self):
        """This function turns logging on if it is turned off.
        
        Examples:
            In a terminal logging provides immediate confirmation of the step that has
            been performed.  It also presents status messages if the proof is complete.
            In a jupyter notebook these would all appear together in the output cell.

            >>> from altrea.boolean import Not, And, Or, Implies, Iff, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import showproof
            >>> proof = Proof()
            >>> P = Wff('P')
            >>> Q = Wff('Q')
            >>> proof.logging_on()
            Logging has started.
            >>> proof.setlogic('C')
            The logic C or Classical Propositional Logic has been set for the proof.
            >>> proof.goal(Q)
            goal: The goal Q has been added to the list of goals Q.
            >>> proof.premise(Implies(P, Q))
            premise: The item P > Q has been added to the premises.
            >>> proof.premise(P)
            premise: The item P has been added to the premises.
            >>> proof.implication_elim(1,2)
            IMPLICATION_ELIM: The item Q is derived from the implication P > Q and P
            The proof is complete.
            >>> showproof(proof, latex=0)
                Item                  Reason   Comment
            0      Q                    GOAL
            1  P > Q                 Premise
            2      P                 Premise
            3      Q  1, 2, Implication Elim  COMPLETE
        """

        if not self.logging:
            self.logging = True
            print('Logging has started.')
        else:
            print('logging is already on.')

    """FUNCTIONS TO BUILD PROOFS"""

    def addhypothesis(self,
                      hypothesis: And | Or | Not | Implies | Iff | Wff | F | T,
                      comments: str = ''):
        """Adds to the currently opened subproof an hypothesis and inserts the new hypothesis into
        a list of hypotheses which now have more than one.
        
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
            if self.logging:
                print(f'ADDHYPOTHESIS: The item {str(hypothesis)} has been added to the set of hypotheses.')      
            newcomment = self.iscomplete('hypothesis', hypothesis, comments)
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

    def coimplication_elim(self, first: int, second: int, comments: str = ''):
        """Given an iff statement and a proposition one can derive the other proposition.
        
        Parameters:
            first: A statement containing either a proposition or an iff statement.
            second: A second statement containing either a proposition or an iff statement.
            comments: Comments on this line of the proof.
        
        Examples:
            The following is a simple example of how the coimplication elimination rule works.

            >>> from altrea.boolean import Implies, Wff, Iff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import showproof
            >>> p = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> p.setlogic('C')
            >>> p.goal(B)
            >>> p.premise(Iff(A, B))
            >>> p.premise(A)
            >>> p.coimplication_elim(1, 2)
            >>> showproof(p, latex=0)
                Item                    Reason   Comment
            0       B                      GOAL
            1  A <> B                   Premise
            2       A                   Premise
            3       B  1, 2, Coimplication Elim  COMPLETE

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
                    if self.logging:
                        print(f'COIMPLICATION_ELIM: The item {str(firststatement.right)} is derived from the coimplication {str(firststatement)}.')
                    newcomment = self.iscomplete('coimplication_elim', firststatement.right, comments)
                    self.lines.append(
                        [
                            firststatement.right, 
                            self.level, 
                            self.currentproofid, 
                            self.coimplication_elim_name, 
                            self.reflines(first, second), 
                            '', 
                            newcomment
                        ]
                    )
                    self.proofdata.append([self.coimplication_elim_tag, firststatement.right.pattern()])
            elif type(secondstatement) == Iff:
                if firststatement != secondstatement.left:
                    self.stopproof(self.stopped_notantecedent, self.blankstatement, self.coimplication_elim_name, '', '', comments)
                else:
                    if self.logging:
                        print(f'COIMPLICATION: The item {str(secondstatement.right)} is derived from the coimplication {str(secondstatement)}.')   
                    newcomment = self.iscomplete('coimplication_elim', secondstatement.right, comments)
                    self.lines.append(
                        [
                            secondstatement.right, 
                            self.level, 
                            self.currentproofid, 
                            self.coimplication_elim_name, 
                            self.reflines(first, second), 
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
            The following is a simple example of how the coimplication introduction rule works.

            >>> from altrea.boolean import Implies, Wff, Iff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import showproof
            >>> p = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> p.setlogic('C')
            >>> p.goal(Iff(A, B))
            >>> p.premise(Implies(A, B))
            >>> p.premise(Implies(B, A))
            >>> p.coimplication_intro(1, 2)
            >>> showproof(p, latex=0)
                 Item                     Reason   Comment
            0  A <> B                       GOAL
            1   A > B                    Premise
            2   B > A                    Premise
            3  A <> B  1, 2, Coimplication Intro  COMPLETE
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
                    elif str(firststatement.left) != str(secondstatement.right):
                        self.stopproof(self.stopped_notsamestatement, self.blankstatement, self.coimplication_intro_name, '', '', comments)
                    elif str(firststatement.right) != str(secondstatement.left):
                        self.stopproof(self.stopped_notsamestatement, self.blankstatement, self.coimplication_intro_name, '', '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            newstatement = Iff(firststatement.left, firststatement.right)
            if self.logging:
                print(f'COIMPLICATION_INTRO: The item {str(newstatement)} is derived from {str(firststatement.left)} and {str(firststatement.right)}.')     
            newcomment = self.iscomplete('coimplication_intro', newstatement, comments)
            self.lines.append(
                [
                    newstatement, 
                    self.level, 
                    self.currentproofid, 
                    self.coimplication_intro_name, 
                    '',
                    self.reflines(first, second), 
                    newcomment
                ]
            )   
            self.proofdata.append([self.coimplication_intro_tag, newstatement.pattern()])   

    def conjunction_elim(self, line: int, side: str = 'left', comments: str = ''):
        """One of the conjuncts, either the left side or the right side, is derived from a conjunction.
        
        Parameters:
            line: The line number of the conjunction to be split.
            side: The side, either left or right, from which the conjunct will be derived.
            comments: Optional user comments for the line.

        Examples:
            The first example shows the conjunct coming from the left side.  This is the default.
            
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

            >>> from altrea.boolean import And, Implies, Iff, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import showproof
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> prf.setlogic('C')
            >>> prf.goal(Iff(And(A, B), And(B, A)))
            >>> prf.hypothesis(And(A, B), comments="Don't use `addhypothesis` to start the subproof.")
            >>> prf.conjunction_elim(1, comments='The left side is the default.')
            >>> prf.conjunction_elim(1, side='right', comments='Now do the right side.')
            >>> prf.conjunction_intro(3, 2, comments='Put the conjuncts on the opposite side.')
            >>> prf.implication_intro()
            >>> prf.hypothesis(And(B, A))
            >>> prf.conjunction_elim(6)
            >>> prf.conjunction_elim(6, side='right')
            >>> prf.conjunction_intro(8, 7, comments='The order is reversed.')
            >>> prf.implication_intro()
            >>> prf.coimplication_intro(10, 5, comments='The order will be like the first statement on line 10.')
            >>> prf.coimplication_intro(5, 10, comments='Now it works using line 5 first.')
            >>> showproof(prf, latex=0)
                             Item  ...                                            Comment
            0   (A & B) <> (B & A)  ...
            1            A & B __|  ...   Don't use `addhypothesis` to start the subproof.
            2                A   |  ...                      The left side is the default.
            3                B   |  ...                             Now do the right side.
            4            B & A   |  ...            Put the conjuncts on the opposite side.
            5    (A & B) > (B & A)  ...
            6            B & A __|  ...
            7                B   |  ...
            8                A   |  ...
            9            A & B   |  ...                             The order is reversed.
            10   (B & A) > (A & B)  ...
            11  (B & A) <> (A & B)  ...  The order will be like the first statement on ...
            12  (A & B) <> (B & A)  ...        COMPLETE - Now it works using line 5 first.
        """

        # Look for errors
        if not self.checkcompleteorstopped():
            if not self.checkline(line):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.conjunction_elim_name, str(line), '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.conjunction_elim_name, '', '', comments)
            else:
                level, statement = self.getlevelstatement(line)
                if not self.checkcurrentlevel(level):
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.conjunction_elim_name, str(line), '', comments)
                elif type(statement) != And:
                    self.stopproof(self.stopped_notconjunction, self.blankstatement, self.conjunction_elim_name, str(line), '', comments)
                elif side not in ['left', 'right']:
                    self.stopproof(self.stopped_sidenotselected, self.blankstatement, self.conjunction_elim_name, str(line), '', comments)

        # If no errors, perform the task
        if not self.checkcompleteorstopped():
            if side == 'left':
                conjunct = statement.left
            else:
                conjunct = statement.right
            if self.logging:
                print(f'CONJUNCTION_ELIM: The item {str(conjunct)} has be separated from the conjunction {str(statement)} on line {str(line)}.')
            newcomment = self.iscomplete('conjunction_elim', conjunct, comments)
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
                
    def conjunction_intro(self, first: int, second: int, comments: str = ''):
        """The statement at first line number is joined with And to the statement at second
        line number.

        Parameters:
            first: The line number of the first conjunct on the left side.
            second: The line number of the second conjunct on the right side.
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
            >>> p.goal(And(A, B))
            >>> p.premise(A)
            >>> p.premise(B)
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
            >>> p.goal(And(A, A))
            >>> p.premise(A)
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
            if self.logging:
                print(f'CONJUNCTION_INTRO: The conjunction {str(andstatement)} is derived from {str(firstconjunct)} on line {str(first)} and {str(secondconjunct)} on line {str(second)}.')
            newcomment = self.iscomplete('conjunction_intro', andstatement, comments)
            self.lines.append(
                [
                    andstatement, 
                    self.level, 
                    self.currentproofid, 
                    self.conjunction_intro_name, 
                    self.reflines(first, second), 
                    '',
                    newcomment
                ]
            ) 
            self.proofdata.append([self.conjunction_intro_tag, andstatement.pattern()])   

    def disjunction_elim(self, disjunction_line: int, left_implication_line: int, right_implication_line: int, comments: str = ''):
        """This rule take a disjunction and two implications starting with each side of the disjunction.
        If the two implications reach the same conclusion, then that conclusion may be derived.
        
        Parameters:
            disjunction: The line number where the disjunction is an item.
            left_implication: The line number of the implication starting with the left side of the disjunction.
            right_implication: The line number of the implication starting with the right side of the disjunction.
            comments: Optional comments may be entered here.
        Examples:
        
        """

        # Look for errors.
        if not self.checkcompleteorstopped():
            if not self.checkline(disjunction_line):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.disjunction_elim_name, str(disjunction_line), '', comments)
            elif not self.checkline(left_implication_line):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.disjunction_elim_name, str(left_implication_line), '', comments)
            elif not self.checkline(right_implication_line):
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.disjunction_elim_name, str(right_implication_line), '', comments)
            else:
                disjunction_level, disjunction = self.getlevelstatement(disjunction_line)
                left_implication_level, left_implication = self.getlevelstatement(left_implication_line)
                right_implication_level, right_implication = self.getlevelstatement(right_implication_line)
                if not self.checkcurrentlevel(disjunction_level): 
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.disjunction_elim_name, '', '', comments)
                elif not self.checkcurrentlevel(left_implication_level): 
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.disjunction_elim_name, '', '', comments)
                elif not self.checkcurrentlevel(right_implication_level): 
                    self.stopproof(self.stopped_linescope, self.blankstatement, self.disjunction_elim_name, '', '', comments)
                elif type(disjunction) != Or:
                    self.stopproof(self.stopped_notdisjunction, self.blankstatement, self.disjunction_elim_name, '', '', comments)
                elif type(left_implication) != Implies:
                    self.stopproof(self.stopped_notimplication, self.blankstatement, self.disjunction_elim_name, '', '', comments)
                elif type(right_implication) != Implies:
                    self.stopproof(self.stopped_notimplication, self.blankstatement, self.disjunction_elim_name, '', '', comments)
                elif str(right_implication.right) != str(left_implication.right):
                    self.stopproof(self.stopped_notsameconclusion, self.blankstatement, self.disjunction_elim_name, '', '', comments)

        # With no errors, perform task.
        if not self.checkcompleteorstopped():
            if self.logging:
                print(f'DISJUNCTION_ELIM: The disjunction {str(disjunction)} on line {str(disjunction_line)} has been eliminated because both disjuncts derived the same conclusion {str(right_implication.left)}.')   
            newcomment = self.iscomplete('disjunction_elim', right_implication.right, comments)
            self.lines.append(
                [
                    right_implication.right, 
                    self.level, 
                    self.currentproofid, 
                    self.disjunction_elim_name, 
                    '', 
                    self.reflines(disjunction_line, left_implication_line, right_implication_line),
                    newcomment
                ]
            )    
            self.proofdata.append([self.disjunction_elim_tag, right_implication.left.pattern()])             

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
                if self.logging:
                    print(f'DISJUNCTION_INTRO: A new disjunction {str(disjunction)} is derived from the item {str(statement)} on line {str(line)} joined on the right with {str(right)}.')
            elif right is None:
                disjunction = Or(left, statement)
                if self.logging:
                    print(f'DISJUNCTION_INTRO: A new disjunction {str(disjunction)} is derived from the item {str(statement)} on line {str(line)} joined on the left with {str(left)}.')
            newcomment = self.iscomplete('disjunction_intro', disjunction, comments)
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
            >>> p.premise(A)
            >>> p.premise(Not(A))
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
            >>> p.goal(And(A, B))
            >>> p.premise(A)
            >>> p.premise(Not(A))
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
            if self.logging:
                print(f'EXPLOSION: The item {str(statement)} is derived from the false item on line {str(line)}.')   
            newcomment = self.iscomplete('explosion', statement, comments)
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
                               
    def goal(self,
                goal: And | Or | Not | Implies | Iff | Wff | F | T, 
                comments: str = ''):
        """Add a goal to the proof.  More than one goal can be assigned although generally
        only one goal is used and only one is needed.  Think of multiple goals as the
        conjuncts to a single goal.
        
        Parameters:
            goal: The goal to add to the proof.
            comments: Optional comments for this line of the proof.

        Examples:

            Once one has a Proof object one has to identify which logic one will be using
            and one has to add a goal to it.  These steps are not lines in the proof itself
            and appear in the display under line 0.  However, without a goal or a
            logic attempting to add any other line will stop the proof from starting.  
            
            Below is an example of a trivial proof and a display that can be used on a terminal.  
            The proof is trivial because the goal and the premise are the same.
            Setting `latex=1` in `showproof` would provide a better display in a notebook.

            What is passed to goal is not a string, but an instantiated Wff (well-formed formula).
            An error is returned if a string is passed.  When Q was passed it was not the string 'Q'
            but the Wff Q.

            >>> from altrea.boolean import Not, And, Or, Implies, Iff, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import showproof
            >>> proof = Proof()
            >>> P = Wff('P')
            >>> Q = Wff('Q')
            >>> proof.setlogic('C')
            >>> proof.goal(Q)
            >>> proof.premise(Q)
            >>> showproof(proof, latex=0)
              Item   Reason   Comment
            0    Q     GOAL
            1    Q  Premise  COMPLETE
        """

        # Look for errors
        if not self.checkcompleteorstopped():
            if self.checkstring(goal):
                self.stopproof(self.stopped_string, goal, self.goal_name, 0, 0, comments)
            elif self.logic == '':
                self.stopproof(self.stopped_nologic, '', self.goal_name, 0, 0, comments)

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
            if self.logging:
                print(f'goal: The goal {str(goal)} has been added to the list of goals {self.goals_string}.')

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
            if self.logging:
                print(f'HYPOTHESIS: A new subproof has been started with the item {str(hypothesis)}.')
            newcomment = self.iscomplete('hypothesis', hypothesis, comments)
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

    def implication_elim(self, first: int, second: int, comments: str = ''):
        """From an implication and its antecedent derive the consequent.
        
        Parameters:
            first: The line number of the first statement. This is either the implication or the antecedent.
            second: The line number of the second statement.  This is either the implication or the antecedent.
            comments: Optional comments the user wishes to enter.  If there are errors AltRea notes the
                error in this column and stops the proof.  If the proof completes, that is also noted in this column.

        Examples:
            Implication elimination is also called "Modus Ponens".  If you have P and P > Q then from both of the
            you can derive Q.

            >>> from altrea.boolean import Implies, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import showproof
            >>> P = Wff('P')
            >>> Q = Wff('Q')
            >>> p = Proof()
            >>> p.setlogic('C')
            >>> p.goal(Q, comments='Modus Ponens')
            >>> p.premise(P)
            >>> p.premise(Implies(P, Q))
            >>> p.implication_elim(1, 2)
            >>> showproof(p, latex=0)
                Item                  Reason       Comment
            0      Q                    GOAL  Modus Ponens
            1      P                 Premise
            2  P > Q                 Premise
            3      Q  1, 2, Implication Elim      COMPLETE

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
                    if self.logging:
                        print(f'IMPLICATION_ELIM: The item {str(firststatement.right)} is derived from the implication {str(firststatement)} and {str(secondstatement)}.')
                    newcomment = self.iscomplete('implication_elim', firststatement.right, comments)
                    self.lines.append(
                        [
                            firststatement.right, 
                            self.level, 
                            self.currentproofid, 
                            self.implication_elim_name, 
                            self.reflines(first, second), 
                            '', 
                            newcomment
                        ]
                    )
                    self.proofdata.append([self.implication_elim_tag, firststatement.right.pattern()])
            elif type(secondstatement) == Implies:
                if firststatement != secondstatement.left:
                    self.stopproof(self.stopped_notantecedent, self.blankstatement, self.implication_elim_name, '', '', comments)
                else:
                    if self.logging:
                        print(f'IMPLICTION_ELIM: The item {str(secondstatement.right)} is derived from the implication {str(secondstatement)} and {str(firststatement)}.')      
                    newcomment = self.iscomplete('implication_elim', secondstatement.right, comments)
                    self.lines.append(
                        [
                            secondstatement.right, 
                            self.level, 
                            self.currentproofid, 
                            self.implication_elim_name, 
                            self.reflines(first, second), 
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
            The following simple example is called the "Reflexitiy of Implication".  Note how the subordinate proof
            contained only one line, the hypothesis.  The hypothesis became both the antecedent and the
            consequent of the implication.
        
            >>> from altrea.boolean import Implies, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import showproof
            >>> P = Wff('P')
            >>> p = Proof()
            >>> p.setlogic('C')
            >>> p.goal(Implies(P, P), comments='Reflexivity of Implication')
            >>> p.hypothesis(P)
            >>> p.implication_intro()
            >>> showproof(p, latex=0)
                Item                  Reason                     Comment
            0  P > P                    GOAL  Reflexivity of Implication
            1  P __|              Hypothesis
            2  P > P  1-1, Implication Intro                    COMPLETE

            The following is a simple, but important example of how the implication introduction rule works.
            Note that it does not require any premises.  One starts immediately with an hypothesis
            to open a subordinate proof and end at the bottom level with the 
            "Axiom of Conditioned Repetition".  The constraint is that we use a logic
            like "C", the "Classical Propositional" logic.

            This example also illustates the use of comments and how one may change the
            headings of the columns of the proof.

            >>> from altrea.boolean import Implies, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import showproof
            >>> P = Wff('P')
            >>> Q = Wff('Q')
            >>> p = Proof()
            >>> p.setlogic('C')
            >>> p.goal(Implies(P, Implies(Q, P)), comments='Axiom of Conditioned Repetition')
            >>> p.hypothesis(P)
            >>> p.hypothesis(Q)
            >>> p.reiterate(1)
            >>> p.implication_intro()
            >>> p.implication_intro()
            >>> showproof(p, columns=['Proposition','Rule','Remarks'], latex=0)
               Proposition                    Rule                          Remarks
            0  P > (Q > P)                    GOAL  Axiom of Conditioned Repetition
            1        P __|              Hypothesis
            2    Q __|   |              Hypothesis
            3    P   |   |          1, Reiteration
            4    Q > P   |  2-3, Implication Intro
            5  P > (Q > P)  1-4, Implication Intro                         COMPLETE

            This example shows the rule of distribution.  Like the previous exampeles it does not
            require any premises.
            
            On the Jupyter Lab Terminal the width is truncated
            so the rules are not completely visible.  Running this in a notebook will show the full table. 
            One can then set latex=1 rather than latex-0 on showproof.

            >>> from altrea.boolean import Implies, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import showproof
            >>> p = Proof()
            >>> p.setlogic('C')
            >>> P = Wff('P')
            >>> Q = Wff('Q')
            >>> R = Wff('R')
            >>> p.goal(Implies(Implies(P, Implies(Q, R)), (Implies(Implies(P, Q), Implies(P, R)))), comments='rule of distribution')
            >>> p.hypothesis(Implies(P, Implies(Q, R)))
            >>> p.hypothesis(Implies(P, Q))
            >>> p.hypothesis(P)
            >>> p.reiterate(1)
            >>> p.implication_elim(3, 4)
            >>> p.reiterate(2)
            >>> p.implication_elim(3, 6)
            >>> p.implication_elim(5, 7)
            >>> p.implication_intro()
            >>> p.implication_intro()
            >>> p.implication_intro()
            >>> showproof(p, latex=0)
                                               Item  ...               Comment
            0   (P > (Q > R)) > ((P > Q) > (P > R))  ...  rule of distribution
            1                       P > (Q > R) __|  ...
            2                         P > Q __|   |  ...
            3                         P __|   |   |  ...
            4               P > (Q > R)   |   |   |  ...
            5                     Q > R   |   |   |  ...
            6                     P > Q   |   |   |  ...
            7                         Q   |   |   |  ...
            8                         R   |   |   |  ...
            9                         P > R   |   |  ...
            10                (P > Q) > (P > R)   |  ...
            11  (P > (Q > R)) > ((P > Q) > (P > R))  ...              COMPLETE
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
            if self.logging:
                print(f'IMPLICATION_INTRO: A subproof has been closed providing the implication {str(implication)} as an item of the proof.')    
            newcomment = self.iscomplete('implication_intro', implication, comments)
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

    def nand_elim(self, first: int, second: int, comments: str = ''):
        pass

    def nand_intro(self, first: int, second: int, comments: str = ''):
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
            >>> p.premise(A)
            >>> p.premise(Not(A))
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
                        self.stopproof(self.stopped_notcontradiction, self.blankstatement, self.negation_elim_name, self.reflines(first, second), '', comments)
                    elif firstlevel > self.level:
                        self.stopproof(self.stopped_linescope, self.blankstatement, self.negation_elim_name, str(first), '', comments)
                    elif secondlevel > self.level:
                        self.stopproof(self.stopped_linescope, self.blankstatement, self.negation_elim_name, str(second), '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            if self.logging:
                print(f'NEGATION_ELIM: The item {str(self.falsename)} is derived from the contradiction between {str(firststatement)} on line {str(first)} and {str(secondstatement)} on line {str(second)}.')   
            newcomment = self.iscomplete('negation_elim', self.falsename, comments)
            self.lines.append(
                [
                    self.falsename, 
                    self.level, 
                    self.currentproofid, 
                    self.negation_elim_name, 
                    self.reflines(first, second), 
                    '',
                    newcomment
                ]
            )            
            self.proofdata.append([self.negation_elim_tag, self.falsename.pattern()])  

    def negation_intro(self, comments: str = ''):
        """This rule closes a subordinate proof that ends in a contradiction by negating the hypotheses of
        the subordinate proof. 
        
        Examples:
            The following example is known as modus tollens.
            
            >>> from altrea.boolean import Implies, Not, Wff
            >>> from altrea.truthfunction import Proof
            >>> from altrea.display import showproof
            >>> P = Wff('P')
            >>> Q = Wff('Q')
            >>> p = Proof()
            >>> p.setlogic('C')
            >>> p.goal(Not(P), comments='Modus Tollens')
            >>> p.premise(Implies(P, Q))
            >>> p.premise(Not(Q))
            >>> p.hypothesis(P)
            >>> p.reiterate(1)
            >>> p.implication_elim(3, 4)
            >>> p.reiterate(2)
            >>> p.negation_elim(5, 6)
            >>> p.negation_intro()
            >>> showproof(p, latex=0)
                    Item                  Reason        Comment
            0         ~P                    GOAL  Modus Tollens
            1      P > Q                 Premise
            2         ~Q                 Premise
            3      P __|              Hypothesis
            4  P > Q   |          1, Reiteration
            5      Q   |  3, 4, Implication Elim
            6     ~Q   |          2, Reiteration
            7      X   |     5, 6, Negation Elim
            8         ~P     3-7, Negation Intro       COMPLETE
            
        """

        if not self.checkcompleteorstopped():
            if self.currentproofid == 0:
                self.stopproof(self.stopped_closezeroblock, self.blankstatement, self.closeblockname, '', '')
            else:
                proofid = self.currentproofid
                #level, antecedent, consequent, parentproofid = self.getproof(proofid)
                self.prooflist[proofid][1].append(len(self.lines)-1)
                level, antecedent, consequent, parentproofid = self.getproof(proofid)
                self.level -= 1
                self.currentproofid = parentproofid
                self.currentproof = self.prooflist[parentproofid][1]
                negation = Not(antecedent)
                if self.logging:
                    print(f'NEGATION_INTRO: The hypothesis {str(antecedent)} of the subproof has been negated {str(negation)} and the subproof has been closed.') 
                newcomment = self.iscomplete('negation_intro', negation, comments)
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

    def nor_elim(self, first: int, second: int, comments: str = ''):
        pass

    def nor_intro(self, first: int, second: int, comments: str = ''):
        pass

    def premise(self, 
                   premise: And | Or | Not | Implies | Iff | Wff | F | T, 
                   comments: str = ''):
        """Add a premise to the proof.  Although a proof does not require a premise one or more of
        them are often provided.
        
        Parameters:
            premise: The premise to add to the proof.
            comments: Optional comments for this line of the proof.
        """

        # Look for errors
        if not self.checkcompleteorstopped():
            if self.checkstring(premise):
                self.stopproof(self.stopped_string, premise, self.premise_name, '', '', comments)
            elif not self.checkhasgoal():
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.premise_name, '', '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            self.premises.append(premise)
            if self.logging:
                print(f'premise: The item {str(premise)} has been added to the premises.')
            newcomment = self.iscomplete('premise', premise, comments)
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
            >>> p.goal(Implies(A, B))
            >>> p.premise(B)
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
                        if i[self.statementindex] == statement and i[self.levelindex] == self.level and i[self.proofidindex] == self.currentproofid:
                            found = True
                            break
                    if found:
                        self.stopproof(self.stopped_alreadyavailable, self.blankstatement, self.reiterate_name, str(line), '', comments)

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            if self.logging:
                print(f'REITERATE: The item {str(statement)} on line {str(line)} has been reiterated into the current subproof.')   
            newcomment = self.iscomplete('reiterate', statement, comments)
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

    """FUNCTIONS TO SUPPORT AXIOMS, TAUTOLOGOES AND SAVED PROOFS"""    

    def use_axiom(self, axiom_name: str):
        pass

    def use_tautology(self, tautology_name: str):
        pass    

    def use_saved_proof(self, saved_proof_name: str):
        pass
    
    def rulehelp(self, rulename: str):
        """Provides information about the rule and how to invoke it in a proof.
        
        """

        rule = self.rules.get(rulename)
        print(f'Name:             {rule[0]}')
        print(f'Logics Supported: {rule[1]}')
        pattern = 'None'
        if rule[2] != '':
            pattern = rule[2]
        print(f'Required Pattern: {pattern}')
        print(f'Ouput Pattern:    {rule[3]}')
        if rule[4] == 1:
            print(f'Required Input:   An integer pointing to a line in the proof or a new statement.')
        else:
            print(f'Required input:   {rule[4]} integers or statement in the order of the required pattern.')
        print(f'Example:          {rule[5]}')


    def userule(self, rulename: str, substitution: And | Or | Not | Implies | Iff | Wff | F | T, itemid: int = 0):
        """Function for using derived rules.
        
        """

        # Look for errors
        if not self.checkcompleteorstopped():
            rule = self.rules.get(rulename)
            if not self.checklogic(rule[1]):
                self.stopproof(self.stopped_logiccannotuserule, self.blankstatement, rule[0], '', '')

        # If no errors, perform task
        if not self.checkcompleteorstopped():
            for i in range(rule[4]):
                if itemid == 0:
                    level, statement = self.getlevelstatement(substitution)
                    newstatement = eval(rule[3].replace(str(i+1), statement.tree()))
                else:
                    newstatement = eval(rule[3].replace(str(i+1), substitution.tree()))
                #newcomment = self.iscomplete('userule', statement, '')
                self.lines.append(
                    [
                        newstatement, 
                        self.level, 
                        self.currentproofid, 
                        rule[0], 
                        '', 
                        '',
                        '' #newcomment
                    ]
                )  

def testingoutsideclass(p, rulename: str, premise: int | And | Or | Not | Implies | Iff | Wff | F | T):
    rule = p.rules.get(rulename)
    for i in range(rule[4]):
        if type(premise) == int:
            level, statement = p.getlevelstatement(premise)
            newstatement = rule[3].replace(str(i+1), statement)
        else:
            newstatement = rule[3].replace(str(i+1), premise)

        return newstatement
