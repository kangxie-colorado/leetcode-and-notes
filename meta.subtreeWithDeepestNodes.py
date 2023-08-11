"""
seems like doing encoding would be a good idea
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def subtreeWithAllDeepest(self, root: TreeNode) -> TreeNode:
        encodings = []
        def encode(root, code):
            if not root:
                return
            
            encodings.append(code)
            encode(root.left, code+'0')
            encode(root.right, code+'1')
        
        encode(root, "1")
        maxDepth = 0
        deepestNodes = []

        for node in encodings:
            nodeDepth = len(node)-1
            if nodeDepth > maxDepth:
                maxDepth = nodeDepth
                deepestNodes = []
            
            if nodeDepth == maxDepth:
                deepestNodes.append(node)
            
        commonPrefix = deepestNodes[0]
        for i in range(1, len(deepestNodes)):
            if deepestNodes[i].startswith(commonPrefix):
                continue
            
            for idx in range(len(commonPrefix)):
                if commonPrefix[idx] != deepestNodes[i][idx]:
                    break
            commonPrefix = commonPrefix[:idx]
        
        curr = root 
        for step in commonPrefix[1:]:
            if step == '0':
                next = curr.left 
            else:
                next = curr.right
            curr = next 
        return curr
    
"""
Runtime: 35 ms, faster than 98.66% of Python3 online submissions for Smallest Subtree with all the Deepest Nodes.
Memory Usage: 16.5 MB, less than 79.46% of Python3 online submissions for Smallest Subtree with all the Deepest Nodes.


although I like my solution
but it is not very clean

the cleanest logic is 
https://leetcode.com/problems/smallest-subtree-with-all-the-deepest-nodes/discuss/146808/C%2B%2BJavaPython-One-Pass

if left depth == right depth,
deepest nodes both in the left and right subtree,
return pair (left.depth + 1, root)

if left depth > right depth,
deepest nodes only in the left subtree,
return pair (left.depth + 1, left subtree)

if left depth < right depth,
deepest nodes only in the right subtree,
return pair (right.depth + 1, right subtree)

yeah.. even no need to bookkeeping the number of depth.. just to know which one is deeper
let me do
"""

class Solution:
    def subtreeWithAllDeepest(self, root: TreeNode) -> TreeNode:
        
        def deep(root):
            if not root:
                return 0, None
            
            lDepth, lMinTree = deep(root.left)
            rDepth, rMinTree = deep(root.right)

            if lDepth > rDepth: return lDepth+1, lMinTree
            elif lDepth < rDepth: return rDepth+1, rMinTree
            else:
                return lDepth + 1, root 
        
        _, minTree = deep(root)
        return minTree

"""
Runtime: 34 ms, faster than 98.66% of Python3 online submissions for Smallest Subtree with all the Deepest Nodes.
Memory Usage: 16.6 MB, less than 51.82% of Python3 online submissions for Smallest Subtree with all the Deepest Nodes.

"""
                
if __name__ == '__main__':
    s = Solution()
    
    nodes = []
    for i in range(7):
      nodes.append(TreeNode(i))
    
    nodes[0].left = nodes[1]
    nodes[1].left = nodes[3]
    nodes[1].right = nodes[2]
    nodes[3].left = nodes[6]
    nodes[2].left = nodes[5]
    nodes[2].right = nodes[4]

    print(s.subtreeWithAllDeepest(nodes[0]))
    

