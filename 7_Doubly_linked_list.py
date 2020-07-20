"""

Assignment 7 :DoublyLinkedList

Chia Jui Hung

Create a doublyLinkedList

"""


class DLLNode:
    """Define single node in doublyLinkedList"""

    # initializer ("constructor") method ------------------------
    def __init__(self):
        # instance attributes
        self.next = None
        self.prev = None

    # list-support -------------------------------------------
    def set_prev(self, prev_node):
        self.prev = prev_node

    def get_prev(self):
        return self.prev

    def set_next(self, next_node):
        self.next = next_node

    def get_next(self):
        return self.next

    def __str__(self):
        return "(generic node)"


class DoublyLinkedList:
    """ Link the DLLnodes in forward and backward directions """

    # constructor ------------------------------------------------
    def __init__(self):
        self.head = None
        self.current = None
        self.tail = None

    # iterator mutators --------------------------------------------------
    def reset_cur(self):
        self.current = self.head
        return self.current

    def iterate(self):
        if self.current is None:
            return None
        self.current = self.current.get_next()

        return self.current

    def rev_iterate(self):
        self.current = self.current.get_prev()
        return self.current

    def add_to_head(self, new_node):
        if isinstance(new_node, DLLNode):
            new_node.set_next(self.head)
            if self.head is None:
                self.head = self.tail = new_node
            else:
                self.head.set_prev(new_node)
                self.head = new_node
                self.head.set_prev(None)

    def remove_from_head(self):
        ret_node = self.head
        if ret_node is not None:  # list is not empty
            self.head = ret_node.get_next()
            ret_node.set_next(None)
            if self.head is not None:  # list has more than one Node
                self.head.set_prev(None)
            else:  # list has only one Node
                self.tail = self.head
        else:  # list is empty
            self.is_empty()
        return ret_node

    def insert_after_cur(self, new_node):
        if isinstance(new_node, DLLNode) and self.current:
            new_node.set_next(self.current.get_next())
            if new_node.get_next() is not None:
                new_node.get_next().set_prev(new_node)
            new_node.set_prev(self.current)
            self.current.set_next(new_node)
            if new_node.get_next() is None:
                self.tail = new_node
            return True
        else:
            return False

    def remove_after_cur(self):
        if self.current is None or self.current.get_next() is None:
            return False
        elif self.current.get_next().get_next() is not None:
            self.current.set_next(self.current.get_next().get_next())
            self.current.get_next().set_prev(self.current)
            return True
        else:
            self.current.set_next(None)
            self.tail = self.current
            return True

    # accessors -------------------------------------------------
    def is_empty(self):
        return self.head is None


"""
Testing initial state of DoublyLinkedList
[<__main__.DLLNode object at 0x10fe24278>]
[<__main__.DLLNode object at 0x10fe24278>, <__main__.DLLNode object at 0x10fe242b0>]
[<__main__.DLLNode object at 0x10fe24278>, <__main__.DLLNode object at 0x10fe242b0>, 
<__main__.DLLNode object at 0x10fe242e8>]
[<__main__.DLLNode object at 0x10fe24278>, <__main__.DLLNode object at 0x10fe242b0>, 
<__main__.DLLNode object at 0x10fe242e8>, 
<__main__.DLLNode object at 0x10fe24320>]
[<__main__.DLLNode object at 0x10fe24278>, <__main__.DLLNode object at 0x10fe242b0>, 
<__main__.DLLNode object at 0x10fe242e8>, 
<__main__.DLLNode object at 0x10fe24320>, <__main__.DLLNode object at 0x10fe24358>]
Test add first node to head and reset current
Test add another node to head
Test insert after current (should add to tail)
Test reset and insert current
Test remove from head
Test iterate and rev_iterate
Test remove after cur, removing tail
Test remove after cur, nothing to remove
Test remove from head three times, last time should fail
"""