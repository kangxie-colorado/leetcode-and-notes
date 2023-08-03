"""
https://leetcode.com/problems/largest-color-value-in-a-directed-graph/?envType=study-plan&id=graph-ii

I am not sure I fully understand this problem
but I think it is asking for the most freqeunt color on a valid path.. 

I could use topo sort... and pass the counter around?
"""


from collections import Counter, defaultdict, deque
from typing import List


class Solution:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        graphs = defaultdict(set)
        incomingLinks  = [0] * len(colors)

        for s,e in edges:
            graphs[s].add(e)
            incomingLinks[e] += 1
        
        bfsQ = deque()
        for i in incomingLinks:
            if incomingLinks[i] == 0:
                bfsQ.append((i, {colors[i]:1} ))

        while bfsQ:
            sz = len(bfsQ)
            while sz:
                node, colorCount = bfsQ.popleft()        

                for nextNode in graphs[node]:
                    # okay.. bumm.. 
                    # what if a node has two parents... 
                    # would be hard to deal with that
                    # so looks like the better way is to dfs 
                    # looking forward from this node and see what most color I can be on
                    ...
                sz-=1
        return -1


""""
let ms see the dfs 
"""
        

class Solution:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        graphs = defaultdict(set)
        for s, e in edges:
            graphs[s].add(e)
        
        status = [0] * len(colors)

        def color(i):
            # from n forward.. the color distribution
            # how to do it? still pretty hard to deal with the path and invoking order
            # hmm.. to do that.. looks like I need to start from the leafs.. 
            # i.e. the nodes without outgoing links... 
            # interesting... back to bfs
            ...
        return None
        

class Solution:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        graphs = defaultdict(set)
        outgoingLinks = [0] * len(colors)

        for s, e in edges:
            graphs[e].add(s)
            outgoingLinks[s] += 1

        bfsQ = deque()
        colorCounterPerNode = defaultdict(dict)
        for i,link in enumerate(outgoingLinks):
            colorCounterPerNode[i] = {colors[i]: 1}
            if link == 0:
                bfsQ.append((i))
                

        connectedNodes = set()
        res = 0
        while bfsQ:
            sz = len(bfsQ)
            while sz:
                node = bfsQ.popleft()
                for nextNode in graphs[node]:
                    for color, cnt in colorCounterPerNode[node].items():
                        if color not in colorCounterPerNode[nextNode]:
                            colorCounterPerNode[nextNode][color] = 0
                        colorCounterPerNode[nextNode][color] += cnt
                        res = max(res, colorCounterPerNode[nextNode][color])
                    
                    outgoingLinks[nextNode] -= 1
                    if outgoingLinks[nextNode] == 0:
                        bfsQ.append(nextNode)
            
                connectedNodes.add(node)
                sz -= 1
        
        if len(connectedNodes) != len(colors):
            return -1
        return res

"""
didn't get too far
"hhqhuqhqff"
[[0,1],[0,2],[2,3],[3,4],[3,5],[5,6],[2,7],[6,7],[7,8],[3,8],[5,8],[8,9],[3,9],[6,9]]

there are 5* double counting... 
so instead of merge counter.. let me just maintain the merge set
and merge them when pop...
"""


class Solution:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        graphs = defaultdict(set)
        outgoingLinks = [0] * len(colors)

        for s, e in edges:
            graphs[e].add(s)
            outgoingLinks[s] += 1

        bfsQ = deque()
        mergeSetsPerNode = defaultdict(set)
        for i, link in enumerate(outgoingLinks):
            mergeSetsPerNode[i].add(i)
            if link == 0:
                bfsQ.append((i))

        connectedNodes = set()
        res = 0
        while bfsQ:
            sz = len(bfsQ)
            while sz:
                node = bfsQ.popleft()
                # count? TLE for sure!
                # but whatever
                counter = defaultdict(int)
                for merge in mergeSetsPerNode[node]:
                    counter[colors[merge]] += 1
                    res = max(res, counter[colors[merge]])

                for nextNode in graphs[node]:
                    mergeSetsPerNode[nextNode].add(node)
                    outgoingLinks[nextNode] -= 1
                    if outgoingLinks[nextNode] == 0:
                        bfsQ.append(nextNode)

                connectedNodes.add(node)
                sz -= 1

        if len(connectedNodes) != len(colors):
            return -1
        return res


"""
I don't know if it is my ability or my capacity or my floating status
but this is dead wrong.. 

you can pass the state twice over
but I can do that by only making this chagne
                    mergeSetsPerNode[nextNode].union(mergeSetsPerNode[node])
                from 
                    mergeSetsPerNode[nextNode].add(node)

and I cna also only do the counting when there is no next node.. 
"""


class Solution:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        graphs = defaultdict(set)
        outgoingLinks = [0] * len(colors)

        for s, e in edges:
            graphs[e].add(s)
            outgoingLinks[s] += 1

        bfsQ = deque()
        mergeSetsPerNode = defaultdict(set)
        for i, link in enumerate(outgoingLinks):
            mergeSetsPerNode[i].add(i)
            if link == 0:
                bfsQ.append((i))

        connectedNodes = set()
        res = 0
        while bfsQ:
            sz = len(bfsQ)
            while sz:
                node = bfsQ.popleft()

                if not graphs[node]:
                    # count? TLE for sure!
                    # but whatever
                    counter = defaultdict(int)
                    for merge in mergeSetsPerNode[node]:
                        counter[colors[merge]] += 1
                        res = max(res, counter[colors[merge]])

                for nextNode in graphs[node]:
                    mergeSetsPerNode[nextNode] = mergeSetsPerNode[nextNode].union(mergeSetsPerNode[node])
                    outgoingLinks[nextNode] -= 1
                    if outgoingLinks[nextNode] == 0:
                        bfsQ.append(nextNode)

                connectedNodes.add(node)
                sz -= 1

        if len(connectedNodes) != len(colors):
            return -1
        return res

""""
hahaha.. 
but now then I merged all the routes back to the root.
it carries more than one routes' information ---- dead wrong


okay.. bfs I kind of confusing now..
I want to do dfs first... 

when it reach the end.. update the counter.. maintain a path
and path can be used for detecting cycle

where to start... start with incoming links=0 maybe a few of them

but that's okay..
If I can cache some.. that be better... 

now focus on interview...
"""


class Solution:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        if not edges:
            return 1

        graphs = defaultdict(set)
        incomingLinks = [0] * len(colors)

        for s, e in edges:
            graphs[s].add(e)
            incomingLinks[e] += 1

        starters = []
        for i,link in enumerate(incomingLinks):
            if link == 0:
                starters.append(i)
        
        res = 0
        maxColors = {}
        # sometimes I tied myself to think I have to cache on both arguments
        # but why cannot I cache on only one?
        def f(node, path):
            if node in maxColors:
                # return what? a maxColor.. but it could be useless on a different path
                # anyway.. let me get the no cache code up first
                return True
            if node in path:
                return False
            
            # reach to a leaf: maintain the res 
            if not graphs[node]:
                nonlocal res
                C = Counter()
                C[colors[node]] += 1
                for n in path:
                    C[colors[n]] += 1
                    res = max(res, C[colors[n]])
                

            for nextNode in graphs[node]:
                if not f(nextNode, path.union({node})):
                    return False
            
            return True

        if not starters:
            return -1
        
        for starter in starters:
            if not f(starter, set()):
                return -1
        return res


"""
have to deal with so many edge cases..?
not a good sign..

TLE after 40 / 83 test cases passed.

"""


class Solution:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        if not edges:
            return 1

        graphs = defaultdict(set)
        incomingLinks = [0] * len(colors)

        for s, e in edges:
            graphs[s].add(e)
            incomingLinks[e] += 1

        starters = []
        for i, link in enumerate(incomingLinks):
            if link == 0:
                starters.append(i)

        # sometimes I tied myself to think I have to cache on both arguments
        # but why cannot I cache on only one?
        nodeColorCounter = defaultdict(dict)
        def f(node, path):
            if node in nodeColorCounter:
                # return what? a maxColor.. but it could be useless on a different path
                # anyway.. let me get the no cache code up first
                return nodeColorCounter[node]
            if node in path:
                return None 

            # reach to a leaf: maintain the res
            if not graphs[node]:
                nodeColorCounter[node][colors[node]] = 1
                return nodeColorCounter[node]

            for nextNode in graphs[node]:
                # huh.. if this node has several sub-trees..
                # how can I maint it???????????
                # fuck.. this problem is probably my blind spot>?
                if not f(nextNode, path.union({node})):
                    return False

            return True

        if not starters:
            return -1

        for starter in starters:
            if not f(starter, set()):
                return -1
        return None

"""
hints:

- Use topological sort.
- let dp[u][c] := the maximum count of vertices with color c of any path starting from vertex u. (by JerryJin2905)

okay.. I missed one dimension
I feel I need a big break 

the hint is genius... 
it is kind of a dfs thoughts.. (maybe that is my feeling)

but then I can bottom up.. which would easier
starting from leaves.. and their color map is easy..

then up/up/ and maintain a biggest value

meantime, topo sort can detect cycle
"""


class Solution:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        dp = {} # {(u,c):integer }
        uniqColors = set(colors)
        for u in range(len(colors)):
            for c in uniqColors:
                dp[u,c] = 0
                if colors[u] == c:
                    dp[u,c] = 1
        # if not edges:
        #     return 1

        graphs = defaultdict(set)
        incomingLinks = [0] * len(colors)

        for s, e in edges:
            # going to parent node 
            graphs[e].add(s)
            incomingLinks[e] += 1

        bfsQ = deque()
        for node,link in enumerate(incomingLinks):
            if link == 0:
                bfsQ.append(node)
            
        while bfsQ:
            sz = len(bfsQ)
            while sz:
                node = bfsQ.popleft()

                for pNode in graphs[node]:
                    # merge node's dp into pNode
                    for c in uniqColors:
                        dp[pNode][c] += dp[node][c]

                sz-=1

        return None

"""
bumm.. it has to be my mental energy quality today
this is a deadend again...

dfs.. 
"""


class Solution:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        dp = {}  # {(u,c):integer }
        uniqColors = set(colors)
        for u in range(len(colors)):
            for c in uniqColors:
                dp[u, c] = 0
                if colors[u] == c:
                    dp[u, c] = 1
            # an extra row to record if this node has been processed
            # 1: in path
            # 2: processed
            dp[u,26] = 0 
        # if not edges:
        #     return 1

        graphs = defaultdict(set)
        incomingLinks = [0] * len(colors)

        for s, e in edges:
            # going to parent node
            graphs[s].add(e)
            incomingLinks[e] += 1
        
        starters = []
        for node,link in enumerate(incomingLinks):
            if link==0:
                starters.append(node)
        
        res = 0
        processedNodes = set()
        def dfs(node):
            if dp[node,26] == 2:
                return True
            if dp[node,26] == 1:
                # cycle detected
                return False 
            
            dp[node,26] = 1
            subDp = {
                c:0 for c in uniqColors
            }
            for nextNode in graphs[node]:
                if not dfs(nextNode):
                    return False
                for c in uniqColors:
                    subDp[c] = max(subDp[c], dp[nextNode, c])
            for c in uniqColors:
                nonlocal res
                dp[node,c] += subDp[c]
                res = max(res, dp[node, c])
            dp[node, 26] = 2
            processedNodes.add(node)
            return True
        
        if not starters:
            # simply a loop
            return -1

        for starter in starters:
            if not dfs(starter):
                # some internal loop
                return -1

        if len(processedNodes) != len(colors):
            # disconnected components and some of them are a loop
            return -1

        return res


"""
82/83 passed
"aaa"
[[1,2],[2,1]]

this has no starter.. 
okay... 
this is a separate graph

so many edge cases.. 
ok.. processed keeping track

Runtime: 2579 ms, faster than 77.14% of Python3 online submissions for Largest Color Value in a Directed Graph.
Memory Usage: 230.4 MB, less than 5.71% of Python3 online submissions for Largest Color Value in a Directed Graph.



"""


class Solution:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        dp = {}  # {(u,c):integer }
        uniqColors = set(colors)
        for u in range(len(colors)):
            for c in uniqColors:
                dp[u, c] = 0
                if colors[u] == c:
                    dp[u, c] = 1

        graphs = defaultdict(set)
        incomingLinks = [0] * len(colors)

        for s, e in edges:
            # going to parent node
            graphs[s].add(e)
            incomingLinks[e] += 1

        starters = []
        for node, link in enumerate(incomingLinks):
            if link == 0:
                starters.append(node)

        res = 0
        processedNodes = set()

        def dfs(node, path):
            if node in processedNodes:
                return True
            if node in path:
                return False

            subDp = {
                c: 0 for c in uniqColors
            }
            path.add(node)
            for nextNode in graphs[node]:
                if not dfs(nextNode, path):
                    return False
                for c in uniqColors:
                    subDp[c] = max(subDp[c], dp[nextNode, c])
            path.remove(node)
            for c in uniqColors:
                nonlocal res
                dp[node, c] += subDp[c]
                res = max(res, dp[node, c])
            processedNodes.add(node)
            return True

        if not starters:
            # simply a loop
            return -1

        for starter in starters:
            if not dfs(starter, set()):
                # some internal loop
                return -1

        if len(processedNodes) != len(colors):
            # disconnected components and some of them are a loop
            return -1

        return res


"""
okay.. this TLE.. 
that set copy is kind of hard 

change to back track ..

Runtime: 2556 ms, faster than 77.86% of Python3 online submissions for Largest Color Value in a Directed Graph.
Memory Usage: 217.7 MB, less than 5.71% of Python3 online submissions for Largest Color Value in a Directed Graph.
"""

"""
I was struggling with the bfs..
even when I figured out the memorization+dp+dfs solution I still find it hard to come up with the bfs route

reaeding this https://leetcode.com/problems/largest-color-value-in-a-directed-graph/discuss/1198658/C%2B%2B-Topological-Sort
it seems clear to me now

I can start with the starters.. and forwards
but again... I am lost.. if different routes are different length
how can you decide.. 

ah.. when each route reachs a node.. just update (the pre dp[26] with that node's color)
then another route reachs.. also do the same update... (the pre dp[26] with that node's color...)

yeah... so yesterday I was too low on energy I even didn't figure out this 
"""


class Solution:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        n = len(colors)
        # for each node, save: up to this node(from a starter), the max count of each color
        # do I need to initialize it?
        # maybe I can do that in later compution 
        # or I can padding a dp[0] with full 0 and then dynamically compute later
        # but notice this will shift the index by 1
        dp = [[0]*26 for _ in range(n+1)]
        
        # establish the graph
        graph = defaultdict(set)
        incomingLinks = [0]*(n+1)
        for s,e in edges:
            graph[s+1].add(e+1)
            incomingLinks[e+1] += 1
        
        # I start with a virtual node 0
        # the node-0 will be become node-1 (idx shift)
        for node,links in enumerate(incomingLinks):
            if links == 0 and node:
                incomingLinks[node] = 1
                graph[0].add(node)

        bfsQ = deque([0])
        processed = set()
        res = 0
        while bfsQ:
            sz = len(bfsQ)
            while sz:
                node = bfsQ.popleft()
                processed.add(node)

                for nextNode in graph[node]:
                    for c in range(26):
                        nextNodeColor = ord(colors[nextNode-1]) - ord('a')
                        if c != nextNodeColor:
                            dp[nextNode][c] = max(dp[nextNode][c], dp[node][c])
                        else:
                            dp[nextNode][c] = max(dp[nextNode][c], dp[node][c]+1)
                        res = max(res, dp[nextNode][c])

                    incomingLinks[nextNode] -=1 
                    if incomingLinks[nextNode] == 0:
                        bfsQ.append(nextNode)

                sz-=1
        
        if len(processed) == n+1:
            return res
        return -1

"""
Runtime: 4535 ms, faster than 29.28% of Python3 online submissions for Largest Color Value in a Directed Graph.
Memory Usage: 105.2 MB, less than 44.28% of Python3 online submissions for Largest Color Value in a Directed Graph.

"""
if __name__ == "__main__":
    s = Solution()

    print(s.largestPathValue(colors="abaca",
          edges=[[0, 1], [0, 2], [2, 3], [3, 4]]))

    print(s.largestPathValue(colors="aaa",edges=[[1, 2], [2, 1]]))


    print(s.largestPathValue(colors='a', edges=[[0,0]]))


    print(s.largestPathValue(colors="hhqhuqhqff",
          edges=[[0,1],[0,2],[2,3],[3,4],[3,5],[5,6],[2,7],[6,7],[7,8],[3,8],[5,8],[8,9],[3,9],[6,9]]))


    colors = "qddqqqddqqdqddddddqdqqddddqdqdqqdddqddqdqqdqqqqqddqddqqddqqqdqqqqdqdddddqdq"
    edges = [[0,1],[1,2],[2,3],[3,4],[3,5],[4,5],[3,6],[5,6],[6,7],[5,7],[3,7],[6,8],[5,8],[4,8],[8,9],[9,10],[10,11],[9,11],[9,12],[11,12],[6,12],[11,13],[9,13],[13,14],[12,14],[10,14],[11,14],[13,15],[14,15],[12,16],[9,16],[7,16],[15,17],[13,17],[17,18],[11,18],[17,19],[18,19],[13,19],[17,20],[18,20],[19,21],[17,21],[12,22],[21,22],[16,22],[22,23],[21,23],[16,24],[22,24],[15,25],[24,25],[20,25],[12,25],[23,26],[26,27],[13,27],[27,28],[21,28],[26,28],[28,29],[15,30],[27,30],[24,30],[21,30],[27,31],[30,31],[25,32],[29,32],[17,33],[31,33],[32,33],[25,34],[33,35],[31,35],[34,35],[30,36],[35,37],[36,37],[26,38],[36,38],[34,38],[37,38],[38,39],[22,39],[39,40],[40,41],[38,41],[20,41],[41,42],[37,42],[40,43],[42,43],[43,44],[41,44],[32,44],[38,44],[39,44],[43,45],[44,45],[44,46],[45,46],[45,47],[42,47],[43,48],[45,49],[45,50],[48,51],[30,51],[46,52],[48,52],[38,52],[51,52],[47,53],[45,53],[53,54],[48,54],[30,54],[50,55],[30,55],[36,55],[55,56],[39,56],[54,56],[50,57],[56,58],[32,58],[57,59],[49,59],[38,60],[60,61],[35,61],[54,61],[53,61],[54,62],[58,62],[62,63],[40,63],[58,63],[49,64],[63,64],[47,64],[39,64],[45,64],[62,65],[64,65],[54,65],[52,66],[61,66],[60,66],[55,67],[65,67],[45,68],[56,68],[36,68],[67,69],[66,69],[27,70],[60,70],[67,70],[48,71],[70,71],[53,71],[62,72],[72,73],[73,74]]
    print(s.largestPathValue(colors, edges))

