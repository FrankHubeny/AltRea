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
from datetime import date
import IPython.display

# from tabulate import tabulate
# from IPython.display import display, Math, Markdown, Latex, display_markdown, HTML

from altrea import __version__
from altrea.wffs import (
    And,
    Or,
    Not,
    Implies,
    Iff,
    Wff,
    Necessary,
    Possibly,
    Predicate,
    Proposition,
    Falsehood,
    Truth,
    ConclusionPremises,
    Definition,
    ConsistentWith,
    StrictIff,
    StrictImplies,
    ThereExists,
    ForAll,
    Subject,
    Connective,
    Variable,
    Couple,
    Identity,
    Relation,
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

    proofdata_nameindex = 0
    proofdata_statementindex = 1
    proofdata_levelindex = 2
    proofdata_proofidindex = 3
    proofdata_ruleindex = 4
    proofdata_linesindex = 5
    proofdata_proofsindex = 6
    proofdata_commentindex = 7
    proofdata_typeindex = 8
    proofdata_subproofstatusindex = 9

    lowestlevel = 0
    blankstatement = ""

    subproof_strict = "STRICT"
    subproof_normal = "NORMAL"

    complete = "COMPLETE"
    partialcompletion = "PARTIAL COMPLETION"
    stopped = "STOPPED"
    vacuous = "VACUOUS"
    contradicted = "GOAL CONTRADICTED"

    color_available = "\\color{green}"
    color_unavailable = "\\color{red}"
    color_conclusion = "\\color{blue}"

    addhypothesis_name = "Add Hypothesis"
    axiom_name = "Axiom"
    binaryconnective_name = "Binary Connective"
    closestrictsubproof_name = "Close Strict Subproof"
    closesubproof_name = "Close Subproof"
    definition_name = "Definition"
    entailment_name = "Entailment"
    goal_name = "GOAL"
    hypothesis_name = "Hypo"
    identity_elim_name = "Identity Elim"
    implication_intro_name = "Implication Intro"
    implication_intro_rulename = "$\\supset~$I"
    implication_intro_strict_name = "Strict Implication Intro"
    implication_intro_strict_rulename = "$\\prec~$"
    necessary_intro_name = "Necessary Intro"
    necessary_intro_rulename = "$\\Box~$I"
    # negation_intro_name = "Negation Intro"
    # negation_intro_rulename = "$\\lnot~$"
    openstrictsubproof_name = "Open Strict Subproof"
    opensubproof_name = "Open Subproof"
    possibly_elim_name = "Possibly Elim"
    possibly_elim_rulename = "$\\Diamond~$E"
    predicate_name = "Predicate"
    reiterate_name = "Reit"
    removeaxiom_name = "Remove Axiom"
    removedefinition_name = "Remove Definition"
    removeproof_name = "Remove Proof"
    removerule_name = "Remove Rule"
    rule_name = "Rule"
    saveaxiom_name = "Save Axiom"
    savedefinition_name = "Save Definition"
    saverule_name = "Save Rule"
    subject_name = "Subject"
    substitution_name = "Substitution"
    variable_name = "Variable"
    

    subproofavailable_not = "No"
    subproofavailable_opennormal = "Open"
    subproofavailable_openstrict = "Open Strict"
    subproofavailable_closenormal = "Close"
    subproofavailable_closestrict = "Close Strict"

    # This set of strings provide names for proof structures which need not be used with natural deduction.

    premise_name = "Premise"
    proof_name = "Proof"
    proposition_name = "Proposition"
    setlogic_name = "Set Logic"
    substitution_name = "Substitution"
    substitute_name = "Substitute Evaluate"
    lemma_name = "Lemma"
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
    stopped_closewrongsubproof = "Attempting to close a subproof that is not open."
    log_closewrongsubproof = '{0}: The current subproof is "{1}" but attempting to close a "{2}" subproof.'
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
    log_nogoal = '{0}: The proof needs a goal before a line can be added to it.'
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
    stopped_notcomplete = "The proof needs to be completed before it can be saved."
    log_notcomplete = (
        '{0}: The proof named "{1}" cannot be saved because it is not yet complete.'
    )
    stopped_notcontradiction = "The referenced items are not negations of each other."
    log_notcontradiction = '{0}: The reference items "{1}" on line {2} and "{3}" on line {4} are not negations of each other.'
    stopped_notenoughsubs = (
        "There are not enough substitution values for the metavariables."
    )
    log_notenoughsubs = '{0}: The metaformula "{1}" require more substution values than are provided in this list "{2}".'
    stopped_notfalse = "The referenced item is not false."
    log_notfalse = '{0}: The referenced item "{1}" on line {2} is not false.'
    stopped_notidentity = "Not an identity."
    log_notidentity = '{0}: The item "{1}" is either not an identity or "{2}" or "{3}" are not what are equated.'
    stopped_notimplication = "The referenced item is not an implication."
    log_notimplication = (
        '{0}: The referenced item "{1}" on line {2} is not an implication.'
    )
    stopped_notinteger = "The line number is not an integer."
    log_notinteger = "{0}: The line number {1} is not an integer."
    stopped_notlist = "The input is not a list."
    log_notlist = '{0}: The input "{1}" is not a list.'
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
    stopped_premiseslengthsdontmatch = (
        "The number of premises do not match the pattern."
    )
    log_premiseslengthsdontmatch = (
        '{0}: The number of premises "{1}" does not match the number in the pattern {2}.'
    )
    stopped_restrictednowff = (
        "In restricted mode objects cannot be used in disjunction introduction."
    )
    log_restrictednowff = '{0}: Only integers referencing statements can be used in restricted mode not "{1}" or "{2}".'
    stopped_ruleclass = "This inference rule is not part of the selected set of rules."
    log_ruleclass = '{0}: This inference rule "{1}" is part of the "{2}" set of rules not the selected "{3}" set of rules.'
    stopped_unavailablesubproof = "The subproof is not available."
    log_unavailablesubproof = '{0}: The subproof has the available status only of "{1}". '

    """Strings to log messages upon successful completion of tasks."""

    log_axiom = '{0}: Item "{1}" has been added through the "{2}" axiom.'
    log_axiomalreadyexists = '{0}: An axiom with the name "{1}" already exists.'
    log_axiomnotfound = '{0}: An axiom with the name "{1}" was not found.'
    log_axiomremoved = '{0}: The axiom named "{1}" has been removed.'
    log_axiomsaved = '{0}: The axiom named "{1}" has been saved.'
    log_closenecessary = "{0}: The current subproof was closed deriving a Necessary item."
    log_closepossibly = "{0}: The current subproof was closed deriving a Possibly item."
    log_closestrictsubproof = '{0}: The current "{1}" subproof {2} has been closed.'
    log_closesubproof = '{0}: The current "{1}" subproof {2} has been closed.'
    log_binaryconnective = '{0}: The name "{1}" refers to a binary connective with {2} so far having been defined for this proof.'
    log_definition = '{0}: Item "{1}" has been added using the "{2}" definition.'
    log_definitionalreadyexists = (
        '{0}: A definition with the name "{1}" already exists.'
    )
    log_definitionnotfound = '{0}: A definition with the name "{1}" was not found.'
    log_definitionremoved = '{0}: The definition named "{1}" has been removed.'
    log_definitionsaved = '{0}: The definition named "{1}" has been saved.'
    log_emptystrictsubproofstarted = "{0}: An empty strict subproof has been started."
    log_goal = '{0}: The goal "{1}" has been added to the goals.'
    log_hypothesis = '{0}: A new subproof {1} has been started with item "{2}".'
    log_identity_elim = '{0}: In "{1}" replace "{2}" with "{3}" derived as identical on line {4}.'
    log_implication_intro = (
        '{0}: Item "{1}" has been derived upon closing subproof {2}.'
    )
    log_implication_intro_strict = (
        '{0}: Item "{1}" has been derived upon closing the strict subproof {2}.'
    )
    log_kindnotrecognized = (
        '{0}: The kind "{2}" for "{1}" is not recognized.'
    )
    log_logdisplayed = "The log will be displayed."
    log_logicdescription = '{0}: "{1}" has been selected as the logic described as "{2}" and stored in database "{3}".'
    log_necessary_intro = '{0}: Item "{1}" has been derived from item "{2}".'
    log_negation_intro = (
        '{0}: Item "{1}" has been derived as the negation of the antecedent of "{2}".'
    )
    log_noproofs = "There are no saved proofs for logic {0}"
    log_opensubproof = '{0}: Subproof {1} has been opened with status "{2}".'
    log_possibly_elim = '{0}: Item "{1}" has been derived from item "{2}".'
    log_predicate = '{0}: The name "{1}" refers to a predicate with {2} so far having been defined for this proof.'
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
    log_rulereadyexists = (
        '{0}: A rule with the name "{1}" already exists.'
    )
    
    log_ruleremoved = '{0}: The rule named "{1}" has been removed.'
    log_rulesaved = '{0}: The rule named "{1}" has been saved.'
    log_strictsubproofstarted = '{0}: A strict subproof "{1}" has been started.'
    log_substitute = '{0}: The placeholder(s) in the string "{1}" have been replaced with "{2}" to become "{3}".'
    log_substitution = (
        '{0}: The statement "{1}" on line "{2}" has been substituted with "{3}".'
    )
    log_subject = '{0}: The name "{1}" refers to a thing or subject in a domain with {2} so far having been defined for this proof.'
    log_useproof = '{0}: Item "{1}" has been added through the "{2}" saved proof.'
    log_userule = (
        '{0}: Item "{1}" has been added through the "{2}" transformation rule.'
    )
    log_vacuous = "The proof is vacuously over."
    log_variable = '{0}: The name "{1}" refers to a variable ranging over a domain with {2} so far having been defined for this proof.'

    """Labels for various reports."""

    label_axiom = "Axiom"
    label_axioms = "Axioms"
    label_checkmarklatex = "\\color{green}\\checkmark"
    label_checkmark = "ok"
    label_comment = "Comment"
    label_connective = "Connective"
    label_connectives = "Connectives"
    label_contradicted = "GOAL CONTRADICTED"
    label_currentproofid = "Current Proof ID"
    label_definition = "Definition"
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
    label_item = "Item"
    label_left = "left"
    label_level = "Level"
    label_lines = "Lines"
    label_linetype = "Type"
    label_logic = "Logic"
    label_logicdatabase = "Logic Database"
    label_logicdescription = "Logic Description"
    label_metavariable = "Metavariable"
    label_name = "Name"
    label_noaxioms = "No Axioms"
    label_noconnectives = "No Connectives"
    label_nodatabase = "No Database"
    label_nodefinition = " No Definitions"
    label_nodefinitions = "No Definitions"
    label_noderivedgoals = "No Derived Goals"
    label_nodescription = "No Description"
    label_nogoals = "No Goals"
    label_nopremises = "No Premises"
    label_nolemmas = "No Saved Proofs"
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
    label_proposition = "Proposition"
    label_right = "right"
    label_rule = "Rule"
    label_lemmas = "Saved Proofs"
    label_stoppedstatus = "Stopped Status"
    label_subproofnormal = "{0}"
    label_subproofstrict = "{1}"
    label_symbols = "Symbols"
    label_tautology = "Tautology"
    label_transformationrules = "Rules"
    label_vacuous = "Vacuous"
    label_valid = "Valid"
    label_value = "Value"

    valueerror_badpremise = 'The premise "{0}" is not an instance of altrea.wffs.Wff.'
    valueerror_badconclusion = 'The conclusion "{0}" is not an instance of altrea.wffs.Wff.'
    valueerror_kind = "The kind '{0}' is not recognized."
    valueerror_names = "Either the name '{0}' or the displayname '{1}' or the description '{2}' is not defined."
    valueerror_rulenotfound = '{0}: A rule with the name "{1}" was not found.'

    """Convenience strings for the user when entering string values."""

    left = "left"
    right = "right"
    section = "section"
    chapter = "chapter"
    document = "document"

    """The following tags are used to differentiate between lines of a proof."""

    linetype_axiom = "AXIOM"
    linetype_definition = "DEF"
    linetype_hypothesis = "HYPO"
    linetype_premise = "PREM"
    linetype_reiterate = "REIT"
    linetype_rule = "RULE"
    linetype_lemma = "LEMMA"
    linetype_replace = "REPLACE"
    linetype_substitution = "SUB"
    linetype_transformationrule = "TR"

    rule_naturaldeduction = "Natural Deducation"
    rule_categorical = "Categorical"
    rule_axiomatic = "Axiomatic"

    write_axiom = "{0}From the {1} axiom we can assert item ${2}$ on line {3}.\n\n"
    write_definition = "{0}The {1} can be rewritten as ${2}$ on line {3} by the {4} definition.\n\n"
    write_definition_norefs = "{0}We can write ${1}$ on line {2} by the {3} definition.\n\n"
    write_hypothesis = "{0}\n\nWe assert the hypothesis ${1}$ on line {2} in order to derive ${3}$ on line {4}.  We now detail how that is done.\n\n"
    write_lemma = "{0}From {1} using {2} we can assert item ${3}$ on line {4}.\n\n"
    write_lemmalist = "{0}{1}"
    write_predicate_one = "Let ${0}$ be an arbitrary predicate. "
    write_predicate_first = "Let ${0}$"
    write_predicate_many = ", ${0}$"
    write_predicate_last = " and ${0}$ be arbitrary predicates in a domain. "
    write_premises_none = "The proof uses no premises. "
    write_premises_one = "As a premise we are given ${0}$. "
    write_premises_first = "As premises we are given ${0}$"
    write_premises_many = ", ${0}$"
    write_premises_last = " and ${}$.\n\n"
    write_premise = "{0}We are given the premise ${1}$ on line {2}.\n"
    write_premises = "We are given {0} premises. "
    write_proofconclusion = "\n\nSince we can derive ${0}$, we have ${1}$.\n\n"
    write_proofintro = "The following table shows the lines of the proof.\n\n"
    write_proposition_one = "Let ${0}$ be an arbitrary proposition. "
    write_proposition_first = "Let ${0}$"
    write_proposition_many = ", ${0}$"
    write_proposition_last = " and ${0}$ be arbitrary propositions. "
    write_referenceditems_first = "item ${0}$ on line {1}"
    write_referenceditems_many = "{0}, item ${1}$ on line {2}"
    write_referenceditems_last = "{0} and item ${1}$ on line {2}"
    write_referenceditems_subproofs ="{0}subproofs {1}"
    write_referenceditems_subproof_one ="{0}subproof {1}"
    write_rule = "{0}From {1} using the {2} rule we can derive item ${3}$ on line {4}. "
    Write_subproofconclusion = "This completes the subproof.\n\n"
    write_rule_norefs = "{0}Using the {1} rule we can derive item ${2}$ on line {3}. "
    write_subject_one = "Let ${0}$ be an arbitrary subject or thing in a domain. "
    write_subject_first = "Let ${0}$"
    write_subject_many = ", ${0}$"
    write_subject_last = " and ${0}$ be arbitrary subjects in a domain. "
    write_substitution = "{0}From {1} using substitution we can derive item ${2}$ on line {3}. "
    write_substitution = "{0}Using substitution we can derive item ${1}$ on line {2}. "
    write_theoremstatement = "\\begin{{theorem*}}[{0}]\n The entailment ${1}$ can be derived. \n\\end{{theorem*}}\n\n"
    write_transformationrule = "{0}Using the {2} rule with {1} we can derive item ${3}$ on line {4}. "
    write_transformationrule_norefs = "{0}Using the {1} rule we can derive item ${2}$ on line {3}. "
    write_variable_one = "Let ${0}$ be a variable ranging over a domain. "
    write_variable_first = "Let ${0}$"
    write_variable_many = ", ${0}$"
    write_variable_last = " and ${0}$ be variables ranging over a domain. "
    write_withoutlemmas = "The proof of the theorem does not require any lemmas.\n\n"
    write_withlemma = "The proof of the theorem depends on the following lemma.\n\n"
    write_withlemmas = "The proof of the theorem depends on the following lemmas.\n\n"

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
        self.logicsymbols = [
            ("(", "Left Parentheses"),
            (")", "Right Parentheses"),
            ("\\models", "Semantic Consequence"),
            ("\\vdash", "Logical Consequence"),
            ("\\bot", "Contradiction"),
            ("\\top", "Tautology"),
        ]
        self.logicconnectives = [
            ("and", "&", "\\wedge~", "Logical And"),
            ("or", "|", "\\vee~", "Logical Or"),
            ("implies", ">", "\\supset~", "Material Implication"),
            ("equiv", "≡", "\\equiv~", "Material Equivalence"),
            # ("\\wedge ", "Logical And"),
            # ("\\vee ", "Logical Or"),
            # ("\\lnot ", "Logical Not"),
            # ("\\supset ", "Logical (Material) Implication"),
            # ("\\equiv ", "Logical Coimplication (IFF)"),
            # ("\\Box ", "Modal Necessity"),
            # ("\\Diamond ", "Modal Possibility"),
            # ("\\prec ", "Modal Strict Implication"),
            # ("\\backsimeq ", "Modal Strict Coimplication"),
            # ("\\circ ", "Modal Consistent With"),
        ]
        self.logicrules = [
            (
                "coimp elim", 
                "ConclusionPremises(And(Implies({0}, {1}), Implies({1}, {0})), [Iff({0}, {1})])", 
                "$\\equiv$ E", 
                "Coimplication Elimination"
            ),
            (
                "coimp intro", 
                "ConclusionPremises(Iff({0}, {1}), [And(Implies({0}, {1}), Implies({1}, {0}))])", 
                "$\\equiv$ I", 
                "Coimplication Introduction"
            ),
            (
                "conj elim l", 
                "ConclusionPremises({0}, [And({0}, {1})])", 
                "$\\wedge$ E-L", 
                "Conjunction Elimination Left Side"
            ),
            (
                "conj elim r", 
                "ConclusionPremises({1}, [And({0}, {1})])", 
                "$\\wedge$ E-R", 
                "Conjunction Elimination Right Side"
            ),
            (
                "conj intro", 
                "ConclusionPremises(And({0}, {1}), [{0}, {1}])", 
                "$\\wedge$ I", 
                "Conjunction Introduction"
            ),
            (
                "consistent intro", 
                "ConclusionPremises(ConsistentWith({0}, {1}), [Possibly(And({0}, {1}))])", 
                "$\\circ$ I", 
                "Consistent With Introduction"
            ),
            (
                "consistent elim", 
                "ConclusionPremises(Possibly(And({0}, {1})), [ConsistentWith({0}, {1})])", 
                "$\\circ$ E", 
                "Consistent With Elimination"
            ),
            (
                "coup elim l", 
                "ConclusionPremises(Identity({0}, {2}), [Identity(Couple({0}, {1}),Couple({2}, {3}))])", 
                "( ) E-L", 
                "Couple Elimination"
            ),
            (
                "coup elim r", 
                "ConclusionPremises(Identity({1}, {3}), [Identity(Couple({0}, {1}),Couple({2}, {3}))])", 
                "( ) E-R", 
                "Couple Elimination"
            ),
            (
                "coup intro", 
                "ConclusionPremises(Identity(Couple({0}, {2}), Couple({1}, {3})), [Identity({0},{1}), Identity({2},{3})])", 
                "( ) I", 
                "Couple Introduction"),
            (
                "disj elim", 
                "ConclusionPremises({2}, [Or({0}, {1}), Implies({0}, {2}), Implies({1}, {2})])", 
                "$\\vee$ E", 
                "Disjunction Elimination"
            ),
            (
                "disj elim l", 
                "ConclusionPremises({2}, [Or({0}, {1}), Implies({0}, {2}), Implies({1}, Falsehood())])", 
                "$\vee$ E-L", 
                "Disjunction Elimination Left"
            ),
            (
                "disj elim r", 
                "ConclusionPremises({2}, [Or({0}, {1}), Implies({0}, Falsehood()), Implies({1}, {2})])", 
                "$\\vee$ E-R", 
                "Disjunction Elimination Right"
            ),
            (
                "disj intro l", 
                "ConclusionPremises(Or({1}, {0}), [{0}])", 
                "$\\lor$ I-L", 
                "Disjunction Introduction Left Side"
            ),
            (
                "disj intro r", 
                "ConclusionPremises(Or({0}, {1}), [{0}])", 
                "$\\lor$ I-R", 
                "Disjunction Introduction Right Side"
            ),
            (
                "imp elim", 
                "ConclusionPremises({1}, [{0}, Implies({0}, {1})])", 
                "$\\supset$ E", 
                "Implication Elimination"),
            (
                "modusponens",
                "ConclusionPremises({1}, [{0}, Implies({0}, {1})])",
                "Modus Ponens",
                "Modus Ponens",
            ),
            (
                "nec elim", 
                "ConclusionPremises({0}, [Necessary({0})])", 
                "$\\Box$ E", 
                "Necessary Elimination"
            ),
            (
                "neg elim", 
                "ConclusionPremises(Falsehood(), [{0}, Not({0})])", 
                "$\\lnot$ E", 
                "Nenegation Elimination"
            ),
            (
                "neg intro", 
                "ConclusionPremises(Not({0}), [Implies({0}, Falsehood())])", 
                "$\\lnot$ I", 
                "Negation Introduction"
            ),
            (   
                "pos intro", 
                "ConclusionPremises(Possibly({0}), [{0}])", 
                "$\\Diamond$ I", 
                "Possibly Introduction"
            ),
            (
                "s coimp elim", 
                "ConclusionPremises(Necessary(Iff({0}, {1})), [StrictIff({0}, {1})])", 
                "$\\backsimeq$ E", 
                "Strict Coimplication Elimination"
            ),
            (
                "s coimp intro", 
                "ConclusionPremises(StrictIff({0}, {1}), [Necessary(Iff({0}, {1}))])", 
                "$\\backsimeq$ I", 
                "Strict Coimplication Introduction"
            ),
            (
                "s imp elim", 
                "ConclusionPremises(Necessary(Implies({0}, {1})), [StrictImplies({0}, {1})])", 
                "$\\prec$ E", 
                "Strict Implication Elimination"
            ),
            (
                "s imp intro", 
                "ConclusionPremises(StrictImplies({0}, {1}), [Necessary(Implies({0}, {1}))])", 
                "$\\prec$ I", 
                "Strict Implication Introduction"
            ),
            (
                "or not to not and",
                "ConclusionPremises(Not(And({0}, {1})), [Or(Not({0}), Not({1}))])",
                "De Morgan",
                "De Morgan Or To Not-And",
            ),
            (
                "not and to or not",
                "ConclusionPremises(Or(Not({0}), Not({1})), [Not(And({0}, {1}))])",
                "De Morgan",
                "De Morgan Not-And To Or",
            ),
            (
                "and not to not or",
                "ConclusionPremises(Not(Or({0}, {1})), [And(Not({0}), Not({1}))])",
                "De Morgan",
                "De Morgan And To Not-Or",
            ),
            (
                "or not to not and",
                "ConclusionPremises(Not(And({0}, {1})), [Or(Not({0}), Not({1}))])",
                "De Morgan",
                "De Morgan Not-Or To And",
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
                "dneg intro",
                "ConclusionPremises(Not(Not({0})), [{0}])",
                "DN I",
                "Double Negation Introduction",
            ),
            (
                "dneg elim",
                "ConclusionPremises({0}, [Not(Not({0}))])",
                "DN E",
                "Double Negation Elimination",
            ),
            (
                "id lem", 
                "ConclusionPremises(Or(Identity({0}, {1}), Not(Identity({0}, {1}))), [])", 
                "id LEM", 
                "Excluded Middle Identity"
            ),
            (
                "id intro", 
                "ConclusionPremises(Identity({0}, {0}), [])", 
                "= I", 
                "Identity Intro"
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
        self.logicaxioms = [
            (
                "id intro", 
                "ConclusionPremises(Identity({0}, {0}), [])", 
                "= I", 
                "Identity Intro"
            ),
            (
                "id lem", 
                "ConclusionPremises(Or(Identity({0}, {1}), Not(Identity({0}, {1}))), [])", 
                "id LEM", 
                "Excluded Middle Identity"
            ),
        ]
        self.logicdefinitionsunrestricted = [
            (
                "iff intro",
                "ConclusionPremises(Iff({0}, {1}), [And(Implies({0}, {1}), Implies({1}, {0}))])",
                "\\equiv I",
                "Coimplication Introduction",
            ),
            (
                "iff elim",
                "ConclusionPremises(And(Implies({0}, {1}), Implies({1}, {0})), [Iff({0}, {1})])",
                "\\equiv E",
                "Coimplication Elimination",
            ),
        ]
        self.logicdefinitions = []
        self.logiclemmas = []
        self.lines = [["", 0, 0, "", "", "", "", "", ""]]
        self.previousproofchain = []
        self.previousproofid = -1
        self.currentproof = [1]
        self.closedproofid = 0
        self.currentproofid = 0
        self.subproof_status = self.subproof_normal
        self.subproofavailable = self.subproofavailable_not
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
        self.proofcodevariable = "proofcode"
        self.proofcode = [
            f'{self.proofcodevariable} = Proof(',
            f'  "{self.name}",',
            f'  "{self.displayname}",',
            f'  "{self.description}"',
            ')'
        ]
        self.proofrules = self.rule_naturaldeduction
        self.level = self.lowestlevel
        self.status = ""
        self.stoppedmessage = ""
        self.necessarylines = []
        self.premises = []
        self.consequences = []
        self.letters = []
        self.subjects = []
        self.variables = []
        self.binaryconnectives = []
        self.predicates = []
        self.metaletters = []
        self.truths = []
        self.objectdictionary = {
            "And": And,
            "ConclusionPremises": ConclusionPremises,
            "Connective": Connective,
            "ConsistentWith": ConsistentWith,
            "Couple": Couple,
            "Definition": Definition,
            "Falsehood": Falsehood,
            "ForAll": ForAll,
            "Identity": Identity,
            "Iff": Iff,
            "Implies": Implies,
            "Necessary": Necessary,
            "Not": Not,
            "Or": Or,
            "Possibly": Possibly,
            "Relation": Relation,
            "StrictImplies": StrictImplies,
            "StrictIff": StrictIff,
            "Subject": Subject,
            "ThereExists": ThereExists,
            "Truth": Truth,
            "Variable": Variable,
        }
        self.metaobjectdictionary = {
            "And": And,
            "ConclusionPremises": ConclusionPremises,
            "Connective": Connective,
            "ConsistentWith": ConsistentWith,
            "Couple": Couple,
            "Definition": Definition,
            "Falsehood": Falsehood,
            "ForAll": ForAll,
            "Identity": Identity,
            "Iff": Iff,
            "Implies": Implies,
            "Necessary": Necessary,
            "Not": Not,
            "Or": Or,
            "Possibly": Possibly,
            "Relation": Relation,
            "StrictImplies": StrictImplies,
            "StrictIff": StrictIff,
            "Subject": Subject,
            "ThereExists": ThereExists,
            "Truth": Truth,
            "Variable": Variable,
        }
        self.log = []
        self.latexwrittenproof = ""
        self.writtenlogicdescription = ""
        self.writtenproof = ""
        self.showlogging = False
        self.restricted = False
        self.mvalpha = ""
        self.mvbeta = ""
        self.mvgamma = ""
        self.mvdelta = ""
        self.mvepsilon = ""
        self.mvzeta = ""
        self.mveta = ""
        self.mvtheta = ""
        self.mviota = ""
        self.mvkappa = ""
        self.mvlambda = ""
        self.mvmu = ""
        self.mvnu = ""
        self.mvomicron = ""
        self.mvpi = ""
        self.mvrho = ""
        self.mvsigma = ""
        self.mvtau = ""
        self.mvupsilon = ""
        self.mvphi = ""
        self.mvchi = ""
        self.mvpsi = ""
        self.mvomega = ""

    """SUPPORT FUNCTIONS 
    
    These are not intended to be called by the user while constructing a proof.
    """

    def appendproofdata(self, statement: Wff):
        """Append a list representing a line of the proof which will be used to save the proof
        lines as a string.
        """

        length = len(self.lines) - 1
        self.proofdata.append(
            [
                self.name,
                statement,
                self.lines[length][self.levelindex],
                self.lines[length][self.proofidindex],
                self.lines[length][self.ruleindex],
                self.lines[length][self.linesindex],
                self.lines[length][self.proofsindex],
                self.lines[length][self.commentindex],
                self.lines[length][self.typeindex],
                self.lines[length][self.subproofstatusindex],
            ]
        )
        if type(statement) == Necessary:
            self.necessarylines.append(length)
        if self.status == self.complete:
            finalresult = self.buildconclusionpremises()
            propositionlist = []
            self.proofdatafinal.append(
                [
                    self.proofdata[0][self.proofdata_nameindex],
                    self.proofdata[0][self.proofdata_statementindex],
                    self.proofdata[0][self.proofdata_levelindex],
                    self.proofdata[0][self.proofdata_proofidindex],
                    finalresult.pattern(propositionlist),
                ]
            )
            for i in range(len(self.proofdata)):
                if i > 0:
                    self.proofdatafinal.append(
                        [
                            self.proofdata[i][self.proofdata_nameindex],
                            self.proofdata[i][self.proofdata_statementindex].pattern(propositionlist),
                            self.proofdata[i][self.proofdata_levelindex],
                            self.proofdata[i][self.proofdata_proofidindex],
                            self.proofdata[i][self.proofdata_ruleindex],
                            self.proofdata[i][self.proofdata_linesindex],
                            self.proofdata[i][self.proofdata_proofsindex],
                            self.proofdata[i][self.proofdata_commentindex],
                            self.proofdata[i][self.proofdata_typeindex],
                            self.proofdata[i][self.proofdata_subproofstatusindex],
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


    def checkitemlines(
        self, caller: str, displayname: str, comment: str, lineslist: list
    ):
        p = []
        lines = []
        for i in lineslist:
            if self.goodline(i, caller, displayname, comment):
                p.append(self.item(i).tree())
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
            if len(premises) != len(matchpremiselist):
                self.logstep(self.log_premiseslengthsdontmatch.format(caller.upper(), len(premises), len(matchpremiselist)))
                self.stopproof(
                    self.stopped_premiseslengthsdontmatch,
                    self.blankstatement,
                    displayname,
                    "",
                    "",
                    comment,
                )
            else:
                for i in range(len(premises)):
                    if premises[i] != matchpremiselist[i]:
                        self.logstep(self.log_premisesdontmatch.format(caller.upper(), premises[i]))
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

    # def closenecessary(self, comment: str = ""):
    #     """Call necessary_intro to close a subproof rather than viewing
    #     subproofs as part of intelim rules.
    #     """

    #     self.logstep(self.log_closenecessary.format(self.closenecessary_name.upper()))

    #     self.necessary_intro(comment)

    # def closepossibly(self, comment: str = ""):
    #     """Call possibly_elim to close a subproof rather than viewing
    #     subproofs as part of intelim rules.
    #     """

    #     self.logstep(self.log_closepossibly.format(self.closepossibly_name.upper()))

    #     self.possibly_elim(comment)

    def closestrictsubproof(self):
        """Mark a strict subproof closed."""

        # Look for errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.implication_intro_name,
                self.implication_intro_name,
                ""
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
        if self.canproceed():
            if self.subproof_status != self.subproof_strict:
                self.logstep(
                        self.log_closewrongsubproof.format(
                            self.closesubproof_name.upper(),
                            self.subproof_status,
                            self.subproof_strict
                        )
                    )
                self.stopproof(
                    self.stopped_closewrongsubproof,
                    self.blankstatement,
                    self.closesubproof_name,
                    "",
                    "",
                )

        # If no errors, perform task
        if self.canproceed():
            #Log code
            self.proofcode.append(f'{self.proofcodevariable}.closestrictsubproof()')

            self.closedproofid = self.currentproofid
            subproof_status = self.subproof_status
            line = len(self.lines) - 1
            self.prooflist[self.currentproofid][1].append(line)
            self.level -= 1
            self.subproofchain = self.subproofchain[:-3]
            previousproofid = self.getpreviousproofid(self.currentproofid)
            self.currentproofid = previousproofid
            self.currentproof = self.prooflist[previousproofid][1]
            self.subproof_status = self.prooflist[previousproofid][4]
            if len(self.previousproofchain) > 1:
                self.previousproofchain.pop(len(self.previousproofchain) - 1)
                self.previousproofid = self.previousproofchain[
                    len(self.previousproofchain) - 1
                ]
            else:
                self.previousproofchain = []
                self.previousproofid = -1
            self.subproofavailable = self.subproofavailable_closestrict
            self.logstep(self.log_closestrictsubproof.format(
                    self.closestrictsubproof_name.upper(), 
                    subproof_status,
                    self.closedproofid
                )
            )


    def closesubproof(self):
        """Mark a normal subproof closed."""

        # Look for errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.implication_intro_name,
                self.implication_intro_name,
                ""
            ):
                if self.currentproofid == 0:
                    self.logstep(
                        self.log_closemainproof.format(
                            self.closesubproof_name.upper()
                        )
                    )
                    self.stopproof(
                        self.stopped_closemainproof,
                        self.blankstatement,
                        self.closesubproof_name,
                        "",
                        "",
                    )
        if self.canproceed():
            #Log code
            self.proofcode.append(f'{self.proofcodevariable}.closesubproof()')

            if self.subproof_status != self.subproof_normal:
                self.logstep(
                        self.log_closewrongsubproof.format(
                            self.closesubproof_name.upper(),
                            self.subproof_status,
                            self.subproof_normal
                        )
                    )
                self.stopproof(
                    self.stopped_closewrongsubproof,
                    self.blankstatement,
                    self.closesubproof_name,
                    "",
                    "",
                )

        # If no errors, perform task
        if self.canproceed():
            self.closedproofid = self.currentproofid
            subproof_status = self.subproof_status
            self.prooflist[self.currentproofid][1].append(len(self.lines) - 1)
            self.level -= 1
            self.subproofchain = self.subproofchain[:-3]
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
            self.subproofavailable = self.subproofavailable_closenormal
            self.logstep(self.log_closesubproof.format(
                    self.closesubproof_name.upper(), 
                    self.subproof_status,
                    self.closedproofid
                )
            )


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
    

    def goodgoal(self, caller: str, displayname: str, comment: str):
        """Check if the proof has at least one goal."""

        if len(self.goals) == 0:
            self.logstep(self.log_nogoal.format(caller.upper()))
            self.stopproof(
                self.stopped_nogoal,
                self.blankstatement,
                displayname,
                "",
                "",
                comment,
            )
            return False
        else:
            return True


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
        
    def goodsubproof(self, caller: str, displayname: str, comment: str):
        """Check if the proof has at least one goal."""

        if self.subproofavailable != self.subproofavailable_not:
            self.logstep(
                self.log_unavailablesubproof.format(
                    caller.upper(), 
                    self.subproofavailable
                )
            )
            self.stopproof(
                self.stopped_unavailablesubproof,
                self.blankstatement,
                displayname,
                "",
                "",
                comment
            )
            return False
        else:
            return True

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


    def item(self, line):
        """Returns the statement associated with the line number."""

        return self.lines[line][self.statementindex]

    # def stringitem(self, prooflines: list, i: int):
    #     """Formats the statement or item in a proof line so it can be displayed as a string.
    #     It includes indenting based on the level of the subordinate proofs.
    #     """

    #     normalbase = "|   "
    #     strictbase = "||   "
    #     statement = str(prooflines[i][self.statementindex])
    #     chain = prooflines[i][self.subproofstatusindex]
    #     subproofchain = chain.format(normalbase, strictbase)
    #     return "".join([subproofchain, statement])

    def formatitem(
        self, 
        prooflines: list, 
        i: int, 
        status: str, 
        latex: bool = True,
        saved: bool = False, 
        color: int = 1
    ):
        """Formats a statement or item in a proof line for display as latex."""

        if prooflines[i][0] != self.blankstatement:
            if latex:
                normalbase = "$|\\hspace{0.35cm} $"
                strictbase = "$\\Vert\\hspace{0.35cm} $"
                chain = prooflines[i][self.subproofstatusindex]
                subproofchain = chain.format(normalbase, strictbase)

                if color == 1:
                    if i == 0:
                        if saved:
                            statement = "".join(
                                ["$\\color{blue}", prooflines[0][0].latex(), "$"]
                            )
                        else:
                            if self.goals_latex != "":
                                statement = "".join(
                                    ["$", self.color_conclusion, self.goals_latex, "$"]
                                )
                            else:
                                statement = ""
                    else:
                        if status != self.complete and status != self.stopped:
                            if self.currentproofid == prooflines[i][2]:
                                statement = "".join(
                                    [
                                        "$",
                                        self.color_available,
                                        prooflines[i][0].latex(),
                                        #statement,
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
                                                #statement,
                                                "$",
                                            ]
                                        )
                                    elif i in self.necessarylines:
                                        statement = "".join(
                                            [
                                                "$",
                                                self.color_available,
                                                prooflines[i][0].latex(),
                                                #statement,
                                                "$",
                                            ]
                                        )
                                    else:
                                        statement = "".join(
                                            [
                                                "$",
                                                self.color_unavailable,
                                                prooflines[i][0].latex(),
                                                #statement,
                                                "$",
                                            ]
                                        )
                                else:
                                    statement = "".join(
                                        [
                                            "$",
                                            self.color_available,
                                            prooflines[i][0].latex(),
                                            #statement,
                                            "$",
                                        ]
                                    )
                            else:
                                statement = "".join(
                                    [
                                        "$",
                                        self.color_unavailable,
                                        prooflines[i][0].latex(),
                                        #statement,
                                        "$",
                                    ]
                                )
                        elif prooflines[i][6][0:8] == self.complete:
                            statement = "".join(
                                [
                                    "$",
                                    self.color_conclusion,
                                    prooflines[i][0].latex(),
                                    #statement,
                                    "$",
                                ]
                            )
                        elif prooflines[i][6][0:18] == self.partialcompletion:
                            statement = "".join(
                                [
                                    "$",
                                    self.color_conclusion,
                                    prooflines[i][0].latex(),
                                    #statement,
                                    "$",
                                ]
                            )
                        else:
                            statement = "".join(
                                #["$", prooflines[i][0].latex(), statement, "$"]
                                ["$", prooflines[i][0].latex(), "$"]
                            )
                else:
                    if i == 0:
                        if saved:
                            statement = "".join(
                                ["$", prooflines[0][0].latex(), "$"]
                            )
                        elif self.goals_latex != "":
                            statement = "".join(
                                ["$", self.goals_latex, "$"]
                            )
                        else:
                            statement = ""
                    else:
                        statement = "".join(["$", prooflines[i][0].latex(), "$"])
                return "".join([subproofchain, statement])
            else:
                normalbase = "|   "
                strictbase = "||   "
                statement = str(prooflines[i][self.statementindex])
                chain = prooflines[i][self.subproofstatusindex]
                subproofchain = chain.format(normalbase, strictbase)
                return "".join([subproofchain, statement])
        else:
        #     statement = self.blankstatement
        #     subproofchain = ""
            return self.blankstatement
        


    def logstep(self, message: str):
        """This function adds a log message collected during the proof construction
        so it can be displayed later or in an ongoing manner.
        """

        self.log.append([message, len(self.lines)])
        if self.showlogging:
            print(message)

    def opensubproof(self):
        """Open a subproof."""

        if self.canproceed():
            #Log code
            self.proofcode.append(f'{self.proofcodevariable}.opensubproof()')

            self.level += 1
            self.subproofchain = "".join(
                [self.subproofchain, self.label_subproofnormal]
            )
            nextline = len(self.lines)
            self.currentproof = [nextline]
            self.subproof_status = self.subproof_normal
            self.previousproofid = self.currentproofid
            self.previousproofchain.append(self.currentproofid)
            self.currentproofid = len(self.prooflist)
            self.subproofavailable = self.subproofavailable_opennormal
            self.prooflist.append(
                [
                    self.currentproofid,
                    self.currentproof,
                    self.previousproofid,
                    [], 
                    self.subproof_status,
                ]
            )

        self.logstep(self.log_opensubproof.format(
                self.opensubproof_name.upper(),
                self.currentproofid,
                self.subproof_status
            )
        )


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

    def identity_elim(self, wff: Wff, first: Wff, second: Wff, line: int, comment: str = ""):
        """Replace one instance of a proposition, thing or variable with one that has been
        derived to be identical with it."""
        
            # Look for errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.identity_elim_name,
                self.identity_elim_name,
                comment,
            ):
                if self.goodline(
                    line,
                    self.identity_elim_name,
                    self.identity_elim_name,
                    comment
                ):
                    item = self.item(line)
                    if isinstance(item, Identity):
                        if first == item.left or first == item.right:
                            if second == item.left or second == item.right:
                                pass
                            else:
                                self.logstep(
                                    self.log_notidentity.format(
                                        self.identity_elim_name.upper(), 
                                        item,
                                        first,
                                        second
                                    )
                                )
                                self.stopproof(
                                    self.stopped_notidentity,
                                    self.blankstatement,
                                    self.identity_elim_name,
                                    "",
                                    "",
                                    comment
                                )
                        else:
                            self.logstep(
                                self.log_notidentity.format(
                                    self.identity_elim_name.upper(), 
                                    item,
                                    first,
                                    second
                                )
                            )
                            self.stopproof(
                                self.stopped_notidentity,
                                self.blankstatement,
                                self.identity_elim_name,
                                "",
                                "",
                                comment
                            )
                    else:
                        self.logstep(
                            self.log_notidentity.format(
                                self.identity_elim_name.upper(), 
                                item,
                                first,
                                second
                            )
                        )
                        self.stopproof(
                            self.stopped_notidentity,
                            self.blankstatement,
                            self.identity_elim_name,
                            "",
                            "",
                            comment
                        )

        # If no errors, perform task
        if self.canproceed():
            # Log code
            self.proofcode.append(f'{self.proofcodevariable}.identity_elim({wff}, {first}, {second}, {line})')

            replaced = wff.tree().replace(first.tree(), second.tree(), 1)
            evaluated = eval(replaced, self.objectdictionary)

            #self.premises.append(premise)
            #nextline = len(self.lines)
            #self.prooflist[self.currentproofid][3].append(nextline)
            self.logstep(self.log_identity_elim.format(self.identity_elim_name.upper(), wff, first, second, line))
            newcomment = self.iscomplete(evaluated, comment)
            self.lines.append(
                [
                    evaluated,
                    0,
                    self.currentproofid,
                    self.identity_elim_name,
                    "",
                    "",
                    newcomment,
                    self.linetype_replace,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(evaluated)


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

    def htmllatex(self, df, html: bool = True):
        if html:
            dfhtml = df.to_html().replace('<td>', '<td style="text-align:left">').replace('<th>', '<th style="text-align:center">')
            return IPython.display.HTML(dfhtml)
        else:
            return df


    def metasubstitute(self, pattern: str):
        substitutedstring = pattern.format(*self.metaletters)
        reconstructedobject = eval(substitutedstring, self.metaobjectdictionary)
        return reconstructedobject

    def axioms(self, latex: bool = True, html: bool = True):
        """Display the axioms associated with the logic being used in the proof.
        
        Parameters:
            latex: Present a display through LaTeX
            html: Present an html display

        Examples:
            This example shows the axioms available with the default logic.  To generate
            this one needs to start a Proof instance which allows one to set a particular
            logic.  The `setlogic` defines the metavariables, those Greek letters
            in the listing below.

            >>> from altrea.wffs import Wff, Or
            >>> from altrea.rules import Proof
            >>> 
            >>> prf = Proof()
            >>> prf.setlogic()
            >>>
            >>> prf.axioms(latex=0, html=False)
                                        Axioms                   Description
            explosion            {α, ~α}  ⊢  β                     Explosion
            dneg intro             {α}  ⊢  ~~α  Double Negation Introduction
            dneg elim              {~~α}  ⊢  α   Double Negation Elimination
            lem                      ⊢  α | ~α        Law of Excluded Middle
            wlem                   ⊢  ~α | ~~α   Weak Law of Excluded Middle
            or to not and  {α | β}  ⊢  ~α & ~β       De Morgan Or To Not-And
            not and to or  {~α & ~β}  ⊢  α | β       De Morgan Not-And To Or
            and to not or  {α & β}  ⊢  ~α | ~β       De Morgan And To Not-Or
            not or to and  {~α | ~β}  ⊢  α & β       De Morgan Not-Or To And
            modus ponens      {α, α ⊃ β}  ⊢  β    Given A and A > B Derive B
        """

        axiomcolumn = "".join([self.logic, " ", self.label_axioms])
        headers = [axiomcolumn, "Description"]
        table = []
        index = []
        for i in self.logicaxioms:
            index.append(i[0])
            reconstructedobject = self.metasubstitute(i[1])
            if latex:
                table.append(["".join(["$", reconstructedobject.latex(), "$"]), i[3]])
            else:
                table.append([str(reconstructedobject), i[3]])
        df = pandas.DataFrame(table, index, headers)
        # if html:
        #     dfhtml = df.to_html().replace('<td>', '<td style="text-align:left">').replace('<th>', '<th style="text-align:center">')
        #     return IPython.display.HTML(dfhtml)
        # else:
        #     return df
        return self.htmllatex(df, html)

    def connectives(self, html: bool = True):
        """display the connectives associated with the logic being used in the proof."""

        connectivecolumn = "".join([self.logic, " ", self.label_connectives])
        headers = [connectivecolumn]
        table = []
        index = []
        for i in self.logicconnectives:
            index.append("".join(["$", i[0], "$"]))
            table.append(i[1])
        df = pandas.DataFrame(table, index, headers)
        return self.htmllatex(df, html)
    
    def definitions(self, html: bool = True):
        """display the definitions associated with the logic being used in the proof."""

        definitioncolumn = "".join([self.logic, " ", self.label_definitions])
        headers = [definitioncolumn, "Description"]
        table = []
        index = []
        for i in self.logicdefinitions:
            index.append(i[0])
            reconstructedobject = self.metasubstitute(i[1])
            table.append(["".join(["$", reconstructedobject.latex(), "$"]), i[3]])
        df = pandas.DataFrame(table, index, headers)
        return self.htmllatex(df, html)

    def rules(self, html: bool = True):
        """display the transformation rules associated with the logic being used in the proof."""

        rulecolumn = "".join([self.logic, " ", self.label_transformationrules])
        headers = [rulecolumn, "Description"]
        table = []
        index = []
        for i in self.logicrules:
            index.append(i[0])
            reconstructedobject = self.metasubstitute(i[1])
            table.append(["".join(["$", reconstructedobject.latex(), "$"]), i[3]])
        df = pandas.DataFrame(table, index, headers)
        return self.htmllatex(df, html)

    def lemmas(self, html: bool = True):
        """display the saved proofs associated with the logic being used in the current proof."""

        proofcolumn = "".join([self.logic, " ", self.label_lemmas])
        headers = [proofcolumn, "Description"]
        table = []
        index = []
        for i in self.logiclemmas:
            index.append(i[0])
            reconstructedobject = self.metasubstitute(i[1])
            table.append(["".join(["$", reconstructedobject.latex(), "$"]), i[3]])
        df = pandas.DataFrame(table, index, headers)
        return self.htmllatex(df, html)
    
    def symbols(self, html: bool = True):
        """display the symbols associated with the logic being used in the proof."""

        symbolcolumn = "".join([self.logic, " ", self.label_symbols])
        headers = [symbolcolumn]
        table = []
        index = []
        for i in self.logicsymbols:
            index.append("".join(["$", i[0], "$"]))
            table.append(i[1])
        df = pandas.DataFrame(table, index, headers)
        return self.htmllatex(df, html)

    def displaylog(self):
        """Displays a log of the proof steps.  This will display the entire log that
        was collected for the proof.  It may be useful just prior to displaying the
        proof itself with `displayproof()`.  They provide two different views of the proof.
        Also, `writeproof()` provides a natural language proof version of the proof."""

        size = len(self.log)
        for i in range(len(self.log)):
            if size < 10:
                print("{: >1} {}".format(self.log[i][1], self.log[i][0]))
            elif size < 100:
                print("{: >2} {}".format(self.log[i][1], self.log[i][0]))
            elif size < 1000:
                print("{: >3} {}".format(self.log[i][1], self.log[i][0]))
            else:
                print("{: >4} {}".format(self.log[i][1], self.log[i][0]))

    def thislemma(
            self, 
            name: str, 
            prooflines: list, 
            short: int = 1, 
            latex: int = 1,
            html: bool = True
        ):
        """This function displays the proof lines of a saved proof called here a lemma.

        Parameters:
            short: Display a three column proof with the item, combined rule and lines referenced and comments.  Using the
                default presents all lines of the proof.
            latex: This sets the display for the statement to use latex rather than text.
        """

        # Create the column.
        if short == 1:
            columns = [self.label_item, self.label_rule, self.label_comment]
        elif short == 2:
            columns = [self.label_item, self.label_rule]
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
        indx = [" "]
        for i in range(len(prooflines) - 1):
            indx.append(i + 1)

        # Create the rows of data.
        newp = []
        for i in range(len(prooflines)):
            if latex == 1:
                statement = self.formatitem(
                    prooflines=prooflines,
                    i=i,
                    status=self.complete,
                    latex=True,
                    saved=True,
                    color=False
                )
            else:
                statement = self.formatitem(
                    prooflines=prooflines, 
                    i=i,
                    status=self.complete,
                    latex=False,
                    saved=True
                )
            if short == 1 or short == 2:
                if prooflines[i][self.linesindex] != "":
                    rule = "".join(
                        [
                            prooflines[i][self.linesindex],
                            ", ",
                            prooflines[i][self.ruleindex],
                        ]
                    )
                elif prooflines[i][self.proofsindex] != "":
                    rule = "".join(
                        [
                            prooflines[i][self.proofsindex],
                            ", ",
                            prooflines[i][self.ruleindex],
                        ]
                    )
                else:
                    rule = prooflines[i][self.ruleindex]
                if short == 1:
                    newp.append(
                        [
                            statement,
                            rule,
                            prooflines[i][self.commentindex],
                        ]
                    )
                elif short == 2:
                    newp.append(
                        [
                            statement,
                            rule
                        ]
                    )
                else:
                    print("Should not reach this line in thislemma.")
            else:
                newp.append(
                    [
                        statement,
                        prooflines[i][self.levelindex],
                        prooflines[i][self.proofidindex],
                        prooflines[i][self.ruleindex],
                        prooflines[i][self.typeindex],
                        prooflines[i][self.linesindex],
                        prooflines[i][self.proofsindex],
                        prooflines[i][self.commentindex],
                    ]
                )

        # Use pandas to display the proof lines.
        df = pandas.DataFrame(newp, index=indx, columns=columns)
        return self.htmllatex(df, html)

    def thisproof(
            self, 
            short: int = 0, 
            flip: bool = False, 
            color: int = 1, 
            latex: int = 1,
            html: bool = True):
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
        elif short == 2:
            columns = [self.label_item, self.label_rule]
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
        indx = [" "]
        for i in range(len(self.lines) - 1):
            indx.append(i + 1)

        # Create the rows of data.
        newp = []
        for i in range(len(self.lines)):
            if latex == 1:
                statement = self.formatitem(
                    prooflines=self.lines,
                    i=i,
                    status=self.status,
                    latex=True,
                    saved=False,
                    color=color
                )
            else:
                statement = self.formatitem(
                    prooflines=self.lines, 
                    i=i,
                    status=self.status,
                    latex=False
                )
            if short == 1 or short == 2:
                if self.lines[i][self.linesindex] != "":
                    if flip:
                        rule = "".join(
                            [
                                self.lines[i][self.linesindex],
                                ", ",
                                self.lines[i][self.ruleindex],
                            ]
                        )
                    else:
                        rule = "".join(
                            [
                                self.lines[i][self.ruleindex],
                                " ",
                                self.lines[i][self.linesindex]
                            ]
                        )
                elif self.lines[i][self.proofsindex] != "":
                    if flip:
                        rule = "".join(
                            [
                                self.lines[i][self.proofsindex],
                                ", ",
                                self.lines[i][self.ruleindex],
                            ]
                        )
                    else:
                        rule = "".join(
                            [
                                self.lines[i][self.ruleindex],
                                " ",
                                self.lines[i][self.linesindex]
                            ]
                        )
                else:
                    rule = self.lines[i][self.ruleindex]
                if short == 1:
                    newp.append(
                        [
                            statement,
                            rule,
                            self.lines[i][self.commentindex],
                        ]
                    )
                elif short == 2:
                    newp.append(
                        [
                            statement,
                            rule
                        ]
                    )
                else:
                    print("Should not reach this line in thisproof. A case needs to be defined.")
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
        return self.htmllatex(df, html)
    

    def proofdetailsnew(self, proofname: str, subs, latex: int = 1):
        """Display the details of a proof."""

        # Retrieve proof data.
        displayname, description, pattern = altrea.data.getsavedproof(
            self.logic, proofname
        )
        rows = altrea.data.getproofdetails(self.logic, proofname)

        # Change references to proof lines into the items on those lines.
        statement = self.substitute(pattern, subs, displayname)
        newrows = []
        newrows.append([statement, 0, 0, self.goal_name, "", "", ""])
        for i in rows:
            newrows.append(list(i))

        # Display the proof.
        newp = []
        if latex == 1:
            for i in range(len(newrows)):
                item = self.formatitem(newrows, i, self.complete, latex=True, saved=True)
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
                item = self.formatitem(newrows, i, self.complete, latex=False)
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
        if len(self.logicconnectives) == 0:
            print(
                "{: <25} {: <25}".format(
                    self.label_connectives, self.label_noconnectives
                )
            )
        else:
            print("{}".format(self.label_connectives))
            for i in self.logicconnectives:
                print("{: >25} {: <25}".format(i[1], i[2]))

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
        if len(self.logicconnectives) == 0:
            data.append([self.label_connectives, self.label_noconnectives])
        else:
            for i in self.logicconnectives:
                data.append([self.label_connective, i[1]])

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
                    row.append(i.getmultivalue())
                    premisesvalue = premisesvalue and i.getmultivalue()
                if premisesvalue:
                    counttruepremises += 1

            # Display the goal and assessment of the interpretation on the line.
            row.append(" ")
            goalvalue = goals.getmultivalue()
            if not goalvalue:
                countfalsegoal += 1
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

    def writelatexbegin(self, sectioning: str = "", name: str = ""):
        if sectioning == self.document:
            return "".join(
                [
                    "\\documentclass{",
                    "article}\n\n",
                    "\\usepackage{",
                    "booktabs, csquotes, amsthm, amssymb}\n",
                    "\\newtheorem*{",
                    "theorem*}{",
                    "Theorem}\n",
                    "\\newtheorem*{",
                    "lemma*}{",
                    "Lemma}\n",
                    "\\newtheorem{",
                    "theorem}{Theorem",
                    "}\n\n",
                    "\\begin{",
                    "document}\n\n",
                    "This document was generated by AltRea",
                    self.writethanks(sectioning),
                    ".\n\n"
                ])
        elif sectioning == self.section:
            if name == "":
                name = self.logicdescription
            return "".join(
                [
                    "\\section{",
                    name,
                    "}\n\n This proof was generated by AltRea",
                    self.writethanks(sectioning),
                    ".\n\n"
                ])
        elif sectioning == self.chapter:
            if name == "":
                name = self.logicdescription
            return "".join(
                [
                    "\\chapter{",
                    name,
                    "}\n\n This proof was generated by AltRea",
                    self.writethanks(sectioning),
                    ".\n\n"
                ])
        else:
            print(f"The sectioning style '{sectioning}' has not been defined.")

    
    def writelatexend(self, sectioning: str = ""):
        if sectioning == self.document:
            return "\\end{document}"
        else:
            return ""
        
    
    def writecenter(self, text: str):
        return "".join(
            [
                "\\begin{center}\n\\small\n",
                text,
                "\\end{center}\n"
            ]
        )
    
    def writethanks(self, sectioning: str):
        return "".join(
                [
                    "\\footnote{This ",
                    sectioning,
                    " was generated from the author's proof on ",
                    str(date.today()),
                    " by AltRea ",
                    __version__,
                    ".}"
                ]
            )

    def writelogic(self, sectioning: str = "", name: str = ""):
        """Constructs an English description of the logic used in the proof."""

        # Report general information about the logic.
        logicdescription = "".join(
            [
                "The \\enquote{",
                self.logic,
                "} logic, as defined in ",
                self.writethanks(sectioning),
                ", is described as \\enquote{",
                self.logicdescription,
                "}.\n\n"
            ]
        )

        # Report on the symbols used by the logic.
        dfsymbols = self.symbols(html=False)
        if len(self.logicsymbols) > 0:
            symbols = "".join(
                [
                    "The following table shows the symbols of the logic.\n\n",
                    self.writecenter(dfsymbols.to_latex()),
                    "\n"
                ]
            )
        else:
            symbols = "The logic contains no symbols.\n\n"

        # Report on the connectives used by the logic.
        dfconnectives = self.connectives(html=False)
        if len(self.logicconnectives) > 0:
            connectives = "".join(
                [
                    "The following table shows the connectives of the logic.\n\n",
                    self.writecenter(dfconnectives.to_latex()),
                    "\n"
                ]
            )
        else:
            connectives = "The logic contains no connectives.\n\n"

        # Report any axioms the logic might have
        dfaxioms = self.axioms(html=False)
        if len(self.logicaxioms) > 0:
            axioms = "".join(
                [
                    "The following table shows the axioms of the logic.\n\n",
                    self.writecenter(dfaxioms.to_latex()),
                    "\n"
                ]
            )
        else:
            axioms = "The logic contains no axioms.\n\n"

        # Report any definitions the logic might have.
        dfdefinitions = self.definitions(html=False)
        if len(self.logicdefinitions) > 0:
            definitions = "".join(
                [
                    "The following table shows the definitions of the logic.\n\n",
                    self.writecenter(dfdefinitions.to_latex()),
                ]
            )
        else:
            definitions = "The logic contains no definitions.\n\n"

        # Report any rules the logic might have.
        dfrules = self.rules(html=False)
        if len(self.logicrules) > 0:
            rules = "".join(
                [
                    "The following table shows the transformation rules of the logic.\n\n",
                    self.writecenter(dfrules.to_latex()),
                ]
            )
        else:
            rules = "The logic contains no rules.\n\n"
        
        # Write the report to a variable.
        self.writtenlogicdescription = "".join(
            [
                self.writelatexbegin(sectioning, name), 
                logicdescription, 
                symbols,
                connectives,
                axioms, 
                definitions,
                rules,
                self.writelatexend(sectioning)
            ]
        )   
    

    def writelemma(
            self, 
            displayname: str, 
            short: int = 1, 
            html: bool = True,
            alignment = "llll"
        ):
        """Construct proof details for saved proofs called `lemmas` used in the current proof.  """
        beginlemma = "".join(
            [
                "\\begin{lemma*}[",
                displayname,
                "]\n"
            ]
        )
        name, description, pattern = altrea.data.getlemma(self.logic, displayname)
        lemmaintro = "".join(
            [
                "Description: ",
                description,
                "\n\n"
            ]
        )

        # Gather the codelisting
        codelisting = f"The following is a list of the code used to generate the lemma.\n\n\\begin{{lstlisting}}[language=Python, caption={displayname}]\n"
        codelines = altrea.data.getproofcodelines(self.logic, name)
        for i in codelines:
            codelisting += "".join([i[0], "\n"])
        codelisting += "\\end{lstlisting}\n\n"

        lemmaresult = self.metasubstitute(pattern).latex()
        pd = altrea.data.getproofdetails(self.logic, name)
        proofdetails = [[pattern, 0, 0, self.goal_name, "", "", "", "", "", ""]]
        for i in pd:
            proofdetails.append(list(i))
        for i in proofdetails:
            i[self.statementindex] = self.metasubstitute(i[self.statementindex])
        df = self.thislemma(name, proofdetails, short, html=html)

        lemmastatement = "".join(
            [
                "The entailment $",
                lemmaresult,
                "$ can be derived. "
            ]
        )
        endlemma = "\n\\end{lemma*}\n\n"
        return "".join(
            [
                lemmaintro,
                beginlemma,
                lemmastatement,
                endlemma,
                codelisting,
                self.writecenter(df.to_latex(column_format=alignment)),
                "\n\n"
            ]
        )


    def writeproof(
            self, 
            sectioning: str, 
            name: str = "", 
            short: int = 2,
            flip: bool = False,
            alignment: str = "llll"
        ):
        """Construct a natural language version of the proof."""

        goal = self.buildconclusionpremises().latex()
        beginproof = "\\begin{proof}\n"
        endproof = "\\end{proof}"
        
        # Gather the lemmas
        lemmalist = []
        for i in range(len(self.lines)):
            if self.lines[i][self.typeindex] == self.linetype_lemma:
                lemmalist.append(self.lines[i][self.ruleindex])
        if len(lemmalist) == 0:
            lemmas = self.write_withoutlemmas
        else:
            if len(lemmalist) == 1:
                lemmas = self.write_withlemma
            else:
                lemmas = self.write_withlemmas
            for sp in lemmalist:
                lemmas = self.write_lemmalist.format(lemmas, self.writelemma(sp, short, html=False))

        # Gather the propositions.
        propositions = len(self.letters)
        proofpropositions = ""
        if propositions > 0:
            if propositions == 1:
                proofpropositions = self.write_proposition_one.format(
                    self.letters[0][0].latex()
                )
            elif propositions > 1:
                proofpropositions = self.write_proposition_first.format(
                    self.letters[0][0].latex()
                )
                for i in range(len(self.letters)):
                    if i > 0 and i < propositions - 1:
                        proofpropositions += self.write_proposition_many.format(
                            self.letters[i][0].latex()
                        )
                    elif i == propositions - 1:
                        proofpropositions += self.write_proposition_last.format( 
                            self.letters[i][0].latex()
                        )

        # Gather the subjects.
        subjects = len(self.subjects)
        proofsubjects = ""
        if subjects > 0:
            if subjects == 1:
                proofsubjects = self.write_subject_one.format(
                    self.subjects[0][0].latex()
                )
            elif subjects > 1:
                proofsubjects = self.write_subject_first.format(
                    self.subjects[0][0].latex()
                )
                for i in range(len(self.subjects)):
                    if i > 0 and i < subjects - 1:
                        proofsubjects += self.write_subject_many.format(
                            self.subjects[i][0].latex()
                        )
                    elif i == subjects - 1:
                        proofsubjects += self.write_subject_last.format( 
                            self.subjects[i][0].latex()
                        )

        # Gather the variables.
        variables = len(self.variables)
        proofvariables = ""
        if variables > 0:
            if variables == 1:
                proofvariables = self.write_variable_one.format(
                    self.variables[0][0].latex()
                )
            elif variables > 1:
                proofvariables = self.write_variable_first.format(
                    self.variables[0][0].latex()
                )
                for i in range(len(self.variables)):
                    if i > 0 and i < variables - 1:
                        proofvariables += self.write_variable_many.format(
                            self.variables[i][0].latex()
                        )
                    elif i == variables - 1:
                        proofvariables += self.write_variable_last.format( 
                            self.variables[i][0].latex()
                        )

        # Gather the predicates.
        predicates = len(self.predicates)
        proofpredicates = ""
        if predicates > 0:
            if predicates == 1:
                proofpredicates = self.write_predicate_one.format(
                    self.predicates[0][0].latex()
                )
            elif predicates > 1:
                proofpredicates = self.write_predicate_first.format(
                    self.predicates[0][0].latex()
                )
                for i in range(len(self.predicates)):
                    if i > 0 and i < predicates - 1:
                        proofpredicates += self.write_predicate_many.format(
                            self.predicates[i][0].latex()
                        )
                    elif i == predicates - 1:
                        proofpredicates += self.write_predicate_last.format( 
                            self.predicates[i][0].latex()
                        )


        # Gather the conclusion of the proof
        proofconclusion = ""
        if self.status == self.complete:
            proofconclusion = self.write_proofconclusion.format(
                self.goals_latex, 
                goal
            )

        # Gather premises
        premises = len(self.premises)
        proofpremises = ""  
        if premises == 0:
            proofpremises = self.write_premises_none
        elif premises == 1:
            proofpremises = self.write_premises_one
        else:
            for i in range(len(self.premises)):
                if i == 0:
                    proofpremises += self.write_premises_first.format(self.premises[i].latex())
                elif i >= 1 and i < premises-1:
                    proofpremises += self.write_premises_many.format(self.premises[i].latex())
                else:
                    proofpremises += self.write_premises_last.format(self.premises[i].latex())

        # Gather the proof lines
        df = self.thisproof(short=short, color=0, flip=flip, html=False)

        # Gather the codelisting
        codelisting = f"The following is a list of the code used to generate the proof.\n\n\\begin{{lstlisting}}[language=Python, caption={self.displayname}]\n"
        for i in self.proofcode:
            codelisting += "".join([i, "\n"])
        codelisting += "\\end{lstlisting}"

        # Go through the proof line by line based on the type of line
        # First get the references to lines and proofs.
        linebyline = ""
        for i in range(1,len(self.lines)):
            if self.lines[i][self.linesindex] != "":
                referencedlines = self.lines[i][self.linesindex].split(", ")
            else:
                referencedlines = ""
            referenceditems = ""
            referencedlineslength = len(referencedlines)
            if referencedlineslength > 0:
                referenceditems = self.write_referenceditems_first.format(
                    self.lines[int(referencedlines[0])][self.statementindex].latex(), 
                    referencedlines[0]
                )
                for j in range(1, referencedlineslength):
                    if j < referencedlineslength - 1:
                        referenceditems = self.write_referenceditems_many.format(
                            referenceditems, 
                            self.lines[int(referencedlines[j])][self.statementindex].latex(), 
                            referencedlines[j]
                        )
                    else:
                        referenceditems = self.write_referenceditems_last.format(
                            referenceditems, self.lines[int(referencedlines[referencedlineslength - 1])][self.statementindex].latex(), 
                            referencedlines[referencedlineslength - 1]
                        )
            elif self.lines[i][self.proofsindex] != "":
                prooflist = self.lines[i][self.proofsindex].split(", ")
                if len(prooflist) == 1:
                    referenceditems = self.write_referenceditems_subproof_one.format(
                        referenceditems,
                        self.lines[i][self.proofsindex]
                    )
                else:
                    referenceditems = self.write_referenceditems_subproofs.format(
                        referenceditems,
                        self.lines[i][self.proofsindex].replace(", ", " and ")
                    )

            # Format the text based on the line type
            if self.lines[i][self.typeindex] == self.linetype_axiom:
                linebyline = self.write_axiom.format(
                    linebyline, 
                    self.lines[i][self.ruleindex], 
                    self.lines[i][self.statementindex].latex(), 
                    i
                )
            elif self.lines[i][self.typeindex] == self.linetype_premise:
                pass
            elif self.lines[i][self.typeindex] == self.linetype_definition:
                if referenceditems == "":
                    linebyline = self.write_definition_norefs(
                        linebyline, 
                        self.lines[i][self.statementindex].latex(), 
                        i, 
                        self.lines[i][self.ruleindex]
                    )
                else:
                    linebyline = self.write_definition(
                        linebyline, 
                        referenceditems, 
                        self.lines[i][self.statementindex].latex(), 
                        i, 
                        self.lines[i][self.ruleindex]
                    )
            elif self.lines[i][self.typeindex] == self.linetype_rule:
                if referenceditems == "":
                    linebyline = self.write_rule_norefs.format(
                        linebyline, 
                        self.lines[i][self.ruleindex], 
                        self.lines[i][self.statementindex].latex(), 
                        i
                    )
                else:
                    linebyline = self.write_rule.format(
                        linebyline, 
                        referenceditems, 
                        self.lines[i][self.ruleindex], 
                        self.lines[i][self.statementindex].latex(), 
                        i
                    )
            elif self.lines[i][self.typeindex] == self.linetype_transformationrule:
                if referenceditems == "":
                    linebyline = self.write_transformationrule_norefs.format(
                        linebyline, 
                        self.lines[i][self.ruleindex], 
                        self.lines[i][self.statementindex].latex(), 
                        i
                    )
                else:
                    linebyline = self.write_transformationrule.format(
                        linebyline, 
                        referenceditems, 
                        self.lines[i][self.ruleindex], 
                        self.lines[i][self.statementindex].latex(), 
                        i
                    )
            elif self.lines[i][self.typeindex] == self.linetype_substitution:
                if referenceditems == "":
                    linebyline = self.write_substitution_norefs.format(
                        linebyline, 
                        self.lines[i][self.statementindex].latex(), 
                        i
                    )
                else:
                    linebyline = self.write_substitution.format(
                        linebyline, 
                        referenceditems, 
                        self.lines[i][self.statementindex].latex(), 
                        i
                    )
            elif self.lines[i][self.typeindex] == self.linetype_hypothesis:
                proofid = self.lines[i][self.proofidindex]
                lastline = self.prooflist[proofid][1][1]
                lastitem = self.lines[lastline][self.statementindex]
                linebyline = self.write_hypothesis.format(
                    linebyline, 
                    self.lines[i][self.statementindex].latex(), 
                    i,
                    lastitem.latex(),
                    lastline
                )
            elif self.lines[i][self.typeindex] == self.linetype_lemma:
                linebyline = self.write_lemma.format(
                    linebyline, 
                    referenceditems, 
                    self.lines[i][self.ruleindex], 
                    self.lines[i][self.statementindex].latex(), 
                    i
                )
            else:
                pass
        
        # Assemble the pieces together
        self.writtenproof = "".join(
            [
                self.writelatexbegin(sectioning, name), 
                lemmas,
                self.write_theoremstatement.format(self.name, goal),
                self.write_proofintro,
                self.writecenter(df.to_latex(column_format=alignment)),
                beginproof,
                proofpropositions,
                proofsubjects, 
                proofvariables,
                proofpredicates,
                proofpremises,
                linebyline, 
                proofconclusion, 
                endproof,
                codelisting,
                self.writelatexend(sectioning)
            ]
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
            print(
                self.log_axiomnotfound.format(self.removeaxiom_name.upper(), name)
            )
        else:
            self.logicaxioms.pop(i)
            if self.logicdatabase != self.label_nodatabase:
                altrea.data.deleteaxiom(self.logic, name)
                print(
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
            print(
                self.log_definitionnotfound.format(
                    self.removedefinition_name.upper(), name
                )
            )
        else:
            self.logicdefinitions.pop(i)
            if self.logicdatabase != self.label_nodatabase:
                altrea.data.deletedefinition(self.logic, name)
                print(
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
            print(
                self.log_proofdeleted.format(
                    self.replaceproof_name.upper(),
                    self.name,
                    self.logicdatabase,
                    self.logic,
                )
            )
        else:
            print(
                self.log_nosavedproof.format(self.removeproof_name.upper(), name)
            )

    def removerule(self, name: str):
        """Remove a rule from the current proof as well as the logic's database if one has been identified.

        Parameters:
            name: The name of the rule to be removed.

        """

        # Look for errors

        # If no errors, perform the task
        indexfound = -1
        for i in range(len(self.logicrules)):
            if self.logicrules[i][0] == name:
                indexfound = i
                break
        if indexfound == -1:
            print(self.valueerror_rulenotfound.format(self.removerule_name.upper(), name))
        else:
            self.logicrules.pop(i)
            if self.logicdatabase != self.label_nodatabase:
                altrea.data.deleterule(self.logic, name)
                print(
                    self.log_ruleremoved.format(
                        self.removerule_name.upper(), name
                    )
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
                    raise ValueError(self.valueerror_badpremise.format(i))
        else:
            raise ValueError(self.valueerror_badconclusion.format(conclusion))

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
                print(
                    self.log_axiomalreadyexists.format(
                        self.saveaxiom_name.upper(), name
                    )
                )
                print(
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
                print(
                    self.log_axiomsaved.format(self.saveaxiom_name.upper(), name)
                )
                print(self.log_axiomsaved.format(self.saveaxiom_name.upper(), name))

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
                    raise ValueError(self.valueerror_badpremise.format(i))
        else:
            raise ValueError(self.valueerror_badconclusion.format(conclusion))

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
                print(
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
                print(
                    self.log_definitionsaved.format(
                        self.savedefinition_name.upper(), name
                    )
                )
                print(self.log_definitionsaved.format(self.savedefinition_name.upper(), name))

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
                raise ValueError(self.log_proofhasnoname.format(
                        self.saveproof_name.upper(),
                        self.name,
                        self.displayname,
                        self.description,
                    ))
            else:
                howmany = altrea.data.addproof(self.proofdatafinal, self.proofcode)
                if howmany == 0:
                    proof = [
                        self.name,
                        self.proofdatafinal[0][4],
                        self.displayname,
                        self.description,
                    ]
                    self.logiclemmas.append(proof)
                    print(
                        self.log_proofsaved.format(
                            self.saveproof_name.upper(),
                            self.name,
                            self.proofdatafinal[0][4],
                            self.logicdatabase,
                            self.logic,
                        )
                    )
                else:
                    print(
                        self.log_proofalreadyexists.format(
                            self.saveproof_name.upper(), self.name
                        )
                    )
        else:
            raise ValueError(self.log_notcomplete.format(self.saveproof_name.upper(), self.name))

    def saverule(
        self,
        name: str,
        displayname: str,
        description: str,
        conclusion: Wff,
        premise: list = [],
    ):
        """Save a rule for the current proof and in the logic's database if one has been identified.

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
        if isinstance(conclusion, altrea.wffs.Wff):
            for i in premise:
                if not isinstance(i, altrea.wffs.Wff):
                    raise ValueError(self.valueerror_badpremise.format(i))
        else:
            raise ValueError(self.valueerror_badconclusion.format(conclusion))

        # If no errors, perform the task
        propositionlist = []
        conclusionpremise = ConclusionPremises(conclusion, premise).pattern(
            propositionlist
        )
        rule = [name, conclusionpremise, displayname, description]
        found = False
        for i in self.logicrules:
            if i[0] == name:
                found = True
                break
        if found:
            print(
                self.log_rulereadyexists.format(
                    self.saverule_name.upper(), name
                )
            )
        else:
            if self.logic != "":
                altrea.data.addrule(
                    self.logic, name, conclusionpremise, displayname, description
                )
            self.logicrules.append(rule)
            print(
                self.log_rulesaved.format(
                    self.saverule_name.upper(), name
                )
            )
            print(self.log_rulesaved.format(self.saverule_name.upper(), name))

    def entailment(
            self, 
            conclusion: Wff, 
            premises: list = [], 
            name: str = "", 
            displayname: str = "", 
            description: str = "", 
            kind: str = ""
        ):
        """View how the conclusion and any premises look as text and latex before actually
        adding them as an axiom, definition or transformation rule.

        There are propositional metavariables available to use representing the Greek letters.
        These are also used to display the axioms, definitions and rules for the logic.
        These can be referenced by referring to self.mvalpha through self.mvomega after one
        has run `setlogic()` which defines these metavariables.

        Parameters:
            conclusion: The conclusion that follows from the premises (if any).
            premises: A list of premises which entail the conclusion.
            name: The name of the axiom, definition or rule that this entailment
                will be assigned to.
            displayname: The name displayed when this entailment is used.
            description: A lengthier description that could store the source of the entailment
                as well as a description of what it is intended to do.
            kind: When this is not "" it will create the axiom, definition or rule
                specified by this kind.  Acceptable values as `prf.label_axiom`,
                `prf.label_definition` and `prf.label_rule`.

        Example:
            In this example we will prove that every statement is true.  This is the
            logic known as `trivialism`.  We only need two axioms which we will define
            in the example.  We will need an axiom that allows us to construct a
            contradiction.  That is done by the entailment named `contradicting`.
            We will also need an axiom that will allow of to derive anything we
            please from a contradiction.  That is called `exploding` below.

            Let B be a variable standing for any proposition.  After the Contradiction
            axiom is applied to a propositional variable C followed by the Exploding
            axiom, we can derive B.  Since B was any proposition, in this logic, 
            all propositions are derivable.

            Although these two axioms have been saved it is only to the currently 
            instantiated Proof object.  The defaults will return when a new Proof
            object is instantiated.  One can preserve this work by saving it to
            a named object or save them to a logic already defined and provided
            with AltRea.

            >>> from altrea.wffs import And, Not
            >>> from altrea.rules import Proof
            >>> 
            >>> prf = Proof()
            >>> prf.setrestricted(False)
            >>> B = prf.proposition("B")
            >>> C = prf.proposition("C")
            >>> prf.setlogic()
            >>> prf.goal(B)
            >>> prf.entailment(
            ...     And(prf.mvalpha, Not(prf.mvalpha)),
            ...     [],
            ...     name="contradicting",
            ...     displayname= "Contradiction",
            ...     description="Contradiction",
            ...     kind=prf.label_axiom)
            SAVE AXIOM: The axiom named "contradicting" has been saved.
            SAVE AXIOM: The axiom named "contradicting" has been saved.
            >>> prf.axiom("contradicting", [C])
            >>> prf.rule("conj elim l", [C, Not(C)], [1])
            >>> prf.rule("conj elim r", [C, Not(C)], [1])
            >>> prf.entailment(
            ...     prf.mvbeta,
            ...     [prf.mvalpha, Not(prf.mvalpha)],
            ...     name="exploding",
            ...     displayname= "Explosion",
            ...     description="Explosion",
            ...     kind=prf.label_axiom)
            SAVE AXIOM: The axiom named "exploding" has been saved.
            SAVE AXIOM: The axiom named "exploding" has been saved.
            >>> prf.axiom("exploding", [C, B], [2, 3])
            >>>
            >>> prf.thisproof(latex=0, short=1, html=False)
                Item                       Rule   Comment
                    B                       GOAL
            1  C & ~C              Contradiction
            2       C   1, Conjunction Elim Left
            3      ~C  1, Conjunction Elim Right
            4       B            2, 3, Explosion  COMPLETE
        """

        prop = ConclusionPremises(conclusion, premises)
        if kind == "":
            latexprop = "".join(["$", prop.latex(), "$"])
            expandedprop = prop.tree()
            wfflist = []
            pattern = "".join(
                [
                    "(logic, \"",
                    name,
                    "\", \"",
                    prop.pattern(wfflist),
                    "\", \"",
                    displayname,
                    "\", \"",
                    description,
                    "\"),"
                ]
            )
            df = pandas.DataFrame(
                [[name], [displayname], [description], [prop], [latexprop], [expandedprop], [pattern]], 
                columns=["Display"], 
                index=["Name", "Display Name", "Description", "Text", "LaTeX", "Expanded", "Pattern"]
            )
            return df
        elif name == "" or displayname == "" or description == "":
            raise ValueError(self.valueerror_names.format(name, displayname, description))
        else:
            if kind == self.label_axiom:
                self.saveaxiom(name, displayname, description, conclusion, premises)
            elif kind == self.label_definition:
                self.savedefinition(name, displayname, description, conclusion, premises)
            elif kind == self.label_rule:
                self.saverule(name, displayname, description, conclusion, premises)
            else:
                raise ValueError(self.valueerror_kind.format(kind))
        

    """NATURAL DEDUCTION AND GENERAL PROOF CONSTRUCTION
    
    These functions include an introduction and an elimination function for each logical connective.
    Also included here are functions to define a goal, reiterate from a parent proof, define a premise 
    or define an hypotheses.
    """

    # def addhypothesis_old(self, hypothesis: Wff, comment: str = ""):
    #     """Add to the currently opened subordinate proof a new hypothesis which will be a conjoint of the antecedent
    #     of the resulting implication when the subproof is finished.

    #     Parameters:
    #         hypothesis: The hypothesis that will be added.
    #         comment: An optional comment the user may add to this line of the proof.

    #     Examples:
    #         To introduce an implication one needs an antecedent and a consequent.  The antecedent is
    #         entered into the proof through an hypothesis which begins a subordinate proof.  Optionally,
    #         additional hypotheses can be added through this function.  These additional hypotheses do
    #         not start a subordinate proof.  Rather, they add to the current one.  After the conclusion
    #         has been derived the subordinate proof is closed by calling `implication_intro` which
    #         introduces an implication in the parent proof containing all of the hypotheses as conjoints
    #         of an `And` object.  That process is illustrated in this example.  The comments are optional.

    #         >>> from altrea. import Implies, And
    #         >>> from altrea.rules import Proof
    #         >>> pr = Proof()
    #         >>> A = pr.proposition('A')
    #         >>> B = pr.proposition('B')
    #         >>> C = pr.proposition('C')
    #         >>> pr.setlogic()
    #         >>> pr.goal(Implies(And(A, C), B), 'The goal of the proof')
    #         >>> pr.premise(B, 'A premise for the proof')
    #         >>> pr.hypothesis(A, 'This opens a subproof with the hypothesis "A"')
    #         >>> pr.addhypothesis(C, 'Add a second hypothesis without opening a subproof')
    #         >>> pr.reiterate(1, 'Bring the premise on line 1 to the subproof')
    #         >>> pr.implication_intro('Close the subproof with an implication in the main proof')
    #         >>> pr.displayproof(short=1, latex=0)
    #                 Item  ...                                                              Comment
    #         (A & C) > B  ...                                                The goal of the proof
    #         1            B  ...                                              A premise for the proof
    #         2        A   |  ...                        This opens a subproof with the hypothesis "A"
    #         3        C __|  ...                   Add a second hypothesis without opening a subproof
    #         4        B   |  ...                          Bring the premise on line 1 to the subproof
    #         5  (A & C) > B  ...  COMPLETE - Close the subproof with an implication in the main proof

    #     See Also:
    #         - `hypothesis`
    #         - `implication_intro`
    #     """

        # # Look for errors
        # if self.canproceed():
        #     if self.goodrule(
        #         self.rule_naturaldeduction,
        #         self.addhypothesis_name,
        #         self.addhypothesis_name,
        #         comment,
        #     ):
        #         if self.goodobject(
        #             hypothesis,
        #             self.addhypothesis_name,
        #             self.addhypothesis_name,
        #             comment,
        #         ):
        #             if self.currentproofid == 0:
        #                 self.logstep(
        #                     self.log_nosubproof.format(
        #                         self.addhypothesis_name.upper(), hypothesis
        #                     )
        #                 )
        #                 self.stopproof(
        #                     self.stopped_nosubproof,
        #                     self.blankstatement,
        #                     self.hypothesis_name,
        #                     "",
        #                     "",
        #                     comment,
        #                 )
        #             elif self.subproofavailable not in [
        #                     self.subproofavailable_not, 
        #                     self.subproofavailable_openstrict
        #                 ]:
        #                 self.logstep(
        #                     self.log_unavailablesubproof.format(
        #                         self.addhypothesis_name.upper(), 
        #                         self.subproofavailable
        #                     )
        #                 )
        #                 self.stopproof(
        #                     self.stopped_unavailablesubproof,
        #                     self.blankstatement,
        #                     self.addhypothesis_name,
        #                     "",
        #                     "",
        #                     comment
        #                 )

        # # If no errors, perform task
        # if self.canproceed():
        #     self.subproofavailable = self.subproofavailable_not
        #     nextline = len(self.lines)
        #     self.prooflist[self.currentproofid][3].append(nextline)
        #     self.logstep(
        #         self.log_addhypothesis.format(
        #             self.addhypothesis_name.upper(), hypothesis, self.currentproofid
        #         )
        #     )
        #     newcomment = self.iscomplete(hypothesis, comment)
        #     self.lines.append(
        #         [
        #             hypothesis,
        #             self.level,
        #             self.currentproofid,
        #             self.hypothesis_name,
            #         "",
            #         "",
            #         newcomment,
            #         self.linetype_hypothesis,
            #         self.subproofchain,
            #     ]
            # )
            # #self.appendproofdata(hypothesis, self.hypothesis_tag)
            # self.appendproofdata(hypothesis)

    def axiom(
        self, name: str, subslist: list, premiselist: list = [], comment: str = ""
    ):
        """Use an axiom that is available for the logic to use.

        Parameters:
            name: The name of the axiom one wishes to use.
            subslist: A list of wff object instances which will be used as substitutes in the order they are provided
                for the string metavariables.
            premiselist: A list of integers referencing previous lines of the proof which will be matched to those required
                to use the axiom in the order the axiom specifies.  Some axioms require no premises.
            comment: An optional comment the user may add to this line of the proof.

        Examples:
            The `lem`, Law of Excluded Middle, is an axiom provided by default if one does not specify any logic.
            If one does specify a logic, this default will be removed, allowing only the axioms that one has
            defined for the logic to be available.  This first example shows how the lem axiom can be used.

            >>> from altrea.wffs import Wff, Or
            >>> from altrea.rules import Proof
            >>> 
            >>> prf = Proof()
            >>> prf.setrestricted(False)
            >>> A = prf.proposition("A")
            >>> prf.setlogic()
            >>>
            >>> prf.goal(A)
            >>> prf.axiom("lem", [A], [])
            >>>
            >>> prf.thisproof(latex=0, short=1, html=False)
                 Item  Rule Comment
                    A  GOAL
            1  A | ~A   LEM
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

        # Look for errors: Available subproof
        if self.canproceed:
            if self.goodsubproof(
                self.axiom_name,
                self.axiom_name,
                comment
            ):
                pass

        # If no errors, perform task.
        if self.canproceed():
             #Log code
            subslisttree = [i.tree() for i in subslist]
            self.proofcode.append(f'{self.proofcodevariable}.axiom("{name}", {subslisttree}, {str(premiselist)})'.replace("'", ""))

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
            self.appendproofdata(conclusionpremises.conclusion)


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

        # Look for errors: Available subproof
        if self.canproceed:
            if self.goodsubproof(
                self.definition_name,
                self.definition_name,
                comment
            ):
                pass

        # If no errors, perform task.
        if self.canproceed():
            #Log code
            subslisttree = [i.tree() for i in subslist]
            self.proofcode.append(f'{self.proofcodevariable}.definition("{name}", {subslisttree}, {str(premiselist)})'.replace("'", ""))

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
            self.appendproofdata(conclusionpremises.conclusion)

 
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
            # Log code
            self.proofcode.append(f'{self.proofcodevariable}.goal({goal.tree()})')

            # Proceed with task
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
            #self.lines[0][self.statementindex] = self.goals_string
            self.lines[0][self.statementindex] = goal
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
                    hypothesis, 
                    self.hypothesis_name, 
                    self.hypothesis_name, 
                    comment
                ):
                    if self.goodgoal(
                        self.hypothesis_name, 
                        self.hypothesis_name, 
                        comment
                    ):
                        if self.subproofavailable not in [
                                self.subproofavailable_opennormal, 
                                self.subproofavailable_openstrict,
                                self.subproofavailable_not
                            ] or self.level == 0:
                            self.logstep(
                                self.log_unavailablesubproof.format(
                                    self.hypothesis_name.upper(), 
                                    self.subproofavailable
                                )
                            )
                            self.stopproof(
                                self.stopped_unavailablesubproof,
                                self.blankstatement,
                                self.hypothesis_name,
                                "",
                                "",
                                comment
                            )

        # If no errors, perform task
        if self.canproceed():
            # Log code
            self.proofcode.append(f'{self.proofcodevariable}.hypothesis({hypothesis.tree()})')

            # self.level += 1
            # self.subproofchain = "".join(
            #     #[self.label_subproofnormal, self.subproofchain]
            #     [self.subproofchain, self.label_subproofnormal]
            # )
            # nextline = len(self.lines)
            # self.currentproof = [nextline]
            # self.currenthypotheses = [nextline]
            # self.subproof_status = self.subproof_normal
            # self.prooflist.append(
            #     [
            #         self.level,
            #         self.currentproof,
            #         self.currentproofid,
            #         self.currenthypotheses,
            #         self.subproofchain,
            #     ]
            # )
            # self.previousproofid = self.currentproofid
            # self.previousproofchain.append(self.currentproofid)
            # self.currentproofid = len(self.prooflist) - 1
            self.subproofavailable = self.subproofavailable_not
            nextline = len(self.lines)
            self.prooflist[self.currentproofid][3].append(nextline)
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
            self.appendproofdata(hypothesis)


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
                if self.subproofavailable not in [self.subproofavailable_closenormal, self.subproofavailable_closestrict]:
                    self.logstep(
                        self.log_unavailablesubproof.format(
                            self.implication_intro_name.upper(), 
                            self.subproofavailable
                        )
                    )
                    self.stopproof(
                        self.stopped_unavailablesubproof,
                        self.blankstatement,
                        self.implication_intro_name,
                        "",
                        "",
                        comment
                    )

        # If no errors, perform task
        if self.canproceed():
            #Log code
            self.proofcode.append(f'{self.proofcodevariable}.implication_intro()')
            antecedent, consequent, previousproofid, previoussubproofstatus = (
                self.getproof(self.closedproofid)
            )
            proofid = self.closedproofid
            self.closedproofid = 0
            self.subproofavailable = self.subproofavailable_not
            implication = Implies(antecedent, consequent)
            if self.subproofavailable == self.subproofavailable_closestrict:
                name = self.implication_intro_strict_name
                rulename = self.implication_intro_strict_rulename
                message = self.log_implication_intro_strict
            else:
                name = self.implication_intro_name
                rulename = self.implication_intro_rulename
                message = self.log_implication_intro
            self.logstep(message.format(name.upper(), implication, proofid))
            newcomment = self.iscomplete(implication, comment)
            self.lines.append(
                [
                    implication,
                    self.level,
                    self.currentproofid,
                    rulename,
                    "",
                    self.refproof(proofid),
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(implication)


    def necessary_intro(self, comment: str = ""):
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
                comment
            ):
                if self.subproofavailable not in [ 
                        self.subproofavailable_closestrict
                    ]:
                    self.logstep(
                        self.log_unavailablesubproof.format(
                            self.necessary_intro_name.upper(), 
                            self.subproofavailable
                        )
                    )
                    self.stopproof(
                        self.stopped_unavailablesubproof,
                        self.blankstatement,
                        self.necessary_intro_name,
                        "",
                        "",
                        comment
                    )

        # If no errors, perform task
        if self.canproceed():
            #Log code
            self.proofcode.append(f'{self.proofcodevariable}.necessary_intro()')

            self.subproofavailable = self.subproofavailable_not
            index = len(self.lines) - 1
            statement = self.item(index)
            necessarystatement = Necessary(statement)
            self.logstep(
                self.log_necessary_intro.format(
                    self.necessary_intro_name.upper(), necessarystatement, statement
                )
            )
            newcomment = self.iscomplete(necessarystatement, comment)
            self.lines.append(
                [
                    necessarystatement,
                    self.level,
                    self.currentproofid,
                    self.necessary_intro_rulename,
                    str(index), #self.reflines(i),
                    "",
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(necessarystatement)


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
                if self.subproofavailable not in [ 
                        self.subproofavailable_closestrict
                    ]:
                    self.logstep(
                        self.log_unavailablesubproof.format(
                            self.possibly_elim_name.upper(), 
                            self.subproofavailable
                        )
                    )
                    self.stopproof(
                        self.stopped_unavailablesubproof,
                        self.blankstatement,
                        self.possibly_elim_name,
                        "",
                        "",
                        comment
                    )

        # If no errors, perform task
        if self.canproceed():
            #Log code
            self.proofcode.append(f'{self.proofcodevariable}.possibly_elim()')

            line = len(self.lines) - 1
            statement = self.item(len(self.lines) - 1)
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
                    self.possibly_elim_rulename,
                    self.reflines(line),
                    "",
                    newcomment,
                    self.linetype_transformationrule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(possiblystatement)


    def premise(
        self,
        premise: Wff,
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
                    premise, 
                    self.premise_name, 
                    self.premise_name, 
                    comment
                ):
                    if self.goodgoal(
                        self.premise_name, 
                        self.premise_name, 
                        comment
                    ):
                        if self.goodsubproof(
                            self.premise_name,
                            self.premise_name,
                            comment
                        ):
                            pass
                        

        # If no errors, perform task
        if self.canproceed():
            # Log code
            self.proofcode.append(f'{self.proofcodevariable}.premise({premise.tree()})')

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
            self.appendproofdata(premise)

    def proposition(self, name: str, latex: str = "", kind: str = "Proposition"):
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
                is a Proposition.  An alternative is Metavariable.

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
        if latex == "":
            latex = name
        self.proofcode.append(f'{name} = {self.proofcodevariable}.proposition("{name}", "{latex}")')
        self.logstep(
            self.log_proposition.format(self.proposition_name.upper(), p, howmany)
        )
        return p

    def subject(self, name: str, latex: str = ""):
        p = Subject(name, latex)
        self.objectdictionary.update({name: p})
        self.subjects.append([p, name, latex])
        howmany = len(self.subjects)
        if latex == "":
            latex = name
        self.proofcode.append(f'{name} = {self.proofcodevariable}.subject("{name}", "{latex}")')
        self.logstep(
            self.log_subject.format(self.subject_name.upper(), p, howmany)
        )
        return p
    
    def connective(self, name: str, string: str, latex: str):
        p = Connective(name, latex)
        self.objectdictionary.update({name: p})
        self.binaryconnectives.append([p, name, string, latex])
        howmany = len(self.binaryconnectives)
        if latex == "":
            latex = name
        self.proofcode.append(f'{name} = {self.proofcodevariable}.connective("{name}", "{latex}")')
        self.logstep(
            self.log_binaryconnective.format(self.binaryconnective_name.upper(), p, howmany)
        )
        return p
    
    def predicate(self, name: str, latex: str):
        p = Predicate(name, latex)
        self.objectdictionary.update({name: p})
        self.predicates.append([p, name, latex])
        howmany = len(self.predicates)
        if latex == "":
            latex = name
        self.proofcode.append(f'{name} = {self.proofcodevariable}.predicate("{name}", "{latex}")')
        self.logstep(
            self.log_predicate.format(self.predicate_name.upper(), p, howmany)
        )
        return p
    
    def variable(self, name: str, latex: str = ""):
        p = Variable(name, latex)
        self.objectdictionary.update({name: p})
        self.variables.append([p, name, latex])
        howmany = len(self.variables)
        if latex == "":
            latex = name
        self.proofcode.append(f'{name} = {self.proofcodevariable}.variable("{name}", "{latex}")')
        self.logstep(
            self.log_thing.format(self.variable_name.upper(), p, howmany)
        )
        return p

    def openstrictsubproof(
        self,
        comment: str = "",
    ):
        """Begin a strict subproof with either a reiterated line or an hypothesis."""

        # Look for errors
        if self.canproceed():
            if self.goodrule(
                self.rule_naturaldeduction,
                self.openstrictsubproof_name,
                self.openstrictsubproof_name,
                comment,
            ):
                pass
            
        # If no errors, perform task
        if self.canproceed():
            #Log code
            self.proofcode.append(f'{self.proofcodevariable}.openstrictsubproof()')

            self.level += 1
            self.subproofchain = "".join(
                [self.subproofchain, self.label_subproofstrict]
            )
            nextline = len(self.lines)
            self.currentproof = [nextline]
            self.subproof_status = self.subproof_strict
            self.previousproofid = self.currentproofid
            self.previousproofchain.append(self.currentproofid)
            self.currentproofid = len(self.prooflist)
            self.subproofavailable = self.subproofavailable_openstrict
            self.prooflist.append(
                [
                    self.currentproofid,
                    self.currentproof,
                    self.previousproofid,
                    [], 
                    self.subproof_status,
                ]
            )
            self.logstep(
                self.log_strictsubproofstarted.format(
                    self.openstrictsubproof_name.upper(),
                    self.currentproofid
                )
            )
            

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
                # elif self.subproofavailable not in [
                #             self.subproofavailable_not, 
                #             self.subproofavailable_openstrict
                #         ]:
                #         self.logstep(
                #             self.log_unavailablesubproof.format(
                #                 self.reiterate_name.upper(), 
                #                 self.subproofavailable
                #             )
                #         )
                #         self.stopproof(
                #             self.stopped_unavailablesubproof,
                #             self.blankstatement,
                #             self.reiterate_name,
                #             "",
                #             "",
                #             comment
                #         )

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
            # Log code
            self.proofcode.append(f'{self.proofcodevariable}.reiterate({str(line)})')

            self.subproofavailable = self.subproofavailable_not
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
                    self.linetype_reiterate,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(statement)

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
            # Log code
            self.proofcode.append(f'{self.proofcodevariable}.setlogic("{logic}")')
            self.proofcode.append(" ")

            # Create metavariables
            self.mvalpha = Wff("α", "\\alpha")
            self.metaletters.append(self.mvalpha.name)
            self.metaobjectdictionary.update({self.mvalpha.name: self.mvalpha})
            self.mvbeta = Wff("β", "\\beta")
            self.metaletters.append(self.mvbeta.name)
            self.metaobjectdictionary.update({self.mvbeta.name: self.mvbeta})
            self.mvgamma = Wff("γ", "\\gamma")
            self.metaletters.append(self.mvgamma.name)
            self.metaobjectdictionary.update({self.mvgamma.name: self.mvgamma})
            self.mvdelta = Wff("δ", "\\delta")
            self.metaletters.append(self.mvdelta.name)
            self.metaobjectdictionary.update({self.mvdelta.name: self.mvdelta})
            self.mvepsilon = Wff("ε", "\\epsilon")
            self.metaletters.append(self.mvepsilon.name)
            self.metaobjectdictionary.update({self.mvepsilon.name: self.mvepsilon})
            self.mvzeta = Wff("ζ", "\\zeta")
            self.metaletters.append(self.mvzeta.name)
            self.metaobjectdictionary.update({self.mvzeta.name: self.mvzeta})
            self.mveta = Wff("η", "\\eta")
            self.metaletters.append(self.mveta.name)
            self.metaobjectdictionary.update({self.mveta.name: self.mveta})
            self.mvtheta = Wff("θ", "\\theta")
            self.metaletters.append(self.mvtheta.name)
            self.metaobjectdictionary.update({self.mvtheta.name: self.mvtheta})
            self.mviota = Wff("ι", "\\iota")
            self.metaletters.append(self.mviota.name)
            self.metaobjectdictionary.update({self.mviota.name: self.mviota})
            self.mvkappa = Wff("κ", "\\kappa")
            self.metaletters.append(self.mvkappa.name)
            self.metaobjectdictionary.update({self.mvkappa.name: self.mvkappa})
            self.mvlambda = Wff("λ", "\\lambda")
            self.metaletters.append(self.mvlambda.name)
            self.metaobjectdictionary.update({self.mvlambda.name: self.mvlambda})
            self.mvmu = Wff("μ", "\\mu")
            self.metaletters.append(self.mvmu.name)
            self.metaobjectdictionary.update({self.mvmu.name: self.mvmu})
            self.mvnu = Wff("ν", "\\nu")
            self.metaletters.append(self.mvnu.name)
            self.metaobjectdictionary.update({self.mvnu.name: self.mvnu})
            self.mvomicron = Wff("ο", "\\omicron")
            self.metaletters.append(self.mvomicron.name)
            self.metaobjectdictionary.update({self.mvomicron.name: self.mvomicron})
            self.mvpi = Wff("π", "\\pi")
            self.metaletters.append(self.mvpi.name)
            self.metaobjectdictionary.update({self.mvpi.name: self.mvpi})
            self.mvrho = Wff("ρ", "\\rho")
            self.metaletters.append(self.mvrho.name)
            self.metaobjectdictionary.update({self.mvrho.name: self.mvrho})
            self.mvsigma = Wff("σ", "\\sigma")
            self.metaletters.append(self.mvsigma.name)
            self.metaobjectdictionary.update({self.mvsigma.name: self.mvsigma})
            self.mvtau = Wff("τ", "\\tau")
            self.metaletters.append(self.mvtau.name)
            self.metaobjectdictionary.update({self.mvtau.name: self.mvtau})
            self.mvupsilon = Wff("υ", "\\upsilon")
            self.metaletters.append(self.mvupsilon.name)
            self.metaobjectdictionary.update({self.mvupsilon.name: self.mvupsilon})
            self.mvphi = Wff("φ", "\\phi")
            self.metaletters.append(self.mvphi.name)
            self.metaobjectdictionary.update({self.mvphi.name: self.mvphi})
            self.mvchi = Wff("χ", "\\chi")
            self.metaletters.append(self.mvchi.name)
            self.metaobjectdictionary.update({self.mvchi.name: self.mvchi})
            self.mvpsi = Wff("ψ", "\\psi")
            self.metaletters.append(self.mvpsi.name)
            self.metaobjectdictionary.update({self.mvpsi.name: self.mvpsi})
            self.mvomega = Wff("ω", "\\omega")
            self.metaletters.append(self.mvomega.name)
            self.metaobjectdictionary.update({self.mvomega.name: self.mvomega})
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
                    self.logiclemmas = altrea.data.getproofs(logic)
                except TypeError:
                    self.logicsavedoriifs = []
                try:
                    self.logicrules = altrea.data.getrules(logic)
                except TypeError:
                    self.logicrules = []
                try:
                    self.logicconnectives = altrea.data.getconnectives(logic)
                except TypeError:
                    self.logicconnectives = []
            else:
                self.setrestricted(self.restricted)
                

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
            statement = self.item(line)
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
            self.appendproofdata(newstatement)

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
            #if self.canproceed:
            if self.goodsubproof(
                self.rule_name,
                self.rule_name,
                comment
            ):
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
                # if self.subproofavailable not in [
                #         self.subproofavailable_not
                #     ]:
                #     self.logstep(
                #         self.log_unavailablesubproof.format(
                #             self.rule_name.upper(), 
                #             self.subproofavailable
                #         )
                #     )
                #     self.stopproof(
                #         self.stopped_unavailablesubproof,
                #         self.blankstatement,
                #         self.rule_name,
                #         "",
                #         "",
                #         comment
                #     )

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

        # Look for errors: Available subproof
        # if self.canproceed:
        #     if self.goodsubproof(
        #         self.rule_name,
        #         self.rule_name,
        #         comment
        #     ):
        #         pass

        # If no errors, perform task.
        if self.canproceed():
            #Log code
            subslisttree = [i.tree() for i in subslist]
            self.proofcode.append(f'{self.proofcodevariable}.rule("{name}", {subslisttree}, {str(lines)})'.replace("'", ""))

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
                    self.linetype_rule,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(conclusionpremises.conclusion)

    def truth(self, name: str, latex: str = ""):
        newtruth = Truth(name, latex)
        self.objectdictionary.update({name: newtruth})
        self.truths.append([newtruth, name])
        howmany = len(self.truths)
        self.logstep(
            f'TRUTH: The letter "{newtruth.name}" (latex: "{newtruth.latexname}") for a generic truth formula has been defined making {howmany} so far.'
        )
        return newtruth

    def lemma(
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
                    self.log_nosavedproof.format(self.lemma_name.upper(), name)
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
                self.lemma_name.upper(), displayname, comment, subslist
            )

        # Look for errors: Check lines entered from the proof.
        if self.canproceed():
            matchpremiselist, lineslist = self.checkitemlines(
                self.lemma_name.upper(), displayname, comment, premiselist
            )

        # Look for errors: Check if substitutions can be made.
        if self.canproceed():
            conclusionpremises = self.substitute(pattern, subs, displayname)

        # Look for errors: Check if premises match identified lines in the current proof.
        if self.canproceed():
            self.checkpremises(
                self.lemma_name.upper(),
                displayname,
                comment,
                conclusionpremises.premises,
                matchpremiselist,
            )

        # Look for errors: Available subproof
        if self.canproceed:
            if self.subproofavailable not in [ 
                    self.subproofavailable_not
                ]:
                self.logstep(
                    self.log_unavailablesubproof.format(
                        self.lemma_name.upper(), 
                        self.subproofavailable
                    )
                )
                self.stopproof(
                    self.stopped_unavailablesubproof,
                    self.blankstatement,
                    self.lemma_name,
                    "",
                    "",
                    comment
                )

        # If no errors, perform task.
        if self.canproceed():
            #Log code
            subslisttree = [i.tree() for i in subslist]
            self.proofcode.append(f'{self.proofcodevariable}.lemma("{name}", {subslisttree}, {str(premiselist)})'.replace("'", ""))

            self.logstep(
                self.log_useproof.format(
                    self.lemma_name.upper(),
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
                    self.linetype_lemma,
                    self.subproofchain,
                ]
            )
            self.appendproofdata(conclusionpremises.conclusion)
