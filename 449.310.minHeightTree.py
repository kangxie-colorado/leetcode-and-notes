"""
https://leetcode.com/problems/minimum-height-trees/

start from any node see how many layer there are using bfs?
but I suspect it will TLE.. 

maybe some early termination is possible 
huh... give some try.. improve later

hmmm.. it is true every node can be root
but not every node can be leaf.. the leaf must be a node that has at most link (parentage link)

if it has two links.. then I cannot be leaf.. must be a internal node or root.. 

this idea is what I coded in 2017.. let me do above brute force first
then down to this one.. 
"""


from collections import defaultdict, deque
from typing import List


class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        graphs = defaultdict(set)
        for s,e in graphs:
            graphs[s].add(e)
            graphs[e].add(s)
        
        def maxDistance(root):
            # I am think that algorithm
            # which I keep relaxing the edges.. 
            # until it is optimial but think that is O(n**2)?
            # or I can do bfs and mark the visited nodes not to return 
            # but this is not directed graph.. so not so sure.. 
            # wait... that all nodes to all nodes distance can be computed as a matrix and 
            # that might give the answer already???
            # open up a new section to code that first
            ...
        # now I treat every node as root 
        # see how many layer I need to travel to reach all nodes
        res = []
        minHeight = n
        for root in range(1, n+1):
            ...

        return res


"""
want to see if I can pre-compute the shortest distance between every two nodes.. 
then I search the row to know its max 

this is going to be O(n**2) or O(n**3)?
but would be intresting to code it up
"""
class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        dist = [[n]*n for _ in range(n)]

        for i in range(n):
            dist[i][i] = 0
        for s,e in edges:
            dist[s][e] = 1
            dist[e][s] = 1
        
        candidates = defaultdict(list)
        minH = n
        for i in range(n):
            
            for j in range(n):
                for k in range(n):
                    dist[i][j] = min(dist[i][j], dist[i][k]+dist[k][j])
            rowMax = max(dist[i])
            candidates[rowMax].append(i)
            minH = min(minH, rowMax)
            
        # print(candidates)

        return candidates[minH]

"""
TLE 
33 / 71 test cases passed.


So coming back to think the solution that solves this by removing leaves layer by layer
basically, any node with only one link is a leaf 
then I think if the tree looks like 1->2->3 with 1 as root.. how can say 1 as leaf
well.. it should better be leaf and let 2 be root to minimize the height

so looking at that hint
 - How many MHTs can a graph have at most?

I didn't think of anything before but now I see
it can only be 1 or 2

a root has a bunch of subtrees
the height of tree is decided by the tallest subtree

if they are balanced... then that is likely the min height we can get
if subtree-A's height = subtree-B's height+2.. 
then there could be some way to balance it...

so I think the answer to that question is either 1 or 2.. 
but where does this lead to?

well.. it leads right back to removing leaves by layer!!!!

"""


class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if not edges:
            return [0]

        linksPerNode = defaultdict(int)
        graphs = defaultdict(set)

        for n1,n2 in edges:
            graphs[n1].add(n2)
            graphs[n2].add(n1)

            linksPerNode[n2] += 1
            linksPerNode[n1] += 1
        
        bfsQ = deque()
        for node, links in linksPerNode.items():
            if links == 1:
                bfsQ.append(node)
        
        removed = 0
        while bfsQ and n-removed>2:
            sz = len(bfsQ)
            while sz:
                node = bfsQ.popleft()
                removed += 1
                for nei in graphs[node]:
                    if linksPerNode[nei] > 1:
                        linksPerNode[nei] -= 1
                        if linksPerNode[nei] == 1:
                            bfsQ.append(nei)
                sz -= 1

        return list(bfsQ)

"""
Runtime: 1043 ms, faster than 35.40% of Python3 online submissions for Minimum Height Trees.
Memory Usage: 26.2 MB, less than 26.41% of Python3 online submissions for Minimum Height Trees.

the for loop can be written as this also
                for nei in graphs[node]:
                    linksPerNode[nei] -= 1
                    if linksPerNode[nei] == 1:
                        bfsQ.append(nei)
"""

if __name__ == '__main__':
    s = Solution()
    print(s.findMinHeightTrees(n=4, edges=[[1, 0], [1, 2], [1, 3]]))
    print(s.findMinHeightTrees(n=6, edges=[
          [3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]))

    n = 210
    a = [[0,1],[1,2],[0,3],[3,4],[4,5],[3,6],[6,7],[7,8],[0,9],[7,10],[6,11],[3,12],[5,13],[8,14],[7,15],[11,16],[12,17],[12,18],[18,19],[7,20],[8,21],[18,22],[7,23],[15,24],[21,25],[14,26],[11,27],[5,28],[15,29],[21,30],[12,31],[22,32],[1,33],[14,34],[14,35],[33,36],[14,37],[18,38],[19,39],[6,40],[29,41],[27,42],[25,43],[0,44],[26,45],[3,46],[1,47],[34,48],[26,49],[9,50],[34,51],[18,52],[41,53],[6,54],[25,55],[55,56],[47,57],[34,58],[58,59],[48,60],[24,61],[43,62],[51,63],[30,64],[24,65],[27,66],[30,67],[41,68],[64,69],[46,70],[49,71],[58,72],[43,73],[24,74],[43,75],[3,76],[32,77],[74,78],[31,79],[59,80],[25,81],[12,82],[26,83],[21,84],[35,85],[37,86],[39,87],[36,88],[67,89],[58,90],[22,91],[91,92],[56,93],[92,94],[3,95],[94,96],[89,97],[81,98],[6,99],[75,100],[56,101],[41,102],[68,103],[46,104],[3,105],[104,106],[56,107],[104,108],[83,109],[9,110],[0,111],[2,112],[53,113],[21,114],[76,115],[34,116],[26,117],[117,118],[116,119],[82,120],[27,121],[101,122],[8,123],[99,124],[79,125],[116,126],[53,127],[46,128],[116,129],[6,130],[46,131],[113,132],[25,133],[79,134],[38,135],[68,136],[116,137],[66,138],[56,139],[102,140],[36,141],[0,142],[126,143],[9,144],[36,145],[34,146],[140,147],[70,148],[117,149],[1,150],[5,151],[38,152],[48,153],[20,154],[145,155],[126,156],[54,157],[21,158],[155,159],[128,160],[34,161],[61,162],[72,163],[64,164],[144,165],[165,166],[60,167],[139,168],[85,169],[133,170],[60,171],[163,172],[120,173],[69,174],[21,175],[84,176],[24,177],[3,178],[131,179],[129,180],[35,181],[159,182],[31,183],[100,184],[110,185],[9,186],[6,187],[149,188],[141,189],[112,190],[22,191],[125,192],[174,193],[19,194],[156,195],[124,196],[88,197],[195,198],[187,199],[164,200],[179,201],[95,202],[48,203],[25,204],[53,205],[13,206],[127,207],[71,208],[119,209]]
    print(s.findMinHeightTrees(n=n,edges=a))