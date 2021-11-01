class Tree:
    def __init__(self,children=[]):
        self.children = children
    def add(self,toBeAdded):
        self.children.append(toBeAdded)
    def addMultple(self, multiple):
        for single in multiple:
            self.children.append(single)
    def isLeaf(self):
        return len(self.children) == 0
    def children(self):
        return self.children
    def childn(self,n):
        return self.children[n]
    def nrChildren(self):
        return len(self.children)
    
        
    
