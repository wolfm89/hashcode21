#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt


def score(library_list, days):
    score = 0
    list_scanned_books = []
    days_remaining = days

    for library in library_list:
        if days_remaining >= library.signup_days:
            days_remaining = days_remaining - library.signup_days
            books_scanning_limit = days_remaining * library.books_per_day
            books_possible_to_scan = library.books[0:books_scanning_limit-1]
            for book in books_possible_to_scan:
                if list_scanned_books.count(book.id) == 0:
                    score = score + book.score
                    list_scanned_books.append(book.id)
    return score

def algorithm1(libraries, scanning_days):
    def algo(timer, lib):
        lib.books.sort(key=lambda book: book.score, reverse=True)
        lib.books = lib.books[:(timer * lib.books_per_day)]

    timer = scanning_days
    libraries.sort(key=lambda library: library.signup_days)
    books_total = set()
    i_break = -1
    for i, library in enumerate(libraries):
        #if (library.id == 163):
            #print(timer, library.id, len(library.books), library.signup_days, library.books_per_day)
        timer = timer - library.signup_days
        if timer <= 0:
            i_break = i
            break
        library.books = [book for book in library.books if book not in books_total]
        if len(library.books) == 0:
            continue
        # create set form books list and disjunct irgendwas
        algo(timer, library)
        books_total = books_total.union(library.books)
    return [library for library[:i_break] in libraries if len(library.books) != 0]

def algorithm2(libraries, scanning_days):
    def calc_scores(libraries, scanning_days):

        select_books = lambda library: sorted(library.books, key=lambda book: book.score, reverse=True)[:scanning_days*library.books_per_day]
        scores = np.array([sum([b.score for b in select_books(library)]) for library in libraries])
        norm_scores = preprocessing.scale(scores)

        n_books = np.array([len(library.books) for library in libraries])
        norm_n_books = - preprocessing.scale(n_books)

        sign_up = np.array([library.signup_days for library in libraries])
        #print(sign_up.min(), sign_up.max())
        norm_sign_up = - preprocessing.scale(sign_up)

        books_per_day = np.array([library.books_per_day for library in libraries])
        norm_books_per_day = preprocessing.scale(books_per_day)

        if False:
            datas = [scores, n_books, sign_up, books_per_day]
            for data in datas:
                plt.hist(data, bins=100)
                plt.show()
                plt.gca().set(title='Frequency Histogram', ylabel='Frequency')

        #library_scores = norm_scores + norm_n_books + norm_sign_up + norm_books_per_day # a, b
        #library_scores = norm_sign_up # c
        #library_scores = norm_scores + norm_n_books # d
        #library_scores = 1.4*norm_scores + norm_n_books + 2*norm_sign_up + norm_books_per_day # e
        library_scores = 6*norm_scores + norm_n_books + 20*norm_sign_up + norm_books_per_day # f

        for library, score in zip(libraries, library_scores.tolist()):
            library.score = score

    def algo(timer, lib):
        lib.books.sort(key=lambda book: book.score, reverse=True)
        lib.books = lib.books[:(timer * lib.books_per_day)]

    print("scanning days: {}".format(scanning_days))
    timer = scanning_days

    calc_scores(libraries, scanning_days)
    libraries.sort(key=lambda library: library.score, reverse=True)

    for lib in libraries[:5]:
        print(lib)

    books_total = set()
    for library in libraries:
        timer = timer - library.signup_days
        if timer <= 0:
            break
        library.books = [book for book in library.books if book not in books_total]
        if len(library.books) == 0:
            continue
        # create set form books list and disjunct irgendwas
        algo(timer, library)
        books_total = books_total.union(library.books)
    print("n_books_total in result: {}".format(len(books_total)))
    print("Total book score: {}".format(sum([b.score for b in books_total])))
    return [library for library in libraries if len(library.books) != 0]


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

    def __str__(self):
        return "Car {}: {}".format(self.ix, self.streets)


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
            cars.append(Car(i_car, car_street_names.split()))
    return sim_duration, n_isec, streets, cars

def write(filename, libraries):
    with open(filename, 'w') as outfile:
        outfile.write(str(len(libraries)) + "\n")
        for library in libraries:
            outfile.write("{} {}".format(library.id, len(library.books)) + "\n")
            outfile.write(" ".join([str(book.id) for book in library.books]) + "\n")

if __name__ == "__main__":
    filenames = ["a", "b", "c", "d", "e", "f"]
    filenames = [filenames[0]]

    for filename in filenames:
        print(filename)
        sim_duration, n_isec, streets, cars = read("data/" + filename + ".txt")
        print("n_streets: {}".format(len(streets)))
        print("n_cars: {}".format(len(cars)))

        for car in cars:
            print(car)

        for street in streets:
            print(street)

        # result_libraries = algorithm2(libraries, scanning_time)

        # print(score(result_libraries, scanning_time))

        # write("output/" + filename + ".out", result_libraries)

