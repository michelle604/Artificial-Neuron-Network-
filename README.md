# Implement an Artificial Neuron Network
Each chapter corresponds to the number of each python file. For example, chapter 1 correpsonds to 1_NNData.py

## Chapter 1: NNData

### Enum
- The Order enum will have elements RANDOM and SEQUENTIAL.  This will define whether the training data is presented in the same order to the neural network each time, or in random order.
- The Set enum will have elements TRAIN and TEST.  At different times as we go along, this enum will help us identify whether we are requesting training set or testing set data.

### Static Method
Our class will have one static method, percentage_limiter(percentage), which accepts percentage as an int and returns 0 if percentage < 0, 100 is percentage is > 100, or percentage if 0 <= percentage <= 100.

### Constructor

Constructor for NNData will have three parameters:

- x should default to None.  x will be the example part of the data we want loaded.  It should be passed as a list of lists, with each row representing one example.  If x is None, then x should be set to [] right away in __init__().  
- y should default to None.  y will be the label part of the data we want loaded.It should be passed as a list of lists, with each row representing one label.  If y is None, then y should be set to [] right away in __init__().  
- percentage is an int that should default to 100, and represents the percentage of the data we want used as our training set.

The constructor will also initialize some internal data:

- self.x and self.y can be set to None to avoid warnings.
- percentage should be passed to NNData.percentage_limiter(), and the result assigned to self.train_percentage.
- self.train_indices, initially set to None, is a list of pointers to the training subset of the data
- self.train_pool, initially set to None, will be a dequeue containing the examples not yet used in the current epoch.  You will learn about dequeue in the next module.
- self.test_indices, initially set to None, is a list of pointers to the testing subset of the data
- self.test_pool, initially set to None, will be a dequeue containing the examples not yet used in the current test run
Finally, the constructor will call load_data(x, y).

### Method Stub
For the 2_NNData.py
