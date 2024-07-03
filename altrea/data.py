"""This module interfaces between the python sqlite3 database."""

import sqlite3
import pandas
import os


# from altrea.wffs import And, Or, Not, Implies, Iff, Wff, Falsehood, Truth, ConclusionPremises

metadata = "altrea/data/metadata.db"
datafolder = "altrea/data/"
proofsfolder = 'altrea/proofs/research/contents/'


def getreservedwords():
    return ["No Database", ""]


def getdatabase(logic: str):
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = "SELECT database FROM logics WHERE logic =?"
    c.execute(statement, (logic,))
    dbname = c.fetchone()
    try:
        database = dbname[0]
    except TypeError:
        print(f'The logic "{logic}" could not be found in the logics table.')
    connection.commit()
    connection.close()
    return database


def createmetadatatables():
    """Create the metadata file and logics and operators table if the logics table does not exist."""

    # Connect to metadata.
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    try:
        c.execute("SELECT COUNT(*) FROM logics")
        rows = c.fetchone()
        print(f"The logics table already has {rows[0]} rows in it.")
    except sqlite3.OperationalError:
        # Create the logics table in the metadata database.
        c.execute("""CREATE TABLE logics (
                    logic       TEXT PRIMARY KEY,
                    database    TEXT UNIQUE,
                    description TEXT NOT NULL)""")
        print("The logics table has been created.")

        # Create the connectives table in the metadata database.
        c.execute("""CREATE TABLE connectives (
                  logic       TEXT NOT NULL, 
                  name        TEXT NOT NULL, 
                  str         TEXT NOT NULL,
                  latex       TEXT NOT NULL,
                  description TEXT NOT NULL, 
                  UNIQUE(logic, name) ON CONFLICT REPLACE,
                  FOREIGN KEY (logic) REFERENCES logics(logic))""")
        print("The connectives table has been created.")

        # Create the definitions table in the metadata database.
        c.execute("""CREATE TABLE definitions (
                logic       TEXT NOT NULL,
                name        TEXT NOT NULL,
                pattern     TEXT NOT NULL,
                displayname TEXT NOT NULL,
                description TEXT NOT NULL,
                UNIQUE(logic, name) ON CONFLICT REPLACE,
                UNIQUE(logic, displayname) ON CONFLICT REPLACE,
                FOREIGN KEY (logic) REFERENCES logics(logic)
                )""")
        print("The definitions table has been created.")

        # Create the axioms table in the metadata database.
        c.execute("""CREATE TABLE axioms (
                logic       TEXT NOT NULL,
                name        TEXT NOT NULL,
                pattern     TEXT NOT NULL,
                displayname TEXT NOT NULL,
                description TEXT NOT NULL,
                UNIQUE(logic, name) ON CONFLICT REPLACE,
                UNIQUE(logic, displayname) ON CONFLICT REPLACE,
                FOREIGN KEY (logic) REFERENCES logics(logic)
                )""")
        print("The axioms table has been created.")

        # Create the rules table in the metadata database.
        c.execute("""CREATE TABLE rules (
                logic       TEXT NOT NULL,
                name        TEXT NOT NULL,
                pattern     TEXT NOT NULL,
                displayname TEXT NOT NULL,
                description TEXT NOT NULL,
                UNIQUE(logic, name) ON CONFLICT REPLACE,
                UNIQUE(logic, displayname) ON CONFLICT REPLACE,
                FOREIGN KEY (logic) REFERENCES logics(logic)
                )""")
        print("The rules table has been created.")

        # Create the bibliography table in the metadata database.
        c.execute("""CREATE TABLE bibliography (
                logic       TEXT NOT NULL,
                name        TEXT NOT NULL,
                pattern     TEXT NOT NULL,
                displayname TEXT NOT NULL,
                description TEXT NOT NULL,
                UNIQUE(logic, name) ON CONFLICT REPLACE,
                FOREIGN KEY (logic) REFERENCES logics(logic)
                )""")
        print("The bibliography table has been created.")

    # Commit and close the connection.
    connection.commit()
    connection.close()


def addlogic(
    logic: str,
    database: str,
    description: str,
    connectives: list = [],
    rules: list = [],
    definitions: list = [],
    axioms: list = [],
):
    """Add the database file and the tables for a new logic."""

    # Reserved name to avoid conflicts with other parts of the software.
    reservedwords = getreservedwords()
    if logic in reservedwords:
        raise ValueError(
            f'The name of the logic "{logic}" cannot be in the list of reserved words "{reservedwords}".'
        )
    if not isinstance(logic, str):
        raise TypeError("The name of the logic must be of string type.")

    # Connect to metadata to see if the logic already exists.
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    try:
        c.execute("SELECT database, description FROM logics WHERE logic=?", (logic,))
        row = c.fetchone()
        database = row[0]
        print(f"The logic {logic} has already been defined.")
    except TypeError:
        # Load the logics table.
        statement = """INSERT INTO logics (
            logic, 
            database, 
            description) 
        VALUES (?, ?, ?)"""
        database = "".join(["altrea/data/", database.replace(" ", "_"), ".db"])
        c.execute(statement, (logic, database, description))
        print(f'The logics table has been loaded for logic "{logic}" with {str(c.rowcount)} records.')

    # Load the connectives table.
    if len(connectives) > 0:
        print(f"There are {len(connectives)} connectives to load.")
        statement = """INSERT INTO connectives (
            logic, 
            name, 
            str,
            latex,
            description) 
        VALUES (?, ?, ?, ?, ?)"""
        c.executemany(statement, connectives)
        print(f'The connectives table for logic "{logic}" has been loaded with {str(c.rowcount)} records.')
    else:
        print("There were no connectives to load.")

    # Load the rules table.
    if len(rules) > 0:
        print(f"There are {len(rules)} rules to load.")
        statement = """INSERT INTO rules (
            logic, 
            name, 
            pattern, 
            displayname, 
            description) 
        VALUES (?, ?, ?, ?, ?)"""
        c.executemany(statement, rules)
        print(f'The rules table for logic "{logic}" has been loaded with {str(c.rowcount)} records.')
    else:
        print("There were no rules to load.")

    # Load the definitions table.
    if len(definitions) > 0:
        print(f"There are {len(definitions)} definitionss to load.")
        statement = """INSERT INTO definitions (
            logic, 
            name, 
            pattern, 
            displayname, 
            description) 
        VALUES (?, ?, ?, ?, ?)"""
        c.executemany(statement, definitions)
        print(f'The definitions table for logic "{logic}" has been loaded with {str(c.rowcount)} records.')
    else:
        print("There were no definitions to load.")

    # Load the axioms table.
    if len(axioms) > 0:
        print(f"There are {len(axioms)} axioms to load.")
        statement = """INSERT INTO axioms (
            logic, 
            name, 
            pattern, 
            displayname, 
            description) 
        VALUES (?, ?, ?, ?, ?)"""
        c.executemany(statement, axioms)
        print(f'The axioms table for logic "{logic}" has been loaded with {str(c.rowcount)} records.')
    else:
        print("There were no axiomss to load.")

    connection.commit()
    print(f"Data loaded to the {metadata} tables have been committed.")
    connection.close()

    # Create the proofs table in the dbname database.
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = "SELECT COUNT(*) FROM proofs"
    
    try:
        c.execute(statement)
        howmany = c.fetchone()
    except sqlite3.OperationalError:
        c.execute("""CREATE TABLE proofs (
                    name         TEXT PRIMARY KEY,
                    pattern      TEXT NOT NULL,
                    displayname  TEXT NOT NULL,
                    description  TEXT NULL,
                    textversion  TEXT NULL,
                    latexversion TEXT NULL,
                    UNIQUE(displayname) ON CONFLICT REPLACE
                    )""")
        print(f"The proofs table has been created in {database}.")

        # Create the proofdetails table in the dbname database.
        c.execute("""CREATE TABLE proofdetails (
                    name           TEXT NOT NULL,
                    item           TEXT NOT NULL,
                    level          INT  NOT NULL,
                    proof          INT  NOT NULL,
                    rule           TEXT NOT NULL,
                    lines          TEXT NULL,
                    usedproofs     TEXT NULL,
                    comment        TEXT NULL,
                    linetype       TEXT NULL,
                    subproofstatus TEXT NULL,
                    FOREIGN KEY (name) 
                        REFERENCES proofs(name)
                    )""")
        print(f"The proofdetails table has been created in {database}.")

        # Create the proofcodelines table in the dbname database.
        c.execute("""CREATE TABLE proofcodelines (
                    name           TEXT NOT NULL,
                    line           TEXT NOT NULL,
                    FOREIGN KEY (name) 
                        REFERENCES proofs(name)
                    )""")
        print(f"The proofcodelines table has been created in {database}.")
    else:
        print(f"The proof table already contains {howmany[0]} rows.")

    # Commit and close the connection.
    connection.commit()
    print(f"Data loaded to the {database} tables have been committed.")
    connection.close()


def deletelogic(logic: str):
    # Connect and get a cursor to the logic database.
    try:
        database = getdatabase(logic)
    except UnboundLocalError:
        # print(f'The logic "{logic}" is not defined in the database.')
        pass
    else:
        connection = sqlite3.connect(database)
        c = connection.cursor()

        # Drop the proofcodelines table.
        statement = "DROP TABLE proofcodelines"
        c.execute(statement)
        print(f"The proofcodelines table for logic {logic} has been dropped.")

        # Drop the proofdetails table.
        statement = "DROP TABLE proofdetails"
        c.execute(statement)
        print(f"The proofdetails table for logic {logic} has been dropped.")

        # Drop the proofs table.
        statement = "DROP TABLE proofs"
        c.execute(statement)
        print(f"The proofs table for logic {logic} has been dropped.")

        # Commit and disconnect.
        connection.commit()
        connection.close()

        # Connect and get cursor to metadata database.
        connection = sqlite3.connect(metadata)
        c = connection.cursor()

        # Delete from the definitions table.
        statement = "DELETE FROM definitions WHERE logic=?"
        c.execute(statement, (logic,))
        print(f"Any definitions associated with {logic} have been deleted.")

        # Delete from the axioms table.
        statement = "DELETE FROM axioms WHERE logic=?"
        c.execute(statement, (logic,))
        print(f"Any axioms associated with {logic} have been deleted.")

        # Delete from the rules table.
        statement = "DELETE FROM rules WHERE logic=?"
        c.execute(statement, (logic,))
        print(f"Any rules associated with {logic} have been deleted.")

        # Delete from the connectives table.
        statement = "DELETE FROM connectives WHERE logic=?"
        c.execute(statement, (logic,))
        print(f"Any connectives associated with {logic} have been deleted.")

        # Delete from the logics table.
        statement = "DELETE FROM logics WHERE logic=?"
        c.execute(statement, (logic,))
        print(f"The record for {logic} in the logics table has been deleted.")

        # Commit and disconnect.
        connection.commit()
        connection.close()


def getlogic(logic: str):
    """Retrieve the details about the logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = """SELECT 
        database, 
        description 
    FROM logics 
    WHERE logic=?"""
    c.execute(statement, (logic,))
    row = c.fetchone()
    connection.commit()
    connection.close()
    if type(row) is not None:
        return row
    else:
        return ("", "")


def getdefinedlogics():
    """Retrieve all of the defined logics."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = """SELECT 
        logic, 
        database, 
        description 
    FROM logics 
    ORDER BY logic"""
    c.execute(statement)
    rows = c.fetchall()
    connection.commit()
    connection.close()
    index = [i for i in range(1, len(rows) + 1)]
    columns = ["Name", "Database", "Description"]
    df = pandas.DataFrame(rows, index=index, columns=columns)
    return df


def addaxiom(logic: str, name: str, pattern: str, displayname: str, description: str):
    """Add an axiom to a logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = "SELECT COUNT(*) FROM axioms WHERE logic=? AND name=?"
    c.execute(
        statement,
        (
            logic,
            name,
        ),
    )
    howmany = c.fetchone()
    if howmany[0] == 0:
        row = (logic, name, pattern, displayname, description)
        statement = """INSERT INTO axioms (
            logic, 
            name, 
            pattern, 
            displayname, 
            description
        ) VALUES (?, ?, ?, ?, ?)"""
        c.execute(statement, row)
        connection.commit()
        print(
            f'The axiom "{name}" defined as "{pattern}" has been loaded to the "{logic}" database.'
        )
    else:
        print(
            f'There is already an axiom by the name "{name}" in the "{logic}" database.'
        )
    connection.close()


def deleteaxiom(logic: str, name: str):
    """Delete an axiom from a logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = "SELECT COUNT(*) FROM axioms WHERE logic=? AND name=?"
    c.execute(
        statement,
        (
            logic,
            name,
        ),
    )
    howmany = c.fetchone()
    if howmany[0] > 0:
        statement = "DELETE FROM axioms WHERE logic=? and name=?"
        c.execute(
            statement,
            (
                logic,
                name,
            ),
        )
        connection.commit()
        print(f'The axiom "{name}" has been deleted from the "{logic}" database.')
    else:
        print(f'There is no axiom by the name "{name}" in the "{logic}" database.')
    connection.close()


def getaxiom(logic: str, name: str):
    """Retrieve a single axiom by name."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = """SELECT 
        displayname, 
        description, 
        pattern 
    FROM axioms 
    WHERE logic=? 
    AND name=?"""
    c.execute(
        statement,
        (
            logic,
            name,
        ),
    )
    displayname, description, pattern = c.fetchone()
    connection.commit()
    connection.close()
    return displayname, description, pattern


def getaxioms(logic: str):
    """Retrieve all of the axioms of this logic."""
    
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = """SELECT 
        name, 
        pattern, 
        displayname, 
        description 
    FROM axioms 
    WHERE logic=? 
    ORDER BY name"""
    try:
        c.execute(statement, (logic,))
    except TypeError:
        return []
    else:
        rows = c.fetchall()
        connection.commit()
        connection.close()
        return rows
    

def addconnective(logic: str, name: str, str: str, latex: str, description: str):
    """Add a connective to a logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = "SELECT COUNT(*) FROM connectives WHERE logic=? AND name=?"
    c.execute(
        statement,
        (
            logic,
            name,
        ),
    )
    howmany = c.fetchone()
    if howmany[0] == 0:
        row = (logic, name, str, latex, description)
        statement = """INSERT INTO axioms (
            logic, 
            name, 
            str, 
            latex, 
            description
        ) VALUES (?, ?, ?, ?, ?)"""
        c.execute(statement, row)
        connection.commit()
        print(
            f'The connective "{name}" represented by "{str}" and "{latex}" has been loaded to the "{logic}" database.'
        )
    else:
        print(
            f'There is already a connective by the name "{name}" in the "{logic}" database.'
        )
    connection.close()


def deleteconnective(logic: str, name: str):
    """Delete an axiom from a logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = "SELECT COUNT(*) FROM connectives WHERE logic=? AND name=?"
    c.execute(
        statement,
        (
            logic,
            name,
        ),
    )
    howmany = c.fetchone()
    if howmany[0] > 0:
        statement = "DELETE FROM connectives WHERE logic=? and name=?"
        c.execute(
            statement,
            (
                logic,
                name,
            ),
        )
        connection.commit()
        print(f'The connective "{name}" has been deleted from the "{logic}" database.')
    else:
        print(f'There is no connective by the name "{name}" in the "{logic}" database.')
    connection.close()


def getconnective(logic: str, name: str):
    """Retrieve a single connective by name."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = """SELECT 
        str, 
        latex,
        description
    FROM connectives 
    WHERE logic=? 
    AND name=?"""
    c.execute(
        statement,
        (
            logic,
            name,
        ),
    )
    str, latex, description = c.fetchone()
    connection.commit()
    connection.close()
    return str, latex, description


def getconnectives(logic: str):
    """Retrieve the connectors of this logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = "SELECT name, str, latex, description FROM connectives WHERE logic=?"
    try:
        c.execute(statement, (logic,))
    except TypeError:
        print(f"The {logic} connectives could not be accessed.")
    else:
        rows = c.fetchall()
        connection.commit()
        connection.close()
        return rows
    

def addrule(
    logic: str, name: str, pattern: str, displayname: str, description: str
):
    """Add a rule to a logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = "SELECT COUNT(*) FROM rules WHERE logic=? AND name=?"
    c.execute(
        statement,
        (
            logic,
            name,
        ),
    )
    howmany = c.fetchone()
    if howmany[0] == 0:
        row = (logic, name, pattern, displayname, description)
        statement = """INSERT INTO rules (
            logic, 
            name, 
            pattern, 
            displayname, 
            description
        ) VALUES (?, ?, ?, ?, ?)"""
        c.execute(statement, row)
        connection.commit()
        print(
            f'The rule "{name}" defined as "{pattern}" has been loaded to the "{logic}" database.'
        )
    else:
        print(
            f'There is already a rule by the name "{name}" in the "{logic}" database.'
        )
    connection.close()


def deleterule(logic: str, name: str):
    """Delete an rule from a logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = "SELECT COUNT(*) FROM rules WHERE logic=? AND name=?"
    c.execute(
        statement,
        (
            logic,
            name,
        ),
    )
    howmany = c.fetchone()
    if howmany[0] > 0:
        statement = "DELETE FROM rules WHERE logic=? and name=?"
        c.execute(
            statement,
            (
                logic,
                name,
            ),
        )
        connection.commit()
        print(f'The rule "{name}" has been deleted from the "{logic}" database.')
    else:
        print(f'There is no rule by the name "{name}" in the "{logic}" database.')
    connection.close()


def getrules(logic: str):
    """Retrieve the transformation rules of this logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = """SELECT 
        name, 
        pattern, 
        displayname, 
        description 
    FROM rules 
    WHERE logic=? 
    ORDER BY name"""
    try:
        c.execute(statement, (logic,))
    except TypeError:
        return []
    else:
        rows = c.fetchall()
        #print(f"The number of rules returned is {len(rows)}.")
        connection.commit()
        connection.close()
        return rows
    
def gethowmanyrules(logic: str):
    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = "SELECT COUNT() FROM rules WHERE logic=?"
    c.execute(statement, (logic,))
    rows = c.fetchone()
    return rows


def adddefinition(
    logic: str, name: str, pattern: str, displayname: str, description: str
):
    """Add a definition to a logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = "SELECT COUNT(*) FROM definitions WHERE logic=? AND name=?"
    c.execute(
        statement,
        (
            logic,
            name,
        ),
    )
    howmany = c.fetchone()
    if howmany[0] == 0:
        row = (logic, name, pattern, displayname, description)
        statement = """INSERT INTO definitions (
            logic, 
            name, 
            pattern, 
            displayname, 
            description
        ) VALUES (?, ?, ?, ?, ?)"""
        c.execute(statement, row)
        connection.commit()
        print(
            f'The definition "{name}" defined as "{pattern}" has been loaded to the "{logic}" database.'
        )
    else:
        print(
            f'There is already a definition by the name "{name}" in the "{logic}" database.'
        )
    connection.close()


def deletedefinition(logic: str, name: str):
    """Delete a definition from a logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = "SELECT COUNT(*) FROM definitions WHERE logic=? AND name=?"
    c.execute(
        statement,
        (
            logic,
            name,
        ),
    )
    howmany = c.fetchone()
    if howmany[0] > 0:
        statement = "DELETE FROM definitions WHERE logic=? and name=?"
        c.execute(
            statement,
            (
                logic,
                name,
            ),
        )
        connection.commit()
        print(f'The definition "{name}" has been deleted from the "{logic}" database.')
    else:
        print(f'There is no definition by the name "{name}" in the "{logic}" database.')
    connection.close()


def getdefinitions(logic: str):
    """Retrieve the axioms of this logic."""

    connection = sqlite3.connect(metadata)
    c = connection.cursor()
    statement = """SELECT 
        name, 
        pattern, 
        displayname, 
        description 
    FROM definitions 
    WHERE logic=? 
    ORDER BY name"""
    try:
        c.execute(statement, (logic,))
    except TypeError:
        return []
    else:
        rows = c.fetchall()
        connection.commit()
        connection.close()
        return rows
    

def addproof(proofdata: list, proofcode: list):
    """Add a proof to a logic."""

    name = proofdata[0][0]
    displayname = proofdata[0][1]
    description = proofdata[0][2]
    logic = proofdata[0][3]
    pattern = proofdata[0][4]
    database = getdatabase(logic)
    print(f"Connecting to {logic} using {database} to store proof {name}.")
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = "SELECT COUNT(*) FROM proofs where name=?"
    c.execute(statement, (name,))
    howmany = c.fetchone()
    if howmany[0] == 0:
        row = (name, pattern, displayname, description)
        statement = """INSERT INTO proofs (
            name, 
            pattern, 
            displayname, 
            description
        ) VALUES (?, ?, ?, ?)"""
        c.execute(statement, row)
        print(
            f'The proof "{name}" has been added to "{logic}".'
        )
        statement = """INSERT INTO proofdetails (
            name, 
            item, 
            level, 
            proof, 
            rule, 
            lines, 
            usedproofs, 
            comment, 
            linetype, 
            subproofstatus
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        c.executemany(statement, proofdata[1:])
        print(
            f'The proof details for "{name}" have been added to "{logic}".'
        )
        statement = """INSERT INTO proofcodelines (
            name, 
            line 
        ) VALUES (?, ?)"""
        codelines = [(name, i) for i in proofcode]
        c.executemany(statement, codelines)
        print(
            f'The proof code lines for "{name}" have been added to "{logic}".'
        )
        connection.commit()
        connection.close()
    else:
        print(
            f'Details for a proof named "{name}" already exist for "{logic}".'
        )
    return howmany[0]


def deleteproof(logic: str, name: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = "DELETE FROM proofdetails WHERE name=?"
    c.execute(statement, (name,))
    print(
        f'The proof details for "{name}" have been deleted from proofdetails for "{logic}".'
    )
    statement = "DELETE FROM proofcodelines WHERE name=?"
    c.execute(statement, (name,))
    print(
        f'The proof code lines for "{name}" have been deleted from proofcodelines for "{logic}".'
    )
    statement = "DELETE FROM proofs WHERE name=?"
    c.execute(statement, (name,))
    print(f'The proof "{name}" has been deleted from proofs for "{logic}".')
    connection.commit()
    connection.close()

    
def getproofs(logic: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = (
        "SELECT name, pattern, displayname, description FROM proofs ORDER BY name"
    )
    try:
        c.execute(statement)
    except sqlite3.OperationalError:
        return []
    else:
        rows = c.fetchall()
        connection.commit()
        connection.close()
        return rows


def getproofdetails(logic: str, name: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = """SELECT 
        item, 
        level, 
        proof, 
        rule, 
        lines, 
        usedproofs, 
        comment, 
        linetype, 
        subproofstatus 
    FROM proofdetails 
    WHERE name=?"""
    try:
        c.execute(statement, (name,))
    except Exception:
        print(f"The proofdetails table is not available for logic {logic}.")
    else:
        rows = c.fetchall()
        connection.commit()
        connection.close()
        return rows
    

def getproofcodelines(logic: str, name: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = """SELECT 
        line 
    FROM proofcodelines 
    WHERE name=?"""
    try:
        c.execute(statement, (name,))
    except Exception:
        print(f"The proofcodelines table is not available for logic {logic}.")
    else:
        rows = c.fetchall()
        connection.commit()
        connection.close()
        return rows


def getlemma(logic: str, displayname: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = "SELECT name, description, pattern FROM proofs WHERE displayname=?"
    c.execute(statement, (displayname,))
    name, description, pattern = c.fetchone()
    connection.commit()
    connection.close()
    return name, description, pattern


def getsavedproof(logic: str, name: str):
    database = getdatabase(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    statement = "SELECT displayname, description, pattern FROM proofs WHERE name=?"
    c.execute(statement, (name,))
    displayname, description, pattern = c.fetchone()
    connection.commit()
    connection.close()
    return displayname, description, pattern





def savetofile(text: str, filename: str, directory: str = "./"):
    fullfilename = ''.join([directory, filename])
    if os.path.exists(fullfilename):
        print(f"The file at {fullfilename} already exists.")
    else:
        f = open(fullfilename, "w")
        f.write(text)
        f.close()
        print(f'The file named "{fullfilename}" has been written.')
