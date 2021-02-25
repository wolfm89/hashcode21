#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import numpy as np
# from sklearn import preprocessing
# import matplotlib.pyplot as plt


class Library(object):
    def __init__(self, id, signup_days, books_per_day, books):
        self.id = id
        self.signup_days = signup_days
        self.books_per_day = books_per_day
        self.books = books
        self.score = 0

    def __str__(self):
        return "{} {} {} {} {}".format(self.id, self.signup_days, self.books_per_day, sum([b.score for b in self.books]), self.score) # + "\n".join([str(b) for b in books])

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
        # n_books_total, scanning_time, books, libraries = read("data/" + filename + ".txt")
        durationD, n_intersections, n_streets, n_cars, bonusF, streets, cars = read("data/" + filename + ".txt")
        # for s in streets:
        #     print(s)

        # for c in cars:
        #     print(c)
        # result_libraries = algorithm2(libraries, scanning_time)

        # print(score(result_libraries, scanning_time))

        # write("output/" + filename + ".out", result_libraries)

