from utils.datastructures.LinkedList import LinkedList, LinkedListNode
import numpy as np

class SkipList:
    """

    Each node stores data (val, row)
    """

    def __init__(self, height : int, p : float):
        assert height>0
        self.p = p
        self.height = height
        self.structure = LinkedList()
        self.VAL, self.ROW = 0, 1
        self.INF = 1e16
        self.left_col, self.right_col = self.init_first_and_last_cols()
        self.structure.set_head(self.left_col[0])
        self.num_vals = 0
        self.num_elts = 0

    def get_num_vals(self):
        return self.num_vals

    def get_num_elts(self):
        return self.num_elts

    def init_node(self, val, row):
        return LinkedListNode((val, row))


    def init_first_and_last_cols(self):
        #left most column of data structure should consist of nodes
        #storing value -self.INF
        left_col = [self.init_node(-self.INF, i) for i in range(self.height)]
        for (a,b) in zip(left_col[:-1],left_col[1:]):
            self.attach_rows([a],[b])

        #right most column should consist of all nodes
        #holding value inf
        right_col = [self.init_node(self.INF, i) for i in range(self.height)]
        for (a,b) in zip(right_col[:-1],right_col[1:]):
            self.attach_rows([a],[b])

        self.attach_columns(left_col, right_col)

        return left_col, right_col


    def attach_rows(self, above_row, below_row):
        """
        given two lists of LinkedListNodes (left_row, and right_row)
        attaches the two rows
        so that the ith node on the top points down to the ith node
        on the right and vise versa

        :param above_row: a list of LinkedListNodes
        :param below_row: a list of LinkedListNodes
        :return:
        """
        #TODO
        assert len(above_row) == len(below_row)
        pass

    def attach_columns(self, left_col, right_col):
        """
        given two lists of LinkedListNodes (left_col, and right_col)
        attaches the two columns
        so that the ith node on the left points right to the ith node
        on the left, and vise versa

        :param left_col: a list of LinkedListNodes
        :param right_col: a list of LinkedListNodes
        :return:
        """
        assert len(left_col) == len(right_col)
        #TODO
        pass



    def row_insert(self, node : LinkedListNode, left : LinkedListNode):
        """
        inserts node to the right of node left
        :param to_insert: the node to insert
        :param node_left: the ode we are inserting to the left of
        :return: the node being inserted
        """
        #TODO

    def row_delete(self, node):
        assert node.has_left() and node.has_right()
        left, right = node.get_left(), node.get_right()
        left.set_right(right)
        right.set_left(left)
        return node

    def get_val(self, node : LinkedListNode):
        return node.get_data()[self.VAL]

    def search(self, val):
        """
        searches for the value val in the data_structure
        and, returns the largest value node in each row who's
        value is smaller than val.

        :param val:
        :return: NONE
        """
        row_nodes = []
        curr_node = self.structure.get_head()
        curr_row = 0
        while curr_row < self.height:
            #traverse down a layer and update the row_nodes
            #we traversed down on
            if self.get_val(curr_node.get_right()) > val:
                #TODO
                pass
            else:
                curr_node = curr_node.get_right()
        assert len(row_nodes) == self.height
        return row_nodes



    def add(self, val):
        # search for the positions where the value would be inserted in each row
        # search for the positions where the value would be inserted in each row
        insertion_points = self.search(val)
        if val == self.get_val(insertion_points[-1]):
            return
        self.num_vals += 1
        # add a new node in the bottom - most row with this value
        below_node = None
        for i in range(1, self.height + 1):
            curr_row = self.height - i
            left = insertion_points[-i]
            node = self.init_node(val, curr_row)
            #TODO : insert node at correct sot in this level

            if below_node is not None:
                self.attach_rows([node], [below_node])
            below_node = node
            # update the number of elements in the data structure
            self.num_elts += 1
            if np.random.uniform() > self.p:
                break
        pass


    def remove(self, val):
        #TODO : remove all nodes with value equal to val
        pass

    def find(self, val):
        row_nodes = self.search(val)
        if self.get_val(row_nodes[-1]) == val:
            return row_nodes[-1]
        return None

    def contains(self, val):
        return self.find(val) is not None







