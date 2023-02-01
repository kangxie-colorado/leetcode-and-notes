"""
https://leetcode.com/problems/sort-items-by-groups-respecting-dependencies/?envType=study-plan&id=graph-ii

interesting and complicated problem

so a group should appear together.. 
the items belong to no group can just go to the end in any order

for groups.. the before array definded their topo order
if there is a cycle dependency then no result

let me see
    1. group them, group 0/1.. can be the group array's index 
        in this iteration, record non-grouped element.. put them into an array
    2. go thru the before array, establist the topo relation
    3. run topo sort.. bfs.. see if the topo order can be establised.. and maintain the order
        if not, return []
        if yes, expand the group to final results..
        within a group there can relationship as well... need to sort that too but with group

so basically, two sorts? 
    huh.. how about I sort it by before relationship and check if some other groups interleaved
    because non-group can be in the before relationship....
    maybe this is better

    let me try
"""

from collections import defaultdict, deque
from typing import Deque, List


class Solution:
    def sortItems(self, n: int, m: int, group: List[int], beforeItems: List[List[int]]) -> List[int]:
        withGroup = defaultdict(set)
        nonGroupId = m

        for i,g in enumerate(group):
            if g==-1:                
                group[i] = nonGroupId
                withGroup[nonGroupId].add(i)
                nonGroupId += 1
            else:
                withGroup[g].add(i)
        
        # establish the graph 
        # what if two elements belonging to two groups are same topo-order 
        # they can be written in two ways: one way makes interleave... one way doesn't...
        # so when I decide the sort order, I still should use group relationship...?
        # and I can give the nonGroup a bigger group
        # so this then becomes sorting groups.. 
        # yeah, I guess so.. complicated.. careful coding 
        # do and think
        incomingLinks = {
            grp:0 for grp in withGroup
        }
        interGrpGraph = defaultdict(set)
        relatedGrps = set()  # use this to see if the connections are full (cycle detection)
        withinGrpGraph = defaultdict(set)
        for i, deps in enumerate(beforeItems):
            for dep in deps:
                grpI, grpDep = group[i], group[dep]
                if grpDep == grpI:
                    withinGrpGraph[dep].add(i)
                else:
                    interGrpGraph[grpDep].add(grpI)
                    incomingLinks[grpI] += 1
                    relatedGrps.add(grpI)
                    relatedGrps.add(grpDep)
        
        bfsQ = deque()
        for grp,link in incomingLinks.items():
            if grp in relatedGrps and link == 0:
                bfsQ.append(grp)
        
        connectedGrps = []
        while bfsQ:
            sz = len(bfsQ)
            while sz:
                grp = bfsQ.popleft()
                for nextGrp in interGrpGraph[grp]:
                    incomingLinks[nextGrp] -= 1
                    if incomingLinks[nextGrp] == 0:
                        bfsQ.append(nextGrp)
                connectedGrps.append(grp)
                sz-=1
        
        if len(connectedGrps) != len(relatedGrps):
            return []
        
        def topoSortGrp(items):
                # using information in withinGrpGraphs
            incomingLinks = {
                item: 0 for item in items
            }
            for val in items:
                if val in withinGrpGraph:
                    for depender in withinGrpGraph[val]:
                        incomingLinks[depender] += 1

            bfsQ = deque()
            for item, link in incomingLinks.items():
                if link == 0:
                    bfsQ.append(item)

            res = []
            while bfsQ:
                sz = len(bfsQ)
                while sz:
                    item = bfsQ.popleft()
                    for nextItem in withinGrpGraph[item]:
                        incomingLinks[nextItem] -= 1
                        if incomingLinks[nextItem] == 0:
                            bfsQ.append(nextItem)
                    res.append(item)
                    sz -= 1

            if len(res) != len(items):
                return None
            return res


        
        # now all the related groups are topo-sorted.. 
        # output them and deal with non-groups.. 
        res = []
        for cGrp in connectedGrps:
            items = topoSortGrp(withGroup[cGrp])
            if not items:
                return None
            res.extend(items)
        

        for grp,items in withGroup.items():
            # topo sort within each group
            items = topoSortGrp(items)
            if not items:
                return None
            if grp not in connectedGrps:
                res.extend(list(items))
        return res



# try to refactor to clean up some code before debugging
class Solution:
    def sortItems(self, n: int, m: int, group: List[int], beforeItems: List[List[int]]) -> List[int]:
        withGroup = defaultdict(set)
        nonGroupId = m

        for i, g in enumerate(group):
            if g == -1:
                group[i] = nonGroupId
                withGroup[nonGroupId].add(i)
                nonGroupId += 1
            else:
                withGroup[g].add(i)

        def topoSort(items, graph):
            # try to make this a reusable function for both inter-intra grp sort
            # items will be the set of related grps or items
            # graph is their dependency relationship
            incomingLinks = {
                item: 0 for item in items
            }
            for val in items:
                if val in graph:
                    for depender in graph[val]:
                        incomingLinks[depender] += 1

            bfsQ = deque()
            for item, link in incomingLinks.items():
                if link == 0:
                    bfsQ.append(item)

            res = []
            while bfsQ:
                sz = len(bfsQ)
                while sz:
                    item = bfsQ.popleft()
                    for nextItem in graph[item]:
                        incomingLinks[nextItem] -= 1
                        if incomingLinks[nextItem] == 0:
                            bfsQ.append(nextItem)
                    res.append(item)
                    sz -= 1

            if len(res) != len(items):
                return []
            return res

        interGrpGraph = defaultdict(set)
        relatedGrps = set()  # use this to see if the connections are full (cycle detection)
        intraGrpGraph = defaultdict(set)
        for i, deps in enumerate(beforeItems):
            for dep in deps:
                grpI, grpDep = group[i], group[dep]
                if grpDep == grpI:
                    intraGrpGraph[dep].add(i)
                else:
                    interGrpGraph[grpDep].add(grpI)
                    relatedGrps.add(grpI)
                    relatedGrps.add(grpDep)
        
        # grpOrder = []
        # if relatedGrps:
        #     # okay.. this is confusing
        #     # it can have no order between groups 
        #     # but when relatedGrps are non-empty and no order it is wrong
        #     grpOrder = topoSortGrp(relatedGrps, interGrpGraph)
        #     if not grpOrder:
        #         return []
        grpOrder = topoSort(relatedGrps, interGrpGraph)
        if relatedGrps and not grpOrder:
            return []

        # now all the related groups are topo-sorted..
        # output them and deal with non-groups..
        res = []
        for cGrp in grpOrder:
            items = topoSort(withGroup[cGrp], intraGrpGraph)
            if not items:
                return None
            res.extend(items)

        for grp, items in withGroup.items():
            # topo sort within each group
            if grp not in relatedGrps:
                items = topoSort(items, intraGrpGraph)
                if not items:
                    return None
                res.extend(list(items))
        return res


"""
surprisingly refactor makes it right for 2nd case

good and bad
16 / 17 test cases passed.
the last case is wrong... 

I didn't do the grp sort valid verify
        if relatedGrps:
            grpOrder = topoSortGrp(relatedGrps, interGrpGraph)
            if not grpOrder:
                return []
    added this!

but not sure at all..
"""



if __name__ ==  '__main__':
    s = Solution()

    print(s.sortItems(n=8, m=2, group=[-1, -1, 1, 0, 0, 1, 0, -1],
          beforeItems=[[], [6], [5], [6], [3, 6], [], [], []]))

    print(s.sortItems(n=5, m=3, group=[0,0,2,1,0],
                      beforeItems=[[3], [], [], [], [1, 3, 2]]))
