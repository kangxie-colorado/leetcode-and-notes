import abc
from abc import ABC, abstractmethod
from typing import List
"""
This is the interface for the expression tree Node.
You should not remove it, and you can define some classes to implement it.
"""


class Node(ABC):
    @abstractmethod
    # define your fields here
    def evaluate(self) -> int:
        pass


class ExpressionTreeNode(Node):
    def __init__(self, val="", left=None, right=None) -> None:
        self.val = val
        self.left = left
        self.right = right 

    def evaluate(self):
        def f(root):
            if root.val.isdigit():
                return int(root.val)
            
            left = f(root.left)
            right = f(root.right)

            if root.val == '+':
                return left+right
            if root.val == '-':
                return left-right
            if root.val == '*':
                return left*right
            if root.val == '/':
                return left//right
        
        return f(self)


"""    
This is the TreeBuilder class.
You can treat it as the driver code that takes the postinfix input
and returns the expression tree represnting it as a Node.
"""


class TreeBuilder(object):
    def buildTree(self, postfix: List[str]) -> 'Node':
        
        stack = []
        for c in postfix:
            if c.isdigit():
                stack.append(ExpressionTreeNode(c))
            else:
                right = stack.pop()
                left = stack.pop()
                stack.append(ExpressionTreeNode(c, left, right))

        return stack[0]
                




"""
Your TreeBuilder object will be instantiated and called as such:
obj = TreeBuilder();
expTree = obj.buildTree(postfix);
ans = expTree.evaluate();
"""


"""
Runtime: 40 ms, faster than 82.90% of Python3 online submissions for Design an Expression Tree With Evaluate Function.
Memory Usage: 13.9 MB, less than 60.65% of Python3 online submissions for Design an Expression Tree With Evaluate Function.
"""