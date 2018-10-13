#!/usr/bin/env python3

"""
Helper Module
"""

import random
import csv
import os
import sys


class RI(object):
    """
    Generateres random instance 

    """
    def __init__(self, instance_size):
        """
        initializes random instance generator

        >>> ri = RI(5)
        >>> print(ri)
        Random instance of size 5 created
        """
        self.instance_size = instance_size

        intensity = [[0 for i in range(instance_size)] for j in range(instance_size)]
        points = self.__generate_random_distance_points()
        distance = self.__generate_distance_matrix(points)

        for i in range(instance_size):
            for j in range(instance_size):
                random_intensity = random.randint(0, 25)
                if i != j:
                    intensity[i][j] = random_intensity
                    intensity[j][i] = random_intensity
        
        self.__distance = distance
        self.__intensity = intensity

    def __str__(self):
        """
        Returns the object information as a string.
        
        """
        return "Random instance of size " + str(self.instance_size) + " created"

    def distance(self):
        """
        return distance matrix
        
        >>> ri = RI(3)
        >>> ri.distance()
        [[0, 707, 387], [707, 0, 320], [387, 320, 0]]
        """
        return self.__distance

    def intensity(self):
        """
        return intensity matrix
        
        >>> ri = RI(3)
        >>> ri.intensity()
        [[0, 4, 3], [4, 0, 1], [3, 1, 0]]
        """
        return self.__intensity

    def __generate_random_distance_points(self):
        """
        generate x y coordinate points randomly
        """
        points = []
        for i in range(self.instance_size):
            x = random.randint(0, 500)
            y = random.randint(0, 500)
            point = [x, y]
            points.append(point)
        return points


    def __generate_distance_matrix(self, points):
        """
        generate points in 500 x 500 coordinate system
        return manhatten norm distance matrix
        """

        distances = [[0 for i in range(len(points))] for j in range(len(points))]
        for i in range(len(points)):
            for j in range(len(points)):
                distances[i][j] = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1]) 

        return distances

class QAP(object):
    """
    initialize QAPlib instance
    """

    def __init__(self, filename):
        """
        intialize QAPlib instance based on filename
        """
        self.__name = filename.replace('qapdat/', '')

        with open(filename, 'r', encoding="utf-8") as inputfile:
            lines = inputfile.readlines()
            returnlines = []
            for line in lines:
                line = line.split()
                if line:
                    returnlines.append(line)
            instancesize = int(returnlines[0][0])
            distance = returnlines[1:instancesize+1][:]
            intensity = returnlines[instancesize+1:instancesize*2+1][:]
            distance = [[float(j) for j in i] for i in distance]
            intensity = [[float(j) for j in i] for i in intensity]

        self.__instancesize = instancesize
        self.__distance = distance
        self.__intensity = intensity

    def __str__(self):
        """
        Returns the object information as a string.
        """

        return "instance " + self.__name +  " with size " + str(self.__instancesize) + " created"

    def instance_size(self):
        """
        """

        return self.__instancesize

    def distance(self):
        """
        """
        return self.__distance

    def intensity(self):
        """
        """
        return self.__intensity

    def name(self):
        """
        """
        return self.__name

    def is_symmetric(self):
        """
        check if given problem is symmetric
        """
        dimension = self.__instancesize
        if len(self.__distance) != len(self.__distance[0]):
            return False
        for row in range(dimension):
            for column in range(dimension):
                if self.__distance[row][column] != self.__distance[column][row]:
                    return False
        return True
    
    def get_solution(self):
        """
        return known solution value based on .sln files 
        => data files need to be placed in qapdat folder
        => solution files in qapsln folder

        
        """
        import os.path
        
        filename = "qapdat/" + self.__name
        filename = filename.replace('dat', 'sln')
        if os.path.isfile(filename):
            with open(filename, 'r', encoding="utf-8") as f:
                optimum = f.readlines()[0].split()[1]
            return optimum
        else:
            return None

    def draw(self, resultvars, file = ""):
        """
        print graph

        resultvars given from pulp solution
        """
        import matplotlib.pyplot as plt
        f = plt.figure()
        ones = [1 for i in range(self.__instancesize)]
        fives = [5 for i in range(self.__instancesize)]
        plt.plot(ones, range(1, self.__instancesize+1), 'ro')
        plt.plot(fives, range(1, self.__instancesize+1), 'bo')

        for var in resultvars:
            var = [var[0] + 1, var[1] + 1]
            plt.plot([1, 5], var)

        if file != "":
            plt.savefig(file)
        
        else:
            plt.show()
        
        plt.gcf().clear()

    def is_solution(self, placed):
        """
        check if found solution is valid and no place or unit appears twice

        >>> from functionalities import *
        >>> qap = QAP('qapdat/chr5a.dat')
        >>> solution = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]
        >>> qap.is_solution(solution)
        True
        >>> new_solution = [[0, 1], [1, 4], [2, 0], [3, 2], [4, 3]]
        >>> qap.is_solution(new_solution)
        True
        >>> false_solution = [[0, 1], [1, 4], [2, 0], [3, 0], [4, 0]]
        >>> qap.is_solution(false_solution)
        False
        >>> false_solution_two = [[0, 1], [1, 0], [2, 2], [3, 9], [4, 5]]
        >>> qap.is_solution(false_solution_two)
        False
        """
        places = []
        units = []
        for pair in placed:
            places.append(pair[0])
            units.append(pair[1])
        
        places = sorted(places)
        units = sorted(units)

        n = self.__instancesize - 1

        if places[0] != 0 or units[0] != 0 or places[-1] != n or units[-1] != n:
            return False

        if len(places) != self.__instancesize or len(units) != self.__instancesize:
            return False

        last = 0
        for i in places[1:]:
            if i - 1 != last:
                return False
            else:
                last = i
        last = 0
        for i in units[1:]:
            if i - 1 != last:
                return False
            else:
                last = i

        return True

def compare(directory, algorithms, models, cutoff, output_file, verbose = True):
    """
    Compares different algorithms.

    Arguments:
    
    """
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_ALL)
        csv_row = ["QAP instance", "instance size", "optimum", "model", "cutoff"]

        for i, algorithm in enumerate(algorithms):
            s = algorithm.name

            csv_row.append(s + "_" + "time")
            csv_row.append(s + "_" + "ov")
            csv_row.append(s + "_" + "solution")
                
        csv_writer.writerow(csv_row)
        csvfile.flush()
            
        for dirpath, _, filenames in os.walk(directory):
            filenames.sort()
            for filename in [f for f in filenames if os.path.splitext(f)[1] == '.' + "dat" and not f.startswith('.')]:
                path = os.path.join(dirpath, filename)
                qap = QAP(path)
                if verbose:
                    print(qap.name() + ":")
                    sys.stdout.flush()

                for j, model in enumerate(models):
                    
                    for k, cut in enumerate(cutoff):
                        csv_row = [qap.name(), str(qap.instance_size()), str(qap.get_solution())]
                        csv_row.append(str(model))
                        csv_row.append(str(cut))
                        for i, algorithm in enumerate(algorithms):
                            
                            if verbose:
                                print(str(algorithm.name) + " " + str(cut) + " " + str(model) + "...")
                                sys.stdout.flush()
                            
                            algorithm.solve(qap, model, cut, False)
                            
                            csv_row.append(str(algorithm.time))
                            csv_row.append(str(algorithm.ov))
                            csv_row.append(str(algorithm.solution))
                            
                            if verbose:
                                print("OK", end="")
                                sys.stdout.flush()
                                if i < len(algorithms) - 1:
                                    print(", ", end="")
                                    sys.stdout.flush()
                                else:
                                    print("")
                                    sys.stdout.flush()
                            
                        csv_writer.writerow(csv_row)
                        csvfile.flush()

    return

def comparison_graph(input_csv, ov_column, compare_column, filename=""):
    """
    create comparison graph
    save if filename is given
    """
    import pandas as pd
    from scipy.stats.mstats import gmean
    import matplotlib.pyplot as plt

    dataframe = pd.read_csv(input_csv, sep=';', skiprows=0)
    dataframe.columns
    s = "Comparison "
    for column in compare_column:
        s += column + " "
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)

    for i, column in enumerate(compare_column):
        dataframe["ratio" + str(i)] = dataframe[column] / dataframe[ov_column]
    group = dataframe.groupby("instance size").agg(lambda x: gmean(list(x)))
    for i, column in enumerate(compare_column):
        ax1.plot(group['ratio' + str(i)],label=column, marker='x', linestyle='--')
    plt.legend(loc='best')
    plt.title(s)
    plt.xlabel("instance size (n)")
    plt.ylabel("ratio to optimum")
    
    if filename == "":
        plt.show()
    else:
        plt.savefig(filename)


"""
helper functions
"""

def get_sorted_x_vars(qap):
    """
    returns x variables of solved qap input
    """

    resultvars = []
    for variable in qap.variables():
        if(str(variable).startswith('x')):
            x_pair = [str(variable), variable.value()]
            resultvars.append(x_pair)
    sorted_resultvars = sorted(resultvars, key=lambda x: x[1], reverse=True)
    return sorted_resultvars

def display_x(qap):
    """
    display x variables with values greater than 0
    """
    for variable in qap.variables():
        if(str(variable).startswith('x') and variable.value() > 0):
           print(variable.value())

def get_not_placed(x_vars, instance_size):
    """
    return ids of not placed units and places
    """
    allElements = [float(i) for i in range(int(instance_size))]
    notPlacedUnit = []
    notPlacedPlace = []
    fromUnit = [i[0] for i in x_vars]
    place = [i[1] for i in x_vars]
    for element in allElements:
        if element not in fromUnit:
            notPlacedUnit.append(element)
        if element not in place:
            notPlacedPlace.append(element)
    return notPlacedUnit, notPlacedPlace

def place_units(x_vars, cut_off):
    """
    place ordered x_vars
    """
    fromUnit = []
    place = []
    placed_units = []
    for x_var in x_vars:
        if(float(x_var[1]) >= cut_off):
            name = str(x_var[0]).replace('x_', '').split('_')
            name = [float(i) for i in name]
            if name[0] not in fromUnit and name[1] not in place:
                fromUnit.append(name[0])
                place.append(name[1])
                placed_units.append(name)
    return placed_units

def create_new_instance(distance_instance, notPlaced):
    """
    get distance or instance matrix of 
    not yet placed places or units
    """
    temp_distance = []
    temp_not_placed = notPlaced[:]
    for missing in notPlaced:
        temp_distance.append(distance_instance[int(missing)][:])

    new_distance_instance = []
    while len(temp_not_placed) > 0:
        new_row = []
        for row in temp_distance:
            new_row.append(row[int(temp_not_placed[0])])
        new_distance_instance.append(new_row)
        del temp_not_placed[0]
    
    return new_distance_instance