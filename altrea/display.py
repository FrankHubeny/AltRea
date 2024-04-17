"""This module contains procedures to forat a display of data.

- `metadata(p)` - Print a list of a proof's metadata.
- `show(p)` - Print a proof line by line.
- `truthtable(p)` - Print a truth table of the proofs premises implying its goal.
"""

import pandas
#import sympy

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

def show(p: altrea.truthfunction.Proof, color: int = 1, latex: int = 1):
    """Display a proof line by line.
    
    Parameters:
        p: The proof containing the lines.
    """

    indx = ['Line']
    for i in range(len(p.lines)-1):
        indx.append(i + 1)
    if latex == 1:
        newp = []
        for i in range(len(p.lines)):
            if p.lines[i][0] == False:
                statement = '$\\bot$'
            else:
                if color == 1 and p.status != p.complete and p.lines[i][1] <= p.level and i > 0:
                    statement = ''.join(['$\\color{red}',p.lines[i][0].latex(),'$'])
                else:
                    statement = ''.join(['$',p.lines[i][0].latex(),'$'])
                if color == 1 and p.status != p.complete and p.lines[i][1] == p.level + 1:
                    block = ''.join(['$\\color{red}',str(p.lines[i][2]),'$'])
                else:
                    block = p.lines[i][2]
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

# def truthtable(p: altrea.truthfunction.Proof):
#     """Display a truth table built from a conjunction of the premises implying the goal.
    
#     Paramters:
#         p: The proof containing the premises and goal.
#     """

#     premises = True
#     for i in p.premises:
#         premises = sympy.logic.boolalg.And(premises, i)
#     expr = sympy.logic.boolalg.Implies(premises, p.goal)
#     vars = list(expr.free_symbols)
#     table = sympy.logic.boolalg.truth_table(expr, vars)
#     letters = '['
#     for s in vars:
#         letters += ''.join([str(s), ', '])
#     letters = letters[:-2] + ']'
#     idx = []
#     for i in range(2**len(vars)):
#         idx.append(i)
#     expr = ''.join(['$',sympy.latex(expr),'$'])
#     print('Truth table for {}'.format(p.name))
#     df = pandas.DataFrame(table, index=idx, columns=[letters, expr])
#     return df

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
