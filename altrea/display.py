"""This module contains procedures to forat a display of data.

- `metadata(p)` - Print a list of a proof's metadata.
- `show(p)` - Print a proof line by line.
- `truthtable(p)` - Print a truth table of the proofs premises implying its goal.
"""

import pandas

import altrea

def metadata(p: altrea.truthfunction.Proof):
    """Display the metadata associated with a proof.
    
    Parameters:
        p: The proof containing the metadata.
    """

    print('Name: {}'.format(p.name))
    print('Goal: {}'.format(p.goal))
    print('Premises')
    for i in p.premises:
        print('   {}'.format(i))
    if p.status == p.complete:
        print('Completed: Yes')
    else:
        print('Completed: No')
    print('Lines: {}'.format(len(p.lines)-1))

def fitch(p: altrea.truthfunction.Proof, color: int = 1, latex: int = 1):
    """Display a proof similar to how Frederic Fitch displayed it in Symbolic Logic.
    
    Parameters:
        p: The proof containing the lines of the proof.
        color: Use color with latex.
        latex: Use latex rather than text.
    """
    def formatcomment(p):
        comment = ''
        if i == 0:
            if p.lines[i][p.commentindex] == '':
                if p.name == '':
                    if p.logic == '':
                        comment = ''
                    else:
                        comment = ''.join({'Logic: ', p.logic})
                else:
                    if p.logic == '':
                        comment = ''.join(['Name: ', p.name])
                    else:
                        comment = ''.join(['Name: ', p.name, ' Logic: ', p.logic])
            else:
                if p.name == '':
                    if p.logic == '':
                        comment = p.lines[i][p.commentindex]
                    else:
                        comment = ''.join({'Logic: ', p.logic, ' Comment: ', p.lines[i][p.commentindex]})
                else:
                    if p.logic == '':
                        comment = ''.join(['Name: ', p.name, ' Comment: ', p.lines[i][p.commentindex]])
                    else:
                        comment = ''.join(['Name: ', p.name, ' Logic: ', p.logic, ' Comment: ', p.lines[i][p.commentindex]])
        else:
            comment = p.lines[i][p.commentindex]
        return comment

    indx = []
    for i in range(len(p.lines)):
        indx.append(i)
    columns = ['Proposition', 'Rule', 'Comment']
    newp = []
    if latex == 1:
        for i in range(len(p.lines)):

            # Format the statement
            statement = ''
            if i == 0:
                if p.goals_latex != '':
                    statement = ''.join(['$', p.goals_latex, '$'])
                else:
                    statement = ' '
            elif color == 1 and p.status != p.complete and p.status != p.stopped and p.lines[i][1] <= p.level and i > 0:
                try:
                    statement = ''.join(['$\\color{red}', p.lines[i][0].latex(), '$'])
                except AttributeError:
                    statement = p.lines[i][0]
            elif color == 1 and p.lines[i][6][0:8] == p.complete: 
                statement = ''.join(['$\\color{blue}', p.lines[i][0].latex(), '$'])
            elif color == 1 and p.lines[i][6][0:18] == p.partialcompletion:
                statement = ''.join(['$\\color{blue}', p.lines[i][0].latex(), '$'])
            else:
                try:
                    statement = ''.join(['$', p.lines[i][0].latex(), '$'])
                except AttributeError:
                    statement = p.lines[i][0]
            
            # Format the rule
            rule =''
            if p.lines[i][p.linesindex] != '':
                rule = ''.join([p.lines[i][p.linesindex], ', ',p.lines[i][p.ruleindex]])
            elif p.lines[i][p.blocksindex] != '':
                rule = ''.join([p.lines[i][p.blocksindex], ', ',p.lines[i][p.ruleindex]])
            else:
                rule = p.lines[i][p.ruleindex]

            # Format the comment
            comment = formatcomment(p)
            # if i == 0:
            #     if p.lines[i][p.commentindex] == '':
            #         if p.name == '':
            #             comment = ''.join({'Logic: ', p.logic})
            #         else:
            #             comment = ''.join(['Name: ', p.name, ' Logic: ', p.logic])
            #     else:
            #         if p.name == '':
            #             comment = ''.join({'Logic: ', p.logic, ' Comment: ', p.lines[i][p.commentindex]})
            #         else:
            #             comment = ''.join({'Name: ', p.name, ' Logic: ', p.logic, ' Comment: ', p.lines[i][p.commentindex]})
            # else:
            #     comment = p.lines[i][p.commentindex]

            newp.append([statement, rule, comment])
        
    else:
        for i in range(len(p.lines)):

            # Format the statement
            statement = p.lines[i][p.statementindex]
        
            # Format the rule
            if p.lines[i][p.linesindex] != '':
                rule = ''.join([p.lines[i][p.linesindex], ', ',p.lines[i][p.ruleindex]])
            elif p.lines[i][p.blocksindex] != '':
                rule = ''.join([p.lines[i][p.blocksindex], ', ',p.lines[i][p.ruleindex]])
            else:
                rule = p.lines[i][p.ruleindex]

            # Format the comment
            comment = formatcomment(p)
            # if i == 0:
            #     if p.lines[i][p.commentindex] == '':
            #         if p.name == '':
            #             if p.logic == '':
            #                 comment = ''
            #             else:
            #                 comment = ''.join({'Logic: ', p.logic})
            #         else:
            #             if p.logic == '':
            #                 comment = ''.join(['Name: ', p.name])
            #             else:
            #                 comment = ''.join(['Name: ', p.name, ' Logic: ', p.logic])
            #     else:
            #         if p.name == '':
            #             if p.logic == '':
            #                 comment = p.lines[i][p.commentindex]
            #             else:
            #                 comment = ''.join({'Logic: ', p.logic, ' Comment: ', p.lines[i][p.commentindex]})
            #         else:
            #             if p.logic == '':
            #                 comment = ''.join(['Name: ', p.name, ' Comment: ', p.lines[i][p.commentindex]])
            #             else:
            #                 comment = ''.join(['Name: ', p.name, ' Logic: ', p.logic, ' Comment: ', p.lines[i][p.commentindex]])
            # else:
            #     comment = p.lines[i][p.commentindex]

            newp.append([statement, rule, comment])
    df = pandas.DataFrame(newp, index=indx, columns=columns)
    return df
            

def show(p: altrea.truthfunction.Proof, color: int = 1, latex: int = 1):
    """Display a proof line by line.
    
    Parameters:
        p: The proof containing the lines.
    """

    indx = [p.logic]
    for i in range(len(p.lines)-1):
        indx.append(i + 1)
    if latex == 1:
        newp = []
        for i in range(len(p.lines)):
            if i == 0:
                if p.goals_latex != '':
                    statement = ''.join(['$', p.goals_latex, '$'])
                else:
                    statement = ' '
            elif color == 1 and p.status != p.complete and p.status != p.stopped and p.lines[i][1] <= p.level and i > 0:
                try:
                    statement = ''.join(['$\\color{red}', p.lines[i][0].latex(), '$'])
                except AttributeError:
                    statement = p.lines[i][0]
            else:
                try:
                    statement = ''.join(['$', p.lines[i][0].latex(), '$'])
                except AttributeError:
                    statement = p.lines[i][0]
            if color == 1 and p.status != p.complete and p.status != p.stopped and p.lines[i][1] == p.level + 1:
                block = ''.join(['$\\color{red}', str(p.lines[i][2]), '$'])
            else:
                block = p.lines[i][2]
            if color == 1 and p.lines[i][6][0:8] == p.complete: 
                statement = ''.join(['$\\color{blue}', p.lines[i][0].latex(), '$'])
            if color == 1 and p.lines[i][6][0:18] == p.partialcompletion:
                statement = ''.join(['$\\color{blue}', p.lines[i][0].latex(), '$'])
            #else:
             #   statement = p.lines[i][0]
            newp.append([statement,
                        p.lines[i][1],
                        block,
                        p.lines[i][3],
                        p.lines[i][4],
                        p.lines[i][5],
                        p.lines[i][6]
                        ]
            )
        df = pandas.DataFrame(newp, index=indx, columns=p.columns)
    else:
        df = pandas.DataFrame(p.lines, index=indx, columns=p.columns)
    return df

def truthtable(premises: list, goal, letters: list):
    """Display a truth table built from a conjunction of the premises implying the goal.
    
    Paramters:
        p: The proof containing the premises and goal.
    """

    from altrea.boolean import And, Or, Not, Implies, Iff, Wff

    def makerow(value: bool, letters: list, goal):
        row = []
        letters[0].setvalue(value)
        row.append(letters[0].booleanvalue)
        for i in premises:
            row.append(i.booleanvalue)
        row.append(goal.booleanvalue)
        return row
    
    columns = []
    for i in letters:
        columns.append(str(i))
    for i in premises:
        statement = ''.join(['$',i.latex(),'$'])
        columns.append(statement)
    statement = ''.join(['$',goal.latex(),'$'])
    columns.append(statement)

    rows = 2**len(letters)
    index = []
    for i in range(rows):
        index.append(i)

    table = []
    if len(letters) == 1:
        table.append(makerow(True, letters, goal))
        table.append(makerow(False, letters, goal))
        # row = []
        # letters[0].setvalue(True)
        # row.append(letters[0].booleanvalue)
        # for i in premises:
        #     row.append(i.booleanvalue)
        # row.append(goal.booleanvalue)
        # table.append(row)

        # row = []
        # letters[0].setvalue(False)
        # row.append(letters[0].booleanvalue)
        # for i in premises:
        #     row.append(i.booleanvalue)
        # row.append(goal.booleanvalue)
        # table.append(row)
        
    df = pandas.DataFrame(table, index=index, columns=columns)
    return df

def showblocklist(p: altrea.truthfunction.Proof):
    """Display the blocklist of a proof.
    
    Parameters:
        p: The proof that contains the blocklist.
    """

    indx = []
    for i in range(len(p.blocklist)):
        indx.append(i)
    df = pandas.DataFrame(p.blocklist, index=indx, columns=['Level', 'Block'])
    return df

def availablelogics():
    """Displays the available logics for proofs."""

    from pandas import DataFrame
    from altrea.boolean import Wff
    from altrea.truthfunction import Proof
    A = Wff('A')
    p = Proof(A)
    df = DataFrame(p.logicdictionary.items(), columns=['Rule', 'Logics Supporting It'])
    return df

def connectors():
    """Displays the available logical connectors for a specific logic."""

    from pandas import DataFrame
    from altrea.boolean import Wff
    from altrea.truthfunction import Proof
    A = Wff('A')
    p = Proof(A)
    df = DataFrame(p.connectors.items(), columns=['Logic', 'Available Connectors'])
    return df