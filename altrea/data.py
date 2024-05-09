"""This module interfaces between the python sqlite3 database."""

import sqlite3

from altrea.boolean import And, Or, Not, Implies, Iff, Wff, F, T

def getdatabase(logic: str):
    connection = sqlite3.connect('altrea/data/metadata.db')
    c = connection.cursor()
    statement = 'SELECT dbname FROM metadata WHERE logic =?'
    c.execute(statement, (logic,))
    database = c.fetchone()
    connection.commit()
    connection.close()
    return database[0]

logicdatabases = {
        'C': 'altrea/data/classical_propositional.db',
        'CI': 'classical_implicational.db',
        'CO': 'classical_non_implicational.db',
        'I': 'intuitionist_propositional.db',
        'MC': 'metamath_classical.db',
        'MI': 'metamath_intuitionist.db',
        'MNF': 'metamath_newfoundations.db',
    }

def addlogic(logic: str, dbname: str, longname: str):
    connection = sqlite3.connect('altrea/data/metadata.db')
    c = connection.cursor()
    # Construct and/or load metadata table with logic record.
    rows = -1
    try:
        c.execute('SELECT COUNT(*) FROM metadata')
        rows = c.fetchone()
    except:
        c.execute("""CREATE TABLE metadata (
                    logic    TEXT PRIMARY KEY,
                    dbname   TEXT UNIQUE,
                    longname TEXT NOT NULL)""")
        print('The metadata table has been created.')
    statement = 'INSERT INTO metadata (logic, dbname, longname) VALUES (?, ?, ?)'
    database = ''.join(['altrea/data/', dbname.replace(' ','_'), '.db'])
    row = (logic, database, longname)
    c.execute(statement, row)
    connection.commit()
    connection.close()
    print(f'The {logic} logic using database {database} has been created with description {longname}.')
    # Create the axioms table in the dbname database.
    connection = sqlite3.connect(database)
    c = connection.cursor()
    c.execute("""CREATE TABLE axioms (
                name        TEXT PRIMARY KEY,
                pattern     TEXT NOT NULL,
                displayname TEXT NOT NULL,
                longname    TEXT NOT NULL
                )"""
              )
    print(f'The axioms table has been created for the {logic} logic.')
    # Create the proofs table in the dbname database.
    c.execute("""CREATE TABLE proofs (
                name        TEXT PRIMARY KEY,
                logic       TEXT NOT NULL,
                pattern     TEXT NOT NULL,
                displayname TEXT NULL,
                longname    TEXT NULL
                )"""
              )
    print(f'The proofs table has been created for the {logic} logic.')
    # Create the proofdetails table in the dbname database.
    c.execute("""CREATE TABLE proofdetails (
                name       TEXT NOT NULL,
                item       TEXT NOT NULL,
                level      INT  NOT NULL,
                proof      INT  NOT NULL,
                rule       TEXT NOT NULL,
                lines      TEXT NULL,
                usedproofs TEXT NULL,
                comment    TEXT NULL,
                FOREIGN KEY (name)
                    REFERENCES proofs(name)
                )"""
            )
    print(f'The proofdetails table has been created for the {logic} logic.')
    connection.commit()
    connection.close()

def getdefinedlogics():
    connection = sqlite3.connect('altrea/data/metadata.db')
    c = connection.cursor()
    statement = 'SELECT * FROM metadata'
    c.execute(statement)
    rows = c.fetchall()
    connection.commit()
    connection.close()
    return rows

def getproofdetails(logic: str, proofname: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = 'SELECT item, level, proof, rule, lines, usedproofs, comment FROM proofdetails WHERE name=?'
    c.execute(statement, (proofname,))
    rows = c.fetchall()
    connection.commit()
    connection.close()
    return rows

def getavailableproofs(logic: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = 'SELECT name, pattern, displayname, longname FROM proofs'
    c.execute(statement)
    rows = c.fetchall()
    connection.commit()
    connection.close()
    return rows

# def checkaxiomstable(logic: str):
#     database = logicdatabases.get(logic)
#     connection = sqlite3.connect(database)
#     c = connection.cursor()
#     rows = -1
#     try:
#         c.execute("SELECT COUNT(*) FROM axioms")
#         rows = c.fetchone()
#     except:
#         c.execute("""CREATE TABLE axioms (
#             name        TEXT PRIMARY KEY,
#             pattern     TEXT NOT NULL,
#             displayname TEXT NOT NULL,
#             longname    TEXT NOT NULL
#         )
#         """)
#         if logic == 'C':
#             data = [
#                 ('lem', 'Or(*1*, Not(*1*))', 'LEM', 'Law of Excluded Middle'),
#                 ('wlem', 'Or(Not(*1*), Not(Not(*1*)))', 'WLEM', 'Weak Law of Excluded Middle'),
#                 ('dne', 'Implies(Not(Not(*1*)), *1*)', 'DNE', 'Double Negation Elimination'),
#                 ('dni', 'Implies(*1*, Not(Not(*1*)))', 'DNI', 'Double Negation Introduction'),
#                 ('mt', 'Implies(Implies(*2*, *1*), Implies(Not(*1*), Not(*2*)))', 'MT', 'Modus Tollens'),
#                 ('dist', 'Implies(Implies(*3*, Implies(*2*, *1*), Implies(Implies(*3*, *2*), Implies(*3*, *1*))))', 'DIST', 'Distribution'),
#                 ('condrefl', 'Implies(*1*, Implies(*2*, *1*))', 'COND REFL', 'Conditional Reflection')
#             ]
#             c.executemany('INSERT INTO axioms VALUES (?, ?, ?, ?)', data)            
#             connection.commit()
#             print(f'Successful insertion of the axioms into the {database} database.')
#     connection.close()
#     return rows

# def checkproofstable(logic: str):
#     database = logicdatabases.get(logic)
#     connection = sqlite3.connect(database)
#     c = connection.cursor()
#     proof_rows = -1
#     details_rows = -1
#     try:
#         c.execute("SELECT COUNT(*) FROM proofs")
#         proof_rows = c.fetchone()
#     except:
#         c.execute("""CREATE TABLE proofs (
#                     name        TEXT PRIMARY KEY,
#                     logic       TEXT NOT NULL,
#                     pattern     TEXT NOT NULL,
#                     displayname TEXT NULL,
#                     longname    TEXT NULL
#                     )"""
#                 )
#     try:
#         c.execute("SELECT COUNT(*) FROM proofdetails")
#         details_rows = c.fetchone()
#     except:
#         c.execute("""CREATE TABLE proofdetails (
#                     name       TEXT NOT NULL,
#                     item       TEXT NOT NULL,
#                     level      INT  NOT NULL,
#                     proof      INT  NOT NULL,
#                     rule       TEXT NOT NULL,
#                     lines      TEXT NULL,
#                     usedproofs TEXT NULL,
#                     FOREIGN KEY (name)
#                         REFERENCES proofs(name)
#                     )"""
#                 )
#     connection.commit()
#     connection.close()
#     return proof_rows, details_rows

def deleteproof(logic: str, name: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = 'DELETE FROM proofdetails WHERE name=?'
    c.execute(statement, (name,))
    print(f'The proof details for {name} have been deleted from {logic}.')
    statement = 'DELETE FROM proofs WHERE name=?'
    c.execute(statement, (name,))
    print(f'The proof {name} has been deleted from {logic}.')
    connection.commit()
    connection.close()

def addproof(proofdata: list):
    database = getdatabase(proofdata[0][3])
    connection = sqlite3.connect(database)
    c = connection.cursor()
    name = proofdata[0][0]
    displayname = proofdata[0][1]
    longname = proofdata[0][2]
    logic = proofdata[0][3]
    pattern = proofdata[0][4]
    statement = 'SELECT COUNT(*) FROM proofs where name=?'
    c.execute(statement, (name,))
    howmany = c.fetchone()
    if howmany[0] > 0:
        print(f'The proof named {name} already exists.  View it with `altrea.display.proofdetails` to decide it you want to delete it.')
    else:
        row = (name, displayname, longname, logic, pattern)
        statement = 'INSERT INTO proofs (name, displayname, longname, logic, pattern) VALUES (?, ?, ?, ?, ?)'
        c.execute(statement, row)
        print(f'The proof {name} has been added to {logic}.')
        statement = 'INSERT INTO proofdetails (name, item, level, proof, rule, lines, usedproofs, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        c.executemany(statement, proofdata[1:])
        print(f'The proof details for {name} have been added to {logic}.')
        connection.commit()
        connection.close()
        print(f'The proof of {longname} was saved in {database}.')

# def loadaxioms(logic: str):
#     database = logicdatabases.get(logic)
#     connection = sqlite3.connect(database)
#     c = connection.cursor()
#     if logic == 'C':
#         c.execute("""INSERT INTO axioms (name, pattern, displayname, longname) VALUES
#             ('lem', 'Or(1, Not(1))', 'LEM', 'Law of Excluded Middle'),
#             ('wlem', 'Or(Not(1), Not(Not(1)))', 'WLEM', 'Weak Law of Excluded Middle')
#         """)
#     connection.close()



def addaxiom(logic: str, name: str, pattern: str, displayname: str, longname: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    row = (name, pattern, displayname, longname)
    statement = "INSERT INTO axioms (name, pattern, displayname, longname) VALUES (?, ?, ?, ?)"
    c.execute(statement, row)
    connection.commit()
    connection.close()


def getproof(logic: str, name: str, *subs: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    c.execute(f"SELECT displayname, longname, pattern FROM proofs WHERE name = '{name}'")
    displayname, longname, pattern = c.fetchone()
    connection.commit()
    connection.close()
    for i in range(len(subs)):
        pattern = pattern.replace(''.join(['*', str(i+1), '*']), subs[i])
    return displayname, longname, pattern

def getsavedproof(logic: str, name: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = 'SELECT displayname, longname, pattern FROM proofs WHERE name=?'
    c.execute(statement, (name,))
    displayname, longname, pattern = c.fetchone()
    connection.commit()
    connection.close()
    # for i in range(len(subs)):
    #     pattern = pattern.replace(''.join(['*', str(i+1), '*']), subs[i])
    return displayname, longname, pattern

# def getdisplay(logic: str, name: str):
#     database = logicdatabases.get(logic)
#     connection = sqlite3.connect(database)
#     c = connection.cursor()
#     c.execute("SELECT display FROM proofs WHERE name = '{}'".format(name))
#     display = c.fetchone()
#     connection.close()
#     return display


def getaxiom(logic: str, name: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = 'SELECT displayname, longname, pattern FROM axioms WHERE name=?'
    c.execute(statement, (name,))
    displayname, longname, pattern = c.fetchone()
    connection.commit()
    connection.close()
    # for i in range(len(subs)):
    #     pattern = pattern.replace(''.join(['*', str(i+1), '*']), subs[i])
    # if name == 'dne':
    #     pattern = pattern[8:-2]
    #     print(pattern)
    #if '[' in pattern:
    #    pattern = eval(pattern)
    #displayname = 'LEM2'
    #longname = 'Lae of Excluded Middle2'
    return displayname, longname, pattern
