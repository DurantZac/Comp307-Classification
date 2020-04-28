class Node:

    def __init__(self, attribute, left, right):
        self.attribute = attribute
        self.left = left
        self.right = right

    def report(self, indent):
        print("{}{} = True".format(indent,self.attribute))
        self.left.report(indent + "     ")
        print("{}{} = False".format(indent, self.attribute))
        self.right.report(indent + "     ")

    

class Leaf:
    def __init__(self, name, prob):
        self.name = name
        self.prob = prob

    def report(self, indent):
        print("{} Class: {} Prob: {:.2f}".format(indent, self.name,self.prob))
