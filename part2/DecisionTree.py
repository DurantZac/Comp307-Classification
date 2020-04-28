import sys
import Node
import operator
import math

classifications = ()
attributes = []
training_instances = []

class Instance:
    def __init__(self, args = []):
        self.properties = {}
        i = 0
        for arg in args:
            if i == 0:
                self.classification = arg
            else:
                self.properties[attributes[i-1]] = arg
            i+=1

def Baseline():
    classes = GetClassCounts(training_instances)
    c = max(classes.items(), key=operator.itemgetter(1))[0]
    return Node.Leaf(c, float(classes[c])/float(len(training_instances)))

def BuildTree (instances, attrs):

    # No instances in tree, return default class chances
    if len(instances) == 0:
        return Baseline()

    classes = GetClassCounts(instances)
    # Only one class left, 100% chance at this point, no need to split further
    if len(classes.keys()) == 1:
        return Node.Leaf(instances[0].classification, 1)

    # Run out of attributes to branch, return current highest prob
    if len(attributes) == 0:
        c = max(classes.items(), key=operator.itemgetter(1))[0]
        return Node.Leaf(c, float(classes[c])/float(len(instances)))
    
    bestAttr = None
    bestInstancesTrue = []
    bestInstancesFalse = []
    bestImpurity = None

    # For attr in attrs, find best split
    for attr in attrs:
        instancesTrue = []
        intancesFalse = []
        # Split instances into true and false
        for instance in instances:
            if instance.properties[attr] == "true":
                instancesTrue.append(instance)
            else:
                intancesFalse.append(instance)
        # Find best impurity split
        impurity = CalculateImpurity(instancesTrue, intancesFalse)
        if bestImpurity is None or impurity < bestImpurity:
            bestImpurity = impurity
            bestAttr = attr
            bestInstancesTrue = instancesTrue
            bestInstancesFalse = intancesFalse
    attrs.remove(bestAttr)
    # Recursivly build tree
    left = BuildTree(bestInstancesTrue, attrs)
    right = BuildTree(bestInstancesFalse, attrs)

    # Return branch node
    return Node.Node(bestAttr, left, right)

def CalculateImpurity(instances_one, instances_two):
    size = len(instances_one) + len(instances_two)

    # Get class counts for each instance
    classes_one = GetClassCounts(instances_one)
    classes_two = GetClassCounts(instances_two)

    # If set is impure, calculate impurity
    if len(classes_one) < 2:
        impurity_one = 0
    else:
        impurity_one = float(classes_one[classifications[0]] * classes_one[classifications[1]]) / float(math.pow(classes_one[classifications[0]] + classes_one[classifications[1]],2))
    
    if len(classes_two) < 2:
        impurity_two = 0
    else:
        impurity_two = float(classes_two[classifications[0]] * classes_two[classifications[1]]) / float(math.pow(classes_two[classifications[0]] + classes_two[classifications[1]],2))

    # Weight impurity by prob that instance falls into this set
    weight_one = impurity_one * (float(len(instances_one)) / float(size))
    weight_two = impurity_two * (float(len(instances_two)) / float(size))

    return weight_one + weight_two
    

def GetClassCounts(instances):
    classes = {}
    for instance in instances:
        c = instance.classification
        if c not in classes:
            classes[c] = 1
        else:
            classes[c] = classes[c] + 1
    return classes

def Classify(node, instance):
    if isinstance(node, Node.Leaf):
        return node
    
    if instance.properties[node.attribute] == "true":
        return Classify(node.left, instance)
    else:
        return Classify(node.right, instance)

def Run(training_name, test_name):
    global classifications
    global attributes
    global training_instances

    training_set = open(training_name)
    test_set = open(test_name)
    test_instances = []

    # Set up names of classifications
    classifications = training_set.readline().split()
    # Set up list of attributes
    attributes = training_set.readline().split()


    for line in training_set:
        training_instances.append(Instance(line.split()))
    
    test_set.readline()
    test_set.readline()

    for line in test_set:
        test_instances.append(Instance(line.split()))

    print("Training decision tree from {}".format(training_name))
    n = BuildTree(training_instances, attributes)

    correct = 0
    incorrect = 0
    base_correct = 0
    base_incorrect = 0

    for instance in test_instances:
        c = Classify(n, instance)
        if c.name == instance.classification:
            correct += 1
        else:
            incorrect += 1
        if Baseline().name == instance.classification:
            base_correct += 1
        else:
            base_incorrect += 1

    accuracy = float(correct)/float(correct+incorrect)
    print("Rate of classification: {:.2f}".format(accuracy))
    print("Baseline classification: {:.2f}".format(float(base_correct)/float(base_correct+base_incorrect)))
    return n, accuracy


if __name__ == "__main__":
    
    print("\n\n")
    if(len(sys.argv) != 3):
        print("Please provide training and test files. CMD: 'TODO")
    
    tree, accuracy = Run(sys.argv[1],sys.argv[2])
    print("Tree generated for {} {}".format(sys.argv[1],sys.argv[2]))
    tree.report("")

    print("\n\n")

    results = []
    for run in range (0,10):
        results.append(Run("hepatitis-training-run-{}".format(run),"hepatitis-test-run-{}".format(run))[1])

    average = float(sum(results)) / float(len(results))
    print("Average perfomance: {}".format(average))