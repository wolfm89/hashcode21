#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import numpy as np
# from sklearn import preprocessing
# import matplotlib.pyplot as plt
import collections


class Car(object):
    def __init__(self, n_streets, streets_name):
        self.n_streets = n_streets
        self.streets_name = streets_name

    def __str__(self):
        return f"Car: {self.n_streets} streets: {self.streets_name}"

class Street(object):
    def __init__(self, start_intersection, end_intersection, street_name, travel_time):
        self.start_intersection = start_intersection
        self.end_intersection = end_intersection
        self.street_name = street_name
        self.travel_time = travel_time

    def __str__(self):
        return f"street {self.street_name}, intersection {self.start_intersection} to {self.end_intersection}, takes time: {self.travel_time}"


def create_street_frequency(cars):
    street_list = []
    for car in cars:
        street_list.extend(car.streets_name)
    return dict(collections.Counter(street_list))

def create_end_intersection_dict(streets):
    intersection_dict = {}
    for street in streets:
        intersection_dict[street.end_intersection] = []
    for street in streets:
        intersection_dict[street.end_intersection].append(street.street_name)

    return intersection_dict

def read(filename):
    with open(filename, 'r') as infile:
        durationD, n_intersections, n_streets, n_cars, bonusF = [int(s) for s in infile.readline().strip().split()]
        streets = []
        cars = []

        for i_street in range(0, n_streets):
            b ,e, street_name, l = infile.readline().strip().split()
            streets.append(Street(b,e,street_name, l))
        
        for i_car in range(0, n_cars):
            readline_list = infile.readline().strip().split()
            cars.append(Car(readline_list[0], readline_list[1:]))

    return durationD, n_intersections, n_streets, n_cars, bonusF, streets, cars

def algo1(street_frequency_dict, end_intersection_dict):
    result_dict = {}
    for street in street_frequency_dict.keys():
        result_dict[street] = 1
    return result_dict

def write(file_name, street_frequency_dict, end_intersection_dict):
    duration_dict = algo1(street_frequency_dict, end_intersection_dict)
    with open(file_name, 'w') as outfile:
        outfile.write(str(len(end_intersection_dict)) + "\n")
        for intersection, street_name_list in end_intersection_dict.items():
            outfile.write(str(intersection) + "\n")
            outfile.write(str(len(street_name_list)) + "\n")

            for i in street_name_list:
                if i in duration_dict.keys():
                    outfile.write(str(i) + " " + str(duration_dict[i]) + "\n")
                else:
                    outfile.write(str(i) + " " + "0" + "\n")
                    

if __name__ == "__main__":
    filenames = ["a", "b", "c", "d", "e", "f"]
    # filenames = [filenames[0]]

    for filename in filenames:
        print(filename)
        # n_books_total, scanning_time, books, libraries = read("data/" + filename + ".txt")
        durationD, n_intersections, n_streets, n_cars, bonusF, streets, cars = read("data/" + filename + ".txt")
        # for s in streets:
        #     print(s)

        # for c in cars:
        #     print(c)
        street_frequency_dict = create_street_frequency(cars)
        end_intersection_dict = create_end_intersection_dict(streets)
        print(street_frequency_dict)
        print(end_intersection_dict)
        # result_libraries = algorithm2(libraries, scanning_time)

        # print(score(result_libraries, scanning_time))

        write("output/" + filename + ".out", street_frequency_dict, end_intersection_dict)

