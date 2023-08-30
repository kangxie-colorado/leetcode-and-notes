# Definition for a binary tree node.
from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
class Solution:
    def lcaDeepestLeaves(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        
        parents = {}
        
        q = deque()
        q.append((root,0))
        nodes = []
        while q:
            node,dep = q.popleft()
            nodes.append((node,dep))
            if node.left:
                parents[node.left] = node
                q.append((node.left, dep+1))
            if node.right:
                parents[node.right] = node
                q.append((node.right, dep+1))
                
        depth = nodes[-1][1]
        lca = nodes[-1][0]
        
        def getLca(n1,n2):
            path = set([n1])
            while n1 in parents:
                path.add(parents[n1])
                n1 = parents[n1]
            
            while n2 not in path:
                n2 = parents[n2]
            
            return n2
        

        for idx in range(len(nodes)-2, -1, -1):
            node,dep = nodes[idx]
            if dep != depth:
                break
                
            lca = getLca(lca, node)
        return lca


if __name__ == "__main__":
    n2 = TreeNode(2, TreeNode(7), TreeNode(4))
    n5 = TreeNode(5, TreeNode(6), n2)
    n1 = TreeNode(1, TreeNode(0), TreeNode(8))
    n3 = TreeNode(3, n5, n1)

    s = Solution()
    s.lcaDeepestLeaves(n3)