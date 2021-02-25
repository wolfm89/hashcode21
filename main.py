#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt


def score(sim_duration, car_score, cars, isec_schedules):
    score = 0

    for t in range(0, sim_duration):
        for car in cars:
            if len(car.way_to_go[0]) == 0:
                continue
            if car.way_to_go[1] != 0:
                car.way_to_go = (car.way_to_go[0], car.way_to_go[1] - 1)
            else:
                if len(car.way_to_go[0]) == 1: # car is done
                    score += car_score + sim_duration - t
                    car.way_to_go = ([], 0)
                    continue
                current_street = car.way_to_go[0][0]
                current_isec = current_street.end_isec
                isec_schedule = [isec_schedule for isec_schedule in isec_schedules if isec_schedule.isec_ix == current_isec][0]
                if is_green(isec_schedule, current_street.name, t):
                    car.way_to_go = (car.way_to_go[0][1:], car.way_to_go[0][1].length - 1)

    return score

def is_green(isec_schedule, street_name, T):
    t = 0
    while True:
        for street_schedule in isec_schedule.street_schedules:
            green_duration = street_schedule[1]
            if t + green_duration > T:
                return street_name == street_schedule[0].name
            else:
                t += green_duration


def algorithm(streets):
    intersections = dict()
    for street in streets:
        if street.end_isec not in intersections:
            intersections[street.end_isec] = set()
            intersections[street.end_isec].add(street)
        else:
            intersections[street.end_isec].add(street)

    isec_schedules = []

    for isec_ix, streets in intersections.items():
        isec_schedule = IntersectionSchedule(isec_ix)
        for street in streets:
            isec_schedule.add_street_schedule(street, 1)
        isec_schedules.append(isec_schedule)

    return isec_schedules


class Street(object):
    def __init__(self, start_isec, end_isec, name, length):
        self.start_isec = start_isec
        self.end_isec = end_isec
        self.name = name
        self.length = length

    def __str__(self):
        return "Street {}: start={} end={} length={}".format(self.name, self.start_isec, self.end_isec, self.length)


class Car(object):
    def __init__(self, ix, streets):
        self.ix = ix
        self.streets = streets
        self.way_to_go = (streets, 0) # name and length remaining to go on current street

    def __str__(self):
        return "Car {}: {}".format(self.ix, [street.name for street in self.streets])


class IntersectionSchedule(object):
    def __init__(self, isec_ix):
        self.isec_ix = isec_ix
        self.street_schedules = []

    def add_street_schedule(self, street, duration):
        self.street_schedules.append((street, duration))


def read(filename):
    with open(filename, 'r') as infile:
        sim_duration, n_isec, n_streets, n_cars, car_score = [int(s) for s in infile.readline().strip().split()]
        streets = []
        for i_street in range(0, n_streets):
            start_isec, end_isec, name, length = infile.readline().strip().split()
            streets.append(Street(int(start_isec), int(end_isec), name, int(length)))

        cars = []
        for i_car in range(0, n_cars):
            n_car_streets, car_street_names = infile.readline().strip().split(maxsplit=1)
            car_street_names = car_street_names.split()
            car_streets = []
            for car_street_name in car_street_names:
                for street in streets:
                    if street.name == car_street_name:
                        car_streets.append(street)
                        break
            cars.append(Car(i_car, car_streets))
    return sim_duration, car_score, n_isec, streets, cars

def write(filename, isec_schedules):
    with open(filename, 'w') as outfile:
        outfile.write(str(len(isec_schedules)) + "\n")
        for isec_schedule in isec_schedules:
            outfile.write("{}".format(isec_schedule.isec_ix) + "\n")
            outfile.write("{}".format(len(isec_schedule.street_schedules)) + "\n")
            for street_schedule in isec_schedule.street_schedules:
                outfile.write("{} {}".format(street_schedule[0].name, street_schedule[1]) + "\n")

if __name__ == "__main__":
    filenames = ["a", "b", "c", "d", "e", "f"]
    # filenames = [filenames[0]]

    for filename in filenames:
        print(filename)
        sim_duration, car_score, n_isec, streets, cars = read("data/" + filename + ".txt")
        print("n_streets: {}".format(len(streets)))
        print("n_cars: {}".format(len(cars)))

        #for car in cars:
        #    print(car)

        #for street in streets:
        #    print(street)

        isec_schedules = algorithm(streets)

        # isec_schedules = []
        #
        # isec_schedule = IntersectionSchedule(1)
        # isec_schedule.add_street_schedule([street for street in streets if street.name == "rue-d-athenes"][0], 2)
        # isec_schedule.add_street_schedule([street for street in streets if street.name == "rue-d-amsterdam"][0], 1)
        # isec_schedules.append(isec_schedule)
        #
        # isec_schedule = IntersectionSchedule(0)
        # isec_schedule.add_street_schedule([street for street in streets if street.name == "rue-de-londres"][0], 2)
        # isec_schedules.append(isec_schedule)
        #
        # isec_schedule = IntersectionSchedule(2)
        # isec_schedule.add_street_schedule([street for street in streets if street.name == "rue-de-moscou"][0], 1)
        # isec_schedules.append(isec_schedule)

        write("output/" + filename + ".out", isec_schedules)

        print("Score: {}".format(score(sim_duration, car_score, cars, isec_schedules)))

