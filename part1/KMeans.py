import sys
import WineClass
import random

cluster_centre = []
clusters = {}
ranges = {}

def Centroid(lst):
    global cluster_centre
    global clusters
    attributes = {}
    for instance in lst:
        for attr in instance.properties:
            if attr == "wine_class":
                continue
            attributes[attr] = attributes.get(attr, 0) + instance.properties[attr]

    vals = {}
    for value in attributes:
        avg = float(attributes[value])/(len(lst))
        vals[value] = avg
    
    return WineClass.WineData(vals["alcohol"],vals["maclic_acid"],vals["ash"],vals["alcalinity_of_ash"],vals["magnesium"],
    vals["total_phenols"],vals["flavanoids"],vals["nonflavanoid_phenols"],vals["proanthocyanins"],vals["colour_intensity"],
    vals["hue"],vals["diluted_wines"],vals["proline"])

def AssignToCentroid(instances):
    global clusters
    global cluster_centre
    for instance in instances:
        min_distance = None
        c = None
        for i in range (0,len(cluster_centre)):
            d = instance.distance(cluster_centre[i],ranges)
            if min_distance is None or d < min_distance:
                min_distance = d
                c = i
        clusters[c].append(instance)

def UpdateCentroid():
    updated = False
    global cluster_centre
    global clusters
    for i in range (0, len(clusters)):
        if (len(clusters[i]) > 0):
            c = Centroid(clusters[i])
            if c.distance(cluster_centre[i],ranges) != 0:
                updated = True
                cluster_centre[i] = c
    
    return updated

if __name__ == "__main__":
    # Number of clusters
    k = 3

    if(len(sys.argv) != 2):
        print("Please provide training file. CMD: 'python KMeans.py wine-training")
    else:
        data = open(sys.argv[1])
        data.readline()

        instances = []
        for line in data:
            vals = line.split()
            instances.append(WineClass.WineData(*vals))

        for i in range (0,k):
            cluster_centre.append(random.choice(instances))
            clusters.setdefault(i,[])

        c1 = 0
        c2 = 0
        c3 = 0
        for instance in instances:
            if instance.properties["wine_class"] == 1:
                c1 += 1
            elif instance.properties["wine_class"] == 2:
                c2 += 1
            else:
                c3 += 1

        print("Class labels: {} {} {}".format(c1,c2,c3))
        ranges = WineClass.GetRange()

        AssignToCentroid(instances)

        print("Initial Allocation")
        for cluster in clusters.values():
            print(len(cluster))

        while(UpdateCentroid()):
            for i in range (0,k):
                del clusters[i][:]
            AssignToCentroid(instances)
            print("Updated Allocation")
            for cluster in clusters.values():
                print(len(cluster))

        print("Final Allocation")
        for cluster in clusters.values():
            print(len(cluster))
