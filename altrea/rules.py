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
    >>> from myaltrea.wffs import And, Or, Not, Implies, Iff, Wff
    >>> import myaltrea.rules
"""

import pandas

from altrea.wffs import (
    And,
    Or,
    Not,
    Implies,
    Iff,
    Wff,
    Necessary,
    Possibly,
    Proposition,
    Falsehood,
    Truth,
    ConclusionPremises,
    Definition,
    ConsistentWith,
    StrictIff,
    StrictImplies,
)
import altrea.data


class Proof:
    """
    This class contains methods to construct and verify proofs in
    in various truth functional logics.

    The following labels should not be changed.  They are not displayed but help control
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
    subproofstatusindex = 8
    lowestlevel = 0
    acceptedtypes = ([And, Or, Not, Implies, Iff, Wff, Falsehood, Truth],)
    coimplication_intro_tag = "COI"
    coimplication_elim_tag = "COE"
    conjunction_intro_tag = "CI"
    conjunction_elim_tag = "CE"
    disjunction_intro_tag = "DI"
    disjunction_elim_tag = "DE"
    explosion_tag = "X"
    hypothesis_tag = "H"
    implication_intro_tag = "II"
    implication_intro_strict_tag = "IIS"
    implication_elim_tag = "IE"
    necessary_intro_tag = "NEI"
    necessary_elim_tag = "NEE"
    negation_intro_tag = "NI"
    negation_elim_tag = "NE"
    possibly_intro_tag = "POI"
    possibly_elim_tag = "POE"
    premise_tag = "P"
    reiterate_tag = "R"
    substitution_tag = "S"
    blankstatement = ""

    subproof_strict = "STRICT"
    subproof_normal = ""

    complete = "COMPLETE"
    partialcompletion = "PARTIAL COMPLETION"
    stopped = "STOPPED"
    vacuous = "VACUOUS"
    contradicted = "GOAL CONTRADICTED"

    color_available = '\\color{green}'
    color_unavailable = '\\color{red}'
    color_conclusion = '\\color{blue}'

    # The following names may be changed.  They are used for display purposes.
    # One could redefine them just after instantiating an instance of the Proof class.

    # The first set of strings provide names of natural deduction function  calls that are displayed in reports.

    addhypothesis_name = "Add Hypothesis"
    axiom_name = "Axiom"
    definition_name = "Definition"
    coimplication_intro_name = "Coimplication Intro"
    coimplication_elim_name = "Coimplication Elim"
    conjunction_intro_name = "Conjunction Intro"
    conjunction_elim_name = "Conjunction Elim"
    disjunction_intro_name = "Disjunction Intro"
    disjunction_elim_name = "Disjunction Elim"
    goal_name = "GOAL"
    hypothesis_name = "Hypothesis"
    implication_intro_name = "Implication Intro"
    implication_intro_strict_name = "Strict Implication Intro"
    implication_elim_name = "Implication Elim"
    necessary_intro_name = "Necessary Intro"
    necessary_elim_name = "Necessary Elim"
    negation_intro_name = "Negation Intro"
    negation_elim_name = "Negation Elim"
    possibly_intro_name = "Possibly Intro"
    possibly_elim_name = "Possibly Elim"
    reiterate_name = "Reiteration"
    removeaxiom_name = "Remove Axiom"
    removedefinition_name = "Remove Definition"
    removeproof_name = "Remove Proof"
    saveaxiom_name = "Save Axiom"
    savedefinition_name = "Save Definition"
    startstrictsubproof_name = "Start Strict Subproof"
    startemptystrictsubproof_name = "Start Empty Strict Subproof"
    substitution_name = "Substitution"
    rule_name = "Transformation Rule"

    # This set of strings provide names for proof structures which need not be used with natural deduction.

    premise_name = "Premise"
    proof_name = "Proof"
    proposition_name = "Proposition"
    setlogic_name = "Set Logic"
    substitution_name = "Substitution"
    substitute_name = "Substitute Evaluate"
    useproof_name = "Use Saved Proof"
    saveproof_name = "Save Proof"
    replaceproof_name = "Replace Proof"
    restricted_name = "Restricted"

    # This set of strings provides formatting details for other strings.

    dash_connector = " - "
    colon_connector = ": "
    space_connector = " "

    # This set of strings provides information for stopped messages and their associated logging.

    stopped_closemainproof = "The main proof cannot be closed only completed."
    log_closemainproof = "{0}: The main proof cannot be closed only completed."
    stopped_contradicted = "The goal has been contradicted."
    log_contradicted = 'The statement "{0}" contradicts the goal "{1}".'
    stopped_linescope = "Referenced item is out of scope."
    log_linescope = "{0}: The line {1} is out of scope."
    stopped_listsnotsamelength = "The lists are not the same length or are not empty."
    log_listsnotsamelength = (
        '{0}: The lists "{1}" and "{2}" are not the same lengths or are not empty.'
    )
    stopped_nodefinitionmatch = "The referenced line does not match the definition."
    log_nodefinitionmatch = '{0}: The referenced item "{1}" on line {2} does not match the definition "{3}".'
    stopped_nogoal = "The proof does not yet have a goal."
    log_nogoal = '{0}: The proof needs a goal before a line with the item "{1}" can be added to it.'
    stopped_nolines = "The list of lines is empty."
    log_nolines = '{0}: The list of lines "{1}" is empty.'
    stopped_nologic = "No logic has been declared for the proof."
    log_nologic = "{0}: No logic has been declared for the proof."
    stopped_logicalreadydefined = "A specified logic is already being used."
    log_logicalreadydefined = '{0}: The logic "{1}" is already being used.'
    stopped_logicnotfound = "The desired logic could not be found."
    log_logicnotfound = '{0}: The desired logic "{1}" could not be found.'
    stopped_nosavedproof = (
        "The named saved proof does not exist in the logic's database."
    )
    log_nosavedproof = '{0}: The saved proof "{1}" cannot be found in the database.'
    stopped_nosubproof = "No subproof has yet been started to add an hypothesis to."
    log_nosubproof = '{0}: There is no subproof to add the hypothesis "{1}" to.'
    stopped_nosubs = "There were no substitutions entered."
    log_nosubs = '{0}: There were no substitutions entered for "{1}".'
    stopped_nosuchaxiom = "The referenced name is not in the axiom list."
    log_nosuchaxiom = '{0}: The name "{1}" does not reference an axiom.'
    stopped_nosuchdefinition = "The referenced name is not in the definition list."
    log_nosuchdefinition = '{0}: The name "{1}" does not reference a definition.'
    stopped_nosuchline = "The referenced line is not a previous line of the proof."
    log_nosuchline = "{0}: The line {1} is not a previous line of the proof."
    stopped_nosuchproof = "The referenced name is not in the saved proof database."
    log_nosuchproof = '{0}: The name "{1}" does not reference a saved proof.'
    stopped_notantecedent = "One item is not the antecedent of the other."
    log_notantecedent = '{0}: Item "{1}" is not the antecedent of the other "{2}".'
    stopped_notcoimplicationelim = (
        "The refernced items cannot be used in coimplication elimination."
    )
    log_notcoimplicationelim = '{0}: The referenced items "{1}" on line {2} and "{3}" on line {4} cannot be used in coimplication elimination.'
    stopped_notcomplete = "The proof needs to be completed before it can be saved."
    log_notcomplete = (
        '{0}: The proof named "{1}" cannot be saved because it is not yet complete.'
    )
    stopped_notconjunction = "The referenced item is not a conjunction."
    log_notconjunction = (
        '{0}: The referenced item "{1}" on line {2} is not a conjunction.'
    )
    stopped_notcontradiction = "The referenced items are not negations of each other."
    log_notcontradiction = '{0}: The reference items "{1}" on line {2} and "{3}" on line {4} are not negations of each other.'
    stopped_notdisjunction = "The referenced item is not a disjunction."
    log_notdisjunction = (
        '{0}: The referenced item "{1}" on line {2} is not a disjunction.'
    )
    stopped_notenoughsubs = (
        "There are not enough substitution values for the metavariables."
    )
    log_notenoughsubs = '{0}: The metaformula "{1}" require more substution values than are provided in this list "{2}".'
    stopped_notfalse = "The referenced item is not false."
    log_notfalse = '{0}: The referenced item "{1}" on line {2} is not false.'
    stopped_notimplication = "The referenced item is not an implication."
    log_notimplication = (
        '{0}: The referenced item "{1}" on line {2} is not an implication.'
    )
    stopped_notinteger = "The line number is not an integer."
    log_notinteger = "{0}: The line number {1} is not an integer."
    stopped_notlist = "The input is not a list."
    log_notlist = '{0}: The input "{1}" is not a list.'
    stopped_notmodusponens = (
        "The referenced items can not be used in implication elimination."
    )
    log_notmodusponens = '{0}: The referenced items "{1}" on line {2} and "{3}" on line {4} cannot be used in implication elimination.'
    stopped_notnecessary = "The referenced item is not necessary."
    log_notnecessary = '{0}: The referenced item "{1}" on line {2} is not necessary.'
    stopped_notproposition = "The object is not a Proposition."
    log_notproposition = '{0}: The object "{1}" is not a Proposition.'
    stopped_notransformationrule = (
        "The transformation rule is not defined in the selected logic."
    )
    log_notransformationrule = (
        '{0}: This transformation rule "{1}" is not part of the logic.'
    )
    stopped_notreiteratescope = "The referenced item is not in the reiterate scope."
    log_notreiteratescope = (
        "{0}: The referenced item on line {1} is not in the reiterate scope."
    )
    stopped_notsamestatement = "The referenced items are not the same."
    log_notsamestatement = '{0}: The referenced items "{1}" and "{2}" are not the same.'
    stopped_notstrictsubproof = "The subproof is not strict."
    log_notstrictsubproof = '{0}: The subproof is "{1}" rather than "{2}".'
    stopped_notwff = "The input is not an instance of the Wff object."
    log_notwff = '{0}: The input "{1}" is not an instance of the Wff object.'
    stopped_novaluepassed = "No value was passed to the function."
    log_novaluepassed = "{0}: No value was passed to the function."
    stopped_premisesdontmatch = (
        "A required premise does not match a line in the current proof."
    )
    log_premisesdontmatch = (
        '{0}: The premise "{1}" does not match a line from the current proof.'
    )
    stopped_restrictednowff = (
        "In restricted mode objects cannot be used in disjunction introduction."
    )
    log_restrictednowff = '{0}: Only integers referencing statements can be used in restricted mode not "{1}" or "{2}".'
    stopped_ruleclass = "This inference rule is not part of the selected set of rules."
    log_ruleclass = '{0}: This inference rule "{1}" is part of the "{2}" set of rules not the selected "{3}" set of rules.'
    stopped_sidenotselected = 'A side, "left" or "right", must be selected.'
    log_sidenotselected = '{0}: The input "{1}" was used rather than "left" or "right".'

    """Strings to log messages upon successful completion of tasks."""

    log_addhypothesis = (
        '{0}: Item "{1}" has been added as an hypothesis to subproof {2}.'
    )
    log_axiom = '{0}: Item "{1}" has been added through the "{2}" axiom.'
    log_axiomalreadyexists = '{0}: An axiom with the name "{1}" already exists.'
    log_axiomnotfound = '{0}: An axiom with the name "{1}" was not found.'
    log_axiomremoved = '{0}: The axiom named "{1}" has been removed.'
    log_axiomsaved = '{0}: The axiom named "{1}" has been saved.'
    log_badpremise = 'The premise "{0}" is not an instance of altrea.wffs.Wff.'
    log_badconclusion = 'The conclusion "{0}" is not an instance of altrea.wffs.Wff.'
    log_coimplication_elim = (
        '{0}: Item "{1}" has been derived from the coimplication "{2}".'
    )
    log_coimplication_intro = '{0}: Item "{1}" has been derived from "{2}" and "{3}".'
    log_conjunction_elim = (
        '{0}: Item "{1}" has been derived from the conjunction "{2}" on line {3}.'
    )
    log_conjunction_intro = '{0}: The conjunction "{1}" has been derived from "{2}" on line {3} and "{4}" on line {5}.'
    # log_couldnotgetconnectors = '{0}: "{1}" could not retrieve its connector permissions.'
    # log_couldnotgettransformationrules = '{0}: "{1}" could not retrieve its transformation rule permissions.'
    log_definition = '{0}: Item "{1}" has been added using the "{2}" definition.'
    log_definitionalreadyexists = (
        '{0}: A definition with the name "{1}" already exists.'
    )
    log_definitionnotfound = '{0}: A definition with the name "{1}" was not found.'
    log_definitionremoved = '{0}: The definition named "{1}" has been removed.'
    log_definitionsaved = '{0}: The definition named "{1}" has been saved.'
    log_disjunction_elim = '{0}: Item "{1}" has been derived as the conclusion of both disjuncts of the disjunction "{2}" on line {3}.'
    log_disjunction_intro = '{0}: Item "{1}" has been derived from item "{2}" on line {3} joined on the {4} with {5}.'
    log_emptystrictsubproofstarted = "{0}: An empty strict subproof has been started."
    log_goal = '{0}: The goal "{1}" has been added to the goals.'
    log_hypothesis = '{0}: A new subproof {1} has been started with item "{2}".'
    log_implication_elim = (
        '{0}: Item "{1}" has been derived from the implication "{2}" and item "{3}".'
    )
    log_implication_intro = (
        '{0}: Item "{1}" has been derived upon closing subproof {2}.'
    )
    log_implication_intro_strict = (
        '{0}: Item "{1}" has been derived upon closing the strict subproof {2}.'
    )
    log_logdisplayed = "The log will be displayed."
    log_logicdescription = '{0}: "{1}" has been selected as the logic described as "{2}" and stored in database "{3}".'
    log_necessary_elim = (
        '{0}: Item "{1}" has been derived from the necessary item "{2}" on line {3}.'
    )
    log_necessary_intro = '{0}: Item "{1}" has been derived from item "{2}".'
    log_negation_elim = '{0}: A falsehood "{1}" has been derived from the contradiction between "{2}" on line {3} and "{4}" on line {5}.'
    log_negation_intro = (
        '{0}: Item "{1}" has been derived as the negation of the antecedent of "{2}".'
    )
    log_noproofs = "There are no saved proofs for logic {0}"
    log_possibly_elim = '{0}: Item "{1}" has been derived from item "{2}".'
    log_possibly_intro = (
        '{0}: Item "{1}" has been derived from the item "{2}" on line {3}.'
    )
    log_premise = '{0}: Item "{1}" has been added to the premises.'
    log_proof = (
        '{0}: A proof named "{1}" or "{2}" with description "{3}" has been started.'
    )
    log_proofalreadyexists = '{0}: A proof name "{1}" already exists in the database.'
    log_proofhasnoname = '{0}: The proof either has an empty name "{1}" or empty displayname "{2}" or empty description "{3}".'
    log_proposition = '{0}: The letter "{1}" for a generic well-formed formula has been defined with {2} so far for this proof.'
    log_reiterate = '{0}: Item "{1}" on line {2} has been reiterated into subproof {3}.'
    log_restricted = "{0}: The restricted use of explosion has been set to {1}."
    log_complete = "The proof is complete."
    log_partiallycomplete = "The proof is partially complete."
    log_proofsaved = (
        '{0}: The proof "{1}" was saved as "{2}" to database "{3}" under logic "{4}".'
    )
    log_proofdeleted = (
        '{0}: The proof "{1}" was deleted form the database "{2}" under logic "{3}".'
    )
    log_strictsubproofstarted = '{0}: A strict subproof "{1}" has been started with either line {2}, additional hypothesis "{3}" or hypothesis "{4}".'
    log_substitute = '{0}: The placeholder(s) in the string "{1}" have been replaced with "{2}" to become "{3}".'
    log_substitution = (
        '{0}: The statement "{1}" on line "{2}" has been substituted with "{3}".'
    )
    log_useproof = '{0}: Item "{1}" has been added through the "{2}" saved proof.'
    log_userule = (
        '{0}: Item "{1}" has been added through the "{2}" transformation rule.'
    )
    log_vacuous = "The proof is vacuously over."

    """Labels for various reports."""

    label_axiom = "Axiom"
    label_axioms = "Axioms"
    label_checkmarklatex = "\\color{green}\\checkmark"
    label_checkmark = "ok"
    label_comment = "Comment"
    label_connective = "Connective"
    label_connectives = "Connectors"
    label_contradicted = "GOAL CONTRADICTED"
    label_currentproofid = "Current Proof ID"
    label_definitions = "Definitions"
    label_derivedgoal = "Derived Goal"
    label_derivedgoals = "Derived Goals"
    label_description = "Description"
    label_displayname = "Display Name"
    label_empty = "Empty"
    label_errorlatex = "\\color{red}\\chi"
    label_error = "x"
    label_goal = "Goal"
    label_goals = "Goals"
    label_inprogress = "In Progress"
    label_invalid = "Invalid"
    label_intelimrule = "IntElim Rule"
    label_intelimrules = "IntElim Rules"
    label_item = "Item"
    label_left = "left"
    label_level = "Level"
    label_lines = "Lines"
    label_linetype = "Type"
    label_logic = "Logic"
    label_logicdatabase = "Logic Database"
    label_logicdescription = "Logic Description"
    label_name = "Name"
    label_noaxioms = "No Axioms"
    label_noconnectives = "No Connectives"
    label_nodatabase = "No Database"
    label_nodefinition = " No Definitions"
    label_nodefinitions = "No Definitions"
    label_noderivedgoals = "No Derived Goals"
    label_nodescription = "No Description"
    label_nogoals = "No Goals"
    label_nointelimrules = "No IntElim Rules"
    label_nopremises = "No Premises"
    label_nosavedproofs = "No Saved Proofs"
    label_notransformationrules = "No Rules"
    label_notstopped = "Not Stopped"
    label_premise = "Premise"
    label_premises = "Premises"
    label_previousproofchain = "Previous Proof Chain"
    label_previousproofid = "Previous Proof ID"
    label_proof = "Proof"
    label_prooflevel = "Proof Level"
    label_proofname = "Proof Name"
    label_proofs = "Proofs"
    label_proofstatus = "Proof Status"
    label_right = "right"
    label_rule = "Rule"
    label_savedproofs = "Saved Proofs"
    label_stoppedstatus = "Stopped Status"
    label_subproofnormal = "{0}"
    label_subproofstrict = "{1}"
    label_tautology = "Tautology"
    label_transformationrules = "Rules"
    label_vacuous = "Vacuous"
    label_valid = "Valid"
    label_value = "Value"

    """Convenience strings for the user when entering string values."""

    left = "left"
    right = "right"

    """The following tags are used to differentiate between lines of a proof."""

    linetype_savedproof = "SP"
    linetype_axiom = "AX"
    linetype_definition = "DEF"
    linetype_transformationrule = "TR"
    linetype_substitution = "SUB"
    linetype_hypothesis = "H"
    linetype_premise = "PR"

    rule_naturaldeduction = "Natural Deducation"
    rule_categorical = "Categorical"
    rule_axiomatic = "Axiomatic"

    def __init__(self, name: str = "", displayname: str = "", description: str = ""):
        """Create a Proof object with an optional name.

        Parameters:
            name: The name assigned to the proof under which it may be saved in the proofs and proofdetail tables of the database.
            displayname: The name to be used in displaying the proof.
            description: A descriptive name giving more information about the proof to be used in queries later.

        Exceptions:
            TypeError: If the input to either the name, displayname or description parameters are not strings,
                then a type error is raised.
        """

        if (
            not isinstance(name, str)
            or not isinstance(displayname, str)
            or not isinstance(description, str)
        ):
            raise TypeError("A value used to define a Proof object was not a string.")

        self.name = name
        self.displayname = displayname
        self.description = description
        self.goals = []
        self.goals_string = ""
        self.goals_latex = ""
        self.goalswff = []
        self.derivedgoals = []
        self.derivedgoalswff = []
        self.comment = ""
        self.logic = ""
        self.logicdescription = ""
        self.logicdatabase = ""
        self.logicalconnectives = []
        self.logicrules = [
            (
                "modusponens",
                "ConclusionPremises({1}, [{0}, Implies({0}, {1})])",
                "Modus Ponens",
                "Modus Ponens",
            ),
        ]
        self.logicaxiomsunrestricted = [
            (
                "explosion",
                "ConclusionPremises({1}, [{0}, Not({0})])",
                "Explosion",
                "Explosion",
            ),
            (
                "contradiction",
                "ConclusionPremises(And({0}, Not({0})), [])",
                "Contradiction",
                "Trivialism: All Contradictions Are True",
            ),
            (
                "dneg intro",
                "ConclusionPremises(Not(Not({0})), [{0}])",
                "DN Intro",
                "Double Negation Introduction",
            ),
            (
                "dneg elim",
                "ConclusionPremises({0}, [Not(Not({0}))])",
                "DN Elim",
                "Double Negation Elimination",
            ),
            (
                "lem",
                "ConclusionPremises(Or({0}, Not({0})), [])",
                "LEM",
                "Law of Excluded Middle",
            ),
            (
                "wlem",
                "ConclusionPremises(Or(Not({0}), Not(Not({0}))), [])",
                "Weak LEM",
                "Weak Law of Excluded Middle",
            ),
            (
                "or to not and",
                "ConclusionPremises(And(Not({0}), Not({1})), [Or({0}, {1})])",
                "De Morgan",
                "De Morgan Or To Not-And",
            ),
            (
                "not and to or",
                "ConclusionPremises(Or({0}, {1}), [And(Not({0}), Not({1}))])",
                "De Morgan",
                "De Morgan Not-And To Or",
            ),
            (
                "and to not or",
                "ConclusionPremises(Or(Not({0}), Not({1})), [And({0}, {1})])",
                "De Morgan",
                "De Morgan And To Not-Or",
            ),
            (
                "not or to and",
                "ConclusionPremises(And({0}, {1}), [Or(Not({0}), Not({1}))])",
                "De Morgan",
                "De Morgan Not-Or To And",
            ),
            (
                "modus ponens",
                "ConclusionPremises({1}, [{0}, Implies({0}, {1})])",
                "Modus Ponens",
                "Given A and A > B Derive B",
            ),
        ]
        self.logicaxioms = []
        self.logicdefinitionsunrestricted = [
            (
                "iff intro",
                "ConclusionPremises(Iff({0}, {1}), [And(Implies({0}, {1}), Implies({1}, {0}))])",
                "Iff Intro",
                "Coimplication Introduction",
            ),
            (
                "iff elim",
                "ConclusionPremises(And(Implies({0}, {1}), Implies({1}, {0})), [Iff({0}, {1})])",
                "Iff Elim",
                "Coimplication Elimination",
            ),
        ]
        self.logicdefinitions = []
        self.logicsavedproofs = []
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
        self.lines = [["", 0, 0, "", "", "", "", "", ""]]
        self.previousproofchain = []
        self.previousproofid = -1
        self.currentproof = [1]
        self.currentproofid = 0
        self.subproof_status = self.subproof_normal
        self.subproofchain = ""
        self.proofdata = [[self.name, self.displayname, self.description]]
        self.proofdatafinal = []
        self.prooflist = [
            [
                self.lowestlevel,
                self.currentproof,
                self.previousproofid,
                [],
                self.subproof_status,
            ]
        ]
        self.proofrules = self.rule_naturaldeduction
        self.level = self.lowestlevel
        self.status = ""
        self.stoppedmessage = ""
        self.necessarylines = []
        self.premises = []
        self.consequences = []
        self.letters = []
        self.truths = []
        self.objectdictionary = {
            "Implies": Implies,
            "Iff": Iff,
            "And": And,
            "Or": Or,
            "Not": Not,
            "Necessary": Necessary,
            "Possibly": Possibly,
            "ConclusionPremises": ConclusionPremises,
            "ConsistentWith": ConsistentWith,
            "StrictImplies": StrictImplies,
            "StrictIff": StrictIff,
            "Definition": Definition,
        }
        self.log = []
        self.latexwrittenproof = ""
        self.writtenproof = ""
        self.showlogging = False
        self.restricted = False
        # self.logstep(self.log_proof.format(self.proof_name.upper(),
        #                                    name,
        #                                    displayname,
        #                                    description))

    """SUPPORT FUNCTIONS 
    
    These are not intended to be called by the user while constructing a proof.
    """

    def appendproofdata(self, statement: Wff, rule: str):
        """Append a list representing a line of the proof which will be used to save the proof
        lines as a string.
        """

        length = len(self.lines) - 1
        self.proofdata.append(
            [
                self.name,
                statement,
                self.lines[length][1],
                self.lines[length][2],
                "".join(["*", rule, "*"]),
                self.lines[length][4],
                self.lines[length][5],
                self.lines[length][6],
                self.lines[length][7],
                self.lines[length][8],
            ]
        )
        if type(statement) == Necessary:
            self.necessarylines.append(length)
        if self.status == self.complete:
            finalresult = self.buildconclusionpremises()
            propositionlist = []
            self.proofdatafinal.append(
                [
                    self.proofdata[0][0],
                    self.proofdata[0][1],
                    self.proofdata[0][2],
                    self.proofdata[0][3],
                    finalresult.pattern(propositionlist),
                ]
            )
            for i in range(len(self.proofdata)):
                if i > 0:
                    self.proofdatafinal.append(
                        [
                            self.proofdata[i][0],
                            self.proofdata[i][1].pattern(propositionlist),
                            self.proofdata[i][2],
                            self.proofdata[i][3],
                            self.proofdata[i][4],
                            self.proofdata[i][5],
                            self.proofdata[i][6],
                            self.proofdata[i][7],
                            self.proofdata[i][8],
                        ]
                    )

    def buildconclusionpremises(self):
        """Saved proofs, definitions and axioms are used as ConclusionPremises objects.
        This function creates such an object for the proof.
        """

        conclusion = self.consequences[0]
        if len(self.consequences) > 1:
            for i in range(len(self.consequences)):
                if i > 0:
                    conclusion = And(conclusion, self.consequences[i])
        return ConclusionPremises(conclusion, self.premises)

    def canproceed(self):
        """Check if there are no errors that block proceeding with the next line of the proof
        or whether the proof is already complete and can accept no more items."""

        return (
            self.status != self.complete
            and self.status != self.stopped
            and self.status != self.vacuous
        )  # \
        # and self.status != self.contradicted

    def checkhasgoal(self):
        """Check if the proof has at least one goal."""

        return len(self.goals) > 0

    def checkitemlines(
        self, caller: str, displayname: str, comment: str, lineslist: list
    ):
        p = []
        lines = []
        for i in lineslist:
            if self.goodline(i, caller, displayname, comment):
                p.append(self.getstatement(i).tree())
                lines.append(i)
            else:
                break
        return p, lines

    def checkline(self, line: int):
        """Check if the line is an integer within the range of the proof lines."""

        if isinstance(line, int):
            return len(self.lines) > line and line > 0
        else:
            return False

    def checkpremises(
        self,
        caller: str,
        displayname: str,
        comment: str,
        premiselist: list = [],
        matchpremiselist: list = [],
    ):
        if len(premiselist) > 0:
            premises = [i.tree() for i in premiselist]
            for i in premises:
                if i not in matchpremiselist:
                    self.logstep(self.log_premisesdontmatch.format(caller.upper(), i))
                    self.stopproof(
                        self.stopped_premisesdontmatch,
                        self.blankstatement,
                        displayname,
                        "",
                        "",
                        comment,
                    )
                    break

    def checksubs(self, caller: str, displayname: str, comment: str, subslist: list):
        s = []
        for i in subslist:
            if len(subslist) == 0:
                self.logstep(self.log_nosubs.format(caller.upper(), ""))
                self.stopproof(
                    self.stopped_nosubs,
                    self.blankstatement,
                    displayname,
                    "",
                    "",
                    comment,
                )
                break
            elif self.goodobject(i, caller, displayname, comment):
                s.append(i)
            else:
                break
        return s

    def getpreviousproofid(self, proofid: int) -> int:
        return self.prooflist[proofid][2]

    def getproof(self, proofid: int) -> tuple:
        """Returns one or more hypothesis statements conjoined together, the conclusion statement
        and the parent proof id.  It is used by functions such as implication_intro and
        negation_intro to close a subordinate proof.
        """

        hypothesis = self.lines[self.prooflist[proofid][3][0]][self.statementindex]
        if len(self.prooflist[proofid][3]) > 1:
            for i in range(len(self.prooflist[proofid][3])):
                if i > 0:
                    hypothesis = And(
                        hypothesis,
                        self.lines[self.prooflist[proofid][3][i]][self.statementindex],
                    )
        conclusion = self.lines[self.prooflist[proofid][1][1]][self.statementindex]
        previousproofid = self.prooflist[proofid][2]
        previoussubproofstatus = self.prooflist[previousproofid][4]
        return hypothesis, conclusion, previousproofid, previoussubproofstatus

    def getstatement(self, line):
        """Returns the statement associated with the line number."""

        return self.lines[line][self.statementindex]

    def goodline(self, line: int, caller: str, displayname: str, comment: str):
        if not isinstance(line, int):
            self.logstep(self.log_notinteger.format(caller.upper(), line))
            self.stopproof(
                self.stopped_notinteger,
                self.blankstatement,
                displayname,
                str(line),
                "",
                comment,
            )
        elif len(self.lines) <= line or line <= 0:
            self.logstep(self.log_nosuchline.format(caller.upper(), line))
            self.stopproof(
                self.stopped_nosuchline,
                self.blankstatement,
                displayname,
                str(line),
                "",
                comment,
            )
            return False
        elif self.lines[line][2] != self.currentproofid:
            self.logstep(self.log_linescope.format(caller.upper(), line))
            self.stopproof(
                self.stopped_linescope,
                self.blankstatement,
                displayname,
                str(line),
                "",
                comment,
            )
            return False
        else:
            return True

    def goodlist(self, object, caller: str, displayname: str, comment: str):
        if not isinstance(object, list):
            self.logstep(self.log_notlist.format(caller.upper(), object))
            self.stopproof(
                self.stopped_notlist, self.blankstatement, displayname, "", "", comment
            )
            return False
        else:
            return True

    def goodlistlength(
        self,
        firstlist: list,
        secondlist: list,
        caller: str,
        displayname: str,
        comment: str,
    ):
        if len(firstlist) > 0 and len(firstlist) == len(secondlist):
            return True
        else:
            self.logstep(
                self.log_listsnotsamelength.format(
                    caller.upper(), len(firstlist), len(secondlist)
                )
            )
            self.stopproof(
                self.stopped_listsnotsamelength,
                self.blankstatement,
                displayname,
                "",
                "",
                comment,
            )
            return False

    def goodobject(self, object, caller: str, displayname: str, comment: str):
        if not isinstance(object, Wff):
            self.logstep(self.log_notwff.format(caller.upper(), object))
            self.stopproof(
                self.stopped_notwff, self.blankstatement, displayname, "", "", comment
            )
            return False
        else:
            return True

    def goodproposition(self, object, caller: str, displayname: str, comment: str):
        if not isinstance(object, Proposition):
            self.logstep(self.log_notproposition.format(caller.upper(), object))
            self.stopproof(
                self.stopped_notproposition,
                self.blankstatement,
                displayname,
                "",
                "",
                comment,
            )
            return False
        else:
            return True

    def goodrule(self, ruleclass: str, caller: str, displayname: str, comment: str):
        if self.proofrules == ruleclass:
            return True
        else:
            self.logstep(
                self.log_ruleclass.format(
                    caller.upper(), displayname, ruleclass, self.proofrules
                )
            )
            self.stopproof(
                self.stopped_ruleclass,
                self.blankstatement,
                displayname,
                "",
                "",
                comment,
            )
            return False

    def iscomplete(self, statement: Wff = None, comment: str = ""):
        """Check if the proof is complete or partially complete and if so leave a message."""

        newcomment = self.status
        if self.level == 0:
            if type(statement) == Falsehood and self.restricted:
                self.status = self.vacuous
                newcomment = self.vacuous
                self.logstep(self.log_vacuous)
            elif str(statement) in self.goals:
                if str(statement) not in self.derivedgoals:
                    self.derivedgoals.append(str(statement))
                    self.derivedgoalswff.append(statement)
                    if len(self.derivedgoals) < len(self.goals):
                        newcomment = self.partialcompletion
                        self.consequences.append(statement)
                        self.logstep(self.log_partiallycomplete)
                    else:
                        self.status = self.complete
                        self.prooflist[0][1].append(len(self.lines))
                        newcomment = self.complete
                        self.consequences.append(statement)
                        self.logstep(self.log_complete)
            for i in self.goalswff:
                if str(Not(statement)) == str(i) or str(statement) == str(Not(i)):
                    self.status = self.contradicted
                    newcomment = self.contradicted
                    self.logstep(self.log_contradicted.format(statement, i))
        if comment == "":
            return newcomment
        else:
            if newcomment == "":
                return comment
            else:
                return "".join([newcomment, self.dash_connector, comment])

    def latexitem(
        self, prooflines: list, i: int, status: str, saved: bool = False, color: int = 1
    ):
        """Formats a statement or item in a proof line for display as latex."""

        if prooflines[i][0] != self.blankstatement:
            normalbase = " \\hspace{0.35cm}|"
            strictbase = " \\hspace{0.35cm}\\Vert"
            # hypothesisnormalbase = ''.join(['\\underline{', normalbase, '}'])
            # hypothesisstrictbase = ''.join(['\\underline{', strictbase, '}'])
            subproofchain = prooflines[i][self.subproofstatusindex]
            statement = subproofchain.format(normalbase, strictbase)

            if color == 1:
                if i == 0:
                    if saved:
                        statement = "".join(
                            ["$\\color{blue}", prooflines[0][0].latex(), "$"]
                        )  
                    else:
                        if self.goals_latex != "":
                            statement = "".join(
                                ["$",self.color_conclusion, self.goals_latex, "$"]
                            )  
                        else:
                            statement = ""
                else:
                    if status != self.complete and status != self.stopped:
                        # if prooflines[i][1] == self.level and self.currentproofid == prooflines[i][2]:
                        if self.currentproofid == prooflines[i][2]:
                            statement = "".join(
                                [
                                    "$",
                                    self.color_available,
                                    prooflines[i][0].latex(),
                                    statement,
                                    "$",
                                ]
                            )
                        elif prooflines[i][2] in self.previousproofchain:
                            if self.subproof_status == self.subproof_strict:
                                if self.label_subproofstrict in prooflines[i][8]:
                                    statement = "".join(
                                        [
                                            "$",
                                            self.color_available,
                                            prooflines[i][0].latex(),
                                            statement,
                                            "$",
                                        ]
                                    )
                                elif i in self.necessarylines:
                                    statement = "".join(
                                        [
                                            "$",
                                            self.color_available,
                                            prooflines[i][0].latex(),
                                            statement,
                                            "$",
                                        ]
                                    )
                                else:
                                    statement = "".join(
                                        [
                                            "$",
                                            prooflines[i][0].latex(),
                                            statement,
                                            "$",
                                        ]
                                    )
                            else:
                                statement = "".join(
                                    [
                                        "$",
                                        self.color_available,
                                        prooflines[i][0].latex(),
                                        statement,
                                        "$",
                                    ]
                                )
                        else:
                            statement = "".join(
                                [
                                    "$",
                                    self.color_unavailable,
                                    prooflines[i][0].latex(),
                                    statement,
                                    "$",
                                ]
                            )
                    elif prooflines[i][6][0:8] == self.complete:
                        statement = "".join(
                            ["$", self.color_conclusion, prooflines[i][0].latex(), statement, "$"]
                        )
                    elif prooflines[i][6][0:18] == self.partialcompletion:
                        statement = "".join(
                            ["$", self.color_conclusion, prooflines[i][0].latex(), statement, "$"]
                        )
                    else:
                        statement = "".join(
                            ["$", prooflines[i][0].latex(), statement, "$"]
                        )
            else:
                if isinstance(prooflines[i][0], str):
                    statement = "".join([prooflines[i][0], statement])
                else:
                    statement = "".join(["$", prooflines[i][0].latex(), statement, "$"])
        else:
            statement = self.blankstatement
        return statement

    def logstep(self, message: str):
        """This function adds a log message collected during the proof construction
        so it can be displayed later or in an ongoing manner.
        """

        self.log.append(message)
        if self.showlogging:
            print(message)

    def reflines(self, *lines):
        """Convert integers to strings and join separated by commas."""

        joined = ""
        if len(lines) > 0:
            joined = str(lines[0])
            for i in range(len(lines)):
                if i > 0:
                    joined = "".join([joined, ", ", str(lines[i])])
        return joined

    def refproof(self, proofid: int):
        """Formats a proof used in a proof."""

        proof = self.prooflist[proofid][1]
        return "".join([str(proof[0]), "-", str(proof[1])])

    def stopproof(
        self,
        message: str,
        statement,
        rule: str,
        lines: str,
        blocks: str,
        comment: str = "",
    ):
        """Logs a status message in the line of a proof that shows no further lines can be added until the error is fixed."""

        self.status = self.stopped
        self.stoppedmessage = ""
        if rule == self.goal_name:
            if comment == "":
                self.lines[0][self.commentindex] = "".join(
                    [self.stopped, self.colon_connector, message]
                )
            else:
                self.lines[0][self.commentindex] = "".join(
                    [
                        self.stopped,
                        self.colon_connector,
                        message,
                        self.dash_connector,
                        comment,
                    ]
                )
        else:
            if comment == "":
                self.stoppedmessage = "".join(
                    [self.stopped, self.colon_connector, message]
                )
            else:
                self.stoppedmessage = "".join(
                    [
                        self.stopped,
                        self.colon_connector,
                        message,
                        self.dash_connector,
                        comment,
                    ]
                )
            self.lines.append(
                [
                    statement,
                    self.level,
                    self.currentproofid,
                    rule,
                    lines,
                    blocks,
                    self.stoppedmessage,
                    "",
                ]
            )

    def stringitem(self, prooflines: list, i: int):
        """Formats the statement or item in a proof line so it can be displayed as a string.
        It includes indenting based on the level of the subordinate proofs.
        """

        normalbase = "   |"
        # strictbase = '__||'
        strictbase = "   ||"
        # hypothesisnormalbase = ''.join(['\\underline{', normalbase, '}'])
        # hypothesisstrictbase = ''.join(['\\underline{', strictbase, '}'])
        subproofchain = prooflines[i][self.subproofstatusindex]
        statement = subproofchain.format(normalbase, strictbase)

        # base = '   |'
        # hypothesisbase = ' __|'
        # statement = ''
        # for j in range(1, prooflines[i][self.levelindex]):
        #     statement = base + statement
        # if prooflines[i][self.statementindex] != '':
        #     if prooflines[i][self.levelindex] > 0:
        #         if i < len(prooflines) - 1:
        #             if prooflines[i][self.ruleindex] == self.hypothesis_name:
        #                 if prooflines[i+1][self.ruleindex] != self.hypothesis_name or prooflines[i][self.levelindex] < prooflines[i+1][self.levelindex]:
        #                     statement = hypothesisbase + statement
        #                 else:
        #                     statement = base + statement
        #             else:
        #                 statement = base + statement
        #         else:
        #             if prooflines[i][self.ruleindex] == self.hypothesis_name:
        #                 statement = hypothesisbase + statement
        #             else:
        #                 statement = base + statement
        statement = "".join([str(prooflines[i][self.statementindex]), statement])
        return statement

    def substitute(self, originalstring: str, subs: list, displayname: str):
        """Substitute placeholders for strings representing the desired objects.  Then eval (evaluate) the resulting
        string to return the desired objects.

        Although this function is not called directly by the user, how this is done is a key component of a logic.
        AltRea uses the Python string function `format` to do the substitution on an arbitrary number of objects (*subs)
        which will replace the placeholders in the string (originalstring).

        This generates a list of strings that is different that what the strings of the objects would normally
        be printed as.  For example, if the object is And(A, B) then str(And(A, B)) would be "A & B".  However,
        And(A, B).tree() would be "And(A, B)".  If the originalstring is "{0}" then {0} would be substitued
        with "And(A, B)" using the print format function.

        The self.objectdirectory dictionary knows what And, A and B are allowing the string "And(A, B)" to be evaluated
        as And(A, B) with all of its properties.

        Parameters:
            originalstring: The original string with the placeholders.
            *subs: An arbitrarily long list of objects, not strings.  The calling function makes sure these are all objects.
                This function converts those objects into a special form of string that can be evaluated to
                return objects to the caller.

        Examples:
            Let the original string be "{0}" containing only the placeholder {0}.  Let the first subs arguemnt
            be the object And(A, B).  Then And(A, B).tree() becomes the string "And(A, B)".  This is handed
            to the Python string format function which does the substitution returning "And(A, B)".  That is then
            evaluated using a dictionary of objects that has been constructed as the objects were defined.
            Both A and B are in this dictionary along with And and the other named objects of the proof.
            The eval function takes the string "And(A, B)" and useds the dictionary to return And(A, B).

            As a more complicated example suppose the original string is "And({0}, {1})".  The subs contain A and B
            in that order.  Then A.tree() becomes "A" and B.tree() becomes "B".  These are substituted into the
            originalstring by the string format function to produce "And(A, B)" where the "A" replaced "{0}"
            and the "B" replaced "{1}".  The eval function took this string and using the dictionary of
            objects returned not the string "And(A, B)" but the object And(A, B).

        See Also:
            In altrea.wffs.Wff the tree() function is defined for each object instantiated.  When And(A, B).tree()
            is called it returns "And("+A.tree()+", "+B.tree()+")" which in turn returns since A.tree() = "A" and
            B.tree() = "B" the string that is ultimately returned is "And(A, B)".
        """

        if len(subs) > 0:
            prep = [i.tree() for i in subs]
            try:
                substitutedstring = originalstring.format(*prep)
                reconstructedobject = eval(substitutedstring, self.objectdictionary)
                self.logstep(
                    self.log_substitute.format(
                        self.substitute_name.upper(),
                        originalstring,
                        prep,
                        substitutedstring,
                    )
                )
                return reconstructedobject
            except IndexError:
                self.logstep(
                    self.log_notenoughsubs.format(
                        self.substitute_name.upper(), originalstring, subs
                    )
                )
                self.stopproof(
                    self.stopped_notenoughsubs,
                    self.blankstatement,
                    displayname,
                    "",
                    "",
                    "",
                )
        else:
            self.logstep(
                self.log_nosubs.format(self.substitute_name.upper(), originalstring)
            )
            self.stopproof(
                self.stopped_nosubs, self.blankstatement, displayname, "", "", ""
            )

    """DISPLAY FUNCTIONS
    
    These functions provide a display to the user who would be epected to call them
    if he chooses to do so.
    """

    def displaylogic(self):
        """Display an identification of the axiom with its axioms and definitions."""

        # Display minimal information about the logic
        # print('{: >22}'.format(self.label_logic))
        print('LOGIC "{}" {}'.format(self.logic, self.logicdescription))

        # Display axioms
        if len(self.logicaxioms) == 0:
            print("{}".format(self.label_noaxioms))
        else:
            print("{}".format(self.label_axioms.upper()))
            for i in self.logicaxioms:
                print(" {: <20} {: <50}".format(i[0], i[1]))

        # Display definitions
        if len(self.logicdefinitions) == 0:
            print("{}".format(self.label_nodefinitions))
        else:
            print("{}".format(self.label_definitions.upper()))
            for i in self.logicdefinitions:
                print(" {: <20} {: <50}".format(i[0], i[1]))

        # Display transformationrules
        if len(self.logicrules) == 0:
            print("{}".format(self.label_notransformationrules))
        else:
            print("{}".format(self.label_transformationrules.upper()))
            for i in self.logicrules:
                print(" {: <20} {: <50}".format(i[0], i[1]))

        # Display saved proofs
        if len(self.logicsavedproofs) == 0:
            print("{}".format(self.label_nosavedproofs))
        else:
            print("{}".format(self.label_savedproofs.upper()))
            for i in self.logicsavedproofs:
                print(" {: <20} {: <50}".format(i[0], i[1]))

    def displaylog(self):
        """Displays a log of the proof steps.  This will display the entire log that
        was collected for the proof.  It may be useful just prior to displaying the
        proof itself with `displayproof()`.  They provide two different views of the proof.
        Also, `writeproof()` provides a natural language proof version of the proof."""

        size = len(self.log)
        for i in range(len(self.log)):
            if size < 10:
                print("{: >1} {}".format(i, self.log[i]))
            elif size < 100:
                print("{: >2} {}".format(i, self.log[i]))
            elif size < 1000:
                print("{: >3} {}".format(i, self.log[i]))
            else:
                print("{: >4} {}".format(i, self.log[i]))

    def displayproof(self, short: int = 0, color: int = 1, latex: int = 1):
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
            columns = [
                self.label_item,
                self.label_level,
                self.label_proof,
                self.label_rule,
                self.label_linetype,
                self.label_lines,
                self.label_proofs,
                self.label_comment,
            ]

        # Create the index.
        indx = [self.displayname]
        for i in range(len(self.lines) - 1):
            indx.append(i + 1)

        # Create the rows of data.
        newp = []
        for i in range(len(self.lines)):
            if latex == 1:
                statement = self.latexitem(
                    prooflines=self.lines,
                    i=i,
                    status=self.status,
                    saved=False,
                    color=color,
                )
            else:
                statement = self.stringitem(prooflines=self.lines, i=i)
            if short == 1:
                if self.lines[i][self.linesindex] != "":
                    rule = "".join(
                        [
                            self.lines[i][self.linesindex],
                            ", ",
                            self.lines[i][self.ruleindex],
                        ]
                    )
                elif self.lines[i][self.proofsindex] != "":
                    rule = "".join(
                        [
                            self.lines[i][self.proofsindex],
                            ", ",
                            self.lines[i][self.ruleindex],
                        ]
                    )
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

    def proofdetailsnew(self, proofname: str, subs, latex: int = 1):
        """Display the details of a proof."""

        # Retrieve proof data.
        displayname, description, pattern = altrea.data.getsavedproof(
            self.logic, proofname
        )
        rows = altrea.data.getproofdetails(self.logic, proofname)

        # Change references to proof lines into the items on those lines.
        # s = []
        # for i in subs:
        #     if type(i) == int:
        #         s.append(self.getstatement(i))
        #     else:
        #         s.append(i)
        statement = self.substitute(pattern, subs, displayname)
        # for k in range(len(s)):
        #     statement = statement.replace(''.join(['*', str(k+1), '*']), s[k].tree())
        newrows = []
        newrows.append([statement, 0, 0, self.goal_name, "", "", ""])
        for i in rows:
            newrows.append(list(i))

        # # Format the item column using the dictionary.
        # for i in range(len(newrows)):
        #     for k in range(len(s)):
        #         newrows[i][0] = newrows[i][0].replace(''.join(['*', str(k+1), '*']), s[k].tree())
        #     newrows[i][0] = eval(newrows[i][0], self.objectdictionary)

        # Format the rules column using the names from the proofs logic operators.
        for i in newrows:
            for k in self.logicoperators:
                i[3] = i[3].replace("".join(["*", k[0], "*"]), k[1])
        for i in newrows:
            for k in self.basicoperators:
                i[3] = i[3].replace("".join(["*", k[0], "*"]), k[1])
        for i in newrows:
            for k in self.basicoperators:
                i[3] = i[3].replace("*", "")

        # Display the proof.
        newp = []
        if latex == 1:
            for i in range(len(newrows)):
                item = self.latexitem(newrows, i, self.complete, saved=True)
                newp.append(
                    [
                        item,
                        newrows[i][1],
                        newrows[i][2],
                        newrows[i][3],
                        newrows[i][4],
                        newrows[i][5],
                        newrows[i][6],
                    ]
                )
        else:
            for i in range(len(newrows)):
                item = self.stringitem(newrows, i)
                newp.append(
                    [
                        item,
                        newrows[i][1],
                        newrows[i][2],
                        newrows[i][3],
                        newrows[i][4],
                        newrows[i][5],
                        newrows[i][6],
                    ]
                )

        # Prepare to run DataFrame.
        columns = [
            self.label_item,
            self.label_level,
            self.label_proof,
            self.label_rule,
            self.label_lines,
            self.label_proofs,
            self.label_comment,
        ]
        index = [displayname]
        for i in range(len(newrows)):
            if i > 0:
                index.append(i)
        df = pandas.DataFrame(newp, index=index, columns=columns)
        return df

    def proofdetails(self, proofname: str, subs: list, latex: int = 1):
        """Display the proof details as saved to the database."""

        # Retrieve proof data.
        displayname, description, pattern = altrea.data.getsavedproof(
            self.logic, proofname
        )
        rows = altrea.data.getproofdetails(self.logic, proofname)

        # Substitute with current objects.
        newrows = []
        statement = self.substitute(pattern, subs, displayname)
        if latex == 1:
            statement = "".join(["$", statement.latexderived(), "$"])
        newrows.append([statement, 0, 0, self.goal_name, "", "", ""])
        for i in range(len(rows)):
            if latex == 1:
                item = "".join(
                    ["$", self.substitute(rows[i][0], subs, proofname).latex(), "$"]
                )
            else:
                item = self.substitute(rows[i][0], subs, proofname)
            row = [
                item,
                rows[i][1],
                rows[i][2],
                rows[i][3],
                rows[i][4],
                rows[i][5],
                rows[i][6],
            ]
            newrows.append(row)

        # Format the rules column using the names from the proofs logic operators.
        for i in newrows:
            for k in self.logicoperators:
                i[3] = i[3].replace("".join(["*", k[0], "*"]), k[1])
        for i in newrows:
            for k in self.basicoperators:
                i[3] = i[3].replace("".join(["*", k[0], "*"]), k[1])
        for i in newrows:
            for k in self.basicoperators:
                i[3] = i[3].replace("*", "")

        # Prepare to run DataFrame.
        columns = [
            self.label_item,
            self.label_level,
            self.label_proof,
            self.label_rule,
            self.label_lines,
            self.label_proofs,
            self.label_comment,
        ]
        index = [displayname]
        for i in range(len(newrows)):
            if i > 0:
                index.append(i)
        df = pandas.DataFrame(newrows, index=index, columns=columns)
        return df

    def proofdetailsraw(self, proofname: str):
        """Display the proof details as saved to the database."""

        # Retrieve proof data.
        rows = altrea.data.getproofdetails(self.logic, proofname)

        # Prepare to run DataFrame.
        columns = [
            self.label_item,
            self.label_level,
            self.label_proof,
            self.label_rule,
            self.label_lines,
            self.label_proofs,
            self.label_comment,
        ]
        index = []
        for i in range(len(rows)):
            index.append(i)
        df = pandas.DataFrame(rows, index=index, columns=columns)
        return df

    def reportstatus(self):
        """A text version of thee `statusreport` function."""

        # Display general information.
        print("{: <25} {: <25}".format(self.label_proofname, self.name))
        print("{: <25} {: <25}".format(self.label_displayname, self.displayname))
        print("{: <25} {: <25}".format(self.label_displayname, self.displayname))
        print("{: <25} {: <25}".format(self.label_description, self.description))
        print("{: <25} {: <25}".format(self.label_logic, self.logic))
        print(
            "{: <25} {: <25}".format(self.label_logicdescription, self.logicdescription)
        )
        print("{: <25} {: <25}".format(self.label_logicdatabase, self.logicdatabase))

        # Display axioms
        if len(self.logicaxioms) == 0:
            print("{: <25} {: <25}".format(self.label_axioms, self.label_noaxioms))
        else:
            print("{}".format(self.label_axioms))
            for i in self.logicaxioms:
                print("{: >25} {: <25}".format(i[0], i[1]))

        # Display definitions
        if len(self.logicdefinitions) == 0:
            print(
                "{: <25} {: <25}".format(
                    self.label_definitions, self.label_nodefinitions
                )
            )
        else:
            print("{}".format(self.label_definitions))
            for i in self.logicdefinitions:
                print("{: >25} {: <25}".format(i[0], i[1]))

        # Display connectives.
        if len(self.logicalconnectives) == 0:
            print(
                "{: <25} {: <25}".format(
                    self.label_connectives, self.label_noconnectives
                )
            )
        else:
            print("{}".format(self.label_connectives))
            for i in self.logicalconnectives:
                print("{: >25} {: <25}".format(i[1], i[2]))

        # Display intelim rules.
        if len(self.logicintelimrules) == 0:
            print(
                "{: <25} {: <25}".format(
                    self.label_intelimrules, self.label_nointelimrules
                )
            )
        else:
            print("{}".format(self.label_intelimrules))
            for i in self.logicintelimrules:
                print("{: <25} {: <25}".format(" ", i[1]))

        # Display goals.
        if len(self.goals) == 0:
            print("{: <25} {: <25}".format(self.label_goals, self.label_nogoals))
        else:
            print("{}".format(self.label_goals))
            for i in self.goals:
                print("{: <25} {: <25}".format(" ", str(i)))

        # Display premises.
        if len(self.premises) == 0:
            print("{: <25} {: <25}".format(self.label_premises, self.label_nopremises))
        else:
            print("{}".format(self.label_premises))
            for i in self.premises:
                print("{: <25} {: <25}".format(" ", str(i)))

        # Display derived goals.
        if len(self.derivedgoals) == 0:
            print(
                "{: <25} {: <25}".format(
                    self.label_derivedgoals, self.label_noderivedgoals
                )
            )
        else:
            print("{}".format(self.derivedgoals))
            for i in self.derivedgoals:
                print("{: <25} {: <25}".format(" ", str(i)))

        # Display proof statuses.
        if self.status == "":
            print(
                "{: <25} {: <25}".format(self.label_proofstatus, self.label_inprogress)
            )
        else:
            print("{: <25} {: <25}".format(self.label_proofstatus, self.status))
        if self.stoppedmessage == "":
            print(
                "{: <25} {: <25}".format(
                    self.label_stoppedstatus, self.label_notstopped
                )
            )
        else:
            print(
                "{: <25} {: <25}".format(self.label_stoppedstatus, self.stoppedmessage)
            )
        print("{: <25} {: <25}".format(self.label_prooflevel, self.level))
        print("{: <25} {: <25}".format(self.label_currentproofid, self.currentproofid))
        print(
            "{: <25} {: <25}".format(self.label_previousproofid, self.previousproofid)
        )
        if self.previousproofchain == []:
            print(
                "{: <25} {: <25}".format(
                    self.label_previousproofchain, self.label_empty
                )
            )
        else:
            print(
                "{: <25} {: <25}".format(
                    self.label_previousproofchain, self.previousproofchain
                )
            )

    def savedproofs(self):
        """Display a list of saved proofs for the logic being used."""

        rows = altrea.data.getproofs(self.logic)
        if len(rows) > 0:
            columns = [
                self.label_name,
                self.label_item,
                self.label_displayname,
                self.label_description,
            ]
            index = []
            for i in range(len(rows)):
                index.append(i)
            df = pandas.DataFrame(rows, index=index, columns=columns)
            return df
        else:
            print(self.log_noproofs.format(self.logic))

    def showlog(self, show: bool = True):
        """This function turns logging on if it is turned off.

        Parameters:
            show: This boolean turns the immediate display of logging on (default True) or off (False).

        Examples:

        """

        if show:
            self.showlogging = True
            self.logstep(self.log_logdisplayed)
        else:
            self.showlogging = False

    def statusreport(self, args: list, latex: int = 1):
        """A pandas DataFrame version of the `reportstatus` function.

        Parameters:
            args: These wff objects will be substituted for the string metavariables and then evaluated as a wff object.
            latex: Use a latex formatting.  This is the default.  Any value besides 1 will turn
                on a text display.
        """

        axiomslist = [list(i) for i in self.logicaxioms]
        columns = [self.label_name, self.label_value]
        data = []

        # Display general information on proof and logic used.
        data.append([self.label_proofname, self.name])
        data.append([self.label_displayname, self.displayname])
        data.append([self.label_description, self.description])
        data.append([self.label_logic, self.logic])
        data.append([self.label_logicdescription, self.logicdescription])
        data.append([self.label_logicdatabase, self.logicdatabase])

        # Display axioms.
        if len(self.logicaxioms) == 0:
            data.append([self.label_axioms, self.label_noaxioms])
        else:
            for i in range(len(self.logicaxioms)):
                axiom = str(axiomslist[i][1])
                axiomwff = self.substitute(axiom, *args)
                if latex == 1:
                    axiom = "".join(["$", axiomwff.latex(), "$"])
                else:
                    axiom = str(axiomwff)
                axiomslist[i][1] = axiom
                data.append([self.label_axiom, axiomslist[i]])

        # Display connectors.
        if len(self.logicalconnectives) == 0:
            data.append([self.label_connectives, self.label_noconnectives])
        else:
            for i in self.logicalconnectives:
                data.append([self.label_connective, i[1]])

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
                    data.append([self.label_goal, "".join(["$", i.latex(), "$"])])
                else:
                    data.append([self.label_goal, str(i)])

        # Display premises.
        if len(self.premises) == 0:
            data.append([self.label_premises, self.label_nopremises])
        else:
            for i in self.premises:
                if latex == 1:
                    data.append([self.label_premise, "".join(["$", i.latex(), "$"])])
                else:
                    data.append([self.label_premise, str(i)])

        # Display derived goals.
        if len(self.derivedgoalswff) == 0:
            data.append([self.label_derivedgoals, self.label_noderivedgoals])
        else:
            for i in self.derivedgoalswff:
                if latex == 1:
                    data.append(
                        [self.label_derivedgoal, "".join(["$", i.latex(), "$"])]
                    )
                else:
                    data.append([self.label_derivedgoal, str(i)])

        # Display status, stopped and proof info.
        if self.status == "":
            data.append([self.label_proofstatus, self.label_inprogress])
        else:
            data.append([self.label_proofstatus, self.status])
        if self.stoppedmessage == "":
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

    def setrestricted(self, booleanvalue: bool = True):
        """Set the logic to accept or reject explosion and unrestricted disjunction introduction."""

        self.restricted = booleanvalue
        if self.logic == "" and not self.restricted:
            self.logicaxioms = self.logicaxiomsunrestricted
            self.logicdefinitions = self.logicdefinitionsunrestricted
        elif self.logic == "" and self.restricted:
            self.logicaxioms = []
            self.logicdefinitions = []
        self.logstep(
            self.log_restricted.format(self.restricted_name.upper(), booleanvalue)
        )

    def truthtable(self, latex: bool = True, useint: bool = False):
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
            if latex:
                columns.append("".join(["$", i[0].latex(), "$"]))
            else:
                columns.append(i[0])
        for i in self.truths:
            if latex:
                columns.append("".join(["$", i[0].latex(), "$"]))
            else:
                columns.append(i[0])

        # Separate the letters from the premises and conclusion.
        if latex:
            columns.append("$\\parallel $")
        else:
            columns.append("|")

        # Optional premises
        if len(self.premises) > 0:
            for i in self.premises:
                if latex:
                    columns.append("".join(["$", i.latex(), "$"]))
                else:
                    columns.append(i)

        # Required models sign
        if latex:
            columns.append("$\\models $")
        else:
            columns.append("|=")

        # Required conclusion
        if len(self.goalswff) > 0:
            goals = self.goalswff[0]
            if len(self.goalswff) > 1:
                for i in range(len(self.goalswff)):
                    if i > 0:
                        goals = And(goals, self.goalswff[i])
            if latex:
                columns.append("".join(["$", goals.latex(), "$"]))
            else:
                columns.append(self.goals_string)
            columns.append(" ")
        else:
            raise ValueError(
                "A goal needs to be set before a truth table can be constructed."
            )

        tt = []
        letters = len(self.letters)
        countfalsegoal = 0
        counttruepremises = 0
        ttrows = 2**letters
        status = "Valid"

        for letter in self.letters:
            letter[0].booleanvalue = True
        for total in range(ttrows):
            row = []

            # Display the letters
            for i in self.letters:
                if useint:
                    row.append(int(i[0].booleanvalue))
                else:
                    row.append(i[0].booleanvalue)
            for i in self.truths:
                if useint:
                    row.append(int(True))
                else:
                    row.append(True)
            if latex:
                row.append("$\\parallel $")
            else:
                row.append("|")

            # Display the optional premises
            premisesvalue = True
            if len(self.premises) > 0:
                for i in self.premises:
                    if useint:
                        row.append(int(i.getvalue()))
                    else:
                        row.append(i.getvalue())
                    premisesvalue = premisesvalue and i.getvalue()
                if premisesvalue:
                    counttruepremises += 1

            # Display the goal and assessment of the interpretation on the line.
            row.append(" ")
            goalvalue = goals.getvalue()
            if not goalvalue:
                countfalsegoal += 1
            if useint:
                row.append(int(goalvalue))
            else:
                row.append(goalvalue)
            if premisesvalue and not goalvalue:
                if latex:
                    row.append("".join(["$", self.label_errorlatex, "$"]))
                else:
                    row.append(self.label_error)
                status = self.label_invalid
            elif premisesvalue and goalvalue:
                if latex:
                    row.append("".join(["$", self.label_checkmarklatex, "$"]))
                else:
                    row.append(self.label_checkmark)
            else:
                row.append(" ")
            tt.append(row)
            for n in range(letters):
                if (total + 1) % (2 ** (letters - 1 - n)) == 0:
                    self.letters[n][0].booleanvalue = flip(
                        self.letters[n][0].booleanvalue
                    )

        if len(self.premises) > 0 and counttruepremises == 0:
            if self.restricted:
                status = self.label_vacuous
            else:
                status = self.label_valid
        elif countfalsegoal == 0:
            status = self.label_tautology
        index = []
        for i in range(len(tt)):
            index.append(i + 1)
        index.append(self.displayname)
        summaryrow = []
        for i in range(len(columns) - 3 - len(self.premises)):
            summaryrow.append(" ")
        if status == self.label_tautology:
            for i in range(len(self.premises)):
                if latex:
                    summaryrow.append("".join(["$", self.label_errorlatex, "$"]))
                else:
                    summaryrow.append(self.label_error)
        else:
            for i in range(len(self.premises)):
                summaryrow.append(" ")
        summaryrow.append(status)
        summaryrow.append(" ")
        summaryrow.append(" ")
        tt.append(summaryrow)

        df = pandas.DataFrame(tt, index=index, columns=columns)
        return df

    def multivaluetruthtable(self, latex: bool = True):
        """Display a truth table built from the premises and goal of the proof.

        Examples:

        """

        def flip(v):
            if v:
                return (True, False)
            elif v == (True, False):
                return False
            elif not v:
                return True

        columns = []
        values = 3

        # Letters
        for i in self.letters:
            if latex:
                columns.append("".join(["$", i[0].latex(), "$"]))
            else:
                columns.append(i[0])
        for i in self.truths:
            if latex:
                columns.append("".join(["$", i[0].latex(), "$"]))
            else:
                columns.append(i[0])

        # Separate the letters from the premises and conclusion.
        if latex:
            columns.append("$\\parallel $")
        else:
            columns.append("|")

        # Optional premises
        if len(self.premises) > 0:
            for i in self.premises:
                if latex:
                    columns.append("".join(["$", i.latex(), "$"]))
                else:
                    columns.append(i)

        # Required models sign
        if latex:
            columns.append("$\\models $")
        else:
            columns.append("|=")

        # Required conclusion
        if len(self.goalswff) > 0:
            goals = self.goalswff[0]
            if len(self.goalswff) > 1:
                for i in range(len(self.goalswff)):
                    if i > 0:
                        goals = And(goals, self.goalswff[i])
            if latex:
                columns.append("".join(["$", goals.latex(), "$"]))
            else:
                columns.append(self.goals_string)
            columns.append(" ")
        else:
            raise ValueError(
                "A goal needs to be set before a truth table can be constructed."
            )

        tt = []
        letters = len(self.letters)
        countfalsegoal = 0
        counttruepremises = 0
        ttrows = values**letters
        status = "Valid"

        for letter in self.letters:
            letter[0].multivalue = True
        for total in range(ttrows):
            row = []

            # Display the letters
            for i in self.letters:
                # if i[0].booleanvalue == True:
                #     row.append(1)
                # else:
                #     row.append(0)
                row.append(i[0].multivalue)
            for i in self.truths:
                # row.append(1)
                row.append((True))
            if latex:
                row.append("$\\parallel $")
            else:
                row.append("|")

            # Display the optional premises
            premisesvalue = True
            if len(self.premises) > 0:
                for i in self.premises:
                    # if i.getvalue() == True:
                    #     row.append(1)
                    # else:
                    #     row.append(0)
                    row.append(i.getmultivalue())
                    premisesvalue = premisesvalue and i.getmultivalue()
                if premisesvalue:
                    counttruepremises += 1

            # Display the goal and assessment of the interpretation on the line.
            row.append(" ")
            goalvalue = goals.getmultivalue()
            if not goalvalue:
                countfalsegoal += 1
            # if goalvalue == True:
            #     row.append(1)
            # else:
            #     row.append(0)
            row.append(goalvalue)
            if premisesvalue and not goalvalue:
                if latex:
                    row.append("".join(["$", self.label_errorlatex, "$"]))
                else:
                    row.append(self.label_error)
                status = self.label_invalid
            elif premisesvalue and goalvalue:
                if latex:
                    row.append("".join(["$", self.label_checkmarklatex, "$"]))
                else:
                    row.append(self.label_checkmark)
            else:
                row.append(" ")
            tt.append(row)
            for n in range(letters):
                if (total + 1) % (values ** (letters - 1 - n)) == 0:
                    self.letters[n][0].multivalue = flip(self.letters[n][0].multivalue)

        if len(self.premises) > 0 and counttruepremises == 0:
            if self.restricted:
                status = self.label_vacuous
            else:
                status = self.label_valid
        elif countfalsegoal == 0:
            status = self.label_tautology
        index = []
        for i in range(len(tt)):
            index.append(i + 1)
        index.append(self.displayname)
        summaryrow = []
        for i in range(len(columns) - 3 - len(self.premises)):
            summaryrow.append(" ")
        if status == self.label_tautology:
            for i in range(len(self.premises)):
                if latex:
                    summaryrow.append("".join(["$", self.label_errorlatex, "$"]))
                else:
                    summaryrow.append(self.label_error)
        else:
            for i in range(len(self.premises)):
                summaryrow.append(" ")
        summaryrow.append(status)
        summaryrow.append(" ")
        summaryrow.append(" ")
        tt.append(summaryrow)

        df = pandas.DataFrame(tt, index=index, columns=columns)
        return df

    def writeproof(self, latex: int = 0):
        """Constructs an English version of the proof."""

        proofvariables = ""
        variables = len(self.letters)
        premises = len(self.premises)
        if variables > 0:
            proofvariables = "".join(
                [
                    "    Let ",
                    str(self.letters[0][0]),
                    " be an arbitrary ",
                    self.letters[0][0].kind,
                ]
            )
            if variables > 1:
                for i in range(len(self.letters)):
                    if i > 0 and i < variables - 1:
                        proofvariables += "".join(
                            [
                                ", let ",
                                str(self.letters[i][0]),
                                " be an arbitrary ",
                                self.letters[i][0].kind,
                            ]
                        )
                    elif i == variables - 1:
                        proofvariables += "".join(
                            [
                                " and let ",
                                str(self.letters[i][0]),
                                " be an arbitrary ",
                                self.letters[i][0].kind,
                            ]
                        )
            proofvariables = "".join([proofvariables, "."])
            print(proofvariables)
        proofpremises = ""
        if premises > 0:
            proofpremises = "".join(["    We are given ", str(self.premises[0])])
            if premises > 1:
                for i in range(len(self.premises)):
                    if i > 0 and i < premises - 1:
                        proofpremises = "".join(
                            [proofpremises, ", ", str(self.premises[i])]
                        )
                    elif i == premises - 1:
                        proofpremises = "".join(
                            [proofpremises, " and ", str(self.premises[i])]
                        )
            proofpremises = "".join([proofpremises, " as premises."])
            print(proofpremises)
        proofconclusion = ""
        if self.status == self.complete:
            proofconclusion = (
                f"    Therefore, {self.goals_string} which completes the proof."
            )
        self.writtenproof = "".join(
            [proofvariables, "\n", proofpremises, "\n", proofconclusion, "\n"]
        )

    """DATABASE FUNCTIONS 
    
    These are intended for the user to call.  They have an effect if a logic has been defined
    in advance which gives them a database to work with.
    """

    def removeaxiom(self, name: str):
        """Remove an axiom from the current proof as well as the logic's database if one has been identified.
        This is mainly useful for logics with stored axioms although removing an axiom for an
        unidentified logic will force the user not to use the default axiom.  That default axiom
        will return when a new proof has been started.

        Parameters:
            name: The name of the axiom to be removed.

        """

        # Look for errors

        # If no errors, perform the task
        indexfound = -1
        for i in range(len(self.logicaxioms)):
            if self.logicaxioms[i][0] == name:
                indexfound = i
                break
        if indexfound == -1:
            self.logstep(
                self.log_axiomnotfound.format(self.removeaxiom_name.upper(), name)
            )
        else:
            self.logicaxioms.pop(i)
            if self.logicdatabase != self.label_nodatabase:
                altrea.data.deleteaxiom(self.logic, name)
                self.logstep(
                    self.log_axiomremoved.format(self.removeaxiom_name.upper(), name)
                )

    def removedefinition(self, name: str):
        """Remove a definition from the current proof as well as the logic's database if one has been identified.
        This is mainly useful for logics with stored definitions although removing a definition for an
        unidentified logic will force the user not to use the default definition.  That default definition
        will return when a new proof has been started.

        Parameters:
            name: The name of the definition to be removed.

        """

        # Look for errors

        # If no errors, perform the task
        indexfound = -1
        for i in range(len(self.logicdefinitions)):
            if self.logicdefinitions[i][0] == name:
                indexfound = i
                break
        if indexfound == -1:
            self.logstep(
                self.log_definitionnotfound.format(
                    self.removedefinition_name.upper(), name
                )
            )
        else:
            self.logicdefinitions.pop(i)
            if self.logicdatabase != self.label_nodatabase:
                altrea.data.deletedefinition(self.logic, name)
                self.logstep(
                    self.log_definitionremoved.format(
                        self.removedefinition_name.upper(), name
                    )
                )

    def removeproof(self, name: str):
        """Delete the proof that already exists with that name and save a proof with the same name
        in the database file associated with the logic.

        The replacement proof must be complete before it can be saved.
        """

        howmany = altrea.data.deleteproof(self.logic, name)
        if howmany == 1:
            self.logstep(
                self.log_proofdeleted.format(
                    self.replaceproof_name.upper(),
                    self.name,
                    self.logicdatabase,
                    self.logic,
                )
            )
        else:
            self.logstep(
                self.log_nosavedproof.format(self.removeproof_name.upper(), name)
            )

    def saveaxiom(
        self,
        name: str,
        displayname: str,
        description: str,
        conclusion: Wff,
        premise: list = [],
    ):
        """Save an axiom for the current proof and in the logic's database if one has been identified.

        Parameters:
            name: The name of the axiom by which it will be accessed when one needs to use it.
            displayname: The way the axiom will be displayed in a proof.
            description: The description of the axiom to help understand it.
            conclusion: An object, not a string, that represents the conclusion that will be placed in the proof
                when the axiom is referenced.
            premise: A list of wff objects, not strings, that will need to be matched to wff objects referenced
                in proof lines before the axiom can later be used.
        """

        # Look for errors
        noerrors = True
        if isinstance(conclusion, altrea.wffs.Wff):
            for i in premise:
                if not isinstance(i, altrea.wffs.Wff):
                    print(self.log_badpremise.format(i))
                    noerrors = False
                    break
        else:
            print(self.log_badconclusion.format(conclusion))
            noerrors = False

        # If no errors, perform the task
        if noerrors:
            propositionlist = []
            conclusionpremise = ConclusionPremises(conclusion, premise).pattern(
                propositionlist
            )
            axiom = [name, conclusionpremise, displayname, description]
            found = False
            for i in self.logicaxioms:
                if i[0] == name:
                    found = True
                    break
            if found:
                self.logstep(
                    self.log_axiomalreadyexists.format(
                        self.saveaxiom_name.upper(), name
                    )
                )
            else:
                if self.logic != "":
                    altrea.data.addaxiom(
                        self.logic, name, conclusionpremise, displayname, description
                    )
                self.logicaxioms.append(axiom)
                self.logstep(
                    self.log_axiomsaved.format(self.saveaxiom_name.upper(), name)
                )

    def savedefinition(
        self,
        name: str,
        displayname: str,
        description: str,
        conclusion: Wff,
        premise: list = [],
    ):
        """Save a definition for the current proof and in the logic's database if one has been identified.

        Parameters:
            name: The name of the axiom by which it will be accessed when one needs to use it.
            displayname: The way the axiom will be displayed in a proof.
            description: The description of the axiom to help understand it.
            conclusion: An object, not a string, that represents the conclusion that will be placed in the proof
                when the axiom is referenced.
            premise: A list of objects, not strings, that need to be matched in proof lines before the
                axiom can be used.
        """

        # Look for errors
        noerrors = True
        if isinstance(conclusion, altrea.wffs.Wff):
            for i in premise:
                if not isinstance(i, altrea.wffs.Wff):
                    print(self.log_badpremise.format(i))
                    noerrors = False
                    break
        else:
            print(self.log_badconclusion.format(conclusion))
            noerrors = False

        # If no errors, perform the task
        if noerrors:
            propositionlist = []
            conclusionpremise = ConclusionPremises(conclusion, premise).pattern(
                propositionlist
            )
            definition = [name, conclusionpremise, displayname, description]
            found = False
            for i in self.logicdefinitions:
                if i[0] == name:
                    found = True
                    break
            if found:
                self.logstep(
                    self.log_definitionalreadyexists.format(
                        self.savedefinition_name.upper(), name
                    )
                )
            else:
                if self.logic != "":
                    altrea.data.adddefinition(
                        self.logic, name, conclusionpremise, displayname, description
                    )
                self.logicdefinitions.append(definition)
                self.logstep(
                    self.log_definitionsaved.format(
                        self.savedefinition_name.upper(), name
                    )
                )

    def saveproof(self, comment: str = ""):
        """Save the proof to a database file associated with the logic.

        The proof must be complete before it can be saved.

        Example:
            Suppose one has created the following proof that given q one can derive p > q.

            >>> from altrea.wffs import Wff, Or, Not, And, Implies, Iff, Necessary, Possibly
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
            To get around that we could replace the proof if we desire with `addcond.replaceproof()` as follows:

            >>> addcond.replaceproof()
            The proof details for add cond have been deleted from fitch.
            The proof add cond has been deleted from fitch.
            The proof add cond has been added to fitch.
            The proof details for add cond have been added to fitch.
            The proof of Principle of Added Condition was saved in altrea/data/fitch.db.

            With this call the old `add cond` proof was deleted and the new one added.  The file lines detail
            what happened.
        """

        if self.status == self.complete or self.status == self.vacuous:
            if self.name == "" or self.displayname == "" or self.description == "":
                self.logstep(
                    self.log_proofhasnoname.format(
                        self.saveproof_name.upper(),
                        self.name,
                        self.displayname,
                        self.description,
                    )
                )
            else:
                howmany = altrea.data.addproof(self.proofdatafinal)
                if howmany == 0:
                    proof = [
                        self.name,
                        self.proofdatafinal[0][4],
                        self.displayname,
                        self.description,
                    ]
                    self.logicsavedproofs.append(proof)
                    self.logstep(
                        self.log_proofsaved.format(
                            self.saveproof_name.upper(),
                            self.name,
                            self.proofdatafinal[0][4],
                            self.logicdatabase,
                            self.logic,
                        )
                    )
                else:
                    self.logstep(
                        self.log_proofalreadyexists.format(
                            self.saveproof_name.upper(), self.name
                        )
                    )
        else:
            self.logstep(
                self.log_notcomplete.format(self.saveproof_name.upper(), self.name)
            )
            self.stopproof(
                self.stopped_notcomplete,
                self.blankstatement,
                self.saveproof_name,
                "",
                "",
                comment,
            )

    """NATURAL DEDUCTION AND GENERAL PROOF CONSTRUCTION
    
    These functions include an introduction and an elimination function for each logical connective.
    Also included here are functions to define a goal, reiterate from a parent proof, define a premise 
    or define an hypotheses.
    """

    def addhypothesis(self, hypothesis: Wff, comment: str = ""):
        """Add to the currently opened subordinate proof a new hypothesis which will be a conjoint of the antecedent
        of the resulting implication when the subproof is finished.

        Parameters:
            hypothesis: The hypothesis that will be added.
            comment: An optional comment the user may add to this line of the proof.

        Examples:
            To introduce an implication one needs an antecedent and a consequent.  The antecedent is
            entered into the proof through an hypothesis which begins a subordinate proof.  Optionally,
            additional hypotheses can be added through this function.  These additional hypotheses do
            not start a subordinate proof.  Rather, they add to the current one.  After the conclusion
            has been derived the subordinate proof is closed by calling `implication_intro` which
            introduces an implication in the parent proof containing all of the hypotheses as conjoints
            of an `And` object.  That process is illustrated in this example.  The comments are optional.

            >>> from altrea. import Implies, And
            >>> from altrea.rules import Proof
            >>> pr = Proof()
            >>> A = pr.proposition('A')
            >>> B = pr.proposition('B')
            >>> C = pr.proposition('C')
            >>> pr.setlogic()
            >>> pr.goal(Implies(And(A, C), B), 'The goal of the proof')
            >>> pr.premise(B, 'A premise for the proof')
            >>> pr.hypothesis(A, 'This opens a subproof with the hypothesis "A"')
            >>> pr.addhypothesis(C, 'Add a second hypothesis without opening a subproof')
            >>> pr.reiterate(1, 'Bring the premise on line 1 to the subproof')
            >>> pr.implication_intro('Close the subproof with an implication in the main proof')
            >>> pr.displayproof(short=1, latex=0)
                    Item  ...                                                              Comment
            (A & C) > B  ...                                                The goal of the proof
            1            B  ...                                              A premise for the proof
            2        A   |  ...                        This opens a subproof with the hypothesis "A"
            3        C __|  ...                   Add a second hypothesis without opening a subproof
            4        B   |  ...                          Bring the premise on line 1 to the subproof
            5  (A & C) > B  ...  COMPLETE - Close the subproof with an implication in the main proof

        See Also:
            - `hypothesis`
            - `implication_intro`
        """

        # Look for errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.addhypothesis_name,
                self.addhypothesis_name,
                comment,
            ):
                if self.goodobject(
                    hypothesis,
                    self.addhypothesis_name,
                    self.addhypothesis_name,
                    comment,
                ):
                    if self.currentproofid == 0:
                        self.logstep(
                            self.log_nosubproof.format(
                                self.addhypothesis_name.upper(), hypothesis
                            )
                        )
                        self.stopproof(
                            self.stopped_nosubproof,
                            self.blankstatement,
                            self.hypothesis_name,
                            "",
                            "",
                            comment,
                        )

        # If no errors, perform task
        if self.canproceed():
            nextline = len(self.lines)
            self.prooflist[self.currentproofid][3].append(nextline)
            self.logstep(
                self.log_addhypothesis.format(
                    self.addhypothesis_name.upper(), hypothesis, self.currentproofid
                )
            )
            newcomment = self.iscomplete(hypothesis, comment)
            self.lines.append(
                [
                    hypothesis,
                    self.level,
                    self.currentproofid,
                    self.hypothesis_name,
                    "",
                    "",
                    newcomment,
                    self.linetype_hypothesis,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(hypothesis, self.hypothesis_tag)

    def axiom(
        self, name: str, subslist: list, premiselist: list = [], comment: str = ""
    ):
        """Use an axiom that is available for the logic to use.

        Parameters:
            name: The name of the axiom one wishes to use.
            subslist: A list of wff object instances which will be used as substitutes in the order they are provided
                for the string metavariables.
            premiselist: A list of integers referencing previous lines of the proof which will be matched to those required
                to use the axiom.  This is only required if the axiom specifies premises that must be met before it can be used.
            comment: An optional comment the user may add to this line of the proof.

        Examples:

        """

        # Look for errors: Find the axiom.
        if self.canproceed():
            foundindex = -1
            for i in range(len(self.logicaxioms)):
                if self.logicaxioms[i][0] == name:
                    foundindex = i
                    break
            if foundindex < 0:
                self.logstep(self.log_nosuchaxiom.format(self.axiom_name.upper(), name))
                self.stopproof(
                    self.stopped_nosuchaxiom, self.blankstatement, name, "", "", comment
                )
        if self.canproceed():
            pattern = self.logicaxioms[foundindex][1]
            displayname = self.logicaxioms[foundindex][2]
            description = self.logicaxioms[foundindex][3]

        # Look for errors: Check the substitution values.
        if self.canproceed():
            subs = self.checksubs(
                self.axiom_name.upper(), displayname, comment, subslist
            )

        # Look for errors: Check lines entered from the proof.
        if self.canproceed():
            matchpremiselist, lineslist = self.checkitemlines(
                self.axiom_name.upper(), displayname, comment, premiselist
            )

        # Look for errors: Can substitutions be made
        if self.canproceed():
            conclusionpremises = self.substitute(pattern, subs, displayname)

        # Look for errors: Do premises match identified lines in the current proof.
        if self.canproceed():
            self.checkpremises(
                self.axiom_name.upper(),
                displayname,
                comment,
                conclusionpremises.premises,
                matchpremiselist,
            )

        # If no errors, perform task.
        if self.canproceed():
            self.logstep(
                self.log_axiom.format(
                    self.axiom_name.upper(), conclusionpremises.conclusion, description
                )
            )
            newcomment = self.iscomplete(conclusionpremises.conclusion, comment)
            self.lines.append(
                [
                    conclusionpremises.conclusion,
                    self.level,
                    self.currentproofid,
                    displayname,
                    self.reflines(*lineslist),
                    "",
                    newcomment,
                    self.linetype_axiom,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(conclusionpremises.conclusion, displayname)

    def coimplication_elim(self, first: int, second: int, comment: str = ""):
        """Given an if and only if (coimplication or iff) statement and a proposition on one side of
        the iff statement, one can derive the proposition the other side.

        Parameters:
            first: A statement containing either a proposition or an iff statement.
            second: A second statement containing either a proposition or an iff statement.
            comment: An optional comment the user may add to this line of the proof.

        Examples:
            The following is a simple example of how the coimplication elimination rule works.

            >>> from altrea.wffs import Iff
            >>> from altrea.rules import Proof
            >>> prf = Proof()
            >>> A = prf.proposition('A')
            >>> B = prf.proposition('B')
            >>> prf.setlogic()
            >>> prf.goal(B)
            >>> prf.premise(Iff(A, B))
            >>> prf.premise(A)
            >>> prf.coimplication_elim(1, 2)
            >>> prf.displayproof(short=1, latex=0)
                 Item                      Rule   Comment
                    B                      GOAL
            1  A <> B                   Premise
            2       A                   Premise
            3       B  1, 2, Coimplication Elim  COMPLETE
        """

        # Look for general errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.coimplication_elim_name,
                self.coimplication_elim_name,
                comment,
            ):
                if self.goodline(
                    first,
                    self.coimplication_elim_name,
                    self.coimplication_elim_name,
                    comment,
                ):
                    if self.goodline(
                        second,
                        self.coimplication_elim_name,
                        self.coimplication_elim_name,
                        comment,
                    ):
                        pass

        # Look for specific errors
        lines = self.reflines(first, second)
        if self.canproceed():
            firststatement = self.getstatement(first)
            secondstatement = self.getstatement(second)
            if type(firststatement) != Iff and type(secondstatement) != Iff:
                self.logstep(
                    self.log_notcoimplicationelim.format(
                        self.coimplication_elim_name.upper(),
                        firststatement,
                        first,
                        secondstatement,
                        second,
                    )
                )
                self.stopproof(
                    self.stopped_notcoimplicationelim,
                    self.blankstatement,
                    self.coimplication_elim_name,
                    lines,
                    "",
                    comment,
                )
            elif (
                type(firststatement) == Iff
                and not secondstatement.equals(firststatement.left)
                and not secondstatement.equals(firststatement.right)
            ):
                self.logstep(
                    self.log_notcoimplicationelim.format(
                        self.coimplication_elim_name.upper(),
                        firststatement,
                        first,
                        secondstatement,
                        second,
                    )
                )
                self.stopproof(
                    self.stopped_notcoimplicationelim,
                    self.blankstatement,
                    self.coimplication_elim_name,
                    lines,
                    "",
                    comment,
                )
            elif (
                type(secondstatement) == Iff
                and not firststatement.equals(secondstatement.left)
                and not firststatement.equals(secondstatement.right)
            ):
                self.logstep(
                    self.log_notcoimplicationelim.format(
                        self.coimplication_elim_name.upper(),
                        firststatement,
                        first,
                        secondstatement,
                        second,
                    )
                )
                self.stopproof(
                    self.stopped_notcoimplicationelim,
                    self.blankstatement,
                    self.coimplication_elim_name,
                    lines,
                    "",
                    comment,
                )

        # If no errors, perform task
        if self.canproceed():
            if type(firststatement) == Iff:
                statement = firststatement.right
                fullstatement = firststatement
            else:
                statement = secondstatement.right
                fullstatement = secondstatement
            self.logstep(
                self.log_coimplication_elim.format(
                    self.coimplication_elim_name.upper(), statement, fullstatement
                )
            )
            newcomment = self.iscomplete(statement, comment)
            self.lines.append(
                [
                    statement,
                    self.level,
                    self.currentproofid,
                    self.coimplication_elim_name,
                    lines,
                    "",
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(statement, self.coimplication_elim_tag)

    def coimplication_intro(self, left: int, right: int, comment: str = ""):
        """Derive a item in a proof using the if and only if symbol.

        Parameters:
            left: The first item number references an implication going in one direction.
            right: The second item number references an implication going in the other direction.
            comment: An optional comment the user may add to this line of the proof.

        Examples:
            The following is a simple example of how the coimplication introduction rule works.

            >>> from altrea. import Implies, Wff, Iff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof
            >>> p = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> p.setlogic()
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

        # Look for general errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.coimplication_intro_name,
                self.coimplication_intro_name,
                comment,
            ):
                if self.goodline(
                    left,
                    self.coimplication_intro_name,
                    self.coimplication_intro_name,
                    comment,
                ):
                    if self.goodline(
                        right,
                        self.coimplication_intro_name,
                        self.coimplication_intro_name,
                        comment,
                    ):
                        pass

        # Look for specific errors
        if self.canproceed():
            firststatement = self.getstatement(left)
            secondstatement = self.getstatement(right)
            if type(firststatement) != Implies:
                self.logstep(
                    self.log_notimplication.format(
                        self.coimplication_intro_name.upper(), firststatement, left
                    )
                )
                self.stopproof(
                    self.stopped_notimplication,
                    self.blankstatement,
                    self.coimplication_intro_name,
                    str(left),
                    "",
                    comment,
                )
            elif type(secondstatement) != Implies:
                self.logstep(
                    self.log_notimplication.format(
                        self.coimplication_intro_name.upper(), secondstatement, right
                    )
                )
                self.stopproof(
                    self.stopped_notimplication,
                    self.blankstatement,
                    self.coimplication_intro_name,
                    str(right),
                    "",
                    comment,
                )
            elif not firststatement.left.equals(secondstatement.right):
                self.logstep(
                    self.log_notsamestatement.format(
                        self.coimplication_intro_name.upper(),
                        firststatement.left,
                        secondstatement.right,
                    )
                )
                self.stopproof(
                    self.stopped_notsamestatement,
                    self.blankstatement,
                    self.coimplication_intro_name,
                    self.reflines(left, right),
                    "",
                    comment,
                )
            elif not firststatement.right.equals(secondstatement.left):
                self.logstep(
                    self.log_notsamestatement.format(
                        self.coimplication_intro_name.upper(),
                        firststatement.right,
                        secondstatement.left,
                    )
                )
                self.stopproof(
                    self.stopped_notsamestatement,
                    self.blankstatement,
                    self.coimplication_intro_name,
                    self.reflines(right, left),
                    "",
                    comment,
                )

        # If no errors, perform task
        if self.canproceed():
            newstatement = Iff(firststatement.left, firststatement.right)
            self.logstep(
                self.log_coimplication_intro.format(
                    self.coimplication_intro_name.upper(),
                    newstatement,
                    firststatement.left,
                    firststatement.right,
                )
            )
            newcomment = self.iscomplete(newstatement, comment)
            self.lines.append(
                [
                    newstatement,
                    self.level,
                    self.currentproofid,
                    self.coimplication_intro_name,
                    self.reflines(left, right),
                    "",
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(newstatement, self.coimplication_intro_tag)

    def conjunction_elim(self, line: int, side: str, comment: str = ""):
        """One of the conjuncts, either the left side or the right side, is derived from a conjunction.

        Parameters:
            line: The line number of the conjunction to be split.
            side: The side, either left or right, from which the conjunct will be derived.
            comment: An optional comment the user may add to this line of the proof.

        Examples:
            The first example shows not only conjunction elimination, but also
            conjunction introduction and coimplication introduction.  For `conjunction_elim`
            not the use of `prf.left` and `prf.right`.  These values are defined
            in the Proof object so you don't have to remember what the strings are.

            >>> from altrea.wffs import And, Implies, Iff, Wff
            >>> from altrea.rules import Proof
            >>> prf = Proof()
            >>> A = prf.proposition('A')
            >>> B = prf.proposition('B')
            >>> prf.setlogic()
            >>> prf.goal(Iff(And(A, B), And(B, A)))
            >>> prf.hypothesis(And(A, B))
            >>> prf.conjunction_elim(1, prf.left)
            >>> prf.conjunction_elim(1, prf.right)
            >>> prf.conjunction_intro(3, 2, comment='Reverse the order of the conjuncts.')
            >>> prf.implication_intro(comment='This gives us the first implication.')
            >>> prf.hypothesis(And(B, A))
            >>> prf.conjunction_elim(6, prf.left)
            >>> prf.conjunction_elim(6, prf.right)
            >>> prf.conjunction_intro(8, 7, comment='The order is reversed.')
            >>> prf.implication_intro(comment='This gives us the second implication.')
            >>> prf.coimplication_intro(5, 10)
            >>> prf.displayproof(short=1, latex=0)
                              Item  ...                                Comment
                (A & B) <> (B & A)  ...
            1            A & B __|  ...
            2                A   |  ...
            3                B   |  ...
            4            B & A   |  ...    Reverse the order of the conjuncts.
            5    (A & B) > (B & A)  ...   This gives us the first implication.
            6            B & A __|  ...
            7                B   |  ...
            8                A   |  ...
            9            A & B   |  ...                 The order is reversed.
            10   (B & A) > (A & B)  ...  This gives us the second implication.
            11  (A & B) <> (B & A)  ...                               COMPLETE

        See Also:
            - `conjunction_intro`
            - `coimplication_intro`
        """

        # Look for general errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.conjunction_elim_name,
                self.conjunction_elim_name,
                comment,
            ):
                if self.goodline(
                    line,
                    self.conjunction_elim_name,
                    self.conjunction_elim_name,
                    comment,
                ):
                    pass

        # Look for specific errors
        if self.canproceed():
            statement = self.getstatement(line)
            if type(statement) != And:
                self.logstep(
                    self.log_notconjunction.format(
                        self.conjunction_elim_name.upper(), statement, line
                    )
                )
                self.stopproof(
                    self.stopped_notconjunction,
                    self.blankstatement,
                    self.conjunction_elim_name,
                    str(line),
                    "",
                    comment,
                )
            elif side not in [self.label_left, self.label_right]:
                self.logstep(
                    self.log_sidenotselected.format(
                        self.conjunction_elim_name.upper(), side
                    )
                )
                self.stopproof(
                    self.stopped_sidenotselected,
                    self.blankstatement,
                    self.conjunction_elim_name,
                    str(line),
                    "",
                    comment,
                )

        # If no errors, perform the task
        if self.canproceed():
            if side == self.label_left:
                conjunct = statement.left
            else:
                conjunct = statement.right
            self.logstep(
                self.log_conjunction_elim.format(
                    self.conjunction_elim_name.upper(), conjunct, statement, line
                )
            )
            newcomment = self.iscomplete(conjunct, comment)
            self.lines.append(
                [
                    conjunct,
                    self.level,
                    self.currentproofid,
                    self.conjunction_elim_name,
                    str(line),
                    "",
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(conjunct, self.conjunction_elim_tag)

    def conjunction_intro(self, left: int, right: int, comment: str = ""):
        """The statement referenced by the first line number (left) is joined as a conjunct
        to the statement referenced by the second line number (right).

        There are two conjuncts for a conjunction.  The statement referenced by the
        first line number will go on the left side of the conjunction.  The statement
        referenced by the second line number will go on the right side of the conjunction.

        Parameters:
            left: The line number of the first conjunct which will appear on the left side
                of the conjunction.
            right: The line number of the second conjunct which will appear on the right side
                of the conjunction.
            comment: An optional comment the user may add to this line of the proof.

        Examples:

            The goal is "B & A".  Since "B" is on line 2, put 2 as the first input value.
            Since "A" is on line 1, put 1 as the second input value.  The `displayproof` function
            shows which lines these are.  It is helpful as one rights the proofs to have that at the
            bottom of the proof.  In a Jupyter Notebook where latex can be used it may be
            helpful to set latex=1.

            >>> from altrea. import And
            >>> from altrea.rules import Proof
            >>> prf = Proof()
            >>> A = prf.proposition('A')
            >>> B = prf.proposition('B')
            >>> prf.setlogic()
            >>> prf.goal(And(B, A))
            >>> prf.premise(A)
            >>> prf.premise(B)
            >>> prf.conjunction_intro(2, 1)
            >>> prf.displayproof(short=1, latex=0)
                Item                     Rule   Comment
               B & A                     GOAL
            1      A                  Premise
            2      B                  Premise
            3  B & A  2, 1, Conjunction Intro  COMPLETE

            This example shows that an obvious result can be derived by letting the first and second lines be the same.

            >>> from altrea.wffs import And, Wff
            >>> from altrea.rules import Proof
            >>> prf = Proof()
            >>> A = prf.proposition('A')
            >>> prf.setlogic()
            >>> prf.goal(And(A, A))
            >>> prf.premise(A)
            >>> prf.conjunction_intro(1, 1)
            >>> prf.displayproof(short=1, latex=0)
                Item                     Rule   Comment
               A & A                     GOAL
            1      A                  Premise
            2  A & A  1, 1, Conjunction Intro  COMPLETE

        See Also:
            - `conjunction_elim`
        """

        # Look for errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.conjunction_intro_name,
                self.conjunction_intro_name,
                comment,
            ):
                if self.goodline(
                    left,
                    self.conjunction_intro_name,
                    self.conjunction_intro_name,
                    comment,
                ):
                    if self.goodline(
                        right,
                        self.conjunction_intro_name,
                        self.conjunction_intro_name,
                        comment,
                    ):
                        pass

        # If no errors, perform task
        if self.canproceed():
            leftconjunct = self.getstatement(left)
            rightconjunct = self.getstatement(right)
            andstatement = And(leftconjunct, rightconjunct)
            self.logstep(
                self.log_conjunction_intro.format(
                    self.conjunction_intro_name.upper(),
                    andstatement,
                    leftconjunct,
                    left,
                    rightconjunct,
                    right,
                )
            )
            newcomment = self.iscomplete(andstatement, comment)
            self.lines.append(
                [
                    andstatement,
                    self.level,
                    self.currentproofid,
                    self.conjunction_intro_name,
                    self.reflines(left, right),
                    "",
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(andstatement, self.conjunction_intro_tag)

    def definition(
        self, name: str, subslist: list, premiselist: list, comment: str = ""
    ):
        """Various axioms may be invoked here such as the law of excluded middle.

        Parameters:
            name: The name of the axiom one wishes to use.
            premiselist: This is a set of line numbers referencing one side of the definition.  Usually there is only one
                such line number, but putting them in a list allows for more than one.
            subslist: An arbitrary long list of substitutions that will be made into the retrieved definition string
                before forming the object and testing whether the definition matches lines in the proof.
            comment: An optional comment the user may add to this line of the proof.

        Examples:

        """

        # Look for errors: Find the definitions
        if self.canproceed():
            foundindex = -1
            for i in range(len(self.logicdefinitions)):
                if self.logicdefinitions[i][0] == name:
                    foundindex = i
                    break
            if foundindex < 0:
                self.logstep(
                    self.log_nosuchdefinition.format(self.definition_name.upper(), name)
                )
                self.stopproof(
                    self.stopped_nosuchdefinition,
                    self.blankstatement,
                    name,
                    "",
                    "",
                    comment,
                )
            else:
                definition = self.logicdefinitions[foundindex][1]
                displayname = self.logicdefinitions[foundindex][2]
                description = self.logicdefinitions[foundindex][3]

        # Look for errors: Check the substitution values.
        if self.canproceed():
            subs = self.checksubs(
                self.definition_name.upper(), displayname, comment, subslist
            )

        # Look for errors: Check lines entered from the proof.
        if self.canproceed():
            matchpremiselist, lineslist = self.checkitemlines(
                self.definition_name.upper(), displayname, comment, premiselist
            )

        # Look for errors: Try to make the requested substitutions.
        if self.canproceed():
            conclusionpremises = self.substitute(definition, subs, displayname)

        # Look for errors: Check that the premises match the identified proof lines.
        if self.canproceed():
            self.checkpremises(
                self.definition_name.upper(),
                displayname,
                comment,
                conclusionpremises.premises,
                matchpremiselist,
            )

        # If no errors, perform task.
        if self.canproceed():
            self.logstep(
                self.log_definition.format(
                    self.definition_name.upper(),
                    conclusionpremises.conclusion,
                    description,
                )
            )
            newcomment = self.iscomplete(conclusionpremises.conclusion, comment)
            self.lines.append(
                [
                    conclusionpremises.conclusion,
                    self.level,
                    self.currentproofid,
                    displayname,
                    self.reflines(*lineslist),
                    "",
                    newcomment,
                    self.linetype_definition,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(conclusionpremises.conclusion, displayname)

    def disjunction_elim(
        self,
        disjunction_line: int,
        left_implication_line: int,
        right_implication_line: int,
        comment: str = "",
    ):
        """This rule take a disjunction and two implications with antecedents on each side of the disjunction.
        If the two implications reach the same conclusion, then that conclusion may be derived.

        Parameters:
            disjunction_line: The line number where the disjunction is an item.
            left_implication_line: The line number of the implication starting with the left side of the disjunction.
            right_implication_line: The line number of the implication starting with the right side of the disjunction.
            comment: An optional comment the user may add to this line of the proof.

        Examples:
            The first example shows that a trivial result can be derived.  If we have A or A and we want to derive just A,
            we can generate an implication by starting a subordinate proof with A as the hypothesis.  We can then
            close that proof with an implication introduction.  Since A is on both sides of the disjunction,
            we can refer to the same subordinate proof twice in the use of disjunction elimination.

            >>> from altrea.wffs import Or, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof, showlines
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> C = Wff('C')
            >>> prf.setlogic()
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

            >>> from altrea.wffs import Or, Implies, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof, showlines
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> C = Wff('C')
            >>> prf.setlogic()
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

        # Look for general errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.disjunction_elim_name,
                self.disjunction_elim_name,
                comment,
            ):
                if self.goodline(
                    disjunction_line,
                    self.disjunction_elim_name,
                    self.disjunction_elim_name,
                    comment,
                ):
                    if self.goodline(
                        left_implication_line,
                        self.disjunction_elim_name,
                        self.disjunction_elim_name,
                        comment,
                    ):
                        if self.goodline(
                            right_implication_line,
                            self.disjunction_elim_name,
                            self.disjunction_elim_name,
                            comment,
                        ):
                            pass

        # Look for specific errors
        if self.canproceed():
            disjunction = self.getstatement(disjunction_line)
            left_implication = self.getstatement(left_implication_line)
            right_implication = self.getstatement(right_implication_line)
            if type(disjunction) != Or:
                self.logstep(
                    self.log_notdisjunction.format(
                        self.disjunction_elim_name.upper(),
                        disjunction,
                        disjunction_line,
                    )
                )
                self.stopproof(
                    self.stopped_notdisjunction,
                    self.blankstatement,
                    self.disjunction_elim_name,
                    str(disjunction_line),
                    "",
                    comment,
                )
            elif type(left_implication) != Implies:
                self.logstep(
                    self.log_notimplication.format(
                        self.disjunction_elim_name.upper(),
                        left_implication,
                        left_implication_line,
                    )
                )
                self.stopproof(
                    self.stopped_notimplication,
                    self.blankstatement,
                    self.disjunction_elim_name,
                    str(left_implication_line),
                    "",
                    comment,
                )
            elif type(right_implication) != Implies:
                self.logstep(
                    self.log_notimplication.format(
                        self.disjunction_elim_name.upper(),
                        right_implication,
                        right_implication_line,
                    )
                )
                self.stopproof(
                    self.stopped_notimplication,
                    self.blankstatement,
                    self.disjunction_elim_name,
                    str(right_implication_line),
                    "",
                    comment,
                )
            elif (
                not right_implication.right.equals(left_implication.right)
                and type(right_implication.right) != Falsehood
                and type(left_implication.right) != Falsehood
            ):
                self.logstep(
                    self.log_notsamestatement.format(
                        self.disjunction_elim_name.upper(),
                        left_implication.right,
                        right_implication.right,
                    )
                )
                self.stopproof(
                    self.stopped_notsamestatement,
                    self.blankstatement,
                    self.disjunction_elim_name,
                    self.reflines(left_implication_line, right_implication_line),
                    "",
                    comment,
                )

        # With no errors, perform task
        if self.canproceed():
            if type(right_implication.right) != Falsehood:
                statement = right_implication.right
            else:
                statement = left_implication.right
            self.logstep(
                self.log_disjunction_elim.format(
                    self.disjunction_elim_name.upper(),
                    statement,
                    disjunction,
                    disjunction_line,
                )
            )
            newcomment = self.iscomplete(statement, comment)
            self.lines.append(
                [
                    statement,
                    self.level,
                    self.currentproofid,
                    self.disjunction_elim_name,
                    self.reflines(
                        disjunction_line, left_implication_line, right_implication_line
                    ),
                    "",
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(statement, self.disjunction_elim_tag)

    def disjunction_intro(
        self,
        line: int,
        left: Wff | int = None,
        right: Wff | int = None,
        negated: bool = True,
        comment: str = "",
    ):
        """The newdisjunct statement and the statement at the line number become a disjunction.

        Parameters:
            line: The line number of the statement that will be the other disjunct.
            left: A statement that will be used in the disjunction on the left side of the one
                referenced by the line.
            right: A state that will be used in the disjunction on the right side of the one
                referenced by the line.
            comment: An optional comment the user may add to this line of the proof.


        Examples:
            One can place the new statement on either the left side or the right side of the
            referenced statement.  The first example shows how this is done for the right side.

            >>> from altrea.wffs import Or, Implies, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof, showlines
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> C = Wff('C')
            >>> prf.setlogic()
            >>> prf.goal(Or(A, B))
            >>> prf.premise(A)
            >>> prf.disjunction_intro(1, right=B)
            >>> showproof(prFalsehood, latex=0)
                Item                Reason   Comment
            0  A | B                  GOAL
            1      A               Premise
            2  A | B  1, Disjunction Intro  COMPLETE

            The second example shows how this is done for the left side.

            >>> from altrea.wffs import Or, Implies, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof, showlines
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> C = Wff('C')
            >>> prf.setlogic()
            >>> prf.goal(Or(A, B))
            >>> prf.premise(B)
            >>> prf.disjunction_intro(1, left=A)
            >>> showproof(prFalsehood, latex=0)
                Item                Reason   Comment
            0  A | B                  GOAL
            1      B               Premise
            2  A | B  1, Disjunction Intro  COMPLETE
        """

        # Look for general errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.disjunction_intro_name,
                self.disjunction_intro_name,
                comment,
            ):
                if self.goodline(
                    line,
                    self.disjunction_intro_name,
                    self.disjunction_intro_name,
                    comment,
                ):
                    if self.restricted:
                        if isinstance(left, int):
                            if self.goodline(
                                left,
                                self.disjunction_intro_name,
                                self.disjunction_intro_name,
                                comment,
                            ):
                                pass
                        elif isinstance(right, int):
                            if self.goodline(
                                right,
                                self.disjunction_intro_name,
                                self.disjunction_intro_name,
                                comment,
                            ):
                                pass
                        elif isinstance(left, Wff) or isinstance(right, Wff):
                            self.logstep(
                                self.log_restrictednowff.format(
                                    self.disjunction_intro_name, left, right
                                )
                            )
                            self.stopproof(
                                self.stopped_restrictednowff,
                                self.blankstatement,
                                self.disjunction_intro_name,
                                str(line),
                                "",
                                comment,
                            )

                    else:
                        if left is not None and self.goodobject(
                            left,
                            self.disjunction_intro_name,
                            self.disjunction_intro_name,
                            comment,
                        ):
                            pass
                        elif right is not None and self.goodobject(
                            right,
                            self.disjunction_intro_name,
                            self.disjunction_intro_name,
                            comment,
                        ):
                            pass

        # Look for specific errors
        if self.canproceed():
            statement = self.getstatement(line)
            if left is None and right is None:
                self.logstep(
                    self.log_novaluepassed.format(self.disjunction_intro_name.upper())
                )
                self.stopproof(
                    self.stopped_novaluepassed,
                    self.blankstatement,
                    self.disjunction_intro_name,
                    str(line),
                    "",
                    comment,
                )

        # If no errors, perform task
        if self.canproceed():
            if isinstance(left, int):
                if negated:
                    disjunction = Or(Not(self.getstatement(left)), statement)
                else:
                    disjunction = Or(self.getstatement(left), statement)
                self.logstep(
                    self.log_disjunction_intro.format(
                        self.disjunction_intro_name.upper(),
                        disjunction,
                        statement,
                        line,
                        self.label_left,
                        left,
                    )
                )
            elif isinstance(right, int):
                if negated:
                    disjunction = Or(statement, Not(self.getstatement(right)))
                else:
                    disjunction = Or(statement, self.getstatement(right))
                self.logstep(
                    self.log_disjunction_intro.format(
                        self.disjunction_intro_name.upper(),
                        disjunction,
                        statement,
                        line,
                        self.label_left,
                        left,
                    )
                )
            elif not self.restricted:
                if left is None:
                    disjunction = Or(statement, right)
                    self.logstep(
                        self.log_disjunction_intro.format(
                            self.disjunction_intro_name.upper(),
                            disjunction,
                            statement,
                            line,
                            self.label_right,
                            left,
                        )
                    )
                else:
                    disjunction = Or(left, statement)
                    self.logstep(
                        self.log_disjunction_intro.format(
                            self.disjunction_intro_name.upper(),
                            disjunction,
                            statement,
                            line,
                            self.label_left,
                            left,
                        )
                    )
            newcomment = self.iscomplete(disjunction, comment)
            self.lines.append(
                [
                    disjunction,
                    self.level,
                    self.currentproofid,
                    self.disjunction_intro_name,
                    str(line),
                    "",
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(disjunction, self.disjunction_intro_tag)

    # def falsehood(self, name: str, latex: str = ''):
    #     newfalsehood = Falsehood(name, latex)
    #     self.objectdictionary.update({name: newfalsehood})
    #     self.falsehoods.append([newfalsehood, name])
    #     howmany = len(self.falsehoods)
    #     self.logstep(f'TRUTH: The letter "{newfalsehood.name}" (latex: "{newfalsehood.latexname}") for a generic falsehood formula has been defined making {howmany} so far.')
    #     return newfalsehood

    def goal(self, goal: Wff, comment: str = ""):
        """Add a goal to the proof.  More than one goal can be assigned although generally
        only one goal is used and only one is needed.  Think of multiple goals as the
        conjuncts to a single goal.

        Parameters:
            goal: The goal to add to the proof.
            comment: An optional comment the user may add to this line of the proof.

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

            >>> from altrea.wffs import Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> prf.setlogic()
            >>> prf.goal(A)
            >>> prf.premise(A)
            >>> showproof(prFalsehood, latex=0)
              Item   Reason   Comment
            0    A     GOAL
            1    A  Premise  COMPLETE
        """

        # Look for errors
        if self.canproceed():
            if self.goodobject(goal, self.goal_name, self.goal_name, comment):
                if self.logicdatabase == "":
                    self.logstep(self.log_nologic.format(self.goal_name.upper()))
                    self.stopproof(
                        self.stopped_nologic,
                        self.blankstatement,
                        self.goal_name,
                        0,
                        0,
                        comment,
                    )

        # If no errors, perform task
        if self.canproceed():
            self.goals.append(str(goal))
            self.goalswff.append(goal)
            if self.goals_string == "":
                self.goals_string = str(goal)
            else:
                self.goals_string += "".join([", ", str(goal)])
            if self.goals_latex == "":
                self.goals_latex = goal.latex()
            else:
                self.goals_latex += "".join([", ", goal.latex()])
            self.lines[0][self.statementindex] = self.goals_string
            self.lines[0][self.ruleindex] = self.goal_name
            if self.lines[0][self.commentindex] == "":
                self.lines[0][self.commentindex] = comment
            elif comment != "":
                self.lines[0][self.commentindex] += "".join(
                    [self.dash_connector, comment]
                )
            self.logstep(self.log_goal.format(self.goal_name.upper(), goal))

    def hypothesis(self, hypothesis: Wff, comment: str = ""):
        """Open a uniquely identified subordinate proof with an hypothesis.

        Parameters:
            hypothesis: The hypothesis that starts the subproof of derived statements.
            comment: An optional comment the user may add to this line of the proof.

        Examples:

        See Also:
            - `addhypothesis`
            - `implication_intro`
        """

        # Look for errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.hypothesis_name,
                self.hypothesis_name,
                comment,
            ):
                if self.goodobject(
                    hypothesis, self.hypothesis_name, self.hypothesis_name, comment
                ):
                    if not self.checkhasgoal():
                        self.logstep(
                            self.log_nogoal.format(
                                self.hypothesis_name.upper(), hypothesis
                            )
                        )
                        self.stopproof(
                            self.stopped_nogoal,
                            self.blankstatement,
                            self.hypothesis_name,
                            "",
                            "",
                            comment,
                        )

        # If no errors, perform task
        if self.canproceed():
            self.level += 1
            self.subproofchain = "".join(
                [self.label_subproofnormal, self.subproofchain]
            )
            nextline = len(self.lines)
            self.currentproof = [nextline]
            self.currenthypotheses = [nextline]
            self.subproof_status = self.subproof_normal
            self.prooflist.append(
                [
                    self.level,
                    self.currentproof,
                    self.currentproofid,
                    self.currenthypotheses,
                    self.subproofchain,
                ]
            )
            self.previousproofid = self.currentproofid
            self.previousproofchain.append(self.currentproofid)
            self.currentproofid = len(self.prooflist) - 1
            self.logstep(
                self.log_hypothesis.format(
                    self.hypothesis_name.upper(), self.currentproofid, hypothesis
                )
            )
            newcomment = self.iscomplete(hypothesis, comment)
            self.lines.append(
                [
                    hypothesis,
                    self.level,
                    self.currentproofid,
                    self.hypothesis_name,
                    "",
                    "",
                    newcomment,
                    self.linetype_hypothesis,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(hypothesis, self.hypothesis_tag)

    def implication_elim(self, first: int, second: int, comment: str = ""):
        """From an implication and its antecedent derive the consequent.

        Parameters:
            first: The line number of the first statement. This is either the implication or the antecedent.
            second: The line number of the second statement.  This is either the implication or the antecedent.
            comment: An optional comment the user may add to this line of the proof.

        Examples:
            Implication elimination is also called "Modus Ponens".  If you have "A" and "A > B" then from both of them
            you can derive "B".

            >>> from altrea.wffs import Implies
            >>> from altrea.rules import Proof
            >>> pr = Proof()
            >>> A = pr.proposition('A')
            >>> B = pr.proposition('B')
            >>> pr.setlogic()
            >>> pr.goal(B)
            >>> pr.premise(A)
            >>> pr.premise(Implies(A, B))
            >>> pr.implication_elim(1, 2)
            >>> pr.displayproof(short=1, latex=0)
                Item                    Rule   Comment
                B                    GOAL
            1      A                 Premise
            2  A > B                 Premise
            3      B  1, 2, Implication Elim  COMPLETE
        """

        # Look for general errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.implication_elim_name,
                self.implication_elim_name,
                comment,
            ):
                if self.goodline(
                    first,
                    self.implication_elim_name,
                    self.implication_elim_name,
                    comment,
                ):
                    if self.goodline(
                        second,
                        self.implication_elim_name,
                        self.implication_elim_name,
                        comment,
                    ):
                        pass

        # Look for specific errors
        if self.canproceed():
            firststatement = self.getstatement(first)
            secondstatement = self.getstatement(second)
            if type(firststatement) == Implies and type(secondstatement) == Implies:
                if not firststatement.left.equals(
                    secondstatement
                ) and not secondstatement.left.equals(firststatement):
                    self.logstep(
                        self.log_notantecedent.format(
                            self.implication_elim_name.upper(),
                            firststatement,
                            secondstatement,
                        )
                    )
                    self.logstep(
                        self.log_notantecedent.format(
                            self.implication_elim_name.upper(),
                            secondstatement,
                            firststatement,
                        )
                    )
                    self.stopproof(
                        self.stopped_notantecedent,
                        self.blankstatement,
                        self.implication_elim_name,
                        self.reflines(first, second),
                        "",
                        comment,
                    )
            elif type(firststatement) == Implies and not secondstatement.equals(
                firststatement.left
            ):
                self.logstep(
                    self.log_notantecedent.format(
                        self.implication_elim_name.upper(),
                        firststatement,
                        secondstatement,
                    )
                )
                self.stopproof(
                    self.stopped_notantecedent,
                    self.blankstatement,
                    self.implication_elim_name,
                    self.reflines(first, second),
                    "",
                    comment,
                )
            elif type(secondstatement) == Implies and not firststatement.equals(
                secondstatement.left
            ):
                self.logstep(
                    self.log_notantecedent.format(
                        self.implication_elim_name.upper(),
                        secondstatement,
                        firststatement,
                    )
                )
                self.stopproof(
                    self.stopped_notantecedent,
                    self.blankstatement,
                    self.implication_elim_name,
                    self.reflines(first, second),
                    "",
                    comment,
                )
            elif type(firststatement) != Implies and type(secondstatement) != Implies:
                self.logstep(
                    self.log_notmodusponens.format(
                        self.implication_elim_name.upper(),
                        firststatement,
                        first,
                        secondstatement,
                        second,
                    )
                )
                self.stopproof(
                    self.stopped_notmodusponens,
                    self.blankstatement,
                    self.implication_elim_name,
                    self.reflines(first, second),
                    "",
                    comment,
                )

        # If no errors, perform task
        if self.canproceed():
            if type(firststatement) == Implies and type(secondstatement) == Implies:
                if str(firststatement) == str(secondstatement.left):
                    statement = secondstatement.right
                    self.logstep(
                        self.log_implication_elim.format(
                            self.implication_elim_name.upper(),
                            secondstatement.right,
                            secondstatement,
                            firststatement,
                        )
                    )
                else:
                    statement = firststatement.right
                    self.logstep(
                        self.log_implication_elim.format(
                            self.implication_elim_name.upper(),
                            firststatement.right,
                            firststatement,
                            secondstatement,
                        )
                    )
            elif type(firststatement) == Implies:
                statement = firststatement.right
                self.logstep(
                    self.log_implication_elim.format(
                        self.implication_elim_name.upper(),
                        firststatement.right,
                        firststatement,
                        secondstatement,
                    )
                )
            else:
                statement = secondstatement.right
                self.logstep(
                    self.log_implication_elim.format(
                        self.implication_elim_name.upper(),
                        secondstatement.right,
                        secondstatement,
                        firststatement,
                    )
                )
            newcomment = self.iscomplete(statement, comment)
            self.lines.append(
                [
                    statement,
                    self.level,
                    self.currentproofid,
                    self.implication_elim_name,
                    self.reflines(first, second),
                    "",
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(statement, self.implication_elim_tag)

    def implication_intro(self, comment: str = ""):
        """From a subproof derive the implication where the antecendent is the hypotheses of subproof joined as conjuncts and the
        consequent is the last line of the proof so far entered.  In the process of deriving the implication as an item of the
        proof, the subproof is closed.

        Parameters:
            comment: An optional comment the user may add to this line of the proof.

        Examples:
            The following example shows that using these inference rules and given the conclusion "B" as a premise then
            any statement whatsoever, call it "A", can be used as the antecedent of the conditional.  It also illustrates how the
            `displaylog` function can provide additional information about the proof.

            >>> from altrea.wffs import Implies, Wff
            >>> from altrea.rules import Proof
            >>> prf = Proof()
            >>> A = prf.proposition('A')
            >>> B = prf.proposition('B')
            >>> prf.setlogic()
            >>> prf.goal(Implies(A, B))
            >>> prf.premise(B)
            >>> prf.hypothesis(A)
            >>> prf.reiterate(1)
            >>> prf.implication_intro()
            >>> prf.displaylog()
            0 PROOF: A proof named "" or "" with description "" has been started.
            1 PROPOSITION: The letter "A" for a generic well-formed formula has been defined with 1 so far for this proof.
            2 PROPOSITION: The letter "B" for a generic well-formed formula has been defined with 2 so far for this proof.
            3 SET LOGIC: "" has been selected as the logic described as "No Description" and stored in database "No Database".
            4 GOAL: The goal "A > B" has been added to the goals.
            5 PREMISE: Item "B" has been added to the premises.
            6 HYPOTHESIS: A new subproof 1 has been started with item "A".
            7 REITERATION: Item "B" on line 1 has been reiterated into subproof 1.
            8 IMPLICATION INTRO: Item "A > B" has been derived upon closing subproof 1.
            9 The proof is complete.
            >>> prf.displayproof(latex=0)
                Item  Level  Proof               Rule Type Lines Proofs   Comment
            A > B      0      0               GOAL
            1      B      0      0            Premise   PR
            2  A __|      1      1         Hypothesis    H
            3  B   |      1      1        Reiteration          1
            4  A > B      0      0  Implication Intro   TR          2-3  COMPLETE

            The following simple example is called the "Reflexitiy of Implication".  Note how the subordinate proof
            contained only one line, the hypothesis.  The hypothesis became both the antecedent and, since it was the last
            line of the subordinate proof, the consequent of the implication.

            >>> from altrea.wffs import Implies, Wff
            >>> from altrea.rules import Proof
            >>> prf = Proof()
            >>> A = prf.proposition('A')
            >>> prf.setlogic()
            >>> prf.goal(Implies(A, A), 'Reflexivity of Implication')
            >>> prf.hypothesis(A)
            >>> prf.implication_intro()
            >>> prf.displayproof(short=1, latex=0)
                Item                    Rule                     Comment
               A > A                    GOAL  Reflexivity of Implication
            1  A __|              Hypothesis
            2  A > A  1-1, Implication Intro                    COMPLETE

            The next example shows how one can create a subproof of a subproof since each call to
            this function opens a new subproof which has to be closed by `implication_intro`
            at some later point.  Reiteration is also important for subproofs.  Although
            any line within a specific proof itself can be used by the proof, not every line
            from outside of it can be used.  A call to `reiterate` makes sure only lines
            are used from a chain of proofs leading to the current one.

            >>> from altrea.wffs import Implies, Wff
            >>> from altrea.rules import Proof
            >>> prf = Proof()
            >>> A = prf.proposition('A')
            >>> B = prf.proposition('B')
            >>> prf.setlogic()
            >>> prf.goal(Implies(A, Implies(B, A)), 'Conditioned Repetition')
            >>> prf.hypothesis(A)
            >>> prf.hypothesis(B)
            >>> prf.reiterate(1)
            >>> prf.implication_intro()
            >>> prf.implication_intro()
            >>> prf.displayproof(short=1, latex=0)
                    Item                    Rule                 Comment
            A > (B > A)                    GOAL  Conditioned Repetition
            1        A __|              Hypothesis
            2    B __|   |              Hypothesis
            3    A   |   |          1, Reiteration
            4    B > A   |  2-3, Implication Intro
            5  A > (B > A)  1-4, Implication Intro                COMPLETE

            This example shows the rule of distribution.  Like the previous exampeles it does not require any premises.

            On the Jupyter Lab Terminal the width is truncated with "...".  Running this in a Jupyter Lab Notebook will show the full table.
            One can then set latex=1 rather than latex=0 on `displayproof`.  By setting short=0 one can see all of the data that is
            stored for each line of a proof.

            >>> from altrea.wffs import Implies, Wff
            >>> from altrea.rules import Proof
            >>> prf = Proof()
            >>> prf.setlogic()
            >>> A = prf.proposition('A')
            >>> B = prf.proposition('B')
            >>> C = prf.proposition('C')
            >>> prf.goal(Implies(Implies(A, Implies(B, C)), (Implies(Implies(A, B), Implies(A, C)))), comment='Rule of Distribution')
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
            >>> prf.displayproof(short=1, latex=0)
                                            Item  ...               Comment
                (A > (B > C)) > ((A > B) > (A > C))  ...  Rule of Distribution
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

        See Also:
            - `hypothesis`
            - `implication_elim`
            - `reiterate`
        """

        # Look for errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.implication_intro_name,
                self.implication_intro_name,
                comment,
            ):
                if self.currentproofid == 0:
                    self.logstep(
                        self.log_closemainproof.format(
                            self.implication_intro_name.upper()
                        )
                    )
                    self.stopproof(
                        self.stopped_closemainproof,
                        self.blankstatement,
                        self.implication_intro_name,
                        "",
                        "",
                    )

        # If no errors, perform task
        if self.canproceed():
            proofid = self.currentproofid
            subproof_status = self.subproof_status
            self.prooflist[self.currentproofid][1].append(len(self.lines) - 1)
            self.level -= 1
            self.subproofchain = self.subproofchain[3:]
            antecedent, consequent, previousproofid, previoussubproofstatus = (
                self.getproof(self.currentproofid)
            )
            self.currentproofid = previousproofid
            self.subproof_status = previoussubproofstatus
            self.currentproof = self.prooflist[previousproofid][1]
            if len(self.previousproofchain) > 1:
                self.previousproofchain.pop(len(self.previousproofchain) - 1)
                self.previousproofid = self.previousproofchain[
                    len(self.previousproofchain) - 1
                ]
            else:
                self.previousproofchain = []
                self.previousproofid = -1
            implication = Implies(antecedent, consequent)
            if subproof_status == self.subproof_strict:
                name = self.implication_intro_strict_name
                message = self.log_implication_intro_strict
            else:
                name = self.implication_intro_name
                message = self.log_implication_intro
            self.logstep(message.format(name.upper(), implication, proofid))
            newcomment = self.iscomplete(implication, comment)
            self.lines.append(
                [
                    implication,
                    self.level,
                    self.currentproofid,
                    name,
                    "",
                    self.refproof(proofid),
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(implication, self.implication_intro_strict_tag)

    def necessary_elim(self, line: int, comment: str = ""):
        """Removes the necessary connector from an item.

        Parameters:
            line: The line on which the item appears.
            comment: An optional comment the user may add to this line of the proof.

        Examples:

        """

        # Look for general errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.necessary_elim_name,
                self.necessary_elim_name,
                comment,
            ):
                if self.goodline(
                    line, self.necessary_elim_name, self.necessary_elim_name, comment
                ):
                    pass

        # Look for specific errors
        if self.canproceed():
            statement = self.getstatement(line)
            if type(statement) != Necessary:
                self.logstep(
                    self.log_notnecessary.format(
                        self.necessary_elim_name.upper(), statement, line
                    )
                )
                self.stopproof(
                    self.stopped_notnecessary,
                    self.blankstatement,
                    self.necessary_elim_name,
                    str(line),
                    "",
                    comment,
                )

        # If no errors, perform task
        if self.canproceed():
            self.logstep(
                self.log_necessary_elim.format(
                    self.necessary_elim_name.upper(), statement.wff, statement, line
                )
            )
            newcomment = self.iscomplete(statement.wff, comment)
            self.lines.append(
                [
                    statement.wff,
                    self.level,
                    self.currentproofid,
                    self.necessary_elim_name,
                    str(line),
                    "",
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(statement.wff, self.necessary_elim_tag)

    def necessary_intro(self, lines, comment: str = ""):
        """Closes a strict subproof with a necessary consequence.

        Parameters:
            comment: An optional comment the user may add to this line of the proof.

        Examples:
        """

        # Look for general errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.necessary_intro_name,
                self.necessary_intro_name,
                comment,
            ):
                if len(lines) == 0:
                    self.logstep(
                        self.log_nolines.format(
                            self.necessary_intro_name.upper(), lines
                        )
                    )
                    self.stopproof(
                        self.stopped_nolines,
                        self.blankstatement,
                        self.necessary_intro_name,
                        "",
                        "",
                        comment,
                    )
                else:
                    for i in lines:
                        if not self.goodline(
                            i,
                            self.necessary_intro_name,
                            self.necessary_intro_name,
                            comment,
                        ):
                            break

        # Look for specific errors
        if self.canproceed():
            if self.subproof_status != self.subproof_strict:
                self.logstep(
                    self.log_notstrictsubproof.format(
                        self.necessary_intro_name.upper(),
                        self.subproof_status,
                        self.subproof_strict,
                    )
                )
                self.stopproof(
                    self.stopped_notstrictsubproof,
                    self.blankstatement,
                    self.necessary_intro_name,
                    "",
                    "",
                    comment,
                )

        # If no errors, perform task
        if self.canproceed():
            # proofid = self.currentproofid
            self.prooflist[self.currentproofid][1].append(len(self.lines) - 1)
            self.level -= 1
            self.subproofchain = self.subproofchain[3:]
            # antecedent, consequent, previousproofid = self.getproof(self.currentproofid)
            previousproofid = self.getpreviousproofid(self.currentproofid)
            self.currentproofid = previousproofid
            self.currentproof = self.prooflist[previousproofid][1]
            if len(self.previousproofchain) > 1:
                self.previousproofchain.pop(len(self.previousproofchain) - 1)
                self.previousproofid = self.previousproofchain[
                    len(self.previousproofchain) - 1
                ]
            else:
                self.previousproofchain = []
                self.previousproofid = -1
            for i in lines:
                statement = self.getstatement(i)
                necessarystatement = Necessary(statement)
                self.logstep(
                    self.log_necessary_intro.format(
                        self.negation_intro_name.upper(), necessarystatement, statement
                    )
                )
                newcomment = self.iscomplete(necessarystatement, comment)
                self.lines.append(
                    [
                        necessarystatement,
                        self.level,
                        self.currentproofid,
                        self.necessary_intro_name,
                        self.reflines(i),
                        "",
                        newcomment,
                        self.linetype_transformationrule,
                        self.subproofchain,
                    ]
                )
                self.appendproofdata(necessarystatement, self.necessary_intro_tag)

    def negation_elim(self, first: int, second: int, comment: str = ""):
        """When two statements are contradictory a false line can be derived.

        Parameters:
            first: The line number of the first statement.
            second: The line number of the second statement.
            comment: An optional comment the user may add to this line of the proof.

        Examples:
            >>> from altrea. import And, Not, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof
            >>> prf = Proof()
            >>> A = Wff('A')
            >>> prf.setlogic()
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

        # Look for general errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.negation_elim_name,
                self.negation_elim_name,
                comment,
            ):
                if self.goodline(
                    first, self.negation_elim_name, self.negation_elim_name, comment
                ):
                    if self.goodline(
                        second,
                        self.negation_elim_name,
                        self.negation_elim_name,
                        comment,
                    ):
                        pass

        # Look for specific errors
        if self.canproceed():
            firststatement = self.getstatement(first)
            secondstatement = self.getstatement(second)
            if not Not(firststatement).equals(secondstatement) and not Not(
                secondstatement
            ).equals(firststatement):
                self.logstep(
                    self.log_notcontradiction.format(
                        self.negation_elim_name.upper(),
                        firststatement,
                        first,
                        secondstatement,
                        second,
                    )
                )
                self.stopproof(
                    self.stopped_notcontradiction,
                    self.blankstatement,
                    self.negation_elim_name,
                    self.reflines(first, second),
                    "",
                    comment,
                )

        # If no errors, perform task
        if self.canproceed():
            falsehood = Falsehood(And(firststatement, secondstatement))
            self.logstep(
                self.log_negation_elim.format(
                    self.negation_elim_name.upper(),
                    falsehood,
                    firststatement,
                    first,
                    secondstatement,
                    second,
                )
            )
            newcomment = self.iscomplete(falsehood, comment)
            self.lines.append(
                [
                    falsehood,
                    self.level,
                    self.currentproofid,
                    self.negation_elim_name,
                    self.reflines(first, second),
                    "",
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(falsehood, self.negation_elim_tag)

    def negation_intro(self, comment: str = ""):
        """This rule closes a subordinate proof that ends in a contradiction by negating the hypotheses of
        the subordinate proof.

        Parameters:
            comment: An optional comment the user may add to this line of the proof.

        Examples:
            The following example is known as modus tollens.

            >>> from altrea.wffs import Implies, Not, Wff
            >>> from altrea.rules import Proof
            >>> from altrea.display import showproof
            >>> A = Wff('A')
            >>> B = Wff('B')
            >>> prf = Proof()
            >>> prf.setlogic()
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

        # Look for general errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.negation_intro_name,
                self.negation_intro_name,
                comment,
            ):
                previousstatement = self.lines[len(self.lines) - 1][self.statementindex]
                if type(previousstatement) == Implies:
                    if type(previousstatement.right) != Falsehood:
                        #     pass
                        # else:
                        self.logstep(
                            self.log_notfalse.format(
                                self.negation_intro_name.upper(),
                                previousstatement,
                                len(self.lines) - 1,
                            )
                        )
                        self.stopproof(
                            self.stopped_notfalse,
                            self.blankstatement,
                            self.negation_intro_name,
                            str(len(self.lines) - 1),
                            "",
                            comment,
                        )
                else:
                    self.logstep(
                        self.log_notimplication.format(
                            self.negation_intro_name.upper(),
                            previousstatement,
                            len(self.lines) - 1,
                        )
                    )
                    self.stopproof(
                        self.stopped_notimplication,
                        self.blankstatement,
                        self.negation_intro_name,
                        str(len(self.lines) - 1),
                        "",
                        comment,
                    )

        # If no errors, perform task
        if self.canproceed():
            negation = Not(previousstatement.left)
            self.logstep(
                self.log_negation_intro.format(
                    self.negation_intro_name.upper(), negation, previousstatement.left
                )
            )
            newcomment = self.iscomplete(negation, comment)
            self.lines.append(
                [
                    negation,
                    self.level,
                    self.currentproofid,
                    self.negation_intro_name,
                    "",
                    "",
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproof_status,
                ]
            )
            self.appendproofdata(negation, self.negation_intro_tag)

    def possibly_elim(self, comment: str = ""):
        """Closes a strict subproof with a possibly consequence.

        Parameters:
            comment: An optional comment the user may add to this line of the proof.

        Examples:
        """

        # Look for general errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.possibly_elim_name,
                self.possibly_elim_name,
                comment,
            ):
                pass
                # if len(lines) == 0:
                #     self.logstep(self.log_nolines.format(self.possibly_elim_name.upper(),
                #                                          lines))
                #     self.stopproof(self.stopped_nolines,
                #                    self.blankstatement,
                #                    self.possibly_elim_name,
                #                '',
                #                '',
                #                comment)
                # else:
                #     for i in lines:
                #         if not self.goodline(i,
                #                              self.possibly_elim_name,
                #                              self.possibly_elim_name,
                #                              comment):
                #             break

        # Look for specific errors
        if self.canproceed():
            if self.subproof_status != self.subproof_strict:
                self.logstep(
                    self.log_notstrictsubproof.format(
                        self.possibly_elim_name.upper(),
                        self.subproof_status,
                        self.subproof_strict,
                    )
                )
                self.stopproof(
                    self.stopped_notstrictsubproof,
                    self.blankstatement,
                    self.possibly_elim_name,
                    "",
                    "",
                    comment,
                )

        # If no errors, perform task
        if self.canproceed():
            line = len(self.lines) - 1
            self.prooflist[self.currentproofid][1].append(line)
            self.level -= 1
            self.subproofchain = self.subproofchain[3:]
            previousproofid = self.getpreviousproofid(self.currentproofid)
            self.currentproofid = previousproofid
            self.currentproof = self.prooflist[previousproofid][1]
            if len(self.previousproofchain) > 1:
                self.previousproofchain.pop(len(self.previousproofchain) - 1)
                self.previousproofid = self.previousproofchain[
                    len(self.previousproofchain) - 1
                ]
            else:
                self.previousproofchain = []
                self.previousproofid = -1
            statement = self.getstatement(len(self.lines) - 1)
            possiblystatement = Possibly(statement)
            self.logstep(
                self.log_possibly_elim.format(
                    self.possibly_elim_name.upper(), possiblystatement, statement
                )
            )
            newcomment = self.iscomplete(possiblystatement, comment)
            self.lines.append(
                [
                    possiblystatement,
                    self.level,
                    self.currentproofid,
                    self.possibly_elim_name,
                    self.reflines(line),
                    "",
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(possiblystatement, self.possibly_elim_tag)

    def possibly_intro(self, line: int, comment: str = ""):
        """Adds the possibly connector to an item.

        Parameters:
            line: The line on which the item appears.
            comment: An optional comment the user may add to this line of the proof.

        Examples:

        """

        # Look for general errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.possibly_intro_name,
                self.possibly_intro_name,
                comment,
            ):
                if self.goodline(
                    line, self.possibly_intro_name, self.possibly_intro_name, comment
                ):
                    pass

        # Look for specific errors
        if self.canproceed():
            statement = self.getstatement(line)
            possiblystatement = Possibly(statement)

        # If no errors, perform task
        if self.canproceed():
            self.logstep(
                self.log_possibly_intro.format(
                    self.possibly_intro_name.upper(), possiblystatement, statement, line
                )
            )
            newcomment = self.iscomplete(possiblystatement, comment)
            self.lines.append(
                [
                    possiblystatement,
                    self.level,
                    self.currentproofid,
                    self.possibly_intro_name,
                    str(line),
                    "",
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(possiblystatement, self.possibly_intro_tag)

    def premise(
        self,
        premise: Wff,
        # premise: And | Or | Not | Implies | Iff | Wff | Falsehood | Truth,
        comment: str = "",
    ):
        """Add a premise to the proof.

        Although a proof does not require a premise one or more of them may be provided.
        A premise differs from an hypothesis in that it does not start a subproof,
        but it is an accepted truth of the main proof.  When a proof is saved, the premises
        are collected together in a list of Wff objects which is attached to the consequence.
        To use the saved proof later, that is, to be able to place the consequence of the
        saved proof into a proof line of a new proof each and all of the premises will have
        to match a previous line that is within the scope of the current line in the new proof.
        Hypotheses used in the saved proof do not place such a constraint on using the saved proof.
        Although they are stored as lines within the details of the saved proof, they are only needed
        when one wants to check that the derivation of the saved proof was correct.

        Parameters:
            premise: The premise to add to the proof.
            comment: An optional comment the user may add to this line of the proof.

        Example:
            In this example, the goal is declared to be "A".  Then the premise is offered which is also "A".
            That immediately completes the proof.

            >>> from altrea.wffs import Implies
            >>> from altrea.rules import Proof
            >>> prf = Proof()
            >>> prf.setlogic()
            >>> A = prf.proposition('A')
            >>> prf.setlogic()
            >>> prf.goal(A)
            >>> prf.premise(A)
            >>> prf.displayproof(short=1, latex=0)
              Item     Rule   Comment
                 A     GOAL
            1    A  Premise  COMPLETE
        """

        # Look for errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.premise_name,
                self.premise_name,
                comment,
            ):
                if self.goodobject(
                    premise, self.premise_name, self.premise_name, comment
                ):
                    if not self.checkhasgoal():
                        self.logstep(
                            self.log_nogoal.format(self.premise_name.upper(), premise)
                        )
                        self.stopproof(
                            self.stopped_nogoal,
                            self.blankstatement,
                            self.premise_name,
                            "",
                            "",
                            comment,
                        )

        # If no errors, perform task
        if self.canproceed():
            self.premises.append(premise)
            nextline = len(self.lines)
            self.prooflist[self.currentproofid][3].append(nextline)
            self.logstep(self.log_premise.format(self.premise_name.upper(), premise))
            newcomment = self.iscomplete(premise, comment)
            self.lines.append(
                [
                    premise,
                    0,
                    self.currentproofid,
                    self.premise_name,
                    "",
                    "",
                    newcomment,
                    self.linetype_premise,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(premise, self.premise_tag)

    def proposition(self, name: str, latex: str = "", kind: str = "proposition"):
        """This function creates an object which can be given a true or false value.
        The function puts the object in a dictionary that is used when a string
        representation saved into the database or a file is read by the user
        to create an object recognized by the proof and for doing substitutions.

        Parameters:
            name: The text name for the proposition returned when the object is
                used in a string.
            latex: The optional text name for the proposition when it is used
                in a latex context.
            kind: A designation for the kind of object being created.  The default
                is a proposition.

        Examples:
            The follow are some of the ways to define propositional variables.

            >>> from altrea.wffs import Wff, And, Or, Not
            >>> from altrea.rules import Proof
            >>> prf = Proof()
            >>> A = prf.proposition('α', 'α')
            >>> B = prf.proposition('\u05e9', '\\textbf{\u05e9}')
            >>> 主 = prf.proposition('主', '\\text{主}')
            >>> samisgood = prf.proposition('Sam is good', '\\text{Sam is good}')
            >>> prf.setlogic()
            >>> prf.goal(A)
            >>> prf.premise(B)
            >>> prf.premise(主)
            >>> prf.premise(samisgood)
            >>> prf.premise(And(A, B))
            >>> prf.premise(And(B, 主))
            >>> prf.premise(Or(A, Not(A)))
            >>> prf.conjunction_intro(1,3)
            >>> prf.displayproof(latex=0, short=1)
                        Item                     Rule Comment
                            α                     GOAL
            1                ש                  Premise
            2                主                  Premise
            3      Sam is good                  Premise
            4            α & ש                  Premise
            5            ש & 主                  Premise
            6           α | ~α                  Premise
            7  ש & Sam is good  1, 3, Conjunction Intro

        """
        p = Proposition(name, latex, kind)
        self.objectdictionary.update({name: p})
        self.letters.append([p, name, latex])
        howmany = len(self.letters)
        self.logstep(
            self.log_proposition.format(self.proposition_name.upper(), p, howmany)
        )
        return p

    # def startemptystrictsubproof(self):
    #     self.level += 1
    #     nextline = len(self.lines)
    #     self.currentproof = [nextline]
    #     #self.currenthypotheses = [nextline]
    #     self.subproof_status = self.subproof_strict
    #     self.prooflist.append(
    #         [
    #             self.level,
    #             self.currentproof,
    #             self.currentproofid,
    #             [],#self.currenthypotheses,
    #             self.subproof_status
    #         ]
    #     )
    #     self.previousproofid = self.currentproofid
    #     self.previousproofchain.append(self.currentproofid)
    #     self.currentproofid = len(self.prooflist) - 1
    #     self.logstep(self.log_emptystrictsubproofstarted.format(self.startemptystrictsubproof_name.upper(),
    #                                                        self.currentproofid))

    def startstrictsubproof(
        self,
        reiterate: int = 0,
        addhypothesis: Wff = None,
        hypothesis: Wff = None,
        comment: str = "",
    ):
        """Begin a strict subproof with either a reiterated line or an hypothesis."""

        # Look for errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.startstrictsubproof_name,
                self.startstrictsubproof_name,
                comment,
            ):
                if (
                    reiterate > 0
                    and reiterate < len(self.lines)
                    and isinstance(reiterate, int)
                ):
                    statement = self.lines[reiterate][self.statementindex]
                    if type(statement) != Necessary:
                        self.logstep(
                            self.log_notnecessary.format(
                                self.startstrictsubproof_name.upper(),
                                statement,
                                reiterate,
                            )
                        )
                        self.stopproof(
                            self.stopped_notnecessary,
                            self.blankstatement,
                            self.startstrictsubproof_name,
                            str(reiterate),
                            "",
                            comment,
                        )
                    else:
                        pass
                elif isinstance(addhypothesis, Wff):
                    if self.goodobject(
                        addhypothesis,
                        self.startstrictsubproof_name,
                        self.startstrictsubproof_name,
                        comment,
                    ):
                        pass
                elif isinstance(hypothesis, Wff):
                    if self.goodobject(
                        hypothesis,
                        self.startstrictsubproof_name,
                        self.startstrictsubproof_name,
                        comment,
                    ):
                        pass

        # If no errors, perform task
        if self.canproceed():
            self.level += 1
            self.subproofchain = "".join(
                [self.label_subproofstrict, self.subproofchain]
            )
            nextline = len(self.lines)
            self.currentproof = [nextline]
            # self.currenthypotheses = [nextline]
            self.subproof_status = self.subproof_strict
            self.prooflist.append(
                [
                    self.level,
                    self.currentproof,
                    self.currentproofid,
                    [],  # self.currenthypotheses,
                    self.subproof_status,
                ]
            )
            self.previousproofid = self.currentproofid
            self.previousproofchain.append(self.currentproofid)
            self.currentproofid = len(self.prooflist) - 1
            self.logstep(
                self.log_strictsubproofstarted.format(
                    self.startstrictsubproof_name.upper(),
                    self.currentproofid,
                    reiterate,
                    addhypothesis,
                    hypothesis,
                )
            )
            if reiterate > 0:
                self.reiterate(reiterate)
            elif isinstance(addhypothesis, Wff):
                self.addhypothesis(addhypothesis)
            else:
                self.hypothesis(hypothesis)

            # else:
            #     newcomment = comment
            #     self.lines.append(
            #         [
            #             self.blankstatement,
            #             self.level,
            #             self.currentproofid,
            #             self.reiterate_name,
            #             str(line),
            #             '',
            #             newcomment,
            #             '',
            #             self.subproof_status
            #         ]
            #     )
            #     self.appendproofdata(self.blankstatement,
            #                          self.reiterate_tag)

    def reiterate(self, line: int, comment: str = ""):
        """Repeat a previous line from the proof if that line is still available.

        When one creates an hypothesis through a call to `hypothesis` one creates a subproof.
        When that subproof is closed by called `implication_into`.  One can create subproofs of
        subproofs.  This builds a chain of proofs all originating with the main proof.

        The lines of a closed subproof still exist in the proof as previous lines, but they are no
        longer available for use.  All one has is the implication that closed the subproof.
        If one is in a subproof one can use lines from within that subproof without concern.
        Each line that one references is checked to make sure it is available for use.

        However, if one wants to use a line outside the current subproof one is in, one
        has to first bring it into the subproof by calling `reiterate`.  The function checks
        if the line is available given the logic one is using then then places it on a new
        line of the subproof.  Once it is in the subproof, it becomes available for use.

        Parameter:
            line: The line number of the item in the proof.
            comment: An optional comment the user may add to this line of the proof.

        Example:

        """

        # Look for general errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.reiterate_name,
                self.reiterate_name,
                comment,
            ):
                # Only check that the line is in the proof, not the full goodline() checks
                if not self.checkline(line):
                    self.logstep(
                        self.log_nosuchline.format(self.reiterate_name.upper(), line)
                    )
                    self.stopproof(
                        self.stopped_nosuchline,
                        self.blankstatement,
                        self.reiterate_name,
                        str(line),
                        "",
                        comment,
                    )

        # Look for specific errors
        if self.canproceed():
            proofid = self.lines[line][self.proofidindex]
            statement = self.lines[line][self.statementindex]
            if proofid not in self.previousproofchain:
                self.logstep(
                    self.log_notreiteratescope.format(self.reiterate_name.upper(), line)
                )
                self.stopproof(
                    self.stopped_notreiteratescope,
                    self.blankstatement,
                    self.reiterate_name,
                    str(line),
                    "",
                    comment,
                )
            # if self.subproof_status == self.subproof_strict and type(statement) != Necessary:
            if self.label_subproofstrict in self.subproofchain:
                if (
                    type(statement) != Necessary
                    and self.label_subproofstrict
                    not in self.lines[line][self.subproofstatusindex]
                ):
                    self.logstep(
                        self.log_notnecessary.format(
                            self.reiterate_name.upper(), statement, line
                        )
                    )
                    self.stopproof(
                        self.stopped_notnecessary,
                        self.blankstatement,
                        self.reiterate_name,
                        str(line),
                        "",
                        comment,
                    )

        # If no errors, perform task
        if self.canproceed():
            self.logstep(
                self.log_reiterate.format(
                    self.reiterate_name.upper(), statement, line, self.currentproofid
                )
            )
            newcomment = self.iscomplete(statement, comment)
            self.lines.append(
                [
                    statement,
                    self.level,
                    self.currentproofid,
                    self.reiterate_name,
                    str(line),
                    "",
                    newcomment,
                    "",
                    self.subproofchain,
                ]
            )
            self.appendproofdata(statement, self.reiterate_tag)

    def setlogic(self, logic: str = "", comment: str = ""):
        """Specify the logic that will be followed in this proof.

        Parameters:
            logic: The code identifying the logic.  Accepting the default links the proof to no database of saved proofs
                and offers a default set of axioms and definitions with all transformation rules available.
            comment: An optional comment the user may add to this line of the proof.

        Examples:
            If you do not know which logics are avaiable, you may run `displaylogics()`.
            A list of the available logics will be displayed.

            If a logic has been incorrectly set an error message may appear
            such as in the following example.

            >>> from altrea.wffs import Wff
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

        # Look for errors
        if self.canproceed():
            if self.logic != "":
                self.logstep(
                    self.log_logicalreadydefined.format(
                        self.setlogic_name.upper(), self.logic
                    )
                )
                self.stopproof(
                    self.stopped_logicalreadydefined,
                    self.blankstatement,
                    self.setlogic_name,
                    "",
                    "",
                    comment,
                )
            else:
                database = self.label_nodatabase
                description = self.label_nodescription
                self.logic = logic
                if logic != "":
                    try:
                        database, description = altrea.data.getlogic(logic)
                    except TypeError:
                        self.logstep(
                            self.log_logicnotfound.format(
                                self.setlogic_name.upper(), logic
                            )
                        )
                        self.stopproof(
                            self.stopped_logicnotfound,
                            self.blankstatement,
                            self.setlogic_name,
                            "",
                            "",
                            comment,
                        )

        # If no errors, perform the task
        if self.canproceed():
            self.logicdatabase = database
            self.logicdescription = description
            self.proofdata[0].append(logic)
            self.logstep(
                self.log_logicdescription.format(
                    self.setlogic_name.upper(),
                    logic,
                    self.logicdescription,
                    self.logicdatabase,
                )
            )
            if self.logic != "":
                try:
                    self.logicaxioms = altrea.data.getaxioms(logic)
                except TypeError:
                    self.logicaxioms = []
                try:
                    self.logicdefinitions = altrea.data.getdefinitions(logic)
                except TypeError:
                    self.logicdefinitions = []
                try:
                    self.logicsavedproofs = altrea.data.getproofs(logic)
                except TypeError:
                    self.logicsavedoriifs = []
                try:
                    self.logicrules = altrea.data.getrules(logic)
                except TypeError:
                    self.logicrules = []
            else:
                self.setrestricted(self.restricted)
                # if database != 'No Database':
                #     try:
                #         intelimrules = altrea.data.getintelimrules(logic)
                #     except:
                #         self.logstep(self.log_couldnotgettransformationrules.format(self.setlogic_name.upper(), self.logic))
                #     else:
                #         if len(intelimrules) > 0:
                #             self.logicintelimrules = []
                #             for i in intelimrules:
                #                 if i[0] != '':
                #                     self.logicintelimrules.append((i[0], eval(i[1])))
                #                 else:
                #                     self.logicintelimrules.append(i)
                #     try:
                #         connectors = altrea.data.getconnectors(logic)
                #     except:
                #         self.logstep(self.log_couldnotgetconnectors.format(self.setlogic_name.upper(), self.logic))
                #     else:
                #         if len(connectors) > 0:
                #             self.connectors = []
                #             for i in connectors:
                #                 if i[0] != '':
                #                     self.logicalconnectives.append((eval(i[0], self.objectdictionary), i[0], i[1]))
                #                 else:
                #                     self.logicalconnectives.append(i)

    def substitution(
        self, line: int, whattosubstitute: list, substitutes: list, comment: str = ""
    ):
        """The rule of substitution given a line in the proof, propositions to substitute and wffs to replace them.

        Parameters:
            line: The previous line in the proof on which the substitutions will be performed.
            whattosubstitute: A list of propositions in the same order as the substitutes that will be replaced
                by the wffs in the substitutes list. It is the same length greater than 0 as the substitutes list.
            substitutes: A list of wffs that will replace the propositions in the whattosubstitute list provided in
                the same order as the whattosubstitute list.  It is the same length greater than 0 as the
                whattosubstitut list.

        Examples:
        """

        # Look for errors.
        if self.canproceed():
            if self.goodrule(
                self.rule_axiomatic,
                self.substitution_name,
                self.substitution_name,
                comment,
            ):
                if self.goodline(
                    line, self.substitution_name, self.substitution_name, comment
                ):
                    if self.goodlist(
                        whattosubstitute,
                        self.substitution_name,
                        self.substitution_name,
                        comment,
                    ):
                        if self.goodlist(
                            substitutes,
                            self.substitution_name,
                            self.substitution_name,
                            comment,
                        ):
                            if self.goodlistlength(
                                whattosubstitute,
                                substitutes,
                                self.substitution_name,
                                self.substitution_name,
                                comment,
                            ):
                                for i in whattosubstitute:
                                    if not self.goodproposition(
                                        i,
                                        self.substitution_name,
                                        self.substitution_name,
                                        comment,
                                    ):
                                        break
                                if self.canproceed():
                                    for i in substitutes:
                                        if not self.goodobject(
                                            i,
                                            self.substitution_name,
                                            self.substitution_name,
                                            comment,
                                        ):
                                            break

        # If no errors, perform task.
        if self.canproceed():
            statement = self.getstatement(line)
            schema = statement.makeschemafromlist(whattosubstitute)
            newstatement = self.substitute(schema, substitutes, self.substitution_name)
            self.logstep(
                self.log_substitution.format(
                    self.substitution_name.upper(), statement, line, newstatement
                )
            )
            newcomment = self.iscomplete(newstatement, comment)
            self.lines.append(
                [
                    newstatement,
                    self.level,
                    self.currentproofid,
                    self.substitution_name,
                    str(line),
                    "",
                    newcomment,
                    self.linetype_substitution,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(newstatement, self.substitution_tag)

    def rule(self, name: str, subslist: list, lines: list = [], comment: str = ""):
        """Use a transformation rule that was stored in the database associated with the logic or the
        default set of transformation rules if no logic has been specified.

        Parameters:
            name: The name of the saved proof one wishes to use.
            subslist: A list of object substitutions, not strings, given in the order that they will be
                substituted into the rule.
            lines: A list of integers representing the lines in the proof that stand for the premises required
                by the rule.  After the substitutions are made and they match between the rule and these
                lines then the conclusion of the rule will be made available.
            comment: An optional comment the user may add to this line of the proof.

        Examples:

        See Also:
            - `setlogic`
            - `saveproof`

        """

        # Look for errors: Get the saved proof.
        if self.canproceed():
            foundindex = -1
            for i in range(len(self.logicrules)):
                if self.logicrules[i][0] == name:
                    foundindex = i
                    break
            if foundindex < 0:
                self.logstep(
                    self.log_notransformationrule.format(self.rule_name.upper(), name)
                )
                self.stopproof(
                    self.stopped_notransformationrule,
                    self.blankstatement,
                    name,
                    "",
                    "",
                    comment,
                )
            else:
                pattern = self.logicrules[foundindex][1]
                displayname = self.logicrules[foundindex][2]
                description = self.logicrules[foundindex][3]

        # Look for errors: Check the substitution values.
        if self.canproceed():
            subs = self.checksubs(
                self.rule_name.upper(), displayname, comment, subslist
            )

        # Look for errors: Check lines entered from the proof.
        if self.canproceed():
            matchlist, lineslist = self.checkitemlines(
                self.rule_name.upper(), displayname, comment, lines
            )

        # Look for errors: Check if substitutions can be made.
        if self.canproceed():
            conclusionpremises = self.substitute(pattern, subs, displayname)

        # Look for errors: Check if premises match identified lines in the current proof.
        if self.canproceed():
            self.checkpremises(
                self.rule_name.upper(),
                displayname,
                comment,
                conclusionpremises.premises,
                matchlist,
            )

        # If no errors, perform task.
        if self.canproceed():
            self.logstep(
                self.log_userule.format(
                    self.rule_name.upper(), conclusionpremises.conclusion, description
                )
            )
            newcomment = self.iscomplete(conclusionpremises.conclusion, comment)
            self.lines.append(
                [
                    conclusionpremises.conclusion,
                    self.level,
                    self.currentproofid,
                    displayname,
                    self.reflines(*lineslist),
                    "",
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(conclusionpremises.conclusion, displayname)

    def truth(self, name: str, latex: str = ""):
        newtruth = Truth(name, latex)
        self.objectdictionary.update({name: newtruth})
        self.truths.append([newtruth, name])
        howmany = len(self.truths)
        self.logstep(
            f'TRUTH: The letter "{newtruth.name}" (latex: "{newtruth.latexname}") for a generic truth formula has been defined making {howmany} so far.'
        )
        return newtruth

    def useproof(
        self, name: str, subslist: list, premiselist: list = [], comment: str = ""
    ):
        """Use a proof that was stored in the database associated with the logic.

        When one runs `setlogic` without any parameters a default, minimal database is made available to the user.
        This logic does not have any saved proofs associated with it.  At the minimal level this function
        has no value.  However, if one creates a logic one can save proofs to that logic's database and
        use them later.  Also, if one connects to a logic that already has a database, one can use
        whatever proof are stored there as well as add to them.

        Parameters:
            name: The name of the saved proof one wishes to use.
            subslist: A list of object substitutions, not strings, given in order that they will be made.
            premiselist: A list of integers representing the lines in the code that stand for the premises of the
                proof being used.  After the substitutions are made and they match between the saved proof and these
                lines then the conclusion of the saved proof will be made available.
            comment: An optional comment the user may add to this line of the proof.

        Examples:

        See Also:
            - `setlogic`
            - `saveproof`

        """

        # Look for errors: Get the saved proof.
        if self.canproceed():
            try:
                displayname, description, pattern = altrea.data.getsavedproof(
                    self.logic, name
                )
            except TypeError:
                self.logstep(
                    self.log_nosavedproof.format(self.useproof_name.upper(), name)
                )
                self.stopproof(
                    self.stopped_nosavedproof,
                    self.blankstatement,
                    name,
                    "",
                    "",
                    comment,
                )

        # Look for errors: Check the substitution values.
        if self.canproceed():
            subs = self.checksubs(
                self.useproof_name.upper(), displayname, comment, subslist
            )

        # Look for errors: Check lines entered from the proof.
        if self.canproceed():
            matchpremiselist, lineslist = self.checkitemlines(
                self.useproof_name.upper(), displayname, comment, premiselist
            )

        # Look for errors: Check if substitutions can be made.
        if self.canproceed():
            conclusionpremises = self.substitute(pattern, subs, displayname)

        # Look for errors: Check if premises match identified lines in the current proof.
        if self.canproceed():
            self.checkpremises(
                self.useproof_name.upper(),
                displayname,
                comment,
                conclusionpremises.premises,
                matchpremiselist,
            )

        # If no errors, perform task.
        if self.canproceed():
            self.logstep(
                self.log_useproof.format(
                    self.useproof_name.upper(),
                    conclusionpremises.conclusion,
                    description,
                )
            )
            newcomment = self.iscomplete(conclusionpremises.conclusion, comment)
            self.lines.append(
                [
                    conclusionpremises.conclusion,
                    self.level,
                    self.currentproofid,
                    displayname,
                    self.reflines(*lineslist),
                    "",
                    newcomment,
                    self.linetype_savedproof,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(conclusionpremises.conclusion, displayname)
