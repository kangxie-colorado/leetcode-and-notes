"""
hmm.. 

going left, colum - 1
going right, column + 1

top to bottomw
so I just maintain the column lists 

and traversal top to bottom, in pre-order 

"""

# Definition for a binary tree node.
from collections import defaultdict, deque
import queue
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def verticalOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        cols = defaultdict(list)

        def f(root, col, row):
            if not root:
                return
            
            cols[col].append[(row, root.val)]
            f(root.left, col-1, row+1)
            f(root.right, col+1, row+1)
        
        f(root,0,0)
        res = []
        for key in sorted(list(cols.keys())):
            # can only sort by key-0,
            # cannot sort by global order.. otherwise, the order could get destroyed
            row_col = sorted(cols[key], key=lambda x: x[0])
            cols_sorted_by_row = [col for _,col in row_col]
            res.append(cols_sorted_by_row)
        
        return res

"""
okay.. I am not ranking high enough
take a break

review these two mediums.. 

ah.. I see. I am doing dfs, so thats why I have to deal with the row order
if I do bfs.. using queue.. it will be naturally, processed/sorted by row 

let me write in bfs
"""


class Solution:
    def verticalOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        
        cols = defaultdict(list)
        queue = deque()
        queue.append((root, 0))

        while queue:
            node, col = queue.popleft()
            if not node:
                continue
                
            cols[col].append(node.val)
            queue.append((node.left, col-1))
            queue.append((node.right, col+1))
        
        return [cols[col] for col in sorted(cols.keys())]

"""
Runtime: 46 ms, faster than 70.89% of Python3 online submissions for Binary Tree Vertical Order Traversal.
Memory Usage: 16.4 MB, less than 59.74% of Python3 online submissions for Binary Tree Vertical Order Traversal.
"""

if __name__ == '__main__':
    root = TreeNode(3, 
                    left=TreeNode(9),
                    right=TreeNode(20,
                                   left=TreeNode(15),
                                   right=TreeNode(7)))
  
    print(Solution().verticalOrder(root))