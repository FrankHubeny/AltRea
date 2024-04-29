"""This module interfaces between the python sqlite3 database."""

import sqlite3

import altrea.truthfunction

logicdatabases = {
        'C': 'altrea/data/classical_propositional.db',
        'CI': 'classical_implicational.db',
        'CO': 'classical_non_implicational.db',
        'I': 'intuitionist_propositional.db',
        'MC': 'metamath_classical.db',
        'MI': 'metamath_intuitionist.db',
        'MNF': 'metamath_newfoundations.db',
    }

def checkdatabase(logic: str):
    database = logicdatabases.get(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    rows = -1
    try:
        c.execute("SELECT COUNT(*) FROM proofs")
        rows = c.fetchone()
    except:
        c.execute("""CREATE TABLE proofs (
            name TEXT,
            proof BLOB
        )
        """)
    connection.close()
    return rows

def addproof(p: altrea.truthfunction.Proof):
    database = logicdatabases.get(p.logic)
    # print(p.logic) 
    # print(p.name) 
    # print(p.proofdata) 
    # print(p.lines)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    row = (p.name, p.proofdata)
    statement = "INSERT INTO proofs (name, proof) VALUES (?, ?)"
    c.execute(statement, row)
    connection.commit()
    connection.close()


def getproof(logic: str, name: str):
    database = logicdatabases.get(logic)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    c.execute(f"SELECT proof FROM proofs WHERE name = '{name}'")
    proof = c.fetchone()
    connection.close()
    return proof

# def getdisplay(logic: str, name: str):
#     database = logicdatabases.get(logic)
#     connection = sqlite3.connect(database)
#     c = connection.cursor()
#     c.execute("SELECT display FROM proofs WHERE name = '{}'".format(name))
#     display = c.fetchone()
#     connection.close()
#     return display

