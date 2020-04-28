import sys
import math
import operator


class WineData:

    # Static measures of property range
    property_max = {"alcohol" : -10000, "maclic_acid": -10000, "ash" : -10000, "alcalinity_of_ash" : -10000, "magnesium" : -10000,
    "total_phenols" : -10000, "flavanoids" : -10000, "nonflavanoid_phenols" : -10000, "proanthocyanins" : -10000, 
    "colour_intensity" : -10000, "hue" : -10000, "diluted_wines" : -10000, "proline" : -10000}

    property_min = {"alcohol" : 10000, "maclic_acid": 10000, "ash" : 10000, "alcalinity_of_ash" : 10000, "magnesium" : 10000,
    "total_phenols" : 10000, "flavanoids" : 10000, "nonflavanoid_phenols" : 10000, "proanthocyanins" : 10000, 
    "colour_intensity" : 10000, "hue" : 10000, "diluted_wines" : 10000, "proline" : 10000}

    def __init__(self, Alcohol, Malic_acid, Ash, Alcalinity_of_ash, Magnesium, Total_phenols, 
    Flavanoids, Nonflavanoid_phenols, Proanthocyanins, Color_intensity, Hue,  diluted_wines, Proline, Wine_class = None):
      self.properties = {}
      self.properties["alcohol"] = float(Alcohol)
      self.properties["maclic_acid"] = float(Malic_acid)
      self.properties["ash"] = float(Ash)
      self.properties["alcalinity_of_ash"] = float(Alcalinity_of_ash)
      self.properties["magnesium"] = float(Magnesium)
      self.properties["total_phenols"] = float(Total_phenols)
      self.properties["flavanoids"] = float(Flavanoids)
      self.properties["nonflavanoid_phenols"] = float(Nonflavanoid_phenols)
      self.properties["proanthocyanins"] = float(Proanthocyanins)
      self.properties["colour_intensity"] = float(Color_intensity)
      self.properties["hue"] = float(Hue)
      self.properties["diluted_wines"] = float(diluted_wines)
      self.properties["proline"] = float(Proline)
      if Wine_class is None:
          Wine_class = 0
      self.properties["wine_class"] = float(Wine_class)

      # Update range of values
      self.__update_ranges()

    # Calculate distance to other node
    def distance(self, obj, ranges = {}):
        d_squared = 0
        for key in self.properties:
            if key not in "wine_class":
                d_squared += math.pow((self.properties[key] - obj.properties[key]),2) / math.pow(ranges[key],2)
        return math.sqrt(d_squared)

    # For each property in this object, check if outside currently recorded range
    def __update_ranges(self):
        for key in self.properties:
            if key in self.property_max and key in self.property_min:
                if self.properties[key] > self.property_max[key]:
                    self.property_max[key] = self.properties[key]
                if self.properties[key] < self.property_min[key]:
                    self.property_min[key] = self.properties[key]

    # Classify this node by its kNN with the training set 'training' and the ranges given in 'ranges'
    def classify(self, k, training = [], ranges = {}):
        closest = {}

        # Get all distances
        for obj in training:
            d = self.distance(obj, ranges)
            closest[obj] = d;
        
        # Get closest nodes
        votes = {}
        for i in range (0,k):
            ordered = min(closest.items(), key=operator.itemgetter(1))
            c = ordered[0].properties['wine_class']
            del closest[ordered[0]]

            ## Vote for closest nodes class
            if not c in votes:
                votes[c] = 1
            else:
                votes[c] += 1

        # Return max votes
        return max(votes.items(), key=operator.itemgetter(1))[0]
            
def GetRange():
    ranges = {}
    for key in WineData.property_max:
        ranges[key] = abs (WineData.property_max[key] - WineData.property_min[key])
    return ranges
    
if __name__ == "__main__":
    # Number of neighbours to consider
    k = 3
    if(len(sys.argv) != 3):
        print("Please provide training and test files. CMD: 'python WineClass.py wine-training wine-test")
    else:
        print("Classifying {} set with {} training set. Considering the {} nearest neighbours".format(sys.argv[1], sys.argv[2], k))
        training_objs = []
        testing_objs = []

        training_set = open(sys.argv[1])
        test_set = open(sys.argv[2])

        training_set.readline()

        correct = 0
        incorrect = 0

        # Training set
        for line in training_set:
            vals = line.split() 
            training_objs.append(WineData(*vals))

        test_set.readline()

        # Get Range of properties
        ranges = GetRange()
        
        # Test set
        for line in test_set:
            vals = line.split() 
            testing_objs.append(WineData(*vals))

        i = 0
        for o in testing_objs:
            result = o.classify(k, training_objs, ranges)
            print("Instance {} classified as class {:d}".format(i,math.trunc(result)))
            i+=1
            if  result == o.properties["wine_class"]:
                correct+= 1
            else: 
                incorrect+= 1
        
        print("Rate of classification: {:.2f}".format(float(correct)/(correct+incorrect)))


