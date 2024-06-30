# fol.py
"""This module support first order logic."""

class Domain():
    """Define a container for the specific elements."""

    lb = "{"
    rb = "}"

    def __init__(self, elements: list, name: str, latexname: str = ""):
        self.elements = elements
        self.name = name
        if latexname == "":
            self.latexname = name
        else:
            self.latexname = latexname

    def __str__(self):
        return f'{self.name}{str([str(i) for i in self.elements])}'.replace("'", "").replace("[", "{").replace("]", "}")
    
    def latex(self):
        return f'{self.latexname}{str([i.latex() for i in self.elements])}'

    def tree(self):
        return f'{self.name}{str([i.tree() for i in self.elements])}'
    
    def pattern(self, objectlist: list):
        return f'{self.name}{str([i.pattern(objectlist) for i in self.elements])}'
    
# class Variable():
#     """Define a container for the specific elements."""

#     lb = "{"
#     rb = "}"

#     def __init__(self, name: str, latexname: str = ""):
#         self.name = name
#         if latexname == "":
#             self.latexname = name
#         else:
#             self.latexname = latexname

#     def __str__(self):
#         return f'{self.name}'
    
#     def latex(self):
#         return f'{self.latexname}'

#     def tree(self):
#         return f'{self.name}'
    
#     # def pattern(self, objectlist: list):
#     #     return f'{self.name}'
    
# class Thing():
#     """Assign a name to a specific thing."""

#     lb = "{"
#     rb = "}"

#     def __init__(self, name: str, latexname: str = ""):
#         self.name = name
#         if latexname == "":
#             self.latexname = name
#         else:
#             self.latexname = latexname

#     def __str__(self):
#         return f'{self.name}'
    
#     def latex(self):
#         return f'{self.latexname}'

#     def tree(self):
#         return f'{self.name}'
    
#     def pattern(self, objectlist: list):
#         try:
#             idx = objectlist.index(self.name)
#         except ValueError:
#             idx = len(objectlist)
#             objectlist.append(self.name)
#         return ''.join(['{', str(idx), '}'])

# class Couple():
#     """Assign a name to a specific thing."""

#     lb = "("
#     rb = ")"
#     c = ", "

#     def __init__(self, left, right):
#         self.left = left,
#         self.right = right,
#         # self.name = name
#         # if latexname == "":
#         #     self.latexname = name
#         # else:
#         #     self.latexname = latexname

#     def __str__(self):
#         return f'{self.lb}{self.left}{self.right}{self.rb}'
    
#     def comma(self):
#         return f'{self.lb}{self.left}{self.c}{self.right}{self.rb}'
    
#     def latex(self):
#         return f'{self.lb}{self.left.latex()}{self.right.latex()}{self.rb}'

#     def tree(self):
#         return f'{self.lb}{self.left.tree()}{self.right.tree()}{self.rb}'
    
#     def pattern(self, objectlist: list):
#         return f'{self.left.pattern(objectlist)}{self.right.pattern(objectlist)}'
    

