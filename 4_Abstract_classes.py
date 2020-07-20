"""
Assignment four: Abstract Classes
Chia Jui Hung

build neurodes and define layertype for
the artificial neuron network

"""

# from module abc we need abc.ABC and abc.abstractmethod
from enum import Enum
from abc import *
import collections as col
import random


class MultiLinkNode(ABC):
    """an abstract class, a neurode in one layer"""
    def __init__(self):
        self.inputNo = 0
        self.outputNo = 0
        self.reporting_inputs = 0
        self.reporting_outputs = 0
        self.input_nodes = col.OrderedDict()
        self.output_nodes = col.OrderedDict()
        self.compare_inputs_full = 0
        self.compare_outputs_full = 0

    @abstractmethod
    def process_new_input_node(self, node):
        pass

    @abstractmethod
    def process_new_output_node(self, node):
        pass

    def clear_and_add_input_nodes(self, nodes):
        self.compare_inputs_full = 2 ** len(nodes) - 1
        self.input_nodes.clear()
        for node in nodes:
            self.input_nodes.update({node: None})
        for node in nodes:
            self.process_new_input_node(node)

    def clear_and_add_output_nodes(self, nodes):
        self.compare_outputs_full = 2 ** len(nodes) - 1
        self.output_nodes.clear()
        for node in nodes:
            self.output_nodes.update({node: None})
        for node in nodes:
            self.process_new_output_node(node)


class LayerType(Enum):
    """includes three layer types """
    HIDDEN = 0
    INPUT = 1
    OUTPUT = 2


class Neurode(MultiLinkNode):
    """a subclass of MultiLinkNode"""
    def __init__(self, my_type):
        super().__init__()
        self.value = 0
        self.my_type = my_type

    def get_type(self):
        return self.my_type

    def get_value(self):
        return self.value

    def process_new_input_node(self, node):
        self.input_nodes[node] = random.random()

    def process_new_output_node(self, node):
        pass


"""runfile('/Users/michellehung/PycharmProjects/intermed software design python
/multiLinkNode.py', wdir='/Users/michellehung/PycharmProjects/
intermed software design python')
"""