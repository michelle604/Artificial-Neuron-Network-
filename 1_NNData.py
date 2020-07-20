"""Builds a class called NNData with methods that will help us efficiently manage our training and testing data.
   And creates a custom exception DatamismatchError"""

from enum import Enum


class DataMismatchError(Exception):
    """Used to raise the Data mismatch exception"""
    pass


class NNData:
    """An artificial neural network class.
    Includes methods that helps us efficiently manage our training and testing data"""
    class Order(Enum):
        """Defines whether the training data is presented in the same order
         to the neural network each time, or in random order."""
        RANDOM = 1
        SEQUENTIAL = 2

    class Set(Enum):
        """Identifies whether we are requesting training set or testing set data."""
        TRAIN = 3
        TEST = 4

    @staticmethod
    def percentage_limiter(percentage):
        """Accepts percentage as an int and returns 0 if percentage < 0,
        100 is percentage is > 100, or percentage if 0 <= percentage <= 100."""
        if int(percentage) < 0:
            return 0
        elif int(percentage) > 100:
            return 100
        else:
            return int(percentage)

    def __init__(self, x=None, y=None, percentage=100):
        """A method to initialize the object every time when creating one"""
        if x is None:
            x = []
        if y is None:
            y = []

        self.x = x
        self.y = y
        self.train_percentage = NNData.percentage_limiter(percentage)
        self.train_indices = None
        self.train_pool = None
        self.test_indices = None
        self.test_pool = None

    def load_data(self, x, y):
        pass


""""/Users/michellehung/PycharmProjects/python/intermed software design python/bin/python" 
"/Users/michellehung/PycharmProjects/intermed software design python/assignment1.py"
No errors were identified by the unit test.
You should still double check that your code meets spec.
You should also check that PyCharm does not identify any PEP-8 issues.

Process finished with exit code 0"""
