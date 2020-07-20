from FFNeurode import *
"""

Assignment six: Backprop and Multiple Inheritance
Chia Jui Hung

creating a backprop neurode that can pass information in the opposite direction

"""


class BPNeurode(Neurode):
    """subclass of Neurode"""
    def __init__(self, my_type):
        super().__init__(my_type)
        self.delta = 0
        self.learning_rate = .05

    @staticmethod
    def sigmoid_derivative(sigmoid):
        """compute derivative of sigmoid"""
        sig_deri = sigmoid * (1 - sigmoid)
        return sig_deri

    def receive_back_input(self, from_node, expected=None):
        """collecting signals from nearby neurons and deciding when to fire."""
        if self.register_back_input(from_node):
            self.calculate_delta(expected)
            self.back_fire()
            if self.my_type is not LayerType.OUTPUT:
                self.update_weights()

    def register_back_input(self, from_node):
        """Process the output data and calculate its own value"""
        if self.my_type is LayerType.OUTPUT:
            return True
        else:
            reporting_node = list(self.output_nodes.keys()).index(from_node)
            self.reporting_outputs = self.reporting_outputs | 2 ** reporting_node
            if self.reporting_outputs == self.compare_outputs_full:
                self.reporting_outputs = 0
                return True
            else:
                return False

    def calculate_delta(self, expected=None):
        """calculate delta"""
        """
        if self.my_type is LayerType.OUTPUT:
            self.delta = (expected - self.value) * self.sigmoid_derivative(self.value)
            return self.delta

        else:
            weighted_delta = 0
            for node in self.output_nodes:
                weight = node.get_weight_for_input_node(self)
                delta = node.get_delta()
                weighted_delta += weight * delta
                self.delta = weighted_delta * self.sigmoid_derivative(self.value)
            return self.delta
        """
        if self.my_type == LayerType.OUTPUT:
            error = expected - self.value
            self.delta = error * self.sigmoid_derivative(self.value)
        else:
            self.delta = 0
            for neurode, data in self.output_nodes.items():
                self.delta += neurode.get_weight_for_input_node(self) * neurode.get_delta()
            self.delta *= self.sigmoid_derivative(self.value)

    def update_weights(self):
        """
        for key, node_data in self.output_nodes.items():
            adjustment = key.get_learning_rate() * key.get_delta() * self.value
            key.adjust_input_node(self, adjustment)

        """
        for key, node_data in self.output_nodes.items():
            adjustment = key.get_learning_rate() * key.get_delta() * self.value
            key.adjust_input_node(self, adjustment)

    def back_fire(self):
        for node in self.input_nodes:
            node.receive_back_input(self)

    def get_learning_rate(self):
        return self.learning_rate

    def get_delta(self):
        return self.delta

    def get_weight_for_input_node(self, from_node):
        return self.input_nodes[from_node]

    def adjust_input_node(self, node, value):
        self.input_nodes[node] += value


class FFBPNeurode(FFNeurode, BPNeurode):
    pass

"""These tests depend on your prior work.
Be sure you have either imported assignments 2, 4 and 5 or include them in the same file as assignment 6.
Testing Sigmoid Derivative
Pass
Testing Instance objects
Pass
Testing register_back_input
Pass
Testing calculate_delta on output nodes
Pass
Testing calculate_delta on hidden nodes
Pass
Testing update_weights
Pass
All that looks good.  Trying to train a trivial dataset on our network
Pass - Learning was done!"""