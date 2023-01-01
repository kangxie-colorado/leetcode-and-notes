"""
https://leetcode.com/problems/design-excel-sum-formula/?envType=study-plan&id=programming-skills-iii

haha.. I think I was interviewed for a similar problem by amazon
and I knew nothing ... 

but this is hard..
i can see it is indeed a graph problem

how to do it
if A cell depends on B, when update B.. pass the update to A?
B impacts A
A depends on B

tricky part may be when the impact is cancelled, how to update that
luckily this is only one jump 

lets say A depends-on B depends-on C
A cancel this.. but B still depends-on C

okay.. 
"""


from collections import defaultdict
from typing import List


class Excel:

    def __init__(self, height: int, width: str):
        self.dependsOn = {}  # e.g. A depends on B
        # e.g. B impacts on A by times (A,2) when B change 1, A should change 2
        self.impacts = {}
        self.values = {}

        for i in range(1, height+1):
            for j in range(ord('A'), ord(width)+1):
                j = chr(j)
                self.dependsOn[i, j] = set()  # x,y
                self.impacts[i, j] = defaultdict(
                    int)  # map (x,y): impact-times
                self.values[i, j] = 0

    def __repr__(self) -> str:
        # return f"Excel(values:{self.values}, dependsOn:{self.dependsOn}, impacts:{self.impacts})"
        # return f"Excel(values:{self.values})"
        res = "Values:"
        for (i, j), v in self.values.items():
            if v:
                res = f"{res} {(i,j)}:{v}"

        return res

    def cancelRelations(self, i, j):
        if self.dependsOn[i, j]:
            # cancel depends and impacts
            for x, y in self.dependsOn[i, j]:
                # cell(i,j) depends on cell(x,y)
                # so cell(x,y) impacts cell(i,j)
                self.impacts[x, y].pop((i, j))
            self.dependsOn[i, j] = set()

    def passImpacts(self, delta, i, j):
        # define a dfs to helper spread the impacts
        def f(x, y, times):
            self.values[x, y] += delta*times
            for (nx, ny), ntime in self.impacts[x, y].items():
                f(nx, ny, times*ntime)

        if self.impacts[i, j]:
            # for any cell impcated by i,j
            # update their values
            # TODO: this needs to be a dfs
            # wait for me to get pass the simpliset cases
            for (x, y), times in self.impacts[i, j].items():
                f(x, y, times)

    def set(self, row: int, column: str, val: int) -> None:
        i, j = row, column
        oldVal = self.values[i, j]
        self.values[i, j] = val
        delta = val - oldVal

        self.cancelRelations(i, j)
        self.passImpacts(delta, i, j)


    def get(self, row: int, column: str) -> int:
        i, j = row, column
        return self.values[i, j]

    def sum(self, row: int, column: str, numbers: List[str]) -> int:
        i, j = row, column
        oldVal = self.values[i, j]

        res = 0
        dependsOn = defaultdict(int)
        # get the depends on cells first
        # if I run the logic in the same time, conflicts may rise
        # conflicts are around the times updating logic
        # so get the cells then run the logic in a 2nd loop
        for dep in numbers:
            if ':' not in dep:
                y, x = dep[0], int(dep[1])
                dependsOn[x, y] += 1
            else:
                dep1, dep2 = dep.split(':')
                y1, x1 = dep1[0], int(dep1[1:])
                y2, x2 = dep2[0], int(dep2[1:])
                for x in range(x1, x2+1):
                    for y in range(ord(y1), ord(y2)+1):
                        y = chr(y)
                        dependsOn[x, y] += 1

        for (x, y), times in dependsOn.items():
            # cancel previous depends and impacts
            # maybe no need? I use a set..
            # create depends and impacts
            self.dependsOn[i, j].add((x, y))
            # not +=, this is a new relationship
            self.impacts[x, y][i, j] = times
            res += self.values[x, y] * times

        # this need impact spreading as well
        # so insteads of setting the value
        # i call set.. cannot call set.
        # in set() I cancel the relations.. I treat set as to set the value to a ordinary val
        self.values[i, j] = res
        self.passImpacts(res-oldVal,i,j)
        return res

"""
Runtime: 40 ms, faster than 84.04% of Python3 online submissions for Design Excel Sum Formula.
Memory Usage: 15.2 MB, less than 6.38% of Python3 online submissions for Design Excel Sum Formula.

"""

if __name__ == '__main__':
    calls = ["Excel","set","sum","set","get"]
    args = [[3,"C"],[1,"A",2],[3,"C",["A1","A1:B2"]],[2,"B",2],[3,"C"]]

    calls=["Excel","set","set","set","sum","get","set","get","sum","set","get","get","sum","set","get","get","get","get"]
    args= [[5,"E"],[1,"A",5],[1,"B",3],[1,"C",2],[1,"C",["A1","A1:B1"]],[1,"C"],[1,"B",5],[1,"C"],[1,"B",["A1:A5"]],[5,"A",10],[1,"B"],[1,"C"],[3,"C",["A1:C1","A1:A5"]],[3,"A",3],[1,"B"],[1,"C"],[3,"C"],[5,"A"]]

    calls = ["Excel","set","set","sum","sum"]
    args = [[26,"Z"],[1,"A",1],[1,"I",1],[7,"D",["A1:D6","A1:G3","A1:C12"]],[10,"G",["A1:D7","D1:F10","D3:I8","I1:I9"]]]

    calls = ["Excel","get","set","get","sum","sum","get","sum","get"]
    args = [[5,"E"],[1,"A"],[1,"A",1],[1,"A"],[2,"B",["A1","A1"]],[2,"C",["A1","B2"]],[2,"C"],[2,"B",["A1"]],[2,"C"]]
    

    for call,arg in zip(calls, args):
        print(call,arg)
        if call == 'Excel':
            excel = Excel(*arg)
        elif call == 'set':
            excel.set(*arg)
        elif call == 'get':
            print(excel.get(*arg))
        else:
            print(excel.sum(*arg))
        print(excel)
        print()