"""This module interfaces between the python sqlite3 database."""

import sqlite3

from altrea.boolean import And, Or, Not, Implies, Iff, Wff, Falsehood, Truth, PremisesConclusion

metadata = 'altrea/data/metadata.db'

def getreservedwords():
    return ['No Database', '']

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

        # Create the intelimrules table in the metadata database.
        c.execute("""CREATE TABLE intelimrules (
                  logic       TEXT NOT NULL, 
                  name        TEXT NOT NULL, 
                  description TEXT NOT NULL, 
                  UNIQUE(logic, name) ON CONFLICT REPLACE,
                  FOREIGN KEY (logic) REFERENCES logics(logic))""")
        print('The intelimrules table has been created.')

        # Create the connectors table in the metadata database.
        c.execute("""CREATE TABLE connectors (
                  logic       TEXT NOT NULL, 
                  name        TEXT NOT NULL, 
                  description TEXT NOT NULL, 
                  UNIQUE(logic, name) ON CONFLICT REPLACE,
                  FOREIGN KEY (logic) REFERENCES logics(logic))""")
        print('The connectors table has been created.')

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

        # Load the generic axioms table.
        genericaxioms = [
            ('dneg intro', 'Implies(*1*, Not(Not(*1*)))', 'dneg intro', 'Double Negation Intro'),
            ('dneg elim', 'Implies(Not(Not(*1*)), *1*)', 'dneg elim', 'Double Negation Elim'),
            ('lem', 'Or(*1*, Not(*1*))', 'lem', 'Law of Excluded Middle'),
            ('wlem', 'Or(Not(*1*), Not(Not(*1*)))', 'wlem', 'Weak Law of Excluded Middle'),
            ('contradiction', 'And(*1*, Not(*1*))', 'Contradiction', 'All contradictions are true'),
            ('explosion', 'Implies(And(*1*, Not(*1*)), *2*)', 'Explosion', 'From a contradiction derive anything'),
        ]
        statement = 'INSERT INTO genericaxioms (name, pattern, displayname, description) VALUES (?, ?, ?, ?)'
        c.executemany(statement, genericaxioms)
        print(f'The generic axiom table has been loaded with initial axioms.')

    # Commit and close the connection.
    connection.commit()
    connection.close()

def addlogic(logic: str, database: str, description: str, connectors: list = [], intelimrules: list = [], axioms: list = []):
    """Add the database file and the tables for a new logic."""

    # Reserved name to avoid conflicts with other parts of the software.
    reservedwords = getreservedwords()
    if logic in reservedwords:
        raise ValueError(f'The name of the logic "{logic}" cannot be in the list of reserved words "{reservedwords}".')
    if type(logic) != str:
        raise TypeError(f'The name of the logic must be of string type.')
    
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
        print(f'The logics table has been loaded for logic {logic}.')

    # Load the connectors table.
    if len(connectors) > 0:
        try:
            statement = 'INSERT INTO connectors (logic, name, description) VALUES (?, ?, ?)'
            c.executemany(statement, connectors)
            print(f'The connectors table for logic {logic} has been loaded.')
        except sqlite3.OperationalError:
            print(f'The connectors table received an operational error for logic {logic}.')

    # Load the intelimrules table.
    if len(intelimrules) > 0:
        try:
            statement = 'INSERT INTO intelimrules (logic, name, description) VALUES (?, ?, ?)'
            c.executemany(statement, intelimrules)
            print(f'The intelimrules table for logic {logic} has been loaded.')
        except sqlite3.OperationalError:
            print(f'The intelimrules table received an operational error for logic {logic}.')

    # Load the axioms table.
    if len(axioms) > 0:
        try:
            statement = 'INSERT INTO axioms (logic, name, pattern, displayname, description) VALUES (?, ?, ?, ?, ?)'
            c.executemany(statement, axioms)
            print(f'The axioms table for logic {logic} has been loaded.')
        except sqlite3.OperationalError:
            print(f'The axioms table received an operational error for logic {logic}.')

    connection.commit()
    print(f'Data loaded to the {metadata} tables have been committed.')
    connection.close()

    # Create the proofs table in the dbname database.
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    try:
        c.execute("""CREATE TABLE proofs (
                    name        TEXT PRIMARY KEY,
                    pattern     TEXT NOT NULL,
                    displayname TEXT NULL,
                    description TEXT NULL
                    )"""
                )
        print(f'The proofs table has been created in {database}.')
    except sqlite3.OperationalError:
        print('The proof table already exists.')

    # Create the proofdetails table in the dbname database.
    try:
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
    except sqlite3.OperationalError:
        print('The proofdetails table already exists.')

    # Commit and close the connection.
    connection.commit()
    print(f'Data loaded to the {database} tables have been committed.')
    connection.close()

def deletelogic(logic: str):
    # Connect and get a cursor to the logic database.
    try:
        database = getdatabase(logic)
    except UnboundLocalError:
        print(f'The logic {logic} does not exist in the database.')
    else:
        connection = sqlite3.connect(database)
        c = connection.cursor()

        # Drop the proofdetails table.
        statement = 'DROP TABLE proofdetails'
        try:
            c.execute(statement)
        except sqlite3.OperationalError:
            print(f'The proofdetails table for logic {logic} does not exist.')
        else:
            print(f'The proofdetails table for logic {logic} has been dropped.')

        # Drop the proofs table.
        statement = 'DROP TABLE proofs'
        try:
            c.execute(statement)
        except sqlite3.OperationalError:
            print(f'The proofs table for logic {logic} does not exist.')
        else:
            print(f'The proofs table for logic {logic} has been dropped.')

        # Commit and disconnect.
        connection.commit()
        connection.close()

        # Connect and get cursor to metadata database.
        connection = sqlite3.connect(metadata)
        c = connection.cursor()

        # Delete from the axioms table.
        statement = 'DELETE FROM axioms WHERE logic=?'
        c.execute(statement, (logic,))
        print(f'Axioms associated with {logic} have been deleted.')

        # Delete from the intelimrules table.
        statement = 'DELETE FROM intelimrules WHERE logic=?'
        c.execute(statement, (logic,))
        print(f'Intelim rules associated with {logic} have been deleted.')

        # Delete from the connectors table.
        statement = 'DELETE FROM connectors WHERE logic=?'
        c.execute(statement, (logic,))
        print(f'Connectors associated with {logic} have been deleted.')

        # Delete from the logics table.
        statement = 'DELETE FROM logics WHERE logic=?'
        c.execute(statement, (logic,))
        print(f'The record for {logic} in the logics table has been deleted.')

        # Commit and disconnect.
        connection.commit()
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
    try:
        c.execute(statement, (name,))
    except:
        print(f'The proofdetails table is not available for logic {logic}.')
    else:
        rows = c.fetchall()
        connection.commit()
        connection.close()
        return rows

def getavailableproofs(logic: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = 'SELECT name, pattern, displayname, description FROM proofs'
    try:
        c.execute(statement)
    except sqlite3.OperationalError:
        print(f'The proofs table is not available for logic {logic}.')
    else:
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

def addintelimrule(logic: str, name: str, description: str):
    """Add a single operator to a logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    row = (logic, name, description)
    statement = "INSERT INTO intelimrules (logic, name, description) VALUES (?, ?, ?)"
    c.execute(statement, row)
    connection.commit()
    connection.close()

def deleteintelimrule(logic: str, name: str):
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = 'DELETE FROM intelimrules WHERE logic=? and name=?'
    c.execute(statement, (logic, name,))
    connection.commit()
    connection.close()

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

def getintelimrules(logic: str):
    """Retrieve the intelim rules of this logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = 'SELECT name, description FROM intelimrules WHERE logic=?'
    try:
        c.execute(statement, (logic,))
    except TypeError:
        return ([])
    else:
        rows = c.fetchall()
        connection.commit()
        connection.close()
        return rows
    
def getconnectors(logic: str):
    """Retrieve the connectors of this logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = 'SELECT name, description FROM connectors WHERE logic=?'
    try:
        c.execute(statement, (logic,))
    except TypeError:
        print(f'The {logic} connectors could not be accessed.')
    else:
        rows = c.fetchall()
        connection.commit()
        connection.close()
        return rows

def testlogic(logic: str):
    spacer = '      '
    print(f'Testing the "{logic}" logic setup in AltRea')

    # Test that the logic has been defined.
    print(f'{spacer}')
    print('Has the logic been defined with metadata and a database table?')
    try:
        database, description = getlogic(logic)
        print(f'The logic "{logic}" with description "{description}" will store proofs in "{database}".')
    except TypeError:
        print(f'The logics table does not have the logic "{logic}" in it.')

    # Test the axioms.
    print(f'{spacer}')
    print('What axioms have been defined?')
    axioms = getaxioms(logic)
    if len(axioms) == 0:
        print(f'The logic "{logic}" has no axioms.')
    else:
        for i in axioms:
            print(i)

    # Test the connectors.
    print(f'{spacer}')
    print('What connectors are available?')
    connectors = getconnectors(logic)
    if len(connectors) == 0:
        print(f'The logic "{logic}" has no connectors.')
    else:
        for i in connectors:
            print(i)

    # Test the intelim rules.
    print(f'{spacer}')
    print('What intelim rules are available?')
    intelimrules = getintelimrules(logic)
    if len(intelimrules) == 0:
        print(f'The logic "{logic}" has no intelimrules.')
    else:
        for i in intelimrules:
            print(i)

    # Test the list of saved proofs.
    print(f'{spacer}')
    print('What proofs have been saved?')
    try:
        proofs = getavailableproofs(logic)
    except sqlite3.OperationalError:
        print(f'The proofs and proofdetails tables are not available for {logic}.')
    except UnboundLocalError:
        print(f'The {logic} database is unavailable.')
    else:
        try:
            prooflen = len(proofs)
        except:
            print(f'The proofs table for logic {logic} returned no records.')
        else:
            if prooflen == 0:
                print(f'The logic "{logic}" has no saved proofs.')
            else:
                for i in proofs:
                    print(i)
