from assignment7 import*
from BPNeurode import*

"""

Assignment 8 :LayerList

Chia Jui Hung

Create a Layer inherits from DLLNode and a LayerList inherits from DoublyLinkedList

"""


class NodePositionError(Exception):
    pass


class Layer(DLLNode):
    """Create a list of neurodes and inherit it from DLLNode"""
    def __init__(self, num_neurodes=5, my_type=LayerType.HIDDEN):
        super().__init__()
        self.my_type = my_type
        self.neurodes = []
        for _ in range(num_neurodes):
            self.add_neurode()

    def add_neurode(self):
        neurode = FFBPNeurode(self.my_type)
        self.neurodes.append(neurode)

    def get_my_neurodes(self):
        return self.neurodes

    def get_my_type(self):
        return self.my_type

    def get_layer_info(self):
        layer_info = (self.my_type, len(self.neurodes))
        return layer_info


class LayerList(DoublyLinkedList):
    """Create several methods for neurode lists in each layer to be able to link/delink with each other
        and inherit the class from DoublyLinkedList"""
    def __init__(self, num_inputs, num_outputs):
        super().__init__()
        input_layer = Layer(num_inputs, LayerType.INPUT)
        self.add_to_head(input_layer)
        output_layer = Layer(num_outputs, LayerType.OUTPUT)
        super().reset_cur()
        self.insert_after_cur(output_layer)

    def insert_after_cur(self, new_layer):
        if new_layer.get_my_type() is LayerType.OUTPUT:
            for neurode in self.current.get_my_neurodes():
                neurode.clear_and_add_output_nodes(new_layer.get_my_neurodes())
            for neurode in new_layer.get_my_neurodes():
                neurode.clear_and_add_input_nodes(self.current.get_my_neurodes())

        if new_layer.get_my_type() is LayerType.HIDDEN:
            for neurode in self.current.get_next().get_my_neurodes():
                neurode.clear_and_add_input_nodes(new_layer.get_my_neurodes())
            for neurode in new_layer.get_my_neurodes():
                neurode.clear_and_add_output_nodes(self.current.get_next().get_my_neurodes())
            for neurode in self.current.get_my_neurodes():
                neurode.clear_and_add_output_nodes(new_layer.get_my_neurodes())
            for neurode in new_layer.get_my_neurodes():
                neurode.clear_and_add_input_nodes(self.current.get_my_neurodes())

        super().insert_after_cur(new_layer)

    def remove_after_cur(self):
        for neurode in self.current.get_my_neurodes():
            neurode.clear_and_add_output_nodes(self.current.get_next().get_next().get_my_neurodes())
        for neurode in self.current.get_next().get_next().get_my_neurodes():
            neurode.clear_and_add_input_nodes(self.current.get_my_neurodes())
        super().remove_after_cur()

    def insert_hidden_layer(self, num_neurodes):
        hidden_layer = Layer(num_neurodes, LayerType.HIDDEN)
        if self.current.get_my_type() is LayerType.OUTPUT:
            raise NodePositionError
        self.insert_after_cur(hidden_layer)

    def remove_hidden_layer(self):
        if self.current is None or self.current is self.tail or self.current.get_next() is self.tail:
            raise NodePositionError
        else:
            self.remove_after_cur()

    def get_input_nodes(self):
        return self.head.get_my_neurodes()

    def get_output_nodes(self):
        return self.tail.get_my_neurodes()


"""
sys.path.extend(['/Users/michellehung/PycharmProjects/intermed software design python'])
PyDev console: starting.
Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 05:52:31) 
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)] on darwin
runfile('/Users/michellehung/PycharmProjects/intermed software design python/assignment8.py', 
wdir='/Users/michellehung/PycharmProjects/intermed software design python')
"""
def main():
    # create a LayerList with two inputs and four outputs
    my_list = LayerList(2, 4)
    # get a list of the input and output nodes, and make sure we have the right number
    inputs = my_list.get_input_nodes()
    outputs = my_list.get_output_nodes()
    assert len(inputs) == 2
    assert len(outputs) == 4
    # check that each has the right number of connections
    for node in inputs:
        assert len(node.output_nodes) == 4
    for node in outputs:
        assert len(node.input_nodes) == 2
    # check that the connections go to the right place
    for node in inputs:
        out_set = set(node.output_nodes)
        check_set = set(outputs)
        assert out_set == check_set
    for node in outputs:
        in_set = set(node.input_nodes)
        check_set = set(inputs)
        assert in_set == check_set
    # add a couple layers and check that they arrived in the right order, and that iterate and rev_iterate work
    my_list.reset_cur()
    my_list.insert_hidden_layer(3)
    my_list.insert_hidden_layer(6)
    assert my_list.current.get_layer_info() == (LayerType.INPUT, 2)
    my_list.iterate()
    assert my_list.current.get_layer_info() == (LayerType.HIDDEN, 6)
    my_list.iterate()
    assert my_list.current.get_layer_info() == (LayerType.HIDDEN, 3)
    # save this layer to make sure it gets properly removed later
    save_layer_for_later = my_list.current
    my_list.iterate()
    assert my_list.current.get_layer_info() == (LayerType.OUTPUT, 4)
    my_list.rev_iterate()
    assert my_list.current.get_layer_info() == (LayerType.HIDDEN, 3)
    # check that information flows through all layers
    save_vals = []
    for node in outputs:
        save_vals.append(node.get_value())
    for node in inputs:
        node.receive_input(None, 1)
    for i, node in enumerate(outputs):
        assert save_vals[i] != node.get_value()
    # check that information flows back as well
    save_vals = []
    for node in inputs[1].output_nodes:
        save_vals.append(node.get_delta())
    for node in outputs:
        node.receive_back_input(None, 1)
    for i, node in enumerate(inputs[1].output_nodes):
        assert save_vals[i] != node.get_delta()
    # try to remove an output layer
    try:
        my_list.remove_hidden_layer()
        assert False
    except NodePositionError:
        pass
    except:
        assert False
    # move and remove a hidden layer
    my_list.rev_iterate()
    my_list.remove_hidden_layer()
    # check the order of layers again
    my_list.reset_cur()
    assert my_list.current.get_layer_info() == (LayerType.INPUT, 2)
    my_list.iterate()
    assert my_list.current.get_layer_info() == (LayerType.HIDDEN, 6)
    my_list.iterate()
    assert my_list.current.get_layer_info() == (LayerType.OUTPUT, 4)
    my_list.rev_iterate()
    assert my_list.current.get_layer_info() == (LayerType.HIDDEN, 6)
    # save a value from the removed layer to make sure it doesn't get changed
    saved_val = save_layer_for_later.get_my_neurodes()[0].get_value()
    # check that information still flows through all layers
    save_vals = []
    for node in outputs:
        save_vals.append(node.get_value())
    for node in inputs:
        node.receive_input(None, 1)
    for i, node in enumerate(outputs):
        assert save_vals[i] != node.get_value()
    # check that information still flows back as well
    save_vals = []
    for node in inputs[1].output_nodes:
        save_vals.append(node.get_delta())
    for node in outputs:
        node.receive_back_input(None, 1)
    for i, node in enumerate(inputs[1].output_nodes):
        assert save_vals[i] != node.get_delta()
    assert saved_val == save_layer_for_later.get_my_neurodes()[0].get_value()
if __name__ == "__main__":
    main()