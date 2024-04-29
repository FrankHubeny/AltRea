"""This module contains procedures to forat a display of data.

- `metadata(p)` - Print a list of a proof's metadata.
- `show(p)` - Print a proof line by line.
- `truthtable(p)` - Print a truth table of the proofs premises implying its goal.
"""

import pandas

import altrea

def fitchnotation(p: altrea.truthfunction.Proof):
    """This function changes the names for rules to better conform to Frederic Fitch's Symbolic Logic text."""

    # Attributes from the altrea.truthfunction.Proof class
    p.premise_name = 'Premise'
    p.hypothesis_name = 'hyp'
    p.disjunction_intro_name = 'disj int'
    p.disjunction_elim_name = 'disj elim'
    p.conjunction_intro_name = 'conj int'
    p.conjunction_elim_name = 'conj elim'
    p.reiterate_name = 'reit'
    p.implication_intro_name = 'Implication Intro'
    p.implication_elim_name = 'Implication Elim'
    p.negation_intro_name = 'Negation Intro'
    p.negation_elim_name = 'Negation Elim'
    p.indirectproof_name = 'Indirect Proof'
    p.coimplication_intro_name = 'cpimp int'
    p.coimplication_elim_name = 'coimp elim'
    #p.xor_intro_name = 'Xor Intro'
    #p.xor_elim_name = 'Xor Elim'
    #p.nand_intro_name = 'Nand Intro'
    #p.nand_elim_name = 'Nand Elim'
    #p.nor_intro_name = 'Nor Intro'
    #p.nor_elim_name = 'Nor Elim'
    #p.xnor_intro_name = 'Xnor Intro'
    #p.xnor_elim_name = 'Xnor Elim'
    p.lem_name = 'lem'
    p.doublenegation_intro_name = 'Double Negation Intro'
    p.doublenegation_elim_name = 'Double Negation Elim'
    p.demorgan_name = 'DeMorgan'
    p.explosion_name = 'Explosion'

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

def showproof(p: altrea.truthfunction.Proof, color: int = 1, latex: int = 1, columns: list = ['Item','Reason','Comment']):
    """Display a proof similar to how Frederic Fitch displayed it in Symbolic Logic.
    
    Parameters:
        p: The proof containing the lines of the proof.
        color: Use color with latex.
        latex: Use latex rather than text.
    """
    
    comment = ''
    def formatcomment(p):
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
    #columns = ['Proposition', 'Rule', 'Comment']
    newp = []
    if latex == 1:
        for i in range(len(p.lines)):

            # Format the statement
            base = ' \\hspace{0.35cm}|'
            #hypothesisbase = ' \\underline{\\hspace{0.35cm}|}'
            hypothesisbase = ''.join(['\\underline{', base, '}']) 
            statement = ''
            for j in range(1, p.lines[i][p.levelindex]):
                statement = base + statement
            if p.lines[i][p.statementindex] != '':
                if p.lines[i][p.levelindex] > 0:
                    if i < len(p.lines) - 1:
                        if p.lines[i][p.ruleindex] == p.hypothesis_name:
                            if p.lines[i+1][p.ruleindex] != p.hypothesis_name or p.lines[i][p.levelindex] < p.lines[i+1][p.levelindex]:
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
                if p.goals_latex != '':
                    statement = ''.join(['$', p.goals_latex, '$', statement, ])
                else:
                    statement = ' '
            elif color == 1 and p.status != p.complete and p.status != p.stopped and p.lines[i][1] <= p.level and i > 0:
                #if p.lines[i][p.ruleindex] == p.hypothesis_name and i < len(p.lines) - 1:
                    # if p.lines[i+1][p.ruleindex] != p.hypothesis_name or p.lines[i][p.levelindex] < p.lines[i+1][p.levelindex]:
                    #     statement = ''.join(['$\\color{red}', p.lines[i][0].latex(), lasthypothesis, statement, '$'])
                    # else:
                    # statement = ''.join(['$\\color{red}', p.lines[i][0].latex(), blankspace, statement, '$' ])
                #else:
                statement = ''.join(['$\\color{red}', p.lines[i][0].latex(), statement, '$' ])
            elif color == 1 and p.lines[i][6][0:8] == p.complete: 
                statement = ''.join(['$\\color{blue}', p.lines[i][0].latex(), statement, '$' ])
            elif color == 1 and p.lines[i][6][0:18] == p.partialcompletion:
                statement = ''.join(['$\\color{blue}', p.lines[i][0].latex(), statement, '$'])
            else:
                # if p.lines[i][p.ruleindex] == p.hypothesis_name and i < len(p.lines) - 1:
                #     if p.lines[i+1][p.ruleindex] != p.hypothesis_name or p.lines[i][p.levelindex] < p.lines[i+1][p.levelindex]:
                #         statement = ''.join(['$', p.lines[i][0].latex(), lasthypothesis, statement, '$' ])
                #     else:
                #         statement = ''.join(['$', p.lines[i][0].latex(), blankspace, statement, '$' ])
                # else:
                statement = ''.join(['$', p.lines[i][0].latex(), statement, '$' ])

            # Format the rule
            rule =''
            if p.lines[i][p.linesindex] != '':
                rule = ''.join([p.lines[i][p.linesindex], ', ',p.lines[i][p.ruleindex]])
            elif p.lines[i][p.proofsindex] != '':
                rule = ''.join([p.lines[i][p.proofsindex], ', ',p.lines[i][p.ruleindex]])
            else:
                rule = p.lines[i][p.ruleindex]

            # Format the comment
            #comment = formatcomment(p)
            comment = p.lines[i][p.commentindex]

            newp.append([statement, rule, comment])
        
    else:  # string display
        for i in range(len(p.lines)):

            # Format the statement
            base = '    |'
            hypothesisbase = ' __|'
            statement = ''
            for j in range(1, p.lines[i][p.levelindex]):
                statement = base + statement
            if p.lines[i][p.statementindex] != '':
                if p.lines[i][p.levelindex] > 0:
                    if i < len(p.lines) - 1:
                        if p.lines[i][p.ruleindex] == p.hypothesis_name:
                            if p.lines[i+1][p.ruleindex] != p.hypothesis_name or p.lines[i][p.levelindex] < p.lines[i+1][p.levelindex]:
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
            statement = ''.join([str(p.lines[i][p.statementindex]), statement])
        
            # Format the rule
            if p.lines[i][p.linesindex] != '':
                rule = ''.join([p.lines[i][p.linesindex], ', ',p.lines[i][p.ruleindex]])
            elif p.lines[i][p.proofsindex] != '':
                rule = ''.join([p.lines[i][p.proofsindex], ', ',p.lines[i][p.ruleindex]])
            else:
                rule = p.lines[i][p.ruleindex]

            # Format the comment
            #comment = formatcomment(p)
            comment = p.lines[i][p.commentindex]

            newp.append([statement, rule, comment])
    df = pandas.DataFrame(newp, index=indx, columns=columns)
    return df
            

def show(p: altrea.truthfunction.Proof, 
         color: int = 1, 
         latex: int = 1, 
         columns: list = ['Statement', 'Level', 'Proof', 'Rule', 'Lines', 'Proofs', 'Comment']):
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
        df = pandas.DataFrame(newp, index=indx, columns=columns)
    else:
        df = pandas.DataFrame(p.lines, index=indx, columns=columns)
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