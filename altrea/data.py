"""This module interfaces between the python sqlite3 database."""

import sqlite3

from altrea.boolean import And, Or, Not, Implies, Iff, Wff, F, T

metadata = 'altrea/data/metadata.db'

def getdatabase(logic: str):
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = 'SELECT database FROM logics WHERE logic =?'
    c.execute(statement, (logic,))
    dbname = c.fetchone()
    try:
        database = dbname[0]
    except TypeError:
        print(f'The logic {logic} does not exist in the logics table.')
    connection.commit()
    connection.close()
    return database

def createmetadatatables():
    """Create the metadata file and logics and operators table if the logics table does not exist."""

    # Connect to metadata.
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    try:
        c.execute('SELECT * FROM logics')
        rows = c.fetchone()
        print('The metadata tables already exist.')
    except sqlite3.OperationalError:

        # Create the logics table in the metadata database.
        c.execute("""CREATE TABLE logics (
                    logic       TEXT PRIMARY KEY,
                    database    TEXT UNIQUE,
                    description TEXT NOT NULL)"""
                )
        print('The logics table has been created.')

        # Create the operators table in the metadata database.
        c.execute("""CREATE TABLE operators (
                  logic       TEXT NOT NULL, 
                  name        TEXT NOT NULL, 
                  description TEXT NOT NULL, 
                  UNIQUE(logic, name) ON CONFLICT REPLACE,
                  FOREIGN KEY (logic) REFERENCES logics(logic))""")
        print('The operators table has been created.')

        # Create the axioms table in the metadata database.
        c.execute("""CREATE TABLE axioms (
                logic       TEXT NOT NULL,
                name        TEXT NOT NULL,
                pattern     TEXT NOT NULL,
                displayname TEXT NOT NULL,
                description TEXT NOT NULL,
                UNIQUE(logic, name) ON CONFLICT REPLACE,
                FOREIGN KEY (logic) REFERENCES logics(logic)
                )"""
                )
        print(f'The axioms table has been created.')

        # Create the generic axioms table in the metadata database.
        c.execute("""CREATE TABLE genericaxioms (
                name        TEXT PRIMARY KEY,
                pattern     TEXT NOT NULL,
                displayname TEXT NOT NULL,
                description TEXT NOT NULL
                )"""
                )
        print(f'The generic axioms table has been created.')

        # Load the generic axcioms table.
        genericaxioms = [
            ('dneg intro', 'Implies(*1*, Not(Not(*1*)))', 'dneg intro', 'Double Negation Intro'),
            ('dneg elim', 'Implies(Not(Not(*1*)), *1*)', 'dneg elim', 'Double Negation Elim'),
            ('lem', 'Or(*1*, Not(*1*))', 'lem', 'Law of Excluded Middle'),
            ('wlem', 'Or(Not(*1*), Not(Not(*1*)))', 'wlem', 'Weak Law of Excluded Middle'),
        ]
        statement = 'INSERT INTO genericaxioms (name, pattern, displayname, description) VALUES (?, ?, ?, ?)'
        c.executemany(statement, genericaxioms)
        print(f'The generic axiom table has been loaded with initial axioms.')

    # Commit and close the connection.
    connection.commit()
    connection.close()

def addlogic(logic: str, database: str, description: str, operators: list = [], axioms: list = []):
    """Add the database file and the tables for a new logic."""

    # Connect to metadata to see if the logic already exists.
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    try:
        c.execute('SELECT database, description FROM logics WHERE logic=?', (logic,))
        row = c.fetchone()
        database = row[0]
        print(f'The logic {logic} has already been defined.')
    except TypeError: 
        # Load the logics table.
        statement = 'INSERT INTO logics (logic, database, description) VALUES (?, ?, ?)'
        database = ''.join(['altrea/data/', database.replace(' ','_'), '.db'])
        c.execute(statement, (logic, database, description))
        print('The logics table has been loaded.')

    # Load the operators table.
    if len(operators) > 0:
        statement = 'INSERT INTO operators (logic, name, description) VALUES (?, ?, ?)'
        c.executemany(statement, operators)
        print('The operators table has been loaded.')

    # Load the axioms table.
    if len(axioms) > 0:
        statement = 'INSERT INTO axioms (logic, name, pattern, displayname, description) VALUES (?, ?, ?, ?, ?)'
        c.executemany(statement, axioms)
        print('The axioms table has been loaded.')

    connection.commit()
    print(f'Data loaded to the {metadata} tables have been committed.')
    connection.close()

    # Create the proofs table in the dbname database.
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    c.execute("""CREATE TABLE proofs (
                name        TEXT PRIMARY KEY,
                pattern     TEXT NOT NULL,
                displayname TEXT NULL,
                description TEXT NULL
                )"""
                )
    print(f'The proofs table has been created in {database}.')

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
    print(f'The proofdetails table has been created in {database}.')

    # Commit and close the connection.
    connection.commit()
    print(f'Data loaded to the {database} tables have been committed.')
    connection.close()

def getlogic(logic: str):
    """Retrieve the details about the logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = 'SELECT database, description FROM logics WHERE logic=?'
    c.execute(statement, (logic,))
    row = c.fetchone()
    connection.commit()
    connection.close()
    if type(row) != None:
        return row
    else:
        return ('', '')
    
def getaxioms(logic: str):
    """Retrieve the axioms of this logic."""

    try:
        connection = sqlite3.connect(metadata)
        c = connection.cursor()
        statement = 'SELECT name, pattern, displayname, description FROM axioms WHERE logic=?'
        c.execute(statement, (logic,))
        rows = c.fetchall()
        connection.commit()
        connection.close()
        return rows
    except TypeError:
        return ()
    
def getgenericaxioms():
    """Retrieve some axioms one might choose to use in one's logic."""

    try:
        connection = sqlite3.connect(metadata)
        c = connection.cursor()
        statement = 'SELECT name, pattern, displayname, description FROM genericaxioms'
        c.execute(statement)
        rows = c.fetchall()
        connection.commit()
        connection.close()
        return rows
    except TypeError:
        return ()

def getdefinedlogics():
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = 'SELECT logic, database, description FROM logics'
    c.execute(statement)
    rows = c.fetchall()
    connection.commit()
    connection.close()
    return rows

def getproofdetails(logic: str, name: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = 'SELECT item, level, proof, rule, lines, usedproofs, comment FROM proofdetails WHERE name=?'
    c.execute(statement, (name,))
    rows = c.fetchall()
    connection.commit()
    connection.close()
    return rows

def getavailableproofs(logic: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = 'SELECT name, pattern, displayname, description FROM proofs'
    c.execute(statement)
    rows = c.fetchall()
    connection.commit()
    connection.close()
    return rows

def deleteproof(logic: str, name: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = 'DELETE FROM proofdetails WHERE name=?'
    c.execute(statement, (name,))
    print(f'The proof details for "{name}" have been deleted from proofdetails for "{logic}".')
    statement = 'DELETE FROM proofs WHERE name=?'
    c.execute(statement, (name,))
    print(f'The proof "{name}" has been deleted from proofs for "{logic}".')
    connection.commit()
    connection.close()

def addproof(proofdata: list):
    database = getdatabase(proofdata[0][3])
    connection = sqlite3.connect(database)
    c = connection.cursor()
    name = proofdata[0][0]
    displayname = proofdata[0][1]
    description = proofdata[0][2]
    logic = proofdata[0][3]
    pattern = proofdata[0][4]
    statement = 'SELECT COUNT(*) FROM proofs where name=?'
    c.execute(statement, (name,))
    howmany = c.fetchone()
    if howmany[0] > 0:
        print(f'A proof named "{name}" already exists.')
    else:
        row = (name, pattern, displayname, description)
        statement = 'INSERT INTO proofs (name, pattern, displayname, description) VALUES (?, ?, ?, ?)'
        c.execute(statement, row)
        print(f'The proof "{name}" for logic "{logic}" has been added to {database}.')
        statement = 'INSERT INTO proofdetails (name, item, level, proof, rule, lines, usedproofs, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        c.executemany(statement, proofdata[1:])
        print(f'The proof details for "{name}" for logic "{logic}" have been added to {database}.')
        connection.commit()
        connection.close()

def addaxiom(logic: str, name: str, pattern: str, displayname: str, description: str):
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    row = (logic, name, pattern, displayname, description)
    statement = "INSERT INTO axioms (logic, name, pattern, displayname, description) VALUES (?, ?, ?, ?)"
    c.execute(statement, row)
    connection.commit()
    connection.close()

def deleteaxiom(logic: str, name: str):
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = 'DELETE FROM axioms WHERE logic=? and name=?'
    c.execute(statement, (logic, name,))
    connection.commit()
    connection.close()

def addgenericaxiom(name: str, pattern: str, displayname: str, description: str):
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    row = (name, pattern, displayname, description)
    statement = "INSERT INTO genericaxioms (name, pattern, displayname, description) VALUES (?, ?, ?, ?)"
    c.execute(statement, row)
    connection.commit()
    connection.close()

def usegenericaxiom(logic: str, name: str):
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = 'SELECT pattern, displayname, description FROM genericaxioms where name='
    c.execute(statement, (name,))
    pattern, displayname, description = c.fetchone()
    row = (logic, name, pattern, displayname, description)
    statement = "INSERT INTO axioms (logic, name, pattern, displayname, description) VALUES (?, ?, ?, ?)"
    c.execute(statement, row)
    connection.commit()
    connection.close()

def deletegenericaxiom(name: str):
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = 'DELETE FROM genericaxioms WHERE name=?'
    c.execute(statement, (name,))
    connection.commit()
    connection.close()

def addoperator(logic: str, name: str, description: str):
    """Add a single operator to a logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    row = (logic, name, description)
    statement = "INSERT INTO operators (logic, name, description) VALUES (?, ?, ?)"
    c.execute(statement, row)
    connection.commit()
    connection.close()

def deleteoperator(logic: str, name: str):
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = 'DELETE FROM operators WHERE logic=? and name=?'
    c.execute(statement, (logic, name,))
    connection.commit()
    connection.close()

# def getproof(logic: str, name: str, *subs: str):
#     database = getdatabase(logic)
#     connection = sqlite3.connect(database)
#     c = connection.cursor()
#     c.execute(f'SELECT displayname, description, pattern FROM proofs WHERE name=?')
#     displayname, description, pattern = c.fetchone()
#     connection.commit()
#     connection.close()
#     for i in range(len(subs)):
#         pattern = pattern.replace(''.join(['*', str(i+1), '*']), subs[i])
#     return displayname, description, pattern

def getsavedproof(logic: str, name: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = 'SELECT displayname, description, pattern FROM proofs WHERE name=?'
    c.execute(statement, (name,))
    displayname, description, pattern = c.fetchone()
    connection.commit()
    connection.close()
    return displayname, description, pattern

def getaxiom(logic: str, name: str):
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = 'SELECT displayname, description, pattern FROM axioms WHERE logic=? and name=?'
    c.execute(statement, (logic, name,))
    displayname, description, pattern = c.fetchone()
    connection.commit()
    connection.close()
    return displayname, description, pattern

def getoperators(logic: str):
    """Retrieve the operators of this logic."""

    try:
        connection = sqlite3.connect(metadata)
        c = connection.cursor()
        statement = 'SELECT name, description FROM operators WHERE logic=?'
        c.execute(statement, (logic,))
        rows = c.fetchall()
        connection.commit()
        connection.close()
        return rows
    except TypeError:
        return ()
