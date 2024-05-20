# altrea/rules.py

"""The module provides functions to construct a proof in propositional logic.

The module contains three groups of functions: 

- Supporting functions called by other functions for routine procesing.
- Basic rules for the list of logical operators that one accepts for the logic.
- Tautologies or axioms that one can add arbitrarily to the proof depending on the chosen logic.

The following methods support other functions.  They are not intended to be called by the user directly.

- `checkavailable(rulename, comment)` - Based on the logic specified check if a warning comment 
should be added to the proof line.
- `canproceed()` - Returns true or false depending on wither the proof is stopped or complete.
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


import pandas

from altrea.boolean import And, Or, Not, Implies, Iff, Wff, Necessary, Possibly, TrueFalse, Falsehood, Truth, PremisesConclusion, Definition
import altrea.data

class Proof:
    """
    This class contains methods to construct and verify proofs in 
    in various truth functional logics.
    """

    """The following labels should not be changed.  They are not displayed but help control
    the state of the software while it is running or record codes in saved proofs.  Changing them
    may make saved proofs difficult to read.
    """

    statementindex = 0
    levelindex = 1
    proofidindex = 2
    ruleindex = 3
    linesindex = 4
    proofsindex = 5
    commentindex = 6
    typeindex = 7
    lowestlevel = 0
    acceptedtypes = [And, Or, Not, Implies, Iff, Wff, Falsehood, Truth],
    false_name = Falsehood()
    coimplication_intro_tag = 'COI'
    coimplication_elim_tag = 'COE'
    conjunction_intro_tag = 'CI'
    conjunction_elim_tag = 'CE'
    disjunction_intro_tag = 'DI'
    disjunction_elim_tag = 'DE'
    explosion_tag = 'X'
    hypothesis_tag = 'H'
    implication_intro_tag = 'II'
    implication_elim_tag = 'IE'
    necessary_intro_tag = 'NEI'
    necessary_elim_tag = 'NEE'
    negation_intro_tag = 'NI'
    negation_elim_tag = 'NE'
    possibly_intro_tag = 'POI'
    possibly_elim_tag = 'POE'
    premise_tag = 'P'
    reiterate_tag = 'R'
    blankstatement = ''
    subproof_strict = 'STRICT'
    subproof_normal = ''

    complete = 'COMPLETE'
    partialcompletion = 'PARTIAL COMPLETION'
    stopped = 'STOPPED'

    """The following names may be changed.  They are used for display purposes.
    One could redefine them just after instantiating an instance of the Proof class.
    """

    addhypothesis_name = 'Add Hypothesis'
    axiom_name = 'Axiom'
    definition_name = 'Definition'
    coimplication_intro_name = 'Coimplication Intro'
    coimplication_elim_name = 'Coimplication Elim'
    conjunction_intro_name = 'Conjunction Intro'
    conjunction_elim_name = 'Conjunction Elim'
    disjunction_intro_name = 'Disjunction Intro'
    disjunction_elim_name = 'Disjunction Elim'
    goal_name = 'GOAL'
    hypothesis_name = 'Hypothesis'
    implication_intro_name = 'Implication Intro'
    implication_elim_name = 'Implication Elim'
    necessary_intro_name = 'Necessary Intro'
    necessary_elim_name = 'Necessary Elim'
    negation_intro_name = 'Negation Intro'
    negation_elim_name = 'Negation Elim'
    possibly_intro_name = 'Possibly Intro'
    possibly_elim_name = 'Possibly Elim'
    premise_name = 'Premise'
    reiterate_name = 'Reiteration'
    setlogic_name = 'Set Logic'
    useproof_name = 'Use Saved Proof'
    comment_connector = ' - '
    stopped_connector = ': '
    stopped_closemainproof = 'The main proof cannot be closed only completed.'
    log_closemainproof = '{0}: The main proof cannot be closed only completed.'
    stopped_linescope = 'Referenced item is out of scope.'
    log_linescope = '{0}: The line {1} is out of scope.'
    stopped_nodefinitionmatch = 'The referenced line does not match the definition.'
    log_nodefinitionmatch = '{0}: The referenced item "{1}" on line {2} does not match the definition "{3}".'
    stopped_nogoal = 'The proof does not yet have a goal.'
    log_nogoal = '{0}: The proof needs a goal before a line with the item "{1}" can be added to it.'
    stopped_nologic = 'No logic has been declared for the proof.'
    log_nologic = '{0}: No logic has been declared for the proof.'
    stopped_nosavedproof = "The named saved proof does not exist in the logic's database."
    log_nosavedproof = '{0}: The saved proof "{1}" cannot be found in the database.'
    stopped_nosuchline = 'The referenced line does not exist.'
    log_nosuchline = '{0}: The line {1} cannot be found in the proof.'
    stopped_nosubs = 'There were no substitutions entered.'
    log_nosubs = '{0}: There were no substitutions entered.'
    stopped_nosubproof = 'No subproof has yet been started to add an hypothesis to.'
    log_nosubproof = '{0}: There is no subproof to add the hypothesis "{1}" to.'
    stopped_notantecedent = 'One item is not the antecedent of the other.'
    log_notantecedent = '{0}: Item "{1}" is not the antecedent of the other "{2}".'
    stopped_notcoimplicationelim = 'The refernced items cannot be used in coimplication elimination.'
    log_notcoimplicationelim = '{0}: The referenced items "{1}" on line {2} and "{3}" on line {4} cannot be used in coimplication elimination.'

    stopped_notcomplete = 'The proof needs to be completed before it can be saved.' 

    stopped_notconjunction = 'The referenced item is not a conjunction.'
    log_notconjunction = '{0}: The referenced item "{1}" on line {2} is not a conjunction.'
    stopped_notcontradiction = 'The referenced items are not negations of each other.'
    log_notcontradiction = '{0}: The reference items "{1}" on line {2} and "{3}" on line {4} are not negations of each other.'
    stopped_notdisjunction = 'The referenced item is not a disjunction.'
    log_notdisjunction = '{0}: The referenced item "{1}" on line {2} is not a disjunction.'
    stopped_notfalse = 'The referenced item is not false.'
    log_notfalse = '{0}: The referenced item "{1}" on line {2} is not false.'
    stopped_notimplication = 'The referenced item is not an implication.'
    log_notimplication = '{0}: The referenced item "{1}" on line {2} is not an implication.'
    stopped_notmodusponens = 'The referenced items can not be used in implication elimination.'
    log_notmodusponens = '{0}: The referenced items "{1}" on line {2} and "{3}" on line {4} cannot be used in implication elimination.'
    stopped_notnecessary = 'The referenced item is not necessary.'
    log_notnecessary = '{0}: The referenced item "{1}" on line {2} is not necessary.'
    stopped_notreiteratescope = 'The referenced item is not in the reiterate scope.'
    log_notreiteratescope = '{0}: The referenced item on line {1} is not in the reiterate scope.'
    stopped_notsamestatement = 'The referenced items are not the same.'
    log_notsamestatement = '{0}: The referenced items "{1}" and "{2}" are not the same.'
    stopped_nosuchaxiom = 'The referenced named is not in the axiom list.'
    log_nosuchaxiom = '{0}: The name "{1}" does not reference an axiom.'
    stopped_nosuchdefinition = 'The referenced name is not in the definition list.'
    log_nosuchdefinition = '{0}: The name "{1}" does not reference a definition.'
    stopped_novaluepassed = 'No value was passed to the function.'
    log_novaluepassed = '{0}: No value was passed to the function.'
    stopped_notstrictsubproof = 'The subproof is not strict.'
    log_notstrictsubproof = '{0}: The subproof is "{1}" rather than "{2}".'
    stopped_sidenotselected = 'A side, "left" or "right", must be selected.'
    log_sidenotselected = '{0}: The input "{1}" was used rather than "left" or "right".'
    stopped_string = 'Input is a string rather than an item in the proof.'
    log_string = '{0}: The input "{1}" is a string rather than a declared item of the proof.'
    stopped_notransformationrule = 'The transformation rule is not defined in the selected logic.'
    log_notransformationrule = '{0}: This transformation rule is not part of the logic.'
    log_logicdescription = '{0}: "{1}" has been selected as the logic described as "{2}" and stored in database "{3}".'

    log_addhypothesis = '{0}: Item "{1}" has been added as an hypothesis to subproof {2}.'
    log_useproof = '{0}: Item "{1}" has been added through the "{2}" saved proof.'
    log_definition = '{0}: Item "{1}" has been added through the "{2}" definition.'
    log_axiom = '{0}: Item "{1}" has been added through the "{2}" axiom.'
    log_coimplication_elim = '{0}: Item "{1}" has been derived from the coimplication "{2}".'
    log_coimplication_intro = '{0}: Item "{1}" has been derived from "{2}" and "{3}".'
    log_conjunction_elim = '{0}: Item "{1}" has been derived from the conjunction "{2}" on line {3}.'
    log_conjunction_intro = '{0}: The conjunction "{1}" has been derived from "{2}" on line {3} and "{4}" on line {5}.'
    log_disjunction_elim = '{0}: Item "{1}" has been derived as the conclusion of both disjuncts of the disjunction "{2}" on line {3}.'
    log_disjunction_intro = '{0}: Item "{1}" has been derived from item "{2}" on line {3} joined on the {4} with {5}.'
    log_goal = '{0}: The goal "{1}" has been added to the goals.'
    log_hypothesis = '{0}: A new subproof {1} has been started with item "{2}".'
    log_implication_elim = '{0}: Item "{1}" has been derived from the implication "{2}" and item "{3}".'
    log_implication_intro = '{0}: Item "{1}" has been derived upon closing subproof {2}.'
    log_necessary_elim = '{0}: Item "{1}" has been derived from the necessary item "{2}" on line {3}.'
    log_negation_elim = '{0}: Item "{1}" has been derived from the contradiction between "{2}" on line {3} and "{4}" on line {5}.'
    log_negation_intro = '{0}: Item "{1}" has been derived as the negation of the hypothesis "{2}" of subproof {3} which is now closed.'
    log_premise = '{0}: Item "{1}" has been added to the premises.'
    log_reiterate = '{0}: Item "{1}" on line {2} has been reiterated into subproof {3}.'
    label_name = 'Name'
    label_proofname = 'Proof Name'
    label_comment = 'Comment'
    label_description = 'Description'
    label_item = 'Item'
    label_rule = 'Rule'
    label_proofs = 'Proofs'
    label_proof = 'Proof'
    label_level = 'Level'
    label_lines = 'Lines'
    label_linetype = 'Type'
    label_value = 'Value'
    label_displayname = 'Display Name'
    label_logic = 'Logic'
    label_logicdescription = 'Logic Description'
    label_nodescription = 'No Description'
    label_logicdatabase = 'Logic Database'
    label_nodatabase = 'No Database'
    label_goals = 'Goals'
    label_goal = 'Goal'
    label_nogoals = 'No Goals'
    label_derivedgoals = 'Derived Goals'
    label_derivedgoal = 'Derived Goal'
    label_noderivedgoals = 'No Derived Goals'
    label_axioms = 'Axioms'
    label_axiom = 'Axiom'
    label_noaxioms = 'No Axioms'
    label_connectors = 'Connectors'
    label_connector = 'Connector'
    label_definitions = 'Definitions'
    label_nodefinition = ' No Definitions'
    label_noconnectors = 'No Connectors'
    label_intelimrules = 'IntElim Rules'
    label_intelimrule = 'IntElim Rule'
    label_nointelimrules = 'No IntElim Rules'
    label_premises = 'Premises'
    label_premise = 'Premise'
    label_nopremises = 'No Premises'
    label_proofstatus = 'Proof Status'
    label_inprogress = 'In Progress'
    label_stoppedstatus = 'Stopped Status'
    label_notstopped = 'Not Stopped'
    label_prooflevel = 'Proof Level'
    label_currentproofid = 'Current Proof ID'
    label_previousproofid = 'Previous Proof ID'
    label_previousproofchain = 'Previous Proof Chain'
    label_empty = 'Empty'
    linetype_savedproof = ' SP'
    linetype_axiom = ' AX'
    linetype_definition = ' DEF'
    linetype_notransformationrule = ' TR'
    linetype_hypothesis = 'H'
    linetype_premise = 'PR'

    def __init__(self, name: str = '', displayname: str = '', description: str = ''):
        """Create a Proof object with an optional name.
        
        Parameters:
            name: The name assigned to the proof under which it may be saved in the proofs and proofdetail tables of the database.
            displayname: The name to be used in displaying the proof.
            description: A descriptive name giving more information about the proof to be used in queries later.

        Exceptions:
            TypeError: If the input to either the name, displayname or description parameters are not strings,
            then a type error is raised.
        """

        if type(name) != str or type(displayname) != str or type(description) != str:
            raise TypeError('A value used to define a Proof object was not a string.')
        
        self.name = name
        self.displayname = displayname
        self.description = description
        self.goals = []
        self.goals_string = ''
        self.goals_latex = ''
        self.goalswff = []
        self.derivedgoals = []
        self.derivedgoalswff = []
        self.comment = ''
        self.logic = ''
        self.logicdescription = ''
        self.logicdatabase = ''
        self.logicconnectors = []
        self.logicaxioms = []
        self.logicdefinitions = []
        self.logicintelimrules = []
        self.logicoperators = [
            (self.coimplication_elim_tag, self.coimplication_elim_name),
            (self.coimplication_intro_tag, self.coimplication_intro_name),
            (self.conjunction_elim_tag, self.conjunction_elim_name),
            (self.conjunction_intro_tag, self.conjunction_intro_name),
            (self.disjunction_elim_tag, self.disjunction_elim_name),
            (self.disjunction_intro_tag, self.disjunction_intro_name),
            (self.implication_elim_tag, self.implication_elim_name),
            (self.implication_intro_tag, self.implication_intro_name),
            (self.necessary_elim_tag, self.necessary_elim_name),
            (self.necessary_intro_tag, self.necessary_intro_name),
            (self.negation_elim_tag, self.negation_elim_name),
            (self.negation_intro_tag, self.negation_intro_name),
            (self.possibly_elim_tag, self.possibly_elim_name),
            (self.possibly_intro_tag, self.possibly_intro_name),
        ]
        self.basicoperators = [
            (self.hypothesis_tag, self.hypothesis_name),
            (self.premise_tag, self.premise_name),
            (self.reiterate_tag, self.reiterate_name),
        ]
        self.lines = [['', 0, 0, '', '', '', '', '']]
        self.previousproofchain = []
        self.previousproofid = -1
        self.currentproof = [1]
        self.currentproofid = 0
        self.subproof_status = self.subproof_normal
        self.proofdata = [[self.name, self.displayname, self.description]]
        self.proofdatafinal = []
        self.truefalselist = ['Wff']
        self.prooflist = [[self.lowestlevel, self.currentproof, self.previousproofid, [], self.subproof_status]]  
        self.level = self.lowestlevel
        self.status = ''
        self.stoppedmessage = ''
        self.premises = []
        self.consequences = []
        self.letters = []
        self.truths = []
        self.falsehoods = []
        self.objectdictionary = {
            'Implies': Implies, 
            'Iff': Iff, 
            'And': And, 
            'Or': Or, 
            'Not': Not, 
            'Necessary': Necessary, 
            'Possibly': Possibly, 
            'PremisesConclusion': PremisesConclusion,
            'Definition': Definition,
            }
        self.log = []
        self.showlogging = False

    """SUPPORT FUNCTIONS NOT INTENTED TO BE DIRECTLY CALLED BY THE USER"""

    def appendproofdata(self, 
                        statement:  And | Or | Not | Implies | Iff | Wff | Falsehood | Truth,
                        rule: str):
        length = len(self.lines) - 1
        self.proofdata.append(
                [
                    self.name,
                    statement,
                    self.lines[length][1], 
                    self.lines[length][2], 
                    ''.join(['*', rule, '*']),
                    self.lines[length][4], 
                    self.lines[length][5],
                    self.lines[length][6],
                    self.lines[length][7]
                ]
            )
        if self.status == self.complete:
            finalresult = self.buildpremisesconclusion()
            self.proofdatafinal.append([
                self.proofdata[0][0], 
                self.proofdata[0][1], 
                self.proofdata[0][2], 
                self.proofdata[0][3],
                finalresult.pattern(self.truefalselist)
                ])
            for i in range(len(self.proofdata)):
                if i > 0:
                    self.proofdatafinal.append([
                        self.proofdata[i][0],
                        self.proofdata[i][1].pattern(self.truefalselist),
                        self.proofdata[i][2],
                        self.proofdata[i][3],
                        self.proofdata[i][4],
                        self.proofdata[i][5],
                        self.proofdata[i][6],
                        self.proofdata[i][7]
                    ])    
        
    def canproceed(self):
        """Check if there are no errors that block proceeding with the next line of the proof or the proof is already complete."""

        return self.status != self.complete and self.status != self.stopped 
    
    def completedproof(self):
        """Check if the proof is complete."""

        return self.status == self.complete

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

    def checkintelimrule(self, intelimrule: str):
        """Check if the operator is defined in the selected logic."""

        found = False
        for i in self.logicintelimrules:
            if i[0] == intelimrule:
                found = True
                break
        return found
    
    def checklinescope(self, line: int):
        """Check if the line is in the current current proof."""

        return self.lines[line][2] == self.currentproofid
    
    def checkstring(self, wff: And | Or | Not | Implies | Iff | Wff | Falsehood | Truth):
        return type(wff) == str

    def buildpremisesconclusion(self):
        conclusion = self.consequences[0]
        if len(self.consequences) > 1:
            for i in range(len(self.consequences)):
                if i > 0:
                    conclusion = And(conclusion, self.consequences[i])
        if len(self.premises) > 0:
            return PremisesConclusion(conclusion, self.premises)
        else:
            return PremisesConclusion(conclusion)
        
    def getantecedentconsequent(self):
        consequent = self.consequences[0]
        if len(self.consequences) > 1:
            for i in range(len(self.consequences)):
                if i > 0:
                    consequent = And(consequent, self.consequences[i])
        if len(self.premises) > 0:
            antecedent = self.premises[0]
            if len(self.premises) > 1:
                for i in range(len(self.premises)):
                    if i > 0:
                        antecedent = And(antecedent, self.premises[i])
            return Implies(antecedent, consequent)
        else:
            return consequent

    def getcurrentitemid(self):
        """Returns the number of the current item of the proof."""

        return len(self.lines)
    
    def getlevelstatement(self, line: int) -> tuple:
        """Given a line id, return the level and the statement on that line."""

        level = self.lines[line][self.levelindex]
        statement = self.lines[line][self.statementindex]
        return level, statement

    def getpreviousproofid(self, proofid: int) -> int:
        """Returns the previous proof id of the current proof id."""

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
        previousproofid = self.getpreviousproofid(proofid)
        return level, hypothesis, conclusion, previousproofid
    
    def getproofidstatement(self, line):
        """Returns the proof id in the line."""

        proofid = self.lines[line][self.proofidindex]
        statement = self.lines[line][self.statementindex]
        return proofid, statement
    
    def getstatement(self, line):
        """Returns the statement associated with the line number."""

        return self.lines[line][self.statementindex]

    def iscomplete(self, 
                   statement:  And | Or | Not | Implies | Iff | Wff | Falsehood | Truth = None, 
                   comment: str = ''):
        """Check if the proof is complete or partially complete and if so leave a message."""

        newcomment = self.status
        if self.level == 0:
            if str(statement) in self.goals:
                if str(statement) not in self.derivedgoals:
                    self.derivedgoals.append(str(statement))
                    self.derivedgoalswff.append(statement)
                    if len(self.derivedgoals) < len(self.goals):
                        newcomment = self.partialcompletion
                        self.consequences.append(statement)
                        self.logstep(f'The proof is partially complete.')
                    else:
                        self.status = self.complete
                        self.prooflist[0][1].append(len(self.lines))
                        newcomment = self.complete
                        self.consequences.append(statement)
                        self.logstep(f'The proof is complete.')
                
        if comment == '':
            return newcomment
        else:
            if newcomment == '':
                return comment
            else:
                return ''.join([newcomment, self.comment_connector, comment])
    
    def logstep(self, message: str):
        self.log.append(message)
        if self.showlogging:
            print(message)

    def stringitem(self, prooflines: list, i: int):
        base = '   |'
        hypothesisbase = ' __|'
        statement = ''
        for j in range(1, prooflines[i][self.levelindex]):
            statement = base + statement
        if prooflines[i][self.statementindex] != '':
            if prooflines[i][self.levelindex] > 0:
                if i < len(prooflines) - 1:
                    if prooflines[i][self.ruleindex] == self.hypothesis_name:
                        if prooflines[i+1][self.ruleindex] != self.hypothesis_name or prooflines[i][self.levelindex] < prooflines[i+1][self.levelindex]:
                            statement = hypothesisbase + statement
                        else:
                            statement = base + statement
                    else:
                        statement = base + statement   
                else:
                    if prooflines[i][self.ruleindex] == self.hypothesis_name:
                        statement = hypothesisbase + statement
                    else:
                        statement = base + statement
        statement = ''.join([str(prooflines[i][self.statementindex]), statement])
        return statement

    def latexitem(self, prooflines: list, i: int, status: str, saved: bool = False, color: int = 1):
        if prooflines[i][0] != self.blankstatement:
            base = ' \\hspace{0.35cm}|'
            hypothesisbase = ''.join(['\\underline{', base, '}']) 
            statement = ''
            for j in range(1, prooflines[i][self.levelindex]):
                statement = base + statement
            if prooflines[i][self.statementindex] != '':
                if prooflines[i][self.levelindex] > 0:
                    if i < len(prooflines) - 1:
                        if prooflines[i][self.ruleindex] == self.hypothesis_name:
                            if prooflines[i+1][self.ruleindex] != self.hypothesis_name or prooflines[i][self.levelindex] < prooflines[i+1][self.levelindex]:
                                statement = hypothesisbase + statement
                            else:
                                statement = base + statement
                        else:
                            statement = base + statement   
                    else:
                        if prooflines[i][self.ruleindex] == self.hypothesis_name:
                            statement = hypothesisbase + statement
                        else:
                            statement = base + statement

            if i == 0:
                if saved:
                    statement = ''.join(['$\\color{blue}', prooflines[0][0].latex(), '$']) #, statement, ])
                else:
                    if self.goals_latex != '':
                        statement = ''.join(['$\\color{blue}', self.goals_latex, '$']) #, statement, ])
                    else:
                        statement = ''
            elif color == 1 and status != self.complete and status != self.stopped and prooflines[i][1] == self.level and self.currentproofid == prooflines[i][2] and i > 0:
                statement = ''.join(['$\\color{green}', prooflines[i][0].latex(), statement, '$' ])
            elif color == 1 and status != self.complete and status != self.stopped and (prooflines[i][2] in self.previousproofchain) and i > 0:
                statement = ''.join(['$\\color{red}', prooflines[i][0].latex(), statement, '$' ])
            elif color == 1 and prooflines[i][6][0:8] == self.complete: 
                statement = ''.join(['$\\color{blue}', prooflines[i][0].latex(), statement, '$' ])
            elif color == 1 and prooflines[i][6][0:18] == self.partialcompletion:
                statement = ''.join(['$\\color{blue}', prooflines[i][0].latex(), statement, '$'])
            else:
                if type(prooflines[i][0]) == str:
                    statement = ''.join([prooflines[i][0], statement])
                else:
                    statement = ''.join(['$', prooflines[i][0].latex(), statement, '$' ])
        else:
            statement = self.blankstatement
        return statement

    def statusreport(self, *args, latex=1):
        axiomslist = [list(i) for i in self.logicaxioms]
        columns = [self.label_name, self.label_value]
        data = []

        # Display general information on proof and logic used.
        data.append([self.label_proofname, self.name])
        data.append([self.label_displayname, self.displayname])
        data.append([self.label_description,self.description])
        data.append([self.label_logic, self.logic])
        data.append([self.label_logicdescription, self.logicdescription])
        data.append([self.label_logicdatabase, self.logicdatabase])

        # Display axioms.
        if len(self.logicaxioms) == 0:
            data.append([self.label_axioms, self.label_noaxioms])
        else:
            for i in range(len(self.logicaxioms)):
                axiom = str(axiomslist[i][1])
                for k in range(len(args)):
                    axiom = axiom.replace(''.join(['*', str(k+1), '*']), args[k].tree())
                axiomwff = eval(axiom, self.objectdictionary)
                if latex == 1:
                    axiom = ''.join(['$', axiomwff.latex(), '$'])
                else:
                    axiom = str(axiomwff)
                axiomslist[i][1] = axiom
                data.append([self.label_axiom, axiomslist[i]])

        # Display connectors.
        if len(self.logicconnectors) == 0:
            data.append([self.label_connectors, self.label_noconnectors])
        else:
            for i in self.logicconnectors:
                data.append([self.label_connector, i[1]])

        # Display intelim rules.
        if len(self.logicintelimrules) == 0:
            data.append([self.label_intelimrules, self.label_nointelimrules])
        else:
            for i in self.logicintelimrules:
                data.append([self.label_intelimrule, i[1]])

        # Display goals.
        if len(self.goalswff) == 0:
            data.append([self.label_goals, self.label_nogoals])
        else:
            for i in self.goalswff:
                if latex == 1:
                    data.append([self.label_goal, ''.join(['$', i.latex(), '$'])])
                else:
                    data.append([self.label_goal, str(i)])

        # Display premises.
        if len(self.premises) == 0:
            data.append([self.label_premises, self.label_nopremises])
        else:
            for i in self.premises:
                if latex == 1:
                    data.append([self.label_premise, ''.join(['$', i.latex(), '$'])])
                else:
                    data.append([self.label_premise, str(i)])

        # Display derived goals.
        if len(self.derivedgoalswff) == 0:
            data.append([self.label_derivedgoals, self.label_noderivedgoals])
        else:
            for i in self.derivedgoalswff:
                if latex == 1:
                    data.append([self.label_derivedgoal, ''.join(['$', i.latex(), '$'])])
                else:
                    data.append([self.label_derivedgoal, str(i)])

        # Display status, stopped and proof info.
        if self.status == '':
            data.append([self.label_proofstatus, self.label_inprogress])
        else:
            data.append([self.label_proofstatus, self.status])
        if self.stoppedmessage == '':
            data.append([self.label_stoppedstatus, self.label_notstopped])
        else:
            data.append([self.label_stoppedstatus, self.stoppedmessage])
        data.append([self.label_prooflevel, self.level])
        data.append([self.label_currentproofid, self.currentproofid])
        data.append([self.label_previousproofid, self.previousproofid])
        if self.previousproofchain == []:
            data.append([self.label_previousproofchain, self.label_empty])
        else:
            data.append([self.label_previousproofchain, self.previousproofchain])
        index = []
        for i in range(len(data)):
            index.append(str(i))
        df = pandas.DataFrame(data, index=index, columns=columns)
        return df

    def reportstatus(self):
        # Display general information.
        print('{: <25} {: <25}'.format(self.label_proofname, self.name))
        print('{: <25} {: <25}'.format(self.label_displayname, self.displayname))
        print('{: <25} {: <25}'.format(self.label_displayname, self.displayname))
        print('{: <25} {: <25}'.format(self.label_description, self.description))
        print('{: <25} {: <25}'.format(self.label_logic, self.logic))
        print('{: <25} {: <25}'.format(self.label_logicdescription, self.logicdescription))
        print('{: <25} {: <25}'.format(self.label_logicdatabase, self.logicdatabase))

        # Display axioms
        if len(self.logicaxioms) == 0:
            print('{: <25} {: <25}'.format(self.label_axioms, self.label_noaxioms))
        else:
            print('{}'.format(self.label_axioms))
            for i in self.logicaxioms:
                print('{: >25} {: <25}'.format(i[0], i[1]))

        # Display definitions
        if len(self.logicdefinitions) == 0:
            print('{: <25} {: <25}'.format(self.label_definitions, self.label_nodefinitions))
        else:
            print('{}'.format(self.label_definitions))
            for i in self.logicdefinitions:
                print('{: >25} {: <25}'.format(i[0], i[1]))

        # Display connectors.
        if len(self.logicconnectors) == 0:
            print('{: <25} {: <25}'.format(self.label_connectors, self.label_noconnectors))
        else:
            print('{}'.format(self.label_connectors))
            for i in self.logicconnectors:
                print('{: >25} {: <25}'.format(i[1], i[2]))

        # Display intelim rules.
        if len(self.logicintelimrules) == 0:
            print('{: <25} {: <25}'.format(self.label_intelimrules, self.label_nointelimrules))
        else:
            print('{}'.format(self.label_intelimrules))
            for i in self.logicintelimrules:
                print('{: <25} {: <25}'.format(' ', i[1]))

        # Display goals.
        if len(self.goals) == 0:
            print('{: <25} {: <25}'.format(self.label_goals, self.label_nogoals))
        else:
            print('{}'.format(self.label_goals))
            for i in self.goals:
                print('{: <25} {: <25}'.format(' ', str(i)))

        # Display premises.
        if len(self.premises) == 0:
            print('{: <25} {: <25}'.format(self.label_premises, self.label_nopremises))
        else:
            print('{}'.format(self.label_premises))
            for i in self.premises:
                print('{: <25} {: <25}'.format(' ', str(i)))

        # Display derived goals.
        if len(self.derivedgoals) == 0:
            print('{: <25} {: <25}'.format(self.label_derivedgoals, self.label_noderivedgoals))
        else:
            print('{}'.format(self.derivedgoals))
            for i in self.derivedgoals:
                print('{: <25} {: <25}'.format(' ', str(i)))

        # Display proof statuses.
        if self.status == '':
            print('{: <25} {: <25}'.format(self.label_proofstatus, self.label_inprogress))
        else:
            print('{: <25} {: <25}'.format(self.label_proofstatus, self.status))
        if self.stoppedmessage == '':
            print('{: <25} {: <25}'.format(self.label_stoppedstatus, self.label_notstopped))
        else:
            print('{: <25} {: <25}'.format(self.label_stoppedstatus, self.stoppedmessage))
        print('{: <25} {: <25}'.format(self.label_prooflevel, self.level))
        print('{: <25} {: <25}'.format(self.label_currentproofid, self.currentproofid))
        print('{: <25} {: <25}'.format(self.label_previousproofid, self.previousproofid))
        if self.previousproofchain == []:
            print('{: <25} {: <25}'.format(self.label_previousproofchain, self.label_empty))
        else:
            print('{: <25} {: <25}'.format(self.label_previousproofchain, self.previousproofchain))

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

    def proofdetailsraw(self, proofname: str):
        """Display the proof details as saved to the database."""

        # Retrieve proof data.
        rows = altrea.data.getproofdetails(self.logic, proofname)

        # Prepare to run DataFrame.
        columns = ['Item', 'Level', 'Proof', 'Rule', 'Lines', 'Proofs', 'Comment']
        index = []
        for i in range(len(rows)):
            index.append(i)
        df = pandas.DataFrame(rows, index=index, columns=columns)
        return df
    
    def proofdetails(self, proofname: str, *args, latex: int = 1):
        # Retrieve proof data.
        displayname, description, pattern = altrea.data.getsavedproof(self.logic, proofname)
        rows = altrea.data.getproofdetails(self.logic, proofname)

        # Change references to proof lines into the items on those lines.
        s = []
        for i in args:
            if type(i) == int:        
                s.append(self.getstatement(i))
            else:
                s.append(i)
        statement = pattern
        for k in range(len(s)):
            statement = statement.replace(''.join(['*', str(k+1), '*']), s[k].tree())
        newrows =[]
        newrows.append([statement, 0, 0, self.goal_name, '', '', ''])
        for i in rows:
            newrows.append(list(i))

        # Format the item column using the dictionary.
        for i in range(len(newrows)):
            for k in range(len(s)):
                newrows[i][0] = newrows[i][0].replace(''.join(['*', str(k+1), '*']), s[k].tree())
            newrows[i][0] = eval(newrows[i][0], self.objectdictionary)

        # Format the rules column using the names from the proofs logic operators.
        for i in newrows:
            for k in self.logicoperators:
                i[3] = i[3].replace(''.join(['*', k[0], '*']), k[1])
        for i in newrows:
            for k in self.basicoperators:
                i[3] = i[3].replace(''.join(['*', k[0], '*']), k[1])
        for i in newrows:
            for k in self.basicoperators:
                i[3] = i[3].replace('*', '')

        # Display the proof.
        newp = []
        if latex == 1:
            for i in range(len(newrows)):
                item = self.latexitem(newrows, i, self.complete, saved=True)
                newp.append([item, newrows[i][1], newrows[i][2], newrows[i][3], newrows[i][4], newrows[i][5], newrows[i][6]])
        else:
            for i in range(len(newrows)):
                item = self.stringitem(newrows, i)
                newp.append([item, newrows[i][1], newrows[i][2], newrows[i][3], newrows[i][4], newrows[i][5], newrows[i][6]])  

        # Prepare to run DataFrame.
        columns = [self.label_item, self.label_level, self.label_proof, self.label_rule, self.label_lines, self.label_proofs, self.label_comment]
        index = [displayname]
        for i in range(len(newrows)):
            if i > 0:
                index.append(i)
        df = pandas.DataFrame(newp, index=index, columns=columns)
        return df

    def displayproof(self, 
                    short: int = 0,
                    color: int = 1, 
                    latex: int = 1):
        """This function displays the proof lines.
        
        Parameters:
            short: Display a three column proof with the item, combined rule and lines referenced and comments.  Using the
            default presents all lines of the proof.
            color: Displays the latex version with color.  This helps if one is using natural deduction with Fitch-style subordinate proofs.
            latex: This sets the display for the statement to use latex rather than text.
            
        """

        # Create the column.
        if short == 1:
            columns = [self.label_item, self.label_rule, self.label_comment]
        else:
            columns = [self.label_item, self.label_level, self.label_proof, self.label_rule, self.label_linetype, self.label_lines, self.label_proofs, self.label_comment]

        # Create the index.
        indx = [self.displayname]
        for i in range(len(self.lines)-1):
            indx.append(i + 1)

        # Create the rows of data.
        newp = []
        for i in range(len(self.lines)):
            if latex == 1:
                statement = self.latexitem(prooflines=self.lines, i=i, status=self.status, saved=False, color=color)
            else:
                statement = self.stringitem(prooflines=self.lines, i=i)
            if short == 1:
                if self.lines[i][self.linesindex] != '':
                    rule = ''.join([self.lines[i][self.linesindex], ', ',self.lines[i][self.ruleindex]])
                elif self.lines[i][self.proofsindex] != '':
                    rule = ''.join([self.lines[i][self.proofsindex], ', ',self.lines[i][self.ruleindex]])
                else:
                    rule = self.lines[i][self.ruleindex]
                newp.append(
                    [
                        statement,
                        rule,
                        self.lines[i][self.commentindex],
                    ]
                )
            else:
                newp.append(
                    [
                        statement,
                        self.lines[i][self.levelindex],
                        self.lines[i][self.proofidindex],
                        self.lines[i][self.ruleindex],
                        self.lines[i][self.typeindex],
                        self.lines[i][self.linesindex],
                        self.lines[i][self.proofsindex],
                        self.lines[i][self.commentindex],
                    ]
                )

        # Use pandas to display the proof lines.
        df = pandas.DataFrame(newp, index=indx, columns=columns)
        return df

    def truthtable(self):
        """Display a truth table built from the premises and goal of the proof.
    
        Examples:
            
        """

        def flip(v: bool):
            if v:
                return False
            else:
                return True
            
        columns = []

        # Letters
        for i in self.letters:
            columns.append(''.join(['$', i[0].latex(), '$']))
        for i in self.truths:
            columns.append(''.join(['$', i[0].latex(), '$']))

        # Separate the letters from the premises and conclusion.
        columns.append('$\\parallel $')

        # Optional premises
        if len(self.premises) > 0:
            for i in self.premises:
                columns.append(''.join(['$', i.latex(), '$']))

        # Required models sign
        columns.append('$\\models $')

        # Required conclusion
        if len(self.goalswff) > 0:
            goals = self.goalswff[0]
            if len(self.goalswff) > 1:
                for i in range(len(self.goalswff)):
                    if i > 0:
                        goals = And(goals, self.goalswff[i])
            columns.append(''.join(['$', goals.latex(), '$']))
            columns.append(' ')
        else:
            raise ValueError('A goal needs to be set before a truth table can be constructed.')
            
        tt = []
        letters = len(self.letters)
        countfalsegoal = 0
        ttrows = 2**letters
        status = 'Valid'

        for letter in self.letters:
            letter[0].booleanvalue = True
        for total in range(ttrows):
            row = []

            # Display the letters
            for i in self.letters:
                row.append(i[0].booleanvalue)
            for i in self.truths:
                row.append(True)
            row.append('$\\parallel $')

            # Display the optional premises
            premisesvalue = True
            if len(self.premises) > 0:
                for i in self.premises:
                    row.append(i.getvalue())
                    premisesvalue = premisesvalue and i.getvalue()

            # Display the goal and assessment of the interpretation on the line.
            row.append(' ')
            goalvalue = goals.getvalue()
            if not goalvalue:
                countfalsegoal += 1
            row.append(goalvalue)
            if premisesvalue == True and goalvalue == False:
                row.append('$\\color{red}\\times $')
                status = 'Invalid'
            elif premisesvalue == True and goalvalue == True:
                row.append('$\\color{green}\\checkmark $')
            else:
                row.append(' ')
            tt.append(row)
            for n in range(letters):
                if (total + 1) % (2**(letters - 1 - n)) == 0:
                    self.letters[n][0].booleanvalue = flip(self.letters[n][0].booleanvalue)

        if countfalsegoal == 0:
            status = 'Tautology'
        index = []
        for i in range(len(tt)):
            index.append(i+1)
        index.append(' ')
        summaryrow = []
        for i in range(len(columns)-3-len(self.premises)):
            summaryrow.append(' ')
        if status == 'Tautology':
            for i in range(len(self.premises)):
                summaryrow.append('$\\color{red}\\times $')
        else:
            for i in range(len(self.premises)):
                summaryrow.append(' ')
        summaryrow.append(status)
        summaryrow.append(' ')
        summaryrow.append(' ')
        tt.append(summaryrow)

        df = pandas.DataFrame(tt, index=index, columns=columns)
        return df

    def savedproofs(self):
        rows = altrea.data.getavailableproofs(self.logic)
        columns = ['Name', 'Pattern', 'Display', 'Description']
        index = []
        for i in range(len(rows)):
            index.append(i)
        df = pandas.DataFrame(rows, index=index, columns=columns)
        return df

    def getgenericaxioms(self, *args, latex: int = 1):
        """Provide a list of generic axioms which the user may add to the proof."""

        # Get generic axiom data.
        axioms = altrea.data.getgenericaxioms()

        # Create a copy of the list of tuples as a list of lists to update it.
        axiomslist = [list(i) for i in axioms]

        # Convert references to proof lines into Wff objects.
        expandedargs = []
        for i in args:
            if type(i) == int:        
                expandedargs.append(self.getstatement(i))
            else:
                expandedargs.append(i)

        # Format the item column by evaluating using the object dictionary.
        for i in axiomslist:
            for k in range(len(expandedargs)):
                i[1] = i[1].replace(''.join(['*', str(k+1), '*']), expandedargs[k].tree())
            i[1] = eval(i[1], self.objectdictionary)

        # Display in latex or text.
        for i in axiomslist:
            if latex == 1:
                i[1] = ''.join(['$', i[1].latex(), '$'])
            else:
                i[1] = str(i[1])  

        # Set up the DataFrame.
        columns = ['Name', 'Pattern', 'Display', 'Description']
        index = [i for i in range(len(axiomslist))]
        df = pandas.DataFrame(axiomslist, index=index, columns=columns)
        return df
    
    def stopproof(self, message: str, statement, rule: str, lines: str, blocks: str, comment: str = ''):
        """Logs a status message in the line of a proof that shows no further lines can be added until the error is fixed."""

        self.status = self.stopped
        self.stoppedmessage = ''
        if rule == self.goal_name:
            if comment == '':
                self.lines[0][self.commentindex] = ''.join([self.stopped, self.stopped_connector, message])
            else:
                self.lines[0][self.commentindex] = ''.join([self.stopped, self.stopped_connector, message, self.comment_connector, comment])
        else:
            if comment == '':
                self.stoppedmessage = ''.join([self.stopped, self.stopped_connector, message])
            else:
                self.stoppedmessage = ''.join([self.stopped, self.stopped_connector, message, self.comment_connector, comment])
            self.lines.append(
                [
                    statement, 
                    self.level, 
                    self.currentproofid, 
                    rule, 
                    lines, 
                    blocks, 
                    self.stoppedmessage,
                    ''
                ]
            )
            self.logstep(self.stoppedmessage)
 
    """SUPPORT FUNCTIONS CALLABLE BY THE USER"""

    def showlog(self, show: bool = True):
        """This function turns logging on if it is turned off.

        Parameters:
            show: This boolean turns the immediate display of logging on (default True) or off (False).
        
        Examples:

        """

        if show:
            self.showlogging = True
            self.logstep('The log will be displayed.')
        else:
            self.showlogging = False
            self.logstep('The log is already being displayed.')

    def displaylog(self):
        size = len(self.log)
        for i in range(len(self.log)):
            if size < 10:
                print('{: >1} {}'.format(i, self.log[i]))
            elif size < 100:
                print('{: >2} {}'.format(i, self.log[i]))
            elif size < 1000:
                print('{: >3} {}'.format(i, self.log[i]))
            else:
                print('{: >4} {}'.format(i, self.log[i]))

    def saveproof(self):
        """Save the proof to a database file associated with the logic.
        
        The proof must be complete before it can be saved.

        Example:
            Suppose one has created the following proof that given q one can derive p > q.  

            >>> from altrea.boolean import Wff, Or, Not, And, Implies, Iff, Necessary, Possibly
            >>> from altrea.rules import Proof
            >>> from altrea.display import displayproof, fitchnotation, showproof
            >>> addcond = Proof(name='add cond', displayname='add cond', description='Principle of Added Condition')
            >>> p = Wff('p')
            >>> q = Wff('q')
            >>> r = Wff('r')
            >>> fitchnotation(addcond)
            >>> addcond.setlogic('fitch')
            >>> addcond.goal(Implies(p, q))
            >>> addcond.premise(q)
            >>> addcond.hypothesis(p)
            >>> addcond.reiterate(1)
            >>> addcond.implication_intro()
            >>> displayproof(addcond, latex=0)
                  Statement  Level  Proof     Rule Lines Proofs   Comment
            fitch     p > q      0      0     GOAL
            1             q      0      0      hyp
            2         p __|      1      1      hyp
            3         q   |      1      1     reit     1
            4         p > q      0      0  imp int          2-3  COMPLETE

            Having already set up the database tables for a logic called `fitch` can can save and retrieve the proof
            with the name we gave it when the Proof object was instantiated.  Here the name is `add cond` and
            its display name is also `add cond`.  It's longer descriptive name is `Principle of Added Condition`.'
            To save the proof we would run `addcond.saveproof()`.  We might get the following response:

            >>> addcond.saveproof()


            The IntegrityError for a unique constraint means that we already have a proof saved under the name `addcond`.
            To get around that we could replace the proof if we desire with `addcond.saveproofreplace()` as follows:

            >>> addcond.saveproofreplace()
            The proof details for add cond have been deleted from fitch.
            The proof add cond has been deleted from fitch.
            The proof add cond has been added to fitch.
            The proof details for add cond have been added to fitch.
            The proof of Principle of Added Condition was saved in altrea/data/fitch.db.

            With this call the old `add cond` proof was deleted and the new one added.  The file lines detail
            what happened.
        """

        if self.completedproof():  
            altrea.data.addproof(self.proofdatafinal)
        else:
            print(self.stopped_notcomplete)
            

    def saveproofreplace(self):
        """Delete the proof that already exists with that name and save a proof with the same name 
        in the database file associated with the logic.
        
        The replacement proof must be complete before it can be saved.
        """

        if self.completedproof(): 
            altrea.data.deleteproof(self.logic, self.name)
            altrea.data.addproof(self.proofdatafinal)
        else:
            print(self.stopped_notcomplete)

    """FUNCTIONS TO BUILD PROOFS"""

    def addhypothesis(self,
                      hypothesis: And | Or | Not | Implies | Iff | Wff | Falsehood | Truth,
                      comment: str = ''):
        """Adds to the currently opened subproof an hypothesis and inserts the new hypothesis into
        a list of hypotheses which now have more than one.
        
        Parameters:
            hypothesis: The hypothesis that will be added.
            comment: Options comment entered by the user.
            
        Examples:
            There are two hypothesis calls.  The `hypothesis` call add the hypothesis to a new subordinate
            proof.  The `addhypothesis` call adds an additional hypothesis to the same subproof
            without creating a new one.  The `addhypothesis` call allows one to have more than
            one hypothesis in a subproof.  Here is an example.

            >>> from altrea.boolean import Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> C = Wff('C')
            >>> prf.setlogic('C')
            >>> prf.goal(B)
            >>> prf.hypothesis(A, comment='Each call to `hypothesis` creates a sub proof.')
            >>> prf.hypothesis(C, comment='Now I have a sub sub proof.')
            >>> prf.addhypothesis(B, comment='This adds a second hypothesis.')
            >>> showproof(prFalsehood, latex=0)
                    Item      Reason                                         Comment
            0          B        GOAL
            1      A __|  Hypothesis  Each call to `hypothesis` creates a sub proof.
            2  C   |   |  Hypothesis                     Now I have a sub sub proof.
            3  B __|   |  Hypothesis                  This adds a second hypothesis.

            There are two error messages that might occur.  One if a string rather than a Wff
            has been entered as the hypothesis and another if the goal has not first
            been set.

            Here is what happens when a string is entered.

            >>> from altrea.boolean import Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof, showlines
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> C = Wff('C')
            >>> prf.setlogic('C')
            >>> prf.goal(B, comment='There is a difference between A and "A"')
            >>> prf.hypothesis('A')
            >>> showproof(prFalsehood, latex=0)
              Item      Reason                                      Comment
            0    B        GOAL      There is a difference between A and "A"
            1       Hypothesis  STOPPED: Input is not a Wff derived object.

            Here is what happens when one neglects to first enter a goal.  It is
            the same proof as above, but `prf.goal` line has been commented out.

            >>> from altrea.boolean import Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof, showlines
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> C = Wff('C')
            >>> prf.setlogic('C')
            >>> #prf.goal(B, comment='There is a difference between A and "A"')
            >>> prf.hypothesis(A)
            >>> showproof(prFalsehood, latex=0)
              Item      Reason                                       Comment
            0
            1       Hypothesis  STOPPED: The proof does not yet have a goal.
        """

        # Look for errors
        if self.canproceed():
            if type(hypothesis) == str:
                self.logstep(self.log_string.format(self.addhypothesis_name.upper(), hypothesis))
                self.stopproof(self.stopped_string, self.blankstatement, self.hypothesis_name, '', '', comment)
            elif self.currentproofid == 0:
                self.logstep(self.log_nosubproof.format(self.addhypothesis_name.upper(), str(hypothesis)))
                self.stopproof(self.stopped_nosubproof, self.blankstatement, self.hypothesis_name, '', '', comment)

        # If no errors, perform task
        if self.canproceed():
            nextline = len(self.lines)
            self.prooflist[self.currentproofid][3].append(nextline)
            self.logstep(self.log_addhypothesis.format(self.addhypothesis_name.upper(), str(hypothesis), str(self.currentproofid))) 
            newcomment = self.iscomplete(hypothesis, comment)
            self.lines.append(
                [
                    hypothesis, 
                    self.level, 
                    self.currentproofid, 
                    self.hypothesis_name, 
                    '', 
                    '',
                    newcomment,
                    self.linetype_hypothesis
                ]
            )
            self.appendproofdata(hypothesis, self.hypothesis_tag)

    def useproof(self, 
                   name: str, 
                   *subs: int | And | Or | Not | Implies | Iff | Wff | Falsehood | Truth,
                   comment: str = ''):
        """Various proofs may be invoked here such as the law of excluded middle.
        
        Parameters:
            name: The name of the saved proof one wishes to use.
            subs: An arbitrarily long list of substitutions one for each distinct term of the pattern.
            comment: An optional comment.

        Examples:

        """

        # Look for errors.
        if self.canproceed():
            s = []
            lines = ''
            for i in subs:
                if len(subs) == 0:
                    self.logstep(self.log_nosubs.format(self.useproof_name.upper()))
                    self.stopproof(self.stopped_nosubs, self.blankstatement, name, '', '', comment)
                elif type(i) == int:
                    lines += ''.join([str(i), ','])
                    if not self.checkline(i):
                        self.logstep(self.log_nosuchline.format(self.useproof_name.upper(), str(i)))
                        self.stopproof(self.stopped_nosuchline, self.blankstatement, name, str(i), '', comment)
                    elif not self.checklinescope(i):
                        self.logstep(self.log_linescope.format(self.useproof_name.upper(), str(i)))
                        self.stopproof(self.stopped_linescope, self.blankstatement, name, str(i), '', comment)
                    else:
                        s.append(self.getstatement(i))
                elif type(i) == str:
                    self.logstep(self.log_string.format(self.useproof_name.upper(), i))
                    self.stopproof(self.stopped_string, self.blankstatement, name, '', '', comment)
                else:
                    s.append(i)
            try:
                displayname, description, pattern = altrea.data.getsavedproof(self.logic, name)
            except TypeError:
                self.logstep(self.log_nosavedproof.format(self.useproof_name.upper(), name))
                self.stopproof(self.stopped_nosavedproof, self.blankstatement, name, '', '', comment)

        # If no errors, perform task.
        if self.canproceed():
            for i in range(len(s)):
                pattern = pattern.replace(''.join(['*', str(i+1), '*']), s[i].tree())
            premisesconclusion = eval(pattern, self.objectdictionary)
            if len(premisesconclusion.premises) == 0:
                self.logstep(self.log_useproof.format(self.useproof_name.format(), str(premisesconclusion.conclusion), description))
            newcomment = self.iscomplete(premisesconclusion.conclusion, comment)
            if len(lines) > 0:
                lines = lines[:-1]
            self.lines.append(
                [
                    premisesconclusion.conclusion, 
                    self.level, 
                    self.currentproofid, 
                    displayname,
                    lines, 
                    '', 
                    newcomment,
                    self.linetype_savedproof
                ]
            )
            self.appendproofdata(premisesconclusion.conclusion, displayname)

    def definition(self, 
              name: str, 
              line: int,
              side: str,
              comment: str = '',
              *subs: And | Or | Not | Implies | Iff | Wff | Falsehood | Truth
              ):
        """Various axioms may be invoked here such as the law of excluded middle.
        
        Parameters:
            name: The name of the axiom one wishes to use.
            line: The line containing statement one wants to transform by invoking the definition.
            side: Which side of the definition to return, the left or the right.
            subs: An arbitrary long list of substitutions.
            comment: An optional comment.

        Examples:

        """

        # Look for errors.
        if self.canproceed():
            if not self.checkline(line):
                self.logstep(self.log_nosuchline.format(self.definition_name.upper(), str(i)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, name, str(line), '', comment)
            elif not self.checklinescope(line):
                self.logstep(self.log_linescope.format(self.definition_name.upper(), str(line)))
                self.stopproof(self.stopped_linescope, self.blankstatement, name, str(line), '', comment)
            elif not side in ['left', 'right']:
                self.logstep(self.log_sidenotselected.format(self.definition_name.upper(), side))
                self.stopproof(self.stopped_sidenotselected, self.blankstatement, name, '', '', comment)
            else:
                for i in subs:
                    if type(i) == str:
                        self.logstep(self.log_string.format(self.definition_name.upper(), i))
                        self.stopproof(self.stopped_string, self.blankstatement, name, '', '', comment)
        if self.canproceed():
            foundindex = -1
            for i in range(len(self.logicdefinitions)):
                if self.logicdefinitions[i][0] == name:
                    foundindex = i
                    break
            if foundindex < 0:
                self.logstep(self.log_nosuchdefinition.format(self.definition_name.upper(), name))
                self.stopproof(self.stopped_nosuchdefinition, self.blankstatement, name, '', '', comment)
            else:
                definition = self.logicdefinitions[foundindex][1]
                for i in range(len(subs)):
                    definition = definition.replace(''.join(['*', str(i+1), '*']), subs[i].tree())
                evaldefinition = eval(definition, self.objectdictionary)
                linestatement = self.getstatement(line)
                if side == 'left':
                    matchstatement = evaldefinition.right
                    returnstatement = evaldefinition.left
                else:
                    matchstatement = evaldefinition.left
                    returnstatement = evaldefinition.right
                if not matchstatement.equals(linestatement):
                    self.logstep(self.log_nodefinitionmatch.format(self.definition_name, str(linestatement), str(line), str(matchstatement)))
                    self.stopproof(self.stopped_nodefinitionmatch, self.blankstatement, name, '', '', comment)      

        # If no errors, perform task.
        if self.canproceed():
            displayname = self.logicdefinitions[foundindex][2]
            description = self.logicdefinitions[foundindex][3]
            self.logstep(self.log_definition.format(self.definition_name.upper(),str(returnstatement), description))
            newcomment = self.iscomplete(returnstatement, comment)
            self.lines.append(
                [
                    returnstatement, 
                    self.level, 
                    self.currentproofid, 
                    displayname,
                    line, 
                    '', 
                    newcomment,
                    self.linetype_definition
                ]
            )
            self.appendproofdata(returnstatement, displayname)

    def axiom(self, 
              name: str, 
              *subs: int | And | Or | Not | Implies | Iff | Wff | Falsehood | Truth,
              comment: str = ''):
        """Various axioms may be invoked here such as the law of excluded middle.
        
        Parameters:
            name: The name of the axiom one wishes to use.
            subs: An arbitrary long list of substitutions.
            comment: An optional comment.

        Examples:

        """

        # Look for errors.
        if self.canproceed():
            s = []
            lines = ''
            for i in subs:
                if type(i) == int:
                    lines += ''.join([str(i), ','])
                    if not self.checkline(i):
                        self.logstep(self.log_nosuchline.format(self.axiom_name.upper(), str(i)))
                        self.stopproof(self.stopped_nosuchline, self.blankstatement, name, str(i), '', comment)
                    elif not self.checklinescope(i):
                        self.logstep(self.log_linescope.format(self.axiom_name.upper(), str(i)))
                        self.stopproof(self.stopped_linescope, self.blankstatement, name, str(i), '', comment)
                    else:
                        s.append(self.getstatement(i))
                elif type(i) == str:
                    self.logstep(self.log_string.format(self.axiom_name.upper(), i))
                    self.stopproof(self.stopped_string, self.blankstatement, name, '', '', comment)
                else:
                    s.append(i)
            foundindex = -1
            for i in range(len(self.logicaxioms)):
                if self.logicaxioms[i][0] == name:
                    foundindex = i
                    break
            if foundindex < 0:
                self.logstep(self.log_nosuchaxiom.format(self.axiom_name.upper(), name))
                self.stopproof(self.stopped_nosuchaxiom, self.blankstatement, name, '', '', comment)

        # If no errors, perform task.
        if self.canproceed():
            pattern = self.logicaxioms[foundindex][1]
            displayname = self.logicaxioms[foundindex][2]
            description = self.logicaxioms[foundindex][3]
            for i in range(len(s)):
                pattern = pattern.replace(''.join(['*', str(i+1), '*']), s[i].tree())
            statement = eval(pattern, self.objectdictionary)
            self.logstep(self.log_axiom.format(self.axiom_name.upper(), str(statement), description))
            newcomment = self.iscomplete(statement, comment)
            if len(lines) > 0:
                lines = lines[:-1]
            self.lines.append(
                [
                    statement, 
                    self.level, 
                    self.currentproofid, 
                    displayname,
                    lines, 
                    '', 
                    newcomment,
                    self.linetype_axiom
                ]
            )
            self.appendproofdata(statement, displayname)

    def coimplication_elim(self, first: int, second: int, comment: str = ''):
        """Given an if and only if (iff) statement and a proposition one can derive the other proposition.
        
        Parameters:
            first: A statement containing either a proposition or an iff statement.
            second: A second statement containing either a proposition or an iff statement.
            comment: comment on this line of the proof.
        
        Examples:
            The following is a simple example of how the coimplication elimination rule works.

            >>> from altrea.boolean import Wff, Iff
            >>> from altrea.rules import Proof
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
        if self.canproceed():
            if not self.checkintelimrule(self.coimplication_elim_tag):
                self.logstep(self.log_notransformationrule.format(self.coimplication_elim_name.upper()))
                self.stopproof(self.stopped_notransformationrule, self.blankstatement, self.coimplication_elim_name, '', '', comment)
            elif not self.checkline(first):
                self.logstep(self.log_nosuchline.format(self.coimplication_elim_name.upper(), str(first)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.coimplication_elim_name, str(first), '', comment)
            elif not self.checkline(second):
                self.logstep(self.log_nosuchline.format(self.coimplication_elim_name.upper(), str(second)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.coimplication_elim_name, str(second), '', comment)
            elif not self.checklinescope(first):
                self.logstep(self.log_linescope.format(self.coimplication_elim_name.upper(), str(first)))
                self.stopproof(self.stopped_linescope, self.blankstatement, self.coimplication_elim_name, str(first), '', comment)
            elif not self.checklinescope(second):
                self.logstep(self.log_linescope.format(self.coimplication_elim_name.upper(), str(second)))
                self.stopproof(self.stopped_linescope, self.blankstatement, self.coimplication_elim_name, str(second), '', comment)
            else:
                firststatement = self.getstatement(first)
                secondstatement = self.getstatement(second)
                if type(firststatement) != Iff and type(secondstatement) != Iff:
                    self.logstep(self.log_notcoimplicationelim.format(self.coimplication_elim_name.upper(), str(firststatement), str(first), str(secondstatement), str(second)))
                    self.stopproof(self.stopped_notcoimplicationelim, self.blankstatement, self.coimplication_elim_name, self.reflines(first, second), '', comment)
                elif type(firststatement) == Iff and not secondstatement.equals(firststatement.left) and not secondstatement.equals(firststatement.right):
                    self.logstep(self.log_notcoimplicationelim.format(self.coimplication_elim_name.upper(), str(firststatement), str(first), str(secondstatement), str(second)))
                    self.stopproof(self.stopped_notcoimplicationelim, self.blankstatement, self.coimplication_elim_name, self.reflines(first, second), '', comment)
                elif type(secondstatement) == Iff and not firststatement.equals(secondstatement.left) and not firststatement.equals(secondstatement.right):
                    self.logstep(self.log_notcoimplicationelim.format(self.coimplication_elim_name.upper(), str(firststatement), str(first), str(secondstatement), str(second)))
                    self.stopproof(self.stopped_notcoimplicationelim, self.blankstatement, self.coimplication_elim_name, self.reflines(first, second), '', comment)

        # If no errors, perform task
        if self.canproceed():      
            if type(firststatement) == Iff:
                self.logstep(self.log_coimplication_elim.format(self.coimplication_elim_name.upper(), str(firststatement.right), str(firststatement)))
                newcomment = self.iscomplete(firststatement.right, comment)
                self.lines.append(
                    [
                        firststatement.right, 
                        self.level, 
                        self.currentproofid, 
                        self.coimplication_elim_name, 
                        self.reflines(first, second), 
                        '', 
                        newcomment,
                        self.linetype_notransformationrule
                    ]
                )
                self.appendproofdata(firststatement.right, self.coimplication_elim_tag)
            else:
                self.logstep(self.log_coimplication_elim.format(self.coimplication_elim_name.upper(), str(secondstatement.right), str(secondstatement)))
                newcomment = self.iscomplete(secondstatement.right, comment)
                self.lines.append(
                    [
                        secondstatement.right, 
                        self.level, 
                        self.currentproofid, 
                        self.coimplication_elim_name, 
                        self.reflines(first, second), 
                        '', 
                        newcomment,
                        self.linetype_notransformationrule
                    ]
                ) 
                self.appendproofdata(secondstatement.right, self.coimplication_elim_tag)
                
    def coimplication_intro(self, first: int, second: int, comment: str = ''):
        """Derive a item in a proof using the if and only if symbol.
        
        Parameters:
            first: The first item number to obtain an implication going in one direction.
            second: The second item number to obtain an implication going in the other direction.
            comment: comment entered by the user for this line.

        Examples:
            The following is a simple example of how the coimplication introduction rule works.

            >>> from altrea.boolean import Implies, Wff, Iff
            >>> from altrea.rules import Proof
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
        if self.canproceed():
            if not self.checkintelimrule(self.coimplication_intro_tag):
                self.logstep(self.log_notransformationrule.format(self.coimplication_intro_name.upper()))
                self.stopproof(self.stopped_notransformationrule, self.blankstatement, self.coimplication_intro_name, '', '', comment)
            elif not self.checkline(first):
                self.logstep(self.log_nosuchline.format(self.coimplication_intro_name.upper(), str(first)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.coimplication_intro_name, str(first), '', comment)
            elif not self.checkline(second):
                self.logstep(self.log_nosuchline.format(self.coimplication_intro_name.upper(), str(second)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.coimplication_intro_name, str(second), '', comment)
            elif not self.checklinescope(first):
                self.logstep(self.log_linescope.format(self.coimplication_intro_name.upper(), str(first)))
                self.stopproof(self.stopped_linescope, self.blankstatement, self.coimplication_intro_name, str(first), '', comment)
            elif not self.checklinescope(second):
                self.logstep(self.log_linescope.format(self.coimplication_intro_name.upper(), str(second)))
                self.stopproof(self.stopped_linescope, self.blankstatement, self.coimplication_intro_name, str(second), '', comment)
            else:
                firststatement = self.getstatement(first)
                secondstatement = self.getstatement(second)
                if type(firststatement) != Implies:
                    self.logstep(self.log_notimplication.format(self.coimplication_intro_name.upper(), str(firststatement), str(first)))
                    self.stopproof(self.stopped_notimplication, self.blankstatement, self.coimplication_intro_name, str(first), '', comment)
                elif type(secondstatement) != Implies:
                    self.logstep(self.log_notimplication.format(self.coimplication_intro_name.upper(), str(secondstatement), str(second)))
                    self.stopproof(self.stopped_notimplication, self.blankstatement, self.coimplication_intro_name, str(second), '', comment)
                elif not firststatement.left.equals(secondstatement.right):
                    self.logstep(self.log_notsamestatement.format(self.coimplication_intro_name.upper(), str(firststatement.left), str(secondstatement.right)))
                    self.stopproof(self.stopped_notsamestatement, self.blankstatement, self.coimplication_intro_name, self.reflines(first, second), '', comment)
                elif not firststatement.right.equals(secondstatement.left):
                    self.logstep(self.log_notsamestatement.format(self.coimplication_intro_name.upper(), str(firststatement.right), str(secondstatement.left)))
                    self.stopproof(self.stopped_notsamestatement, self.blankstatement, self.coimplication_intro_name, self.reflines(second, first), '', comment)

        # If no errors, perform task
        if self.canproceed():
            newstatement = Iff(firststatement.left, firststatement.right)
            self.logstep(self.log_coimplication_intro.format(self.coimplication_intro_name.upper(), str(newstatement), str(firststatement.left), str(firststatement.right)))
            newcomment = self.iscomplete(newstatement, comment)
            self.lines.append(
                [
                    newstatement, 
                    self.level, 
                    self.currentproofid, 
                    self.coimplication_intro_name, 
                    self.reflines(first, second), 
                    '',
                    newcomment,
                    self.linetype_notransformationrule
                ]
            )   
            self.appendproofdata(newstatement, self.coimplication_intro_tag)

    def conjunction_elim(self, line: int, side: str = 'left', comment: str = ''):
        """One of the conjuncts, either the left side or the right side, is derived from a conjunction.
        
        Parameters:
            line: The line number of the conjunction to be split.
            side: The side, either left or right, from which the conjunct will be derived.
            comment: Optional user comment for the line.

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

            The comment on lines 2 and 3, "PARTIAL COMPLETION" and "COMPLETE" were generated
            by AltRea.  This comment column can be used both by the user and AltRea to
            provide a message about the proof.

            >>> from altrea.boolean import And, Implies, Iff, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> prf.setlogic('C')
            >>> prf.goal(Iff(And(A, B), And(B, A)))
            >>> prf.hypothesis(And(A, B), comment="Don't use `addhypothesis` to start the subproof.")
            >>> prf.conjunction_elim(1, comment='The left side is the default.')
            >>> prf.conjunction_elim(1, side='right', comment='Now do the right side.')
            >>> prf.conjunction_intro(3, 2, comment='Put the conjuncts on the opposite side.')
            >>> prf.implication_intro()
            >>> prf.hypothesis(And(B, A))
            >>> prf.conjunction_elim(6)
            >>> prf.conjunction_elim(6, side='right')
            >>> prf.conjunction_intro(8, 7, comment='The order is reversed.')
            >>> prf.implication_intro()
            >>> prf.coimplication_intro(10, 5, comment='The order will be like the first statement on line 10.')
            >>> prf.coimplication_intro(5, 10, comment='Now it works using line 5 first.')
            >>> showproof(prFalsehood, latex=0)
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
        if self.canproceed():
            if not self.checkintelimrule(self.conjunction_elim_tag):
                self.logstep(self.log_notransformationrule.format(self.conjunction_elim_name.upper()))
                self.stopproof(self.stopped_notransformationrule, self.blankstatement, self.conjunction_elim_name, '', '', comment)
            elif not self.checkline(line):
                self.logstep(self.log_nosuchline.format(self.conjunction_elim_name.upper(), str(line)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.conjunction_elim_name, str(line), '', comment)
            elif not self.checklinescope(line):
                self.logstep(self.log_linescope.format(self.conjunction_elim_name.upper(), str(line)))
                self.stopproof(self.stopped_linescope, self.blankstatement, self.conjunction_elim_name, str(line), '', comment)
            else:
                statement = self.getstatement(line)
                if type(statement) != And:
                    self.logstep(self.log_notconjunction.format(self.conjunction_elim_name.upper(), str(statement), str(line)))
                    self.stopproof(self.stopped_notconjunction, self.blankstatement, self.conjunction_elim_name, str(line), '', comment)
                elif side not in ['left', 'right']:
                    self.logstep(self.log_sidenotselected.format(self.conjunction_elim_name.upper(), side))
                    self.stopproof(self.stopped_sidenotselected, self.blankstatement, self.conjunction_elim_name, str(line), '', comment)

        # If no errors, perform the task
        if self.canproceed():
            if side == 'left':
                conjunct = statement.left
            else:
                conjunct = statement.right
            self.logstep(self.log_conjunction_elim.format(self.conjunction_elim_name.upper(), str(conjunct), str(statement), str(line)))
            newcomment = self.iscomplete(conjunct, comment)
            self.lines.append(
                [
                    conjunct, 
                    self.level, 
                    self.currentproofid, 
                    self.conjunction_elim_name, 
                    str(line), 
                    '',
                    newcomment,
                    self.linetype_notransformationrule
                ]
            )   
            self.appendproofdata(conjunct, self.conjunction_elim_tag)
                
    def conjunction_intro(self, first: int, second: int, comment: str = ''):
        """The statement at first line number is joined as a conjunct to the statement at the second
        line number.  These these two conjuncts for a conjunction with the first conjunct on the
        left side and the second on the right side.

        Parameters:
            first: The line number of the first conjunct on the left side.
            second: The line number of the second conjunct on the right side.
            comment: Optional comment that a user may enter.

        Exception:
            Starting with two named well-formed formulas (Wff), "A" and "B" one can start a proof p.
            This example will derive from those two statements given as premises in line 1 and 2
            the statement displayed as "A & B" on line 3.  The comment on line 3 shows that
            the proof is complete.  Also on line 3 is information on the lines (1 and 2) that were
            referenced to justify the presence in the proof.

            >>> from altrea.boolean import And, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof, showlines
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> C = Wff('C')
            >>> prf.setlogic('C')
            >>> prf.goal(And(A, B))
            >>> prf.premise(A)
            >>> prf.premise(B)
            >>> prf.conjunction_intro(1, 2)
            >>> showproof(prFalsehood, latex=0)
                Item                   Reason   Comment
            0  A & B                     GOAL
            1      A                  Premise
            2      B                  Premise
            3  A & B  1, 2, Conjunction Intro  COMPLETE

            This example shows that an obvious result can be derived by letting the first and second lines be the same.  

            >>> from altrea.boolean import And, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof, showlines
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> C = Wff('C')
            >>> prf.setlogic('C')
            >>> prf.goal(And(A, A))
            >>> prf.premise(A)
            >>> prf.conjunction_intro(1, 1)
            >>> showproof(prFalsehood, latex=0)
                Item                   Reason   Comment
            0  A & A                     GOAL
            1      A                  Premise
            2  A & A  1, 1, Conjunction Intro  COMPLETE

            In the previous examples all of the statements were on level 0, the same level.
            Both the and_into and conjunction_elim require that the statenents they use be on the 
            same level as the current level.  However, one can use statements from a
            lower level by reiterateerating then using the reiterate rule.  Here is an example of that.
        """

        # Look for errors
        if self.canproceed():
            if not self.checkintelimrule(self.conjunction_intro_tag):
                self.logstep(self.log_notransformationrule.format(self.coimplication_intro_name.upper()))
                self.stopproof(self.stopped_notransformationrule, self.blankstatement, self.conjunction_intro_name, '', '', comment)
            elif not self.checkline(first):
                self.logstep(self.log_nosuchline.format(self.conjunction_intro_name.upper(), str(first)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.conjunction_intro_name, str(first), '', comment)
            elif not self.checkline(second):
                self.logstep(self.log_nosuchline.format(self.conjunction_intro_name.upper(), str(second)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.conjunction_intro_name, str(second), '', comment)
            elif not self.checklinescope(first):
                self.logstep(self.log_linescope.format(self.conjunction_intro_name.upper(), str(first)))
                self.stopproof(self.stopped_linescope, self.blankstatement, self.conjunction_intro_name, str(first), '', comment) 
            elif not self.checklinescope(second):
                self.logstep(self.log_linescope.format(self.conjunction_intro_name.upper(), str(second)))
                self.stopproof(self.stopped_linescope, self.blankstatement, self.conjunction_intro_name, str(second), '', comment)
                    
        # If no errors, perform task
        if self.canproceed():
            firstconjunct = self.getstatement(first)
            secondconjunct = self.getstatement(second)
            andstatement = And(firstconjunct, secondconjunct)
            self.logstep(self.log_conjunction_intro.format(self.conjunction_intro_name.upper(), str(andstatement), str(firstconjunct), str(first), str(secondconjunct), str(second)))
            newcomment = self.iscomplete(andstatement, comment)
            self.lines.append(
                [
                    andstatement, 
                    self.level, 
                    self.currentproofid, 
                    self.conjunction_intro_name, 
                    self.reflines(first, second), 
                    '',
                    newcomment,
                    self.linetype_notransformationrule
                ]
            ) 
            self.appendproofdata(andstatement, self.conjunction_intro_tag)

    def disjunction_elim(self, disjunction_line: int, left_implication_line: int, right_implication_line: int, comment: str = ''):
        """This rule take a disjunction and two implications with antecedents on each side of the disjunction.
        If the two implications reach the same conclusion, then that conclusion may be derived.
        
        Parameters:
            disjunction: The line number where the disjunction is an item.
            left_implication: The line number of the implication starting with the left side of the disjunction.
            right_implication: The line number of the implication starting with the right side of the disjunction.
            comment: Optional comment may be entered here.

        Examples:
            The first example shows that a trivial result can be derived.  If we have A or A and we want to derive just A,
            we can generate an implication by starting a subordinate proof with A as the hypothesis.  We can then
            close that proof with an implication introduction.  Since A is on both sides of the disjunction,
            we can refer to the same subordinate proof twice in the use of disjunction elimination.

            >>> from altrea.boolean import Or, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof, showlines
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> C = Wff('C')
            >>> prf.setlogic('C')
            >>> prf.goal(A)
            >>> prf.premise(Or(A, A))
            >>> prf.hypothesis(A)
            >>> prf.implication_intro()
            >>> prf.disjunction_elim(1, 3, 3)
            >>> showproof(prFalsehood, latex=0)
                Item                     Reason   Comment
            0      A                       GOAL
            1  A | A                    Premise
            2  A __|                 Hypothesis
            3  A > A     2-2, Implication Intro
            4      A  1, 3, 3, Disjunction Elim  COMPLETE

            The next example sets up a more typical situation for disjunction elimination.  

            It also illustrates the `showlines` display.  This display shows what is in the lines of a proof.
            The `showproof` display illustrated in the above example uses a natural deduction display style.

            >>> from altrea.boolean import Or, Implies, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof, showlines
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> C = Wff('C')
            >>> prf.setlogic('C')
            >>> prf.goal(A)
            >>> prf.premise(Implies(B, A))
            >>> prf.premise(Implies(C, A))
            >>> prf.premise(Or(B, C))
            >>> prf.hypothesis(B)
            >>> prf.reiterate(1)
            >>> prf.implication_elim(4, 5)
            >>> prf.implication_intro()
            >>> prf.hypothesis(C)
            >>> prf.reiterate(2)
            >>> prf.implication_elim(8, 9)
            >>> prf.implication_intro()
            >>> prf.disjunction_elim(3, 7, 11)
            >>> showlines(prFalsehood, latex=0)
               Statement  Level  Proof               Rule     Lines Proofs   Comment
            C          A      0      0               GOAL
            1      B > A      0      0            Premise
            2      C > A      0      0            Premise
            3      B | C      0      0            Premise
            4          B      1      1         Hypothesis
            5      B > A      1      1        Reiteration         1
            6          A      1      1   Implication Elim      4, 5
            7      B > A      0      0  Implication Intro              4-6
            8          C      1      2         Hypothesis
            9      C > A      1      2        Reiteration         2
            10         A      1      2   Implication Elim      8, 9
            11     C > A      0      0  Implication Intro             8-10
            12         A      0      0   Disjunction Elim  3, 7, 11         COMPLETE
        """

        # Look for errors.
        if self.canproceed():
            if not self.checkintelimrule(self.disjunction_elim_tag):
                self.logstep(self.log_notransformationrule.format(self.disjunction_elim_name.upper()))
                self.stopproof(self.stopped_notransformationrule, self.blankstatement, self.disjunction_elim_name, '', '', comment)
            elif not self.checkline(disjunction_line):
                self.logstep(self.log_nosuchline.format(self.disjunction_elim_name.upper(), str(disjunction_line)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.disjunction_elim_name, str(disjunction_line), '', comment)
            elif not self.checkline(left_implication_line):
                self.logstep(self.log_nosuchline.format(self.disjunction_elim_name.upper(), str(left_implication_line)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.disjunction_elim_name, str(left_implication_line), '', comment)
            elif not self.checkline(right_implication_line):
                self.logstep(self.log_nosuchline.format(self.disjunction_elim_name.upper(), str(right_implication_line)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.disjunction_elim_name, str(right_implication_line), '', comment)
            elif not self.checklinescope(disjunction_line):
                self.logstep(self.log_linescope.format(self.disjunction_elim_name.upper(), str(disjunction_line)))
                self.stopproof(self.stopped_linescope, self.blankstatement, self.disjunction_elim_name, str(disjunction_line), '', comment)
            elif not self.checklinescope(left_implication_line):
                self.logstep(self.log_linescope.format(self.disjunction_elim_name.upper(), str(left_implication_line)))
                self.stopproof(self.stopped_linescope, self.blankstatement, self.disjunction_elim_name, str(left_implication_line), '', comment)
            elif not self.checklinescope(right_implication_line):
                self.logstep(self.log_linescope.format(self.disjunction_elim_name.upper(), str(right_implication_line)))
                self.stopproof(self.stopped_linescope, self.blankstatement, self.disjunction_elim_name, str(right_implication_line), '', comment)
            else:
                disjunction = self.getstatement(disjunction_line)
                left_implication = self.getstatement(left_implication_line)
                right_implication = self.getstatement(right_implication_line)
                if type(disjunction) != Or:
                    self.logstep(self.log_notdisjunction.format(self.disjunction_elim_name.upper(), str(disjunction), str(disjunction_line)))
                    self.stopproof(self.stopped_notdisjunction, self.blankstatement, self.disjunction_elim_name, str(disjunction_line), '', comment)
                elif type(left_implication) != Implies:
                    self.logstep(self.log_notimplication.format(self.disjunction_elim_name.upper(), str(left_implication), str(left_implication_line)))
                    self.stopproof(self.stopped_notimplication, self.blankstatement, self.disjunction_elim_name, str(left_implication_line), '', comment)
                elif type(right_implication) != Implies:
                    self.logstep(self.log_notimplication.format(self.disjunction_elim_name.upper(), str(right_implication), str(right_implication_line)))
                    self.stopproof(self.stopped_notimplication, self.blankstatement, self.disjunction_elim_name, str(right_implication_line), '', comment)
                elif not right_implication.right.equals(left_implication.right):
                    self.logstep(self.log_notsamestatement.format(self.disjunction_elim_name.upper(), str(left_implication.right), str(right_implication.right)))
                    self.stopproof(self.stopped_notsamestatement, self.blankstatement, self.disjunction_elim_name, self.reflines(left_implication_line, right_implication_line), '', comment)

        # With no errors, perform task.
        if self.canproceed():
            self.logstep(self.log_disjunction_elim.format(self.disjunction_elim_name.upper(), str(right_implication.left), str(disjunction), str(disjunction_line)))
            newcomment = self.iscomplete(right_implication.right, comment)
            self.lines.append(
                [
                    right_implication.right, 
                    self.level, 
                    self.currentproofid, 
                    self.disjunction_elim_name, 
                    self.reflines(disjunction_line, left_implication_line, right_implication_line),
                    '',
                    newcomment,
                    self.linetype_notransformationrule
                ]
            )    
            self.appendproofdata(right_implication.left, self.disjunction_elim_tag)

    def disjunction_intro(self, 
                 line: int,
                 left: And | Or | Not | Implies | Iff | Wff | Falsehood | Truth = None,
                 right: And | Or | Not | Implies | Iff | Wff | Falsehood | Truth = None,  
                 comment: str = ''):
        """The newdisjunct statement and the statement at the line number become a disjunction.
        
        Parameters:
            line: The line number of the statement that will be the other disjunct.
            left: A statement that will be used in the disjunction on the left side of the one
                referenced by the line.
            right: A state that will be used in the disjunction on the right side of the one
                referenced by the line.
 

        Examples:
            One can place the new statement on either the left side or the right side of the
            referenced statement.  The first example shows how this is done for the right side.

            >>> from altrea.boolean import Or, Implies, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof, showlines
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> C = Wff('C')
            >>> prf.setlogic('C')
            >>> prf.goal(Or(A, B))
            >>> prf.premise(A)
            >>> prf.disjunction_intro(1, right=B)
            >>> showproof(prFalsehood, latex=0)
                Item                Reason   Comment
            0  A | B                  GOAL
            1      A               Premise
            2  A | B  1, Disjunction Intro  COMPLETE

            The second example shows how this is done for the left side.

            >>> from altrea.boolean import Or, Implies, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof, showlines
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> C = Wff('C')
            >>> prf.setlogic('C')
            >>> prf.goal(Or(A, B))
            >>> prf.premise(B)
            >>> prf.disjunction_intro(1, left=A)
            >>> showproof(prFalsehood, latex=0)
                Item                Reason   Comment
            0  A | B                  GOAL
            1      B               Premise
            2  A | B  1, Disjunction Intro  COMPLETE
        """

        # Look for errors
        if self.canproceed():
            if not self.checkintelimrule(self.disjunction_intro_tag):
                self.logstep(self.log_notransformationrule.format(self.disjunction_intro_name.upper()))
                self.stopproof(self.stopped_notransformationrule, self.blankstatement, self.disjunction_intro_name, '', '', comment)
            elif left is not None and self.checkstring(left):
                self.logstep(self.log_string.format(self.disjunction_intro_name.upper(), left))
                self.stopproof(self.stopped_string, self.blankstatement, self.disjunction_intro_name, str(line), '', comment)
            elif right is not None and self.checkstring(right):
                self.logstep(self.log_string.format(self.disjunction_intro_name.upper(), right))
                self.stopproof(self.stopped_string, self.blankstatement, self.disjunction_intro_name, str(line), '', comment)
            elif not self.checkline(line):
                self.logstep(self.log_nosuchline.format(self.disjunction_intro_name.upper(), str(line)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.disjunction_intro_name, str(line), '', comment)
            elif not self.checklinescope(line):
                self.logstep(self.log_linescope.format(self.disjunction_intro_name.upper(), str(line)))
                self.stopproof(self.stopped_linescope, self.blankstatement, self.disjunction_intro_name, str(line), '', comment)
            else:
                statement = self.getstatement(line)
                if left is None and right is None:
                    self.logstep(self.log_novaluepassed.format(self.disjunction_intro_name.upper()))
                    self.stopproof(self.stopped_novaluepassed, self.blankstatement, self.disjunction_intro_name, str(line), '', comment)

        # If no errors, perform task
        if self.canproceed():
            if left is None:
                disjunction = Or(statement, right)
                self.logstep(self.log_disjunction_intro.format(self.disjunction_intro_name.upper(), str(disjunction), str(statement), str(line), 'right', str(left)))
            elif right is None:
                disjunction = Or(left, statement)
                self.logstep(self.log_disjunction_intro.format(self.disjunction_intro_name.upper(), str(disjunction), str(statement), str(line), 'left', str(left)))
            newcomment = self.iscomplete(disjunction, comment)
            self.lines.append(
                [
                    disjunction, 
                    self.level, 
                    self.currentproofid, 
                    self.disjunction_intro_name, 
                    str(line), 
                    '',
                    newcomment,
                    self.linetype_notransformationrule
                ]
            )    
            self.appendproofdata(disjunction, self.disjunction_intro_tag)
                               
    def goal(self,
                goal: And | Or | Not | Implies | Iff | Wff | Falsehood | Truth, 
                comment: str = ''):
        """Add a goal to the proof.  More than one goal can be assigned although generally
        only one goal is used and only one is needed.  Think of multiple goals as the
        conjuncts to a single goal.
        
        Parameters:
            goal: The goal to add to the proof.
            comment: Optional comment for this line of the proof.

        Examples:

            Once one has a Proof object one has to identify which logic one will be using
            and one has to add a goal to it.  These steps are not lines in the proof itself
            and appear in the display under line 0.  However, without a goal or a
            logic attempting to add any other line will stop the proof from starting.  
            
            Below is an example of a trivial proof and a display that can be used on a terminal.  
            The proof is trivial because the goal and the premise are the same.
            Setting `latex=1` in `showproof` would provide a better display in a notebook.

            What is passed to goal is not a string, but an instantiated Wff (well-formed formula).
            An error is returned if a string is passed.  When Q was passed it was not the string 'A'
            but the Wff A.

            >>> from altrea.boolean import Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> prf.setlogic('C')
            >>> prf.goal(A)
            >>> prf.premise(A)
            >>> showproof(prFalsehood, latex=0)
              Item   Reason   Comment
            0    A     GOAL
            1    A  Premise  COMPLETE
        """

        # Look for errors
        if self.canproceed():
            if self.checkstring(goal):
                self.logstep(self.log_string.format(self.goal_name.upper(), goal))
                self.stopproof(self.stopped_string, goal, self.goal_name, 0, 0, comment)
            elif self.logic == '':
                self.logstep(self.log_nologic.format(self.goal_name.upper()))
                self.stopproof(self.stopped_nologic, self.blankstatement, self.goal_name, 0, 0, comment)

        # If no errors, perform task
        if self.canproceed():
            self.goals.append(str(goal))
            self.goalswff.append(goal)
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
                self.lines[0][self.commentindex] = comment
            elif comment != '':
                self.lines[0][self.commentindex] += ''.join([self.comment_connector, comment])
            self.logstep(self.log_goal.format(self.goal_name.upper(), str(goal)))

    def hypothesis(self, 
                   hypothesis: And | Or | Not | Implies | Iff | Wff | Falsehood | Truth,
                   comment: str = ''):
        """Opens a uniquely identified subproof of items with an hypothesis.
        
        Parameters:
            hypothesis: The hypothesis that starts the block of derived statements.
            comment: Optional comment the user may enter.

        Examples:
        """

        # Look for errors
        if self.canproceed():
            if self.checkstring(hypothesis):
                self.logstep(self.log_string.format(self.hypothesis_name.upper(), hypothesis))
                self.stopproof(self.stopped_string, self.blankstatement, self.hypothesis_name, '', '', comment)
            elif not self.checkhasgoal():
                self.logstep(self.log_nogoal.format(self.hypothesis_name.upper(), str(hypothesis)))
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.hypothesis_name, '', '', comment)

        # If no errors, perform task
        if self.canproceed():
            self.level += 1
            nextline = len(self.lines)
            self.currentproof = [nextline]
            self.currenthypotheses = [nextline]
            self.prooflist.append([self.level, self.currentproof, self.currentproofid, self.currenthypotheses])  
            self.previousproofid = self.currentproofid  
            self.previousproofchain.append(self.currentproofid) 
            self.currentproofid = len(self.prooflist) - 1
            self.logstep(self.log_hypothesis.format(self.hypothesis_name.upper(), str(self.currentproofid), str(hypothesis)))
            newcomment = self.iscomplete(hypothesis, comment)
            self.lines.append(
                [
                    hypothesis, 
                    self.level, 
                    self.currentproofid, 
                    self.hypothesis_name, 
                    '', 
                    '',
                    newcomment,
                    self.linetype_hypothesis
                ]
            )      
            self.appendproofdata(hypothesis, self.hypothesis_tag)       

    def implication_elim(self, first: int, second: int, comment: str = ''):
        """From an implication and its antecedent derive the consequent.
        
        Parameters:
            first: The line number of the first statement. This is either the implication or the antecedent.
            second: The line number of the second statement.  This is either the implication or the antecedent.
            comment: Optional comment the user wishes to enter.  

        Examples:
            Implication elimination is also called "Modus Ponens".  If you have A and A > B then from both of them
            you can derive B.

            >>> from altrea.boolean import Implies, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof, showlines
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> prf = Proof()
            >>> prf.setlogic('C')
            >>> prf.goal(B, comment='Modus Ponens')
            >>> prf.premise(A)
            >>> prf.premise(Implies(A, B))
            >>> prf.implication_elim(1, 2)
            >>> showproof(prFalsehood, latex=0)
                Item                  Reason       Comment
            0      B                    GOAL  Modus Ponens
            1      A                 Premise
            2  A > B                 Premise
            3      B  1, 2, Implication Elim      COMPLETE
        """

        # Look for errors
        if self.canproceed():
            if not self.checkintelimrule(self.implication_elim_tag):
                self.logstep(self.log_notransformationrule.format(self.implication_elim_name.upper()))
                self.stopproof(self.stopped_notransformationrule, self.blankstatement, self.implication_elim_name, '', '', comment)
            elif not self.checkline(first):
                self.logstep(self.log_nosuchline.format(self.implication_elim_name.upper(), str(first)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.implication_elim_name, str(first), '', comment)
            elif not self.checkline(second):
                self.logstep(self.log_nosuchline.format(self.implication_elim_name.upper(), str(first)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.implication_elim_name, str(second), '', comment)
            elif not self.checklinescope(first):
                self.logstep(self.log_linescope.format(self.implication_elim_name.upper(), str(first)))
                self.stopproof(self.stopped_linescope, self.blankstatement, self.implication_elim_name, str(first), '', comment)
            elif not self.checklinescope(second):
                self.logstep(self.log_linescope.format(self.implication_elim_name.upper(), str(second)))
                self.stopproof(self.stopped_linescope, self.blankstatement, self.implication_elim_name, str(second), '', comment)
            else:
                firststatement = self.getstatement(first)
                secondstatement = self.getstatement(second)
                if type(firststatement) == Implies and type(secondstatement) == Implies:
                    if not firststatement.left.equals(secondstatement) and not secondstatement.left.equals(firststatement):
                        self.logstep(self.log_notantecedent.format(self.implication_elim_name.upper(), str(firststatement), str(secondstatement)))
                        self.logstep(self.log_notantecedent.format(self.implication_elim_name.upper(), str(secondstatement), str(firststatement)))
                        self.stopproof(self.stopped_notantecedent, self.blankstatement, self.implication_elim_name, self.reflines(first, second), '', comment)
                elif type(firststatement) == Implies and not secondstatement.equals(firststatement.left):
                    self.logstep(self.log_notantecedent.format(self.implication_elim_name.upper(), str(firststatement), str(secondstatement)))
                    self.stopproof(self.stopped_notantecedent, self.blankstatement, self.implication_elim_name, self.reflines(first, second), '', comment)
                elif type(secondstatement) == Implies and not firststatement.equals(secondstatement.left):
                    self.logstep(self.log_notantecedent.format(self.implication_elim_name.upper(), str(secondstatement), str(firststatement)))
                    self.stopproof(self.stopped_notantecedent, self.blankstatement, self.implication_elim_name, self.reflines(first, second), '', comment)
                elif type(firststatement) != Implies and type(secondstatement) != Implies:
                    self.logstep(self.log_notmodusponens.format(self.implication_elim_name.upper(), str(firststatement), str(first), str(secondstatement), str(second)))
                    self.stopproof(self.stopped_notmodusponens, self.blankstatement, self.implication_elim_name, self.reflines(first, second), '', comment)

        # If no errors, perform task
        if self.canproceed():    
            if type(firststatement) == Implies and type(secondstatement) == Implies:
                if str(firststatement) == str(secondstatement.left):  
                    statement = secondstatement.right
                    self.logstep(self.log_implication_elim.format(self.implication_elim_name.upper(), str(secondstatement.right), str(secondstatement), str(firststatement)))
                else:
                    statement = firststatement.right
                    self.logstep(self.log_implication_elim.format(self.implication_elim_name.upper(), str(firststatement.right), str(firststatement), str(secondstatement)))
            elif type(firststatement) == Implies:
                statement = firststatement.right
                self.logstep(self.log_implication_elim.format(self.implication_elim_name.upper(), str(firststatement.right), str(firststatement), str(secondstatement)))
            else:
                statement = secondstatement.right
                self.logstep(self.log_implication_elim.format(self.implication_elim_name.upper(), str(secondstatement.right), str(secondstatement), str(firststatement)))
            newcomment = self.iscomplete(statement, comment)
            self.lines.append(
                [
                    statement, 
                    self.level, 
                    self.currentproofid, 
                    self.implication_elim_name, 
                    self.reflines(first, second), 
                    '', 
                    newcomment,
                    self.linetype_notransformationrule
                ]
            )
            self.appendproofdata(statement, self.implication_elim_tag)

    def implication_intro(self, comment: str = ''):
        """From a subproof derive the implication where the antecendent is the hypotheses of subproof joined as conjuncts and the
        consequent is the last line of the proof so far entered.  In the process of deriving the implication as an item of the
        proof, the subproof is closed.
        
        Parameters:
            comment: Optional comment the user wishes to enter.  Also a place where AltRea may display in addition
                stopped and completion messages.
                
        Examples:
            The following simple example is called the "Reflexitiy of Implication".  Note how the subordinate proof
            contained only one line, the hypothesis.  The hypothesis became both the antecedent and the
            consequent of the implication.
        
            >>> from altrea.boolean import Implies, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof, showlines
            >>> A = Wff('A')
            >>> prf = Proof()
            >>> prf.setlogic('C')
            >>> prf.goal(Implies(A, A), comment='Reflexivity of Implication')
            >>> prf.hypothesis(A)
            >>> prf.implication_intro()
            >>> showproof(prFalsehood, latex=0)
                Item                  Reason                     Comment
            0  A > A                    GOAL  Reflexivity of Implication
            1  A __|              Hypothesis
            2  A > A  1-1, Implication Intro                    COMPLETE

            The following is a simple, but important example of how the implication introduction rule works.
            Note that it does not require any premises.  One starts immediately with an hypothesis
            to open a subordinate proof and end at the bottom level with the 
            "Axiom of Conditioned Repetition".  The constraint is that we use a logic
            like "C", the "Classical Propositional" logic.

            This example also illustates the use of comment and how one may change the
            headings of the columns of the proof.

            >>> from altrea.boolean import Implies, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> prf.setlogic('C')
            >>> prf.goal(Implies(A, Implies(B, A)), comment='Axiom of Conditioned Repetition')
            >>> prf.hypothesis(A)
            >>> prf.hypothesis(B)
            >>> prf.reiterate(1)
            >>> prf.implication_intro()
            >>> prf.implication_intro()
            >>> showproof(prFalsehood, latex=0)
                      Item                  Reason                          Comment
            0  A > (B > A)                    GOAL  Axiom of Conditioned Repetition
            1        A __|              Hypothesis
            2    B __|   |              Hypothesis
            3    A   |   |          1, Reiteration
            4    B > A   |  2-3, Implication Intro
            5  A > (B > A)  1-4, Implication Intro                         COMPLETE

            This example shows the rule of distribution.  Like the previous exampeles it does not
            require any premises.
            
            On the Jupyter Lab Terminal the width is truncated
            so the rules are not completely visible.  Running this in a notebook will show the full table. 
            One can then set latex=1 rather than latex-0 on showproof.

            >>> from altrea.boolean import Implies, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof, fitchnotation
            >>> prf = Proof()
            >>> prf.setlogic('C')
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> C = Wff('C')
            >>> prf.goal(Implies(Implies(A, Implies(B, C)), (Implies(Implies(A, B), Implies(A, C)))), comment='rule of distribution')
            >>> prf.hypothesis(Implies(A, Implies(B, C)))
            >>> prf.hypothesis(Implies(A, B))
            >>> prf.hypothesis(A)
            >>> prf.reiterate(1)
            >>> prf.implication_elim(3, 4)
            >>> prf.reiterate(2)
            >>> prf.implication_elim(3, 6)
            >>> prf.implication_elim(5, 7)
            >>> prf.implication_intro()
            >>> prf.implication_intro()
            >>> prf.implication_intro()
            >>> showproof(prFalsehood, latex=0)
                                               Item  ...               Comment
            0   (A > (B > C)) > ((A > B) > (A > C))  ...  rule of distribution
            1                       A > (B > C) __|  ...
            2                         A > B __|   |  ...
            3                         A __|   |   |  ...
            4               A > (B > C)   |   |   |  ...
            5                     B > C   |   |   |  ...
            6                     A > B   |   |   |  ...
            7                         B   |   |   |  ...
            8                         C   |   |   |  ...
            9                         A > C   |   |  ...
            10                (A > B) > (A > C)   |  ...
            11  (A > (B > C)) > ((A > B) > (A > C))  ...              COMPLETE
        """

        # Look for errors
        if self.canproceed():
            if not self.checkintelimrule(self.implication_intro_tag):
                self.logstep(self.log_notransformationrule.format(self.implication_intro_name.upper()))
                self.stopproof(self.stopped_notransformationrule, self.blankstatement, self.implication_intro_name, '', '', comment)
            elif self.currentproofid == 0:
                self.logstep(self.log_closemainproof.format(self.implication_intro_name.upper()))
                self.stopproof(self.stopped_closemainproof, self.blankstatement, self.implication_intro_name, '', '')

        # If no errors, perform task
        if self.canproceed():
            proofid = self.currentproofid
            self.prooflist[self.currentproofid][1].append(len(self.lines)-1)
            self.level -= 1
            level, antecedent, consequent, previousproofid = self.getproof(self.currentproofid)
            self.currentproofid = previousproofid
            self.currentproof = self.prooflist[previousproofid][1]
            if len(self.previousproofchain) > 1:  
                self.previousproofchain.pop(len(self.previousproofchain)-1)  
                self.previousproofid = self.previousproofchain[len(self.previousproofchain)-1] 
            else: 
                self.previousproofchain = [] 
                self.previousproofid = -1  
            implication = Implies(antecedent, consequent)
            self.logstep(self.log_implication_intro.format(self.implication_intro_name.upper(), str(implication), str(proofid)))
            newcomment = self.iscomplete(implication, comment)
            self.lines.append(
                [
                    implication, 
                    self.level, 
                    self.currentproofid, 
                    self.implication_intro_name, 
                    '', 
                    self.refproof(proofid), 
                    newcomment,
                    self.linetype_notransformationrule
                ]
            )   
            self.appendproofdata(implication, self.implication_intro_tag)     

    def necessary_elim(self, line: int, comment: str = ''):
        """Removes the necessary connector from an item.
        
        Parameters:
            line: The line on which the item appears.
            comment: An optional user comment for this line.
            
        Examples:
        
        """

        # Look for errors.
        if self.canproceed():
            if not self.checkintelimrule(self.necessary_elim_tag):
                self.logstep(self.log_notransformationrule.format(self.necessary_elim_name.upper()))
                self.stopproof(self.stopped_notransformationrule, self.blankstatement, self.necessary_elim_name, '', '', comment)
            elif not self.checkline(line):
                self.logstep(self.log_nosuchline.format(self.implication_intro_name.upper(), str(line)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.necessary_elim_name, str(line), '', comment)
            elif not self.checklinescope(line):
                self.logstep(self.log_linescope.format(self.necessary_elim_name.upper(), str(line)))
                self.stopproof(self.stopped_linescope, self.blankstatement, self.necessary_elim_name, str(line), '', comment)
            else:
                statement = self.getstatement(line)
                if type(statement) != Necessary:
                    self.logstep(self.log_notnecessary.format(self.necessary_elim_name.upper(), str(statement), str(line)))
                    self.stopproof(self.stopped_notnecessary, self.blankstatement, self.necessary_elim_name, str(line), '', comment)

        # If no errors, perform task
        if self.canproceed():
            self.logstep(self.log_necessary_elim.format(self.necessary_elim_name.upper(), str(statement.truefalse), str(statement), str(line)))
            newcomment = self.iscomplete(statement.truefalse, comment)
            self.lines.append(
                [
                    statement.truefalse, 
                    self.level, 
                    self.currentproofid, 
                    self.necessary_elim_name, 
                    str(line), 
                    '',
                    newcomment,
                    self.linetype_notransformationrule
                ]
            )      
            self.appendproofdata(statement.truefalse, self.necessary_elim_tag)  

    def necessary_intro(self, comment: str = ''):
        """Closes a strict subproof with a necessary consequence.
        
        Parameters: none
        
        Examples:
        """ 

        # Look for errors.
        if self.canproceed():
            if not self.checkintelimrule(self.necessary_intro_tag):
                self.logstep(self.log_notransformationrule.format(self.necessary_intro_name.upper()))
                self.stopproof(self.stopped_notransformationrule, self.blankstatement, self.necessary_elim_name, '', '', comment)
            elif self.subproof_status != self.subproof_strict:
                self.logstep(self.log_notstrictsubproof.format(self.necessary_elim_name.upper(), self.subproof_status, self.subproof_strict))
                self.stopproof(self.stopped_notstrictsubproof, self.blankstatement, self.necessary_elim_name, '', '', comment)

    def negation_elim(self, first: int, second: int, comment: str = ''):
        """When two statements are contradictory a false line can be derived.
        
        Parameters:
            first: The line number of the first statement.
            second: The line number of the second statement.
            comment: An optional comment for this line.

        Examples:
            >>> from altrea.boolean import And, Not, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> prf.setlogic('C')
            >>> prf.goal(And(A, A))
            >>> prf.premise(A)
            >>> prf.premise(Not(A))
            >>> prf.negation_elim(1, 2)
            >>> showproof(prFalsehood, latex=0)
                Item               Reason Comment
            0  A & A                 GOAL
            1      A              Premise
            2     ~A              Premise
            3      X  1, 2, Negation Elim 
        """
        
        # Look for errors
        if self.canproceed():
            if not self.checkintelimrule(self.negation_elim_tag):
                self.logstep(self.log_notransformationrule.format(self.negation_elim_name.upper()))
                self.stopproof(self.stopped_notransformationrule, self.blankstatement, self.negation_elim_name, '', '', comment)
            elif not self.checkline(first):
                self.logstep(self.log_nosuchline.format(self.negation_elim_name.upper(), str(first)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.negation_elim_name, str(first), '', comment)
            elif not self.checkline(second):
                self.logstep(self.log_nosuchline.format(self.negation_elim_name.upper(), str(second)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.negation_elim_name, str(second), '', comment)
            elif not self.checklinescope(first):
                self.logstep(self.log_linescope.format(self.negation_elim_name.upper(), str(first)))
                self.stopproof(self.stopped_linescope, self.blankstatement, self.negation_elim_name, str(first), '', comment)
            elif not self.checklinescope(second):
                self.logstep(self.log_linescope.format(self.negation_elim_name.upper(), str(second)))
                self.stopproof(self.stopped_linescope, self.blankstatement, self.negation_elim_name, str(second), '', comment)
            else:
                firststatement = self.getstatement(first)
                secondstatement = self.getstatement(second)
                if not Not(firststatement).equals(secondstatement) and not Not(secondstatement).equals(firststatement):
                    self.logstep(self.log_notcontradiction.format(self.negation_elim_name.upper(), str(firststatement), str(first), str(secondstatement), str(second)))
                    self.stopproof(self.stopped_notcontradiction, self.blankstatement, self.negation_elim_name, self.reflines(first, second), '', comment)

        # If no errors, perform task
        if self.canproceed():
            self.logstep(self.log_negation_elim.format(self.negation_elim_name.upper(), str(self.false_name), str(firststatement), str(first), str(secondstatement), str(second)))
            newcomment = self.iscomplete(self.false_name, comment)
            self.lines.append(
                [
                    self.false_name, 
                    self.level, 
                    self.currentproofid, 
                    self.negation_elim_name, 
                    self.reflines(first, second), 
                    '',
                    newcomment,
                    self.linetype_notransformationrule
                ]
            )      
            self.appendproofdata(self.false_name, self.negation_elim_tag)    

    def negation_intro(self, comment: str = ''):
        """This rule closes a subordinate proof that ends in a contradiction by negating the hypotheses of
        the subordinate proof. 

        Parameters:
            comment: Optional comment the user may provide.
        
        Examples:
            The following example is known as modus tollens.
            
            >>> from altrea.boolean import Implies, Not, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> prf = Proof()
            >>> prf.setlogic('C')
            >>> prf.goal(Not(A), comment='Modus Tollens')
            >>> prf.premise(Implies(A, B))
            >>> prf.premise(Not(B))
            >>> prf.hypothesis(A)
            >>> prf.reiterate(1)
            >>> prf.implication_elim(3, 4)
            >>> prf.reiterate(2)
            >>> prf.negation_elim(5, 6)
            >>> prf.negation_intro()
            >>> showproof(prFalsehood, latex=0)
                    Item                  Reason        Comment
            0         ~A                    GOAL  Modus Tollens
            1      A > B                 Premise
            2         ~B                 Premise
            3      A __|              Hypothesis
            4  A > B   |          1, Reiteration
            5      B   |  3, 4, Implication Elim
            6     ~B   |          2, Reiteration
            7      X   |     5, 6, Negation Elim
            8         ~A     3-7, Negation Intro       COMPLETE
        """

        # Look for errors
        if self.canproceed():
            if not self.checkintelimrule(self.negation_intro_tag):
                self.logstep(self.log_notransformationrule.format(self.negation_intro_name.upper()))
                self.stopproof(self.stopped_notransformationrule, self.blankstatement, self.negation_intro_name, '', '', comment)
            elif self.currentproofid == 0:
                self.logstep(self.log_closemainproof.format(self.negation_intro_name.upper()))
                self.stopproof(self.stopped_closemainproof, self.blankstatement, self.negation_intro_name, '', '', comment)
            elif str(self.lines[len(self.lines)-1][self.statementindex]) != str(self.false_name):
                self.logstep(self.log_notfalse.format(self.negation_intro_name.upper(), str(self.lines[len(self.lines)-1][self.statementindex]), str(len(self.lines)-1)))
                self.stopproof(self.stopped_notfalse, self.blankstatement, self.negation_intro_name, str(len(self.lines)-1), '', comment)
        
        # If no errors, perform task
        if self.canproceed():
            proofid = self.currentproofid
            self.prooflist[self.currentproofid][1].append(len(self.lines)-1)
            level, antecedent, consequent, previousproofid = self.getproof(self.currentproofid)
            self.level -= 1
            self.currentproofid = previousproofid
            self.currentproof = self.prooflist[previousproofid][1]
            if len(self.previousproofchain) > 1:  
                self.previousproofchain.pop(len(self.previousproofchain)-1)  
                self.previousproofid = self.previousproofchain[len(self.previousproofchain)-1] 
            else: 
                self.previousproofchain = [] 
                self.previousproofid = -1  
            negation = Not(antecedent)
            self.logstep(self.log_negation_intro.format(self.negation_intro_name.upper(), str(negation), str(antecedent), str(proofid)))
            newcomment = self.iscomplete(negation, comment)
            self.lines.append(
                [
                    negation, 
                    self.level, 
                    self.currentproofid, 
                    self.negation_intro_name, 
                    '', 
                    self.refproof(proofid), 
                    newcomment,
                    self.linetype_notransformationrule
                ]
            )  
            self.appendproofdata(negation, self.negation_intro_tag)

    def premise(self, 
                   premise: And | Or | Not | Implies | Iff | Wff | Falsehood | Truth, 
                   comment: str = ''):
        """Add a premise to the proof.  Although a proof does not require a premise one or more of
        them may be provided.  
        
        Parameters:
            premise: The premise to add to the proof.
            comment: Optional comment for this line of the proof.
        """

        # Look for errors
        if self.canproceed():
            if self.checkstring(premise):
                self.logstep(self.log_string.format(self.premise_name.upper(), premise))
                self.stopproof(self.stopped_string, self.blankstatement, self.premise_name, '', '', comment)
            elif not self.checkhasgoal():
                self.logstep(self.log_nogoal.format(self.premise_name.upper(), str(premise)))
                self.stopproof(self.stopped_nogoal, self.blankstatement, self.premise_name, '', '', comment)

        # If no errors, perform task
        if self.canproceed():
            self.premises.append(premise)
            nextline = len(self.lines)
            self.prooflist[self.currentproofid][3].append(nextline)
            self.logstep(self.log_premise.format(self.premise_name.upper(), str(premise)))
            newcomment = self.iscomplete(premise, comment)
            self.lines.append(
                [
                    premise, 
                    0, 
                    self.currentproofid, 
                    self.premise_name, 
                    '', 
                    '', 
                    newcomment,
                    self.linetype_premise
                ]
            )
            self.appendproofdata(premise, self.premise_tag)
       
    def reiterate(self, line: int, comment: str = ''):
        """An item that already exists in the proof but is in a different subproof may be accessed using
        this function provided the location of the item meets certain conditions.  In general the
        condition is that the item is in a proof for which the current proof is a subproof, subsubproof, or deeper.

        Parameter:
            line: The line number of the statement.

        Example:
            In this example in order to use
            >>> from altrea.boolean import Not, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof, showlines
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> prf.setlogic('C')
            >>> prf.goal(Not(Not(A)))
            >>> prf.premise(A)
            >>> prf.hypothesis(Not(A))
            >>> prf.reiterate(1)
            >>> prf.negation_intro()
            >>> showproof(prFalsehood, latex=0)
                 Item               Reason   Comment
            0     ~~A                 GOAL
            1       A              Premise
            2  ~A __|           Hypothesis
            3   A   |       1, Reiteration
            4     ~~A  2-3, Negation Intro  COMPLETE
        """
        
        # Look for errors
        if self.canproceed():
            if not self.checkline(line):
                self.logstep(self.log_nosuchline.format(self.reiterate_name.upper(), str(line)))
                self.stopproof(self.stopped_nosuchline, self.blankstatement, self.reiterate_name, str(line), '', comment)
            else:
                proofid, statement = self.getproofidstatement(line)
                if not proofid in self.previousproofchain:
                    self.logstep(self.log_notreiteratescope.format(self.reiterate_name.upper(), str(line)))
                    self.stopproof(self.stopped_notreiteratescope, self.blankstatement, self.reiterate_name, str(line), '', comment)
                if self.subproof_status == self.subproof_strict and type(statement) != Necessary:
                    self.logstep(self.log_notnecessary.format(self.reiterate_name.upper(), str(statement), str(line)))
                    self.stopproof(self.stopped_notnecessary, self.blankstatement, self.reiterate_name, str(line), '', comment)

        # If no errors, perform task
        if self.canproceed():
            self.logstep(self.log_reiterate.format(self.reiterate_name.upper(), str(statement), str(line), str(self.currentproofid)))
            newcomment = self.iscomplete(statement, comment)
            self.lines.append(
                [
                    statement, 
                    self.level, 
                    self.currentproofid, 
                    self.reiterate_name, 
                    str(line), 
                    '',
                    newcomment,
                    ''
                ]
            )  
            self.appendproofdata(statement, self.reiterate_tag)

    def setlogic(self, logic: str):
        """Sets the logic for the proof.
        
        Parameters:
            logic: The code identifying the logic.
            
        Examples:
            If you do not know which logics are avaiable, you may run `displaylogics()`.
            A list of the available logics will be displayed.

            If a logic has been incorrectly set an error message may appear
            such as in the following example.
            
            >>> from altrea.boolean import Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof
            >>> p = Proof()
            >>> A = Wff('A')
            >>> p.setlogic('X')
            >>> p.goal(A)
            >>> showproof(p, latex=0)
              Item Reason                                    Comment
            0              STOPPED: This logic has not been defined.
            """
        
        self.logic = logic
        try:
            database, description = altrea.data.getlogic(logic)
        except TypeError:
            database = self.label_nodatabase
            description = self.label_nodescription
        self.logicdatabase = database
        self.logicdescription = description
        self.logstep(self.log_logicdescription.format(self.setlogic_name.upper(), logic, self.logicdescription, self.logicdatabase))
        self.proofdata[0].append(logic)
        try:
            self.logicaxioms = altrea.data.getaxioms(logic)
        except TypeError:
            self.logicaxioms = []
        try:
            self.logicdefinitions = altrea.data.getdefinitions(logic)
        except TypeError:
            self.logicaxioms = []
        if database != 'No Database':
            try:
                intelimrules = altrea.data.getintelimrules(logic)
            except:
                self.logstep(f'SETLOGIC: "{logic}" could not retrieve its intelim rule permissions.')
            else:
                if len(intelimrules) > 0:
                    self.logicintelimrules = []
                    for i in intelimrules:
                        if i[0] != '':
                            self.logicintelimrules.append((i[0], eval(i[1])))
                        else:
                            self.logicintelimrules.append(i)
            try: 
                connectors = altrea.data.getconnectors(logic)
            except:
                self.logstep(f'SETLOGIC: "{logic}" could not retrieve its connector permissions.')
            else:
                if len(connectors) > 0:
                    self.connectors = []
                    for i in connectors:
                        if i[0] != '':
                            self.logicconnectors.append((eval(i[0], self.objectdictionary), i[0], i[1]))
                        else:
                            self.logicconnectors.append(i)
        else:
            self.logicintelimrules = [
                (self.coimplication_elim_tag, self.coimplication_elim_name),
                (self.coimplication_intro_tag, self.coimplication_intro_name),
                (self.conjunction_elim_tag, self.conjunction_elim_name),
                (self.conjunction_intro_tag, self.conjunction_intro_name),
                (self.disjunction_elim_tag, self.disjunction_elim_name),
                (self.disjunction_intro_tag, self.disjunction_intro_name),
                (self.implication_elim_tag, self.implication_elim_name),
                (self.implication_intro_tag, self.implication_intro_name),
                (self.necessary_elim_tag, self.necessary_elim_name),
                (self.necessary_intro_tag, self.necessary_intro_name),
                (self.negation_elim_tag, self.negation_elim_name),
                (self.negation_intro_tag, self.negation_intro_name),
                (self.possibly_elim_tag, self.possibly_elim_name),
                (self.possibly_intro_tag, self.possibly_intro_name),
            ]
            self.logicconnectors = [

            ]

    def truefalse(self, name: str, latex: str = ''):
        newtruefalse = TrueFalse(name, latex)
        self.objectdictionary.update({name: newtruefalse})
        self.letters.append([newtruefalse, name])
        howmany = len(self.letters)
        self.logstep(f'WFF: The letter "{name}" for a generic well-formed formula has been defined making {howmany} so far.')
        return newtruefalse

    def truth(self, name: str, latex: str = ''):
        newtruth = Truth(name, latex)
        self.objectdictionary.update({name: newtruth})
        self.truths.append([newtruth, name])
        howmany = len(self.truths)
        self.logstep(f'TRUTH: The letter "{newtruth.name}" (latex: "{newtruth.latexname}") for a generic truth formula has been defined making {howmany} so far.')
        return newtruth

    def falsehood(self, name: str, latex: str = ''):
        newfalsehood = Falsehood(name, latex)
        self.objectdictionary.update({name: newfalsehood})
        self.falsehoods.append([newfalsehood, name])
        howmany = len(self.falsehoods)
        self.logstep(f'TRUTH: The letter "{newfalsehood.name}" (latex: "{newfalsehood.latexname}") for a generic falsehood formula has been defined making {howmany} so far.')
        return newfalsehood
