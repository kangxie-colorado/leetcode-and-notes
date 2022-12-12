class Node:
    def __init__(self, data):
        self.data = data
        self.left_node = None
        self.right_node = None


def Morris(root):
    # Set current to root of binary tree
    curr = root

    while(curr is not None):

        if curr.left_node is None:
            print(curr.data)
            curr = curr.right_node
        else:
            # Find the previous (prev) of curr
            prev = curr.left_node
            while(prev.right_node is not None and prev.right_node != curr):
                prev = prev.right_node

            # Make curr as right child of its prev
            if(prev.right_node is None):
                prev.right_node = curr
                curr = curr.left_node

            # fix the right child of prev
            else:
                prev.right_node = None
                print(curr.data)
                curr = curr.right_node


root = Node(4)
root.left_node = Node(2)
root.right_node = Node(5)
root.left_node.left_node = Node(1)
root.left_node.right_node = Node(3)

Morris(root)
