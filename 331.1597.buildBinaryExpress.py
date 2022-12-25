"""
https://leetcode.com/problems/build-binary-expression-tree-from-infix-expression/?envType=study-plan&id=programming-skills-iii

maybe I can use same idea

1. add a pair of () to generilize this
2. still evaluate the layer by layer
3. each layer reduces to a node.. instead of a number
4. for a flat layer.. +- ?
    - */ will need to form front/end into a tree
    - +- can wait until the last 

if should be very fun to code it up.. even I fail

"""

# Definition for a binary tree node.
class Node(object):
    def __init__(self, val=" ", left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    def __repr__(self) -> str:
        return f"Node(val={self.val}, left={self.left}, right={self.right})"

def myEval(run):
    # return a Node object
    nodes = []
    op = '+'
    for c in run:
        if c in '*/+-':
            op = c
        else:
            if op in '*/':
                leftNode = nodes.pop()
                rightNode = Node(c) 
                nodes.append( Node(op, leftNode, rightNode) )
            else:
                if nodes:
                    # for + and -, just record it in the stack and 
                    # will do a final run up 
                    # at first digit, it will be op +... but no need to appeped that
                    # so if stack test is used here
                    nodes.append(Node(op))
                nodes.append(Node(c))

    def buildTree_wrong(nodes, l, r):
        # it must be odd number size 
        # e.g. [node(1), node(-), node(*, node(2), node(3))]
        # so I can build in half/half fathion
        # WRONG! 1+6-5+8 will be built as 
        # Node(val=-, left=Node(val=+, left=Node(val=1, left=None, right=None), right=Node(val=6, left=None, right=None)), right=Node(val=+, left=Node(val=5, left=None, right=None), right=Node(val=8, left=None, right=None)))
        # must do this sequentially.. actually from right to left
        if l==r:
            return nodes[l]
        m = l + (r-l)//2
        if nodes[m].val not in '+-':
            m += 1
        root = nodes[m]
        root.left = buildTree(nodes, l, m-1)
        root.right = buildTree(nodes, m+1, r)
        return root
    
    def buildTree(nodes):
        if len(nodes) == 1:
            return nodes[0]
        root = nodes[-2]
        root.left = buildTree(nodes[:-2])
        root.right = nodes[-1]

        return root
    
    return buildTree(nodes)
        

class Solution:
    def expTree(self, s: str) -> 'Node':
        def myEval(run):
            # return a Node object
            print(f"run is {run}")
            nodes = []
            op = '+'
            for node in run:
                if node.val in '*/+-' and node.left is None and node.right is None:
                    # need to test node.left is None and node.right is Noone
                    # because the child layer operator cannot be treated as operator in this layer
                    # like 3/(5*2), the (5*2) will become a operand node.. not a operator node
                    op = node.val
                else:
                    if op in '*/':
                        leftNode = nodes.pop()
                        rightNode = node
                        nodes.append(Node(op, leftNode, rightNode))
                    else:
                        if nodes:
                            # for + and -, just record it in the stack and
                            # will do a final run up
                            # at first digit, it will be op +... but no need to appeped that
                            # so if stack test is used here
                            nodes.append(Node(op))
                        nodes.append(node)

            def buildTree(nodes):
                if len(nodes) == 1:
                    return nodes[0]
                root = nodes[-2]
                root.left = buildTree(nodes[:-2])
                root.right = nodes[-1]

                return root

            return buildTree(nodes)

        curr = []
        stack = [curr]
        for c in s:
            if c == '(':
                curr = []
                stack.append(curr)
            elif c == ')':
                node = myEval(stack.pop())
                if stack:
                    curr = stack[-1]
                    curr.append(node)
            else:
                assert c.isdigit() or c in '+-*/'
                curr.append(Node(c))

        return myEval(curr)

"""
Runtime: 31 ms, faster than 98.54% of Python3 online submissions for Build Binary Expression Tree From Infix Expression.
Memory Usage: 14 MB, less than 32.85% of Python3 online submissions for Build Binary Expression Tree From Infix Expression.
"""


if __name__ == '__main__':
    # S = Solution()
    # print(S.expTree("2-3/(5*2)+1"))
    print(myEval("1+2-3+4"))