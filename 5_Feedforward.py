from multiLinkNode import *
import numpy as np

"""
Assignment five: Feedforward
Chia Jui Hung

creating a feedforward neurode that can

- Accept data from it's input side
- Process that data and calculate its own value
- 'fire' when appropriate, passing its data to the output side.

"""


class FFNeurode(Neurode):
    """Feedforward is a subclass of Neurode"""
    def __init__(self, my_type):
        super().__init__(my_type)

    @staticmethod
    def activate_sigmoid(value):
        sigmoid = 1 / (1 + np.exp(-value))
        return sigmoid

    def receive_input(self, from_node=None, input_value=0):
        """Accept data from it's input side"""
        if self.my_type is LayerType.INPUT:
            self.value = input_value
            for node in self.output_nodes:
                node.receive_input(self)
        elif self.register_input(from_node):
            self.fire()

    def register_input(self, from_node):
        """Process that data and calculate its own value"""
        reporting_node = list(self.input_nodes.keys()).index(from_node)
        self.reporting_inputs = 2 ** reporting_node | self.reporting_inputs
        if self.reporting_inputs == self.compare_inputs_full:
            self.reporting_inputs = 0
            return True
        return False

    def fire(self):
        """Pass its data to the output side"""
        """
        our_neurode = 0
        for node in self.input_nodes:
            our_neurode += node.get_value() * self.input_nodes[node]
        self.value = self.activate_sigmoid(our_neurode)
        for node in self.output_nodes:
            node.receive_input(self)
        """
        input_sum = 0
        for key, node_data in self.input_nodes.items():
            input_sum += key.get_value() * node_data
        self.value = FFNeurode.activate_sigmoid(input_sum)
        for key in self.output_nodes:
            key.receive_input(self)


"""
PyDev console: starting.
Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 05:52:31) 
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)] on darwin
runfile('/Users/michellehung/PycharmProjects/intermed software design python/assignment5.py',
wdir='/Users/michellehung/PycharmProjects/intermed software design python')
"""