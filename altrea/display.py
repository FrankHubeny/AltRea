"""This module contains procedures to forat a display of data.

- `metadata(p)` - Print a list of a proof's metadata.
- `show(p)` - Print a proof line by line.
- `truthtable(p)` - Print a truth table of the proofs premises implying its goal.
"""

import pandas

from altrea.rules import Proof
import altrea.data


def fitchnotation(p: Proof):
    """This function changes the names for rules to better conform to Frederic Fitch's Symbolic Logic text."""

    # Attributes from the altrea.truthfunction.Proof class
    p.premise_name = "hyp"
    p.hypothesis_name = "hyp"
    p.disjunction_intro_name = "disj int"
    p.disjunction_elim_name = "disj elim"
    p.conjunction_intro_name = "conj int"
    p.conjunction_elim_name = "conj elim"
    p.reiterate_name = "reit"
    p.implication_intro_name = "imp int"
    p.implication_elim_name = "imp elim"
    p.negation_intro_name = "neg int"
    p.negation_elim_name = "neg elim"
    p.coimplication_intro_name = "coimp int"
    p.coimplication_elim_name = "coimp elim"
    p.explosion_name = "Explosion"


def definedlogics():
    rows = list(altrea.data.getdefinedlogics())
    columns = ["Logic", "Database", "Description"]
    index = []
    for i in range(len(rows)):
        index.append(i)
    df = pandas.DataFrame(rows, index=index, columns=columns)
    return df


# def proofdetails(logic: str, proofname: str):
#     rows = altrea.data.getproofdetails(logic, proofname)
#     columns = ['Item', 'Level', 'Proof', 'Rule', 'Lines', 'Proofs']
#     index = []
#     for i in range(len(rows)):
#             index.append(i)
#     df = pandas.DataFrame(rows, index=index, columns=columns)
#     return df


def stringitem(p: Proof, prooflines: list, i: int):
    base = "   |"
    hypothesisbase = " __|"
    statement = ""
    for j in range(1, prooflines[i][p.levelindex]):
        statement = base + statement
    if prooflines[i][p.statementindex] != "":
        if prooflines[i][p.levelindex] > 0:
            if i < len(prooflines) - 1:
                if prooflines[i][p.ruleindex] == p.hypothesis_name:
                    if (
                        prooflines[i + 1][p.ruleindex] != p.hypothesis_name
                        or prooflines[i][p.levelindex] < prooflines[i + 1][p.levelindex]
                    ):
                        statement = hypothesisbase + statement
                    else:
                        statement = base + statement
                else:
                    statement = base + statement
            else:
                if prooflines[i][p.ruleindex] == p.hypothesis_name:
                    statement = hypothesisbase + statement
                else:
                    statement = base + statement
    statement = "".join([str(prooflines[i][p.statementindex]), statement])
    return statement


def latexitem(p: Proof, prooflines: list, i: int, color=1):
    if prooflines[i][0] != p.blankstatement:
        base = " \\hspace{0.35cm}|"
        hypothesisbase = "".join(["\\underline{", base, "}"])
        statement = ""
        for j in range(1, prooflines[i][p.levelindex]):
            statement = base + statement
        if prooflines[i][p.statementindex] != "":
            if prooflines[i][p.levelindex] > 0:
                if i < len(prooflines) - 1:
                    if prooflines[i][p.ruleindex] == p.hypothesis_name:
                        if (
                            prooflines[i + 1][p.ruleindex] != p.hypothesis_name
                            or prooflines[i][p.levelindex]
                            < prooflines[i + 1][p.levelindex]
                        ):
                            statement = hypothesisbase + statement
                        else:
                            statement = base + statement
                    else:
                        statement = base + statement
                else:
                    if prooflines[i][p.ruleindex] == p.hypothesis_name:
                        statement = hypothesisbase + statement
                    else:
                        statement = base + statement
        if isinstance(prooflines[i][0], str):
            statement = "".join([prooflines[i][0], statement])
        else:
            statement = "".join(["$", prooflines[i][0].latex(), statement, "$"])
    else:
        statement = p.blankstatement
    return statement


# def proofdetailsraw(p: Proof, proofname: str):
#     """Display the proof details as saved to the database."""

#     # Retrieve proof data.
#     rows = altrea.data.getproofdetails(p.logic, proofname)

#     # Prepare to run DataFrame.
#     columns = ['Item', 'Level', 'Proof', 'Rule', 'Lines', 'Proofs', 'Comment']
#     index = []
#     for i in range(len(rows)):
#         index.append(i)
#     df = pandas.DataFrame(rows, index=index, columns=columns)
#     return df


# def proofdetails(p: proof, proofname: str, *args, latex: int = 1):
def displayproofdetails(p: Proof, newrows: list, latex: int = 1):
    """Display the details of a saved proof."""

    # # Retrieve proof data.
    # rows = altrea.data.getproofdetails(p.logic, proofname)

    # # Create an augmented dictionary from the args.
    # newrows =[]
    # for i in rows:
    #     newrows.append(list(i))
    # s = []
    # for i in args:
    #     if type(i) == int:
    #         s.append(p.getstatement(i))
    #     else:
    #         s.append(i)
    # dict = p.objectdictionary
    # for i in s:
    #     dict = i.dictionary(dict)

    # # Format the item column using the dictionary.
    # for i in newrows:
    #     for k in range(len(s)):
    #         i[0] = i[0].replace(''.join(['*', str(k+1), '*']), s[k].tree())
    #     i[0] = eval(i[0], dict)

    # # Format the rules column using the names from the proofs logic operators.
    # for i in newrows:
    #     for k in p.logicoperators:
    #         i[3] = i[3].replace(''.join(['*', k[0], '*']), k[1])
    # for i in newrows:
    #     for k in p.basicoperatorseval:
    #         i[3] = i[3].replace(''.join(['*', k[0], '*']), k[1])
    # for i in newrows:
    #     i[3] = eval(i[3])

    # Format the item column to use latex or strings.
    newp = []
    if latex == 1:
        for i in range(len(newrows)):
            item = latexitem(p, newrows, i)
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
            item = stringitem(p, newrows, i)
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
    columns = ["Item", "Level", "Proof", "Rule", "Lines", "Proofs", "Comment"]
    index = []
    for i in range(len(newrows)):
        index.append(i)
    df = pandas.DataFrame(newp, index=index, columns=columns)
    return df


# def availableproofs(logic: str):
#     rows = altrea.data.getproofs(logic)
#     columns = ['Name', 'Pattern', 'Display', 'Description']
#     index = []
#     for i in range(len(rows)):
#             index.append(i)
#     df = pandas.DataFrame(rows, index=index, columns=columns)
#     return df

# def metadata(p: Proof):
#     """Display the metadata associated with a proof.

#     Parameters:
#         p: The proof containing the metadata.
#     """

#     print('Name: {}'.format(p.name))
#     print('Goal: {}'.format(p.goal))
#     print('Premises')
#     for i in p.premises:
#         print('   {}'.format(i))
#     if p.status == p.complete:
#         print('Completed: Yes')
#     else:
#         print('Completed: No')
#     print('Lines: {}'.format(len(p.lines)-1))


def formatlatexstatement(p: Proof, i: int, color=1):
    if p.lines[i][0] != p.blankstatement:
        base = " \\hspace{0.35cm}|"
        hypothesisbase = "".join(["\\underline{", base, "}"])
        statement = ""
        for j in range(1, p.lines[i][p.levelindex]):
            statement = base + statement
        if p.lines[i][p.statementindex] != "":
            if p.lines[i][p.levelindex] > 0:
                if i < len(p.lines) - 1:
                    if p.lines[i][p.ruleindex] == p.hypothesis_name:
                        if (
                            p.lines[i + 1][p.ruleindex] != p.hypothesis_name
                            or p.lines[i][p.levelindex] < p.lines[i + 1][p.levelindex]
                        ):
                            statement = hypothesisbase + statement
                        else:
                            statement = base + statement
                    else:
                        statement = base + statement
                else:
                    if p.lines[i][p.ruleindex] == p.hypothesis_name:
                        statement = hypothesisbase + statement
                    else:
                        statement = base + statement

        if i == 0:
            if p.goals_latex != "":
                statement = "".join(
                    [
                        "$\\color{blue}",
                        p.goals_latex,
                        "$",
                        statement,
                    ]
                )
            else:
                statement = ""
        elif (
            color == 1
            and p.status != p.complete
            and p.status != p.stopped
            and p.lines[i][1] == p.level
            and p.currentproofid == p.lines[i][2]
            and i > 0
        ):
            statement = "".join(
                ["$\\color{green}", p.lines[i][0].latex(), statement, "$"]
            )
        elif (
            color == 1
            and p.status != p.complete
            and p.status != p.stopped
            and (p.lines[i][2] in p.previousproofchain)
            and i > 0
        ):
            statement = "".join(
                ["$\\color{red}", p.lines[i][0].latex(), statement, "$"]
            )
        elif color == 1 and p.lines[i][6][0:8] == p.complete:
            statement = "".join(
                ["$\\color{blue}", p.lines[i][0].latex(), statement, "$"]
            )
        elif color == 1 and p.lines[i][6][0:18] == p.partialcompletion:
            statement = "".join(
                ["$\\color{blue}", p.lines[i][0].latex(), statement, "$"]
            )
        else:
            if isinstance(p.lines[i][0], str):
                statement = "".join([p.lines[i][0], statement])
            else:
                statement = "".join(["$", p.lines[i][0].latex(), statement, "$"])
    else:
        statement = p.blankstatement
    return statement


def formatstringstatement(p: Proof, i: int):
    base = "   |"
    hypothesisbase = " __|"
    statement = ""
    for j in range(1, p.lines[i][p.levelindex]):
        statement = base + statement
    if p.lines[i][p.statementindex] != "":
        if p.lines[i][p.levelindex] > 0:
            if i < len(p.lines) - 1:
                if p.lines[i][p.ruleindex] == p.hypothesis_name:
                    if (
                        p.lines[i + 1][p.ruleindex] != p.hypothesis_name
                        or p.lines[i][p.levelindex] < p.lines[i + 1][p.levelindex]
                    ):
                        statement = hypothesisbase + statement
                    else:
                        statement = base + statement
                else:
                    statement = base + statement
            else:
                if p.lines[i][p.ruleindex] == p.hypothesis_name:
                    statement = hypothesisbase + statement
                else:
                    statement = base + statement
    statement = "".join([str(p.lines[i][p.statementindex]), statement])
    return statement


def showproof(
    p: Proof,
    color: int = 1,
    latex: int = 1,
    columns: list = ["Item", "Reason", "Comment"],
):
    """Display a proof similar to how Frederic Fitch displayed it in Symbolic Logic.

    Parameters:
        p: The proof containing the lines of the proof.
        color: Use color with latex.
        latex: Use latex rather than text.
    """

    comment = ""

    def formatcomment(p):
        if i == 0:
            if p.lines[i][p.commentindex] == "":
                if p.name == "":
                    if p.logic == "":
                        comment = ""
                    else:
                        comment = "".join({"Logic: ", p.logic})
                else:
                    if p.logic == "":
                        comment = "".join(["Name: ", p.name])
                    else:
                        comment = "".join(["Name: ", p.name, " Logic: ", p.logic])
            else:
                if p.name == "":
                    if p.logic == "":
                        comment = p.lines[i][p.commentindex]
                    else:
                        comment = "".join(
                            {
                                "Logic: ",
                                p.logic,
                                " Comment: ",
                                p.lines[i][p.commentindex],
                            }
                        )
                else:
                    if p.logic == "":
                        comment = "".join(
                            ["Name: ", p.name, " Comment: ", p.lines[i][p.commentindex]]
                        )
                    else:
                        comment = "".join(
                            [
                                "Name: ",
                                p.name,
                                " Logic: ",
                                p.logic,
                                " Comment: ",
                                p.lines[i][p.commentindex],
                            ]
                        )
        else:
            comment = p.lines[i][p.commentindex]
        return comment

    indx = []
    for i in range(len(p.lines)):
        indx.append(i)
    # columns = ['Proposition', 'Rule', 'Comment']
    newp = []
    if latex == 1:
        for i in range(len(p.lines)):
            # Format the statement
            base = " \\hspace{0.35cm}|"
            hypothesisbase = "".join(["\\underline{", base, "}"])
            statement = ""
            for j in range(1, p.lines[i][p.levelindex]):
                statement = base + statement
            if p.lines[i][p.statementindex] != "":
                if p.lines[i][p.levelindex] > 0:
                    if i < len(p.lines) - 1:
                        if p.lines[i][p.ruleindex] == p.hypothesis_name:
                            if (
                                p.lines[i + 1][p.ruleindex] != p.hypothesis_name
                                or p.lines[i][p.levelindex]
                                < p.lines[i + 1][p.levelindex]
                            ):
                                statement = hypothesisbase + statement
                            else:
                                statement = base + statement
                        else:
                            statement = base + statement
                    else:
                        if p.lines[i][p.ruleindex] == p.hypothesis_name:
                            statement = hypothesisbase + statement
                        else:
                            statement = base + statement

            if i == 0:
                if p.goals_latex != "":
                    statement = "".join(
                        [
                            "$",
                            p.goals_latex,
                            "$",
                            statement,
                        ]
                    )
                else:
                    statement = " "
            elif (
                color == 1
                and p.status != p.complete
                and p.status != p.stopped
                and p.lines[i][1] <= p.level
                and i > 0
            ):
                statement = "".join(
                    ["$\\color{red}", p.lines[i][0].latex(), statement, "$"]
                )
            elif color == 1 and p.lines[i][6][0:8] == p.complete:
                statement = "".join(
                    ["$\\color{blue}", p.lines[i][0].latex(), statement, "$"]
                )
            elif color == 1 and p.lines[i][6][0:18] == p.partialcompletion:
                statement = "".join(
                    ["$\\color{blue}", p.lines[i][0].latex(), statement, "$"]
                )
            else:
                if isinstance(p.lines[i][0], str):
                    statement = "".join([p.lines[i][0], statement])
                else:
                    statement = "".join(["$", p.lines[i][0].latex(), statement, "$"])

            # Format the rule
            rule = ""
            if p.lines[i][p.linesindex] != "":
                rule = "".join(
                    [p.lines[i][p.linesindex], ", ", p.lines[i][p.ruleindex]]
                )
            elif p.lines[i][p.proofsindex] != "":
                rule = "".join(
                    [p.lines[i][p.proofsindex], ", ", p.lines[i][p.ruleindex]]
                )
            else:
                rule = p.lines[i][p.ruleindex]

            # Format the comment
            comment = p.lines[i][p.commentindex]

            newp.append([statement, rule, comment])

    else:  # string display
        for i in range(len(p.lines)):
            # Format the statement
            base = "   |"
            hypothesisbase = " __|"
            statement = ""
            for j in range(1, p.lines[i][p.levelindex]):
                statement = base + statement
            if p.lines[i][p.statementindex] != "":
                if p.lines[i][p.levelindex] > 0:
                    if i < len(p.lines) - 1:
                        if p.lines[i][p.ruleindex] == p.hypothesis_name:
                            if (
                                p.lines[i + 1][p.ruleindex] != p.hypothesis_name
                                or p.lines[i][p.levelindex]
                                < p.lines[i + 1][p.levelindex]
                            ):
                                statement = hypothesisbase + statement
                            else:
                                statement = base + statement
                        else:
                            statement = base + statement
                    else:
                        if p.lines[i][p.ruleindex] == p.hypothesis_name:
                            statement = hypothesisbase + statement
                        else:
                            statement = base + statement
            statement = "".join([str(p.lines[i][p.statementindex]), statement])

            # Format the rule
            if p.lines[i][p.linesindex] != "":
                rule = "".join(
                    [p.lines[i][p.linesindex], ", ", p.lines[i][p.ruleindex]]
                )
            elif p.lines[i][p.proofsindex] != "":
                rule = "".join(
                    [p.lines[i][p.proofsindex], ", ", p.lines[i][p.ruleindex]]
                )
            else:
                rule = p.lines[i][p.ruleindex]

            # Format the comment
            comment = p.lines[i][p.commentindex]

            newp.append([statement, rule, comment])
    df = pandas.DataFrame(newp, index=indx, columns=columns)
    return df


def showlines(
    p: Proof,
    color: int = 1,
    latex: int = 1,
    columns: list = [
        "Statement",
        "Level",
        "Proof",
        "Rule",
        "Lines",
        "Proofs",
        "Comment",
    ],
):
    """Display a proof line by line.

    Parameters:
        p: The proof containing the lines.
    """

    indx = [p.logic]
    for i in range(len(p.lines) - 1):
        indx.append(i + 1)
    if latex == 1:
        newp = []
        for i in range(len(p.lines)):
            if i == 0:
                if p.goals_latex != "":
                    statement = "".join(["$", p.goals_latex, "$"])
                else:
                    statement = " "
            elif (
                color == 1
                and p.status != p.complete
                and p.status != p.stopped
                and p.lines[i][1] <= p.level
                and i > 0
            ):
                try:
                    statement = "".join(["$\\color{red}", p.lines[i][0].latex(), "$"])
                except AttributeError:
                    statement = p.lines[i][0]
            else:
                try:
                    statement = "".join(["$", p.lines[i][0].latex(), "$"])
                except AttributeError:
                    statement = p.lines[i][0]
            if (
                color == 1
                and p.status != p.complete
                and p.status != p.stopped
                and p.lines[i][1] == p.level + 1
            ):
                block = "".join(["$\\color{red}", str(p.lines[i][2]), "$"])
            else:
                block = p.lines[i][2]
            if color == 1 and p.lines[i][6][0:8] == p.complete:
                statement = "".join(["$\\color{blue}", p.lines[i][0].latex(), "$"])
            if color == 1 and p.lines[i][6][0:18] == p.partialcompletion:
                statement = "".join(["$\\color{blue}", p.lines[i][0].latex(), "$"])
            # else:
            #   statement = p.lines[i][0]
            newp.append(
                [
                    statement,
                    p.lines[i][1],
                    block,
                    p.lines[i][3],
                    p.lines[i][4],
                    p.lines[i][5],
                    p.lines[i][6],
                ]
            )
        df = pandas.DataFrame(newp, index=indx, columns=columns)
    else:
        df = pandas.DataFrame(p.lines, index=indx, columns=columns)
    return df
