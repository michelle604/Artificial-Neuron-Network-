from enum import Enum
import collections
import random

"""Assignment two:Building a Data Class
Chia Jui Hung

Creates methods in class NNData to link two dataset, 
x and y and their subsets
"""


class DataMismatchError(Exception):
    """Number of x and y elements do not match"""
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
        if percentage < 0:
            return 0
        elif percentage > 100:
            return 100
        else:
            return int(percentage)

    def __init__(self, x=None, y=None, percentage=100):
        """A method to initialize the object every time when creating one
        and calls method load_data"""
        if x is None:
            x = []
        if y is None:
            y = []

        self.x = x
        self.y = y
        self.train_percentage = NNData.percentage_limiter(percentage)
        self.train_indices = None
        self.test_indices = None
        self.train_pool = None
        self.test_pool = None
        self.load_data(x, y)

    def load_data(self, x, y):
        """Compares the size of dataset x and y,
         and calls method split_set"""
        if len(x) != len(y):
            raise DataMismatchError
        self.x = x
        self.y = y
        self.split_set(new_train_percentage=None)

    def split_set(self, new_train_percentage=None):
        """Splits dataset x into two subsets"""
        if new_train_percentage is not None:
            self.train_percentage = NNData.percentage_limiter(new_train_percentage)
        train_size = int(self.train_percentage * 0.01 * len(self.x))
        self.train_indices = random.sample(range(0, len(self.x)), train_size)
        self.test_indices = list(set(range(0, len(self.x))) - set(self.train_indices))
        self.prime_data(my_set=None, order=None)

    def prime_data(self, my_set=None, order=None):
        """Primes the subsets by copying the subsets to deque pools"""
        if order is None:
            order = NNData.Order.SEQUENTIAL

        if order is NNData.Order.SEQUENTIAL:
            if my_set is not NNData.Set.TRAIN:
                self.test_pool = collections.deque(self.test_indices)
            if my_set is not NNData.Set.TEST:
                self.train_pool = collections.deque(self.train_indices)

        elif order is NNData.Order.RANDOM:
            if my_set is not NNData.Set.TRAIN:
                test_indices_temp = list(self.test_indices)
                random.shuffle(test_indices_temp)
                self.test_pool = collections.deque(test_indices_temp)
            if my_set is not NNData.Set.TEST:
                train_indices_temp = list(self.train_indices)
                random.shuffle(train_indices_temp)
                self.train_pool = collections.deque(train_indices_temp)

    def empty_pool(self, my_set=None):
        """Returns True if the pool indicated by my_set is empty,
         or False if not."""
        if my_set is None:
            my_set = NNData.Set.TRAIN
        if my_set is NNData.Set.TRAIN:
            if len(self.train_pool) == 0:
                return True
            return False
        if my_set is NNData.Set.TEST:
            if len(self.test_pool) == 0:
                return True
            return False

    def get_number_samples(self, my_set=None):
        """Returns the size of the pools"""
        if my_set is None:
            return len(self.x)
        elif my_set is NNData.Set.TRAIN:
            return len(self.train_pool)
        elif my_set is NNData.Set.TEST:
            return len(self.test_pool)

    def get_one_item(self, my_set=None):
        """Gets the leftmost item of the pool and
        returns the x and y data of the item"""
        list_x_y = []
        if my_set is None:
            my_set = NNData.Set.TRAIN
        if my_set is NNData.Set.TRAIN:
            if len(self.train_pool) == 0:
                return None
            else:
                train_pool_popleft = self.train_pool.popleft()
                popleft_x = self.x[train_pool_popleft]
                popleft_y = self.y[train_pool_popleft]
                list_x_y.append(popleft_x)
                list_x_y.append(popleft_y)
                return list_x_y
        if my_set is NNData.Set.TEST:
            if len(self.test_pool) == 0:
                return None
            else:
                test_pool_popleft = self.test_pool.popleft()
                popleft_x = self.x[test_pool_popleft]
                popleft_y = self.y[test_pool_popleft]
                list_x_y.append(popleft_x)
                list_x_y.append(popleft_y)
                return list_x_y


"""No errors were identified by the unit test.
You should still double check that your code meets spec.
You should also check that PyCharm does not identify any PEP-8 issues."""
def main():
    errors = False
    try:
        X = list(range(10))
        Y = X
        our_data = NNData(X, Y)
        X = list(range(100))
        Y = X
        our_big_data = NNData(X, Y, 50)
        Y = [1]
        try:
            our_bad_data = NNData(X, Y)
            raise Exception
        except DataMismatchError:
            pass
        except:
            raise Exception
        X = ['a', 'b', 'c', 'd']
        Y = ['A', 'B', 'C', 'D']
        our_char_data = NNData(X, Y, 50)
    except:
        print("There are errors that likely come from __init__ or a method called by __init__")
        errors = True
    try:
        our_data.split_set(30)
        assert len(our_data.train_indices) == 3
        assert len(our_data.test_indices) == 7
        assert (list(set(our_data.train_indices + our_data.test_indices))) == list(range(10))
    except:
        print("There are errors that likely come from split_set")
        errors = True
    try:
        our_data.prime_data(order=NNData.Order.SEQUENTIAL)
        assert len(our_data.train_pool) == 3
        assert len(our_data.test_pool) == 7
        assert our_data.train_indices == list(our_data.train_pool)
        assert our_data.test_indices == list(our_data.test_pool)
        our_big_data.prime_data(order=NNData.Order.RANDOM)
        assert our_big_data.train_indices != list(our_big_data.train_pool)
        assert our_big_data.test_indices != list(our_big_data.test_pool)
    except:
        print("There are errors that likely come from prime_data")
        errors = True

    try:
        our_data.prime_data(order=NNData.Order.SEQUENTIAL)
        my_x_list = []
        my_y_list = []
        while not our_char_data.empty_pool():
            example = our_char_data.get_one_item()
            my_x_list.append(example[0])
            my_y_list.append(example[1])
        assert len(my_x_list) == 2
        assert my_x_list != my_y_list
        my_upper_x_list = [k.upper() for k in my_y_list]
        assert my_upper_x_list == my_y_list
        while not our_char_data.empty_pool(our_char_data.Set.TEST):
            example = our_char_data.get_one_item(our_char_data.Set.TEST)
            my_x_list.append(example[0])
            my_y_list.append(example[1])
        assert my_x_list != my_y_list
        my_upper_x_list = [k.upper() for k in my_y_list]
        assert my_upper_x_list == my_y_list
        assert set(my_x_list) == set(X)
        assert set(my_y_list) == set(Y)
    except:
        print("There are errors that may come from prime_data, but could be from another method")
        errors = True
    if errors:
        print("You have one or more errors.  Please fix them before submitting")
    else:
        print("No errors were identified by the unit test.")
        print("You should still double check that your code meets spec.")
        print("You should also check that PyCharm does not identify any PEP-8 issues.")
if __name__ == "__main__":
    main()