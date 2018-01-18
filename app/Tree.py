class Node:

    def __init__(self, id, data):
        self._id = id
        self._data = data
        self._children = []

    def getdata(self):
        return self._data

    def getid(self):
        return self._id

    def getchildren(self):
        return self._children

    def add(self, node):
        self._children.append(node)

    def gobydata(self, data):
        for child in self._children:
            if child.getdata() == data:
                return child
        return None

class Tree:

    def __init__(self):
        self._head = Node('0', 'header')
'''
    def insert(self, fid, id, data):
        cur = self._head
        for step in
'''