"""
https://leetcode.com/problems/insert-delete-getrandom-o1-duplicates-allowed/?envType=study-plan&id=programming-skills-iii


I failed at another randomized problem so I had no idea how to tackle it
then I see there is a simpler problem 380 https://leetcode.com/problems/insert-delete-getrandom-o1/

and the randomization idea is just store all the numbers in an array then randomly pick one
the remove is the tricky one

in 380.. it needs to swap and shrink
in 381.. maybe I can borrow the same idea

so let me review 380 and then do 381

"""

# 380


from collections import defaultdict
import random


class RandomizedSet:

    def __init__(self):
        self.nums = []
        self.numsAndPos = {}

    def insert(self, val: int) -> bool:
        if val in self.numsAndPos:
            return False
        self.numsAndPos[val] = len(self.nums)
        self.nums.append(val)

        return True

    def remove(self, val: int) -> bool:
        if val not in self.numsAndPos:
            return False
        
        if val == self.nums[-1]:
            self.nums = self.nums[:-1]
        else:
            pos = self.numsAndPos[val]
            self.nums[pos] = self.nums[-1]
            self.nums.pop()
            self.numsAndPos[self.nums[pos]] = pos
        self.numsAndPos.pop(val)

        return True
        

    def getRandom(self) -> int:
        return random.choice(self.nums)
"""
Runtime: 433 ms, faster than 89.61% of Python3 online submissions for Insert Delete GetRandom O(1).
Memory Usage: 61.8 MB, less than 7.24% of Python3 online submissions for Insert Delete GetRandom O(1).

okay.. the tricky part is don't forget to update the swapped values' pos mapping 
"""


class RandomizedCollection:

    def __init__(self):
        self.nums = []
        # use a defaultdict for convinience but it also complicates the existence testing
        self.numsAndPos = defaultdict(set) 

    def insert(self, val: int) -> bool:
        ret =  True
        if val in self.numsAndPos and self.numsAndPos[val]:
            ret = False
        self.numsAndPos[val].add(len(self.nums))
        self.nums.append(val)

        return ret

    def remove(self, val: int) -> bool:
        if val not in self.numsAndPos or not self.numsAndPos[val]:
            return False
        # is this O(1)? otherwise, I can create my own class to maintain a max pos for a val
        # that is not difficult
        pos = list(self.numsAndPos[val])[-1]
        if val == self.nums[-1]:
            # pay attention to the order.. they impacts each other
            self.numsAndPos[val].remove(len(self.nums)-1)
            self.nums.pop()
            
        else:
            self.nums[pos] = self.nums[-1]
            # this new val needs to pop len(nums)-1
            self.numsAndPos[self.nums[pos]].remove(len(self.nums)-1)
            # then add the new position
            self.numsAndPos[self.nums[pos]].add(pos)
            self.nums.pop()
            self.numsAndPos[val].remove(pos)

        return True

    def getRandom(self) -> int:
        return random.choice(self.nums)

"""
Runtime: 456 ms, faster than 89.32% of Python3 online submissions for Insert Delete GetRandom O(1) - Duplicates allowed.
Memory Usage: 66 MB, less than 40.98% of Python3 online submissions for Insert Delete GetRandom O(1) - Duplicates allowed.

that get a number from a set is kind of O(n) I feel
let me do a MaxSet -- hum.. when removing, the max could change.. so still not that good

how about a double linked list?
"""


class DblLinkNode:
    def __init__(self, val, left=None, right=None) -> None:
        self.val = val
        self.left = left
        self.right = right

class DblLinkedSet:
    def __init__(self) -> None:
        self.head = DblLinkNode(-1)
        self.tail = DblLinkNode(-1)
        self.head.right = self.tail
        self.tail.left = self.head
        self.nodes = {}
    
    def add(self, val):
        node = DblLinkNode(val)
        prev = self.tail.left
        next = self.tail 
        
        prev.right = node 
        node.right = next 

        next.left = node 
        node.left = prev 

        self.nodes[val] = node
    
    def remove(self, val):
        node = self.nodes[val]
        self.nodes.pop(val)

        prev,next = node.left, node.right 
        prev.right = next 
        next.left = prev 
    
    def getAPos(self):
        return self.head.right.val
    
    def empty(self):
        return self.head.right == self.tail

def defaultDblLinkSet():
    return DblLinkedSet()


class RandomizedCollection:

    def __init__(self):
        self.nums = []
        # use a defaultdict for convinience but it also complicates the existence testing
        self.numsAndPos = defaultdict(defaultDblLinkSet)

    def insert(self, val: int) -> bool:
        ret = True
        if val in self.numsAndPos and not self.numsAndPos[val].empty():
            ret = False
        self.numsAndPos[val].add(len(self.nums))
        self.nums.append(val)

        return ret

    def remove(self, val: int) -> bool:
        if val not in self.numsAndPos or self.numsAndPos[val].empty():
            return False
        
        if val == self.nums[-1]:
            # pay attention to the order.. they impacts each other
            self.numsAndPos[val].remove(len(self.nums)-1)
            self.nums.pop()
        else:
            pos = self.numsAndPos[val].getAPos()
            self.nums[pos] = self.nums[-1]
            # this new val needs to pop len(nums)-1
            self.numsAndPos[self.nums[pos]].remove(len(self.nums)-1)
            # then add the new position
            self.numsAndPos[self.nums[pos]].add(pos)
            self.nums.pop()
            self.numsAndPos[val].remove(pos)

        return True

    def getRandom(self) -> int:
        return random.choice(self.nums)

"""
Runtime: 542 ms, faster than 73.10% of Python3 online submissions for Insert Delete GetRandom O(1) - Duplicates allowed.
Memory Usage: 70.6 MB, less than 7.04% of Python3 online submissions for Insert Delete GetRandom O(1) - Duplicates allowed.

wow.. I made it work.. 
but not any better
"""


class RandomizedCollection:

    def __init__(self):
        self.nums = []
        # use a defaultdict for convinience but it also complicates the existence testing
        self.numsAndPos = defaultdict(set)

    def insert(self, val: int) -> bool:
        ret = True
        if val in self.numsAndPos and self.numsAndPos[val]:
            ret = False
        self.numsAndPos[val].add(len(self.nums))
        self.nums.append(val)

        return ret

    def remove(self, val: int) -> bool:
        def getAValFromSet(s):
            # for k in s:
            #     return k
            # return None
            # just use
            return next(iter(s))


        if val not in self.numsAndPos or not self.numsAndPos[val]:
            return False
        # is this O(1)? otherwise, I can create my own class to maintain a max pos for a val
        # that is not difficult
        if val == self.nums[-1]:
            # pay attention to the order.. they impacts each other
            self.numsAndPos[val].remove(len(self.nums)-1)
            self.nums.pop()

        else:
            pos = getAValFromSet(self.numsAndPos[val])
            self.nums[pos] = self.nums[-1]
            # this new val needs to pop len(nums)-1
            self.numsAndPos[self.nums[pos]].remove(len(self.nums)-1)
            # then add the new position
            self.numsAndPos[self.nums[pos]].add(pos)
            self.nums.pop()
            self.numsAndPos[val].remove(pos)

        return True

    def getRandom(self) -> int:
        return random.choice(self.nums)

"""
Runtime: 474 ms, faster than 83.86% of Python3 online submissions for Insert Delete GetRandom O(1) - Duplicates allowed.
Memory Usage: 66.5 MB, less than 7.04% of Python3 online submissions for Insert Delete GetRandom O(1) - Duplicates allowed.

not too much better either using next(iter(s))
anyway... 
"""

if __name__ == '__main__':
    calls = ["RandomizedCollection","insert","insert","insert","insert","insert","insert","insert","insert","insert","remove","remove"]
    args = [[],[1],[0],[1],[1],[1],[1],[1],[1],[0],[0],[0]]

    for call,arg in zip(calls, args):
        print(f"{call}({arg}) ")
        if call == 'RandomizedCollection':
            rdc = RandomizedCollection(*arg)
        elif call == 'insert':
            print(rdc.insert(*arg))
        elif call == 'remove':
            print(rdc.remove(*arg))
        