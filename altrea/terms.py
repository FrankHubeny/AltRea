# term.py
"""This is a class for terms"""

class Term():
    """Either a subject or a predicate term."""

    def __init__(self, name: str):
        self.name = name
        self.distributed = ''

    def __str__(self):
        return f'{self.name}'