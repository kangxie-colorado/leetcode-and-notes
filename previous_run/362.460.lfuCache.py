"""
https://leetcode.com/problems/lfu-cache/?envType=study-plan&id=programming-skills-iii

store map, map key to list-node in a binary search tree like ds, i.e. the beloved sortedlist
hmm.. it will not be O(1) and SortedList doesn't support customized class

if I use SortedDict(), then it is not O(1)
so I am think

keep the frequency map
{freq: double linkedlist} -- keeping the most recently used at the tail or head 
and also promote, demote the item thru the freq list..

in the run, maintain a maxFreq var, and that will help you retrieve the maxFreq
well.. maybe I ought to keep a least used freq, to retrieve the frist eveit item quicker
"""

from sortedcontainers import SortedList

class DblLinkedNode:
    def __init__(self, key=0, val=0, freq=0, left=None, right=None) -> None:
        self.key = key
        self.val = val
        self.freq = freq
        self.left = left 
        self.right = right


class LFUCache:

    def __init__(self, capacity: int):
        self.cap = capacity
        self.nodes = 0
        self.keys = {} # maps to a node in one of the double linked list's node
        self.freqMap = {} # maps to a double linked list, keeping the head and list 
        self.leastFreq = 0
    
    def initFreqList(self, freq):
        assert freq not in self.freqMap

        head = DblLinkedNode()
        tail = DblLinkedNode()
        head.right = tail 
        tail.left = head

        self.freqMap[freq] = [head, tail]

    def get(self, key: int) -> int:
        if key in self.keys:
            node = self.keys[key] # a DblLinkedNode
            self.moveNode(node)
            return node.val

        return -1



    def put(self, key: int, value: int) -> None:
        if key in self.keys:
            node = self.keys[key]  # a DblLinkedNode
            node.val = value
            self.moveNode(node)
        else:
            self.nodes += 1
            node = DblLinkedNode(key=key, val=value)
            self.keys[key] = node
            self.moveNode(node, new=True)
            
            if self.nodes > self.cap:
                # remove the elemet after least freq head
                if self.leastFreq:
                    linkHead, linkTail = self.freqMap[self.leastFreq]
                    remove = linkHead.right 
                    self.keys.pop(remove.key)

                    prev = linkHead
                    next = linkHead.right.right
                    prev.right = next
                    next.left = prev 

                    if linkHead.right == linkTail:
                        self.freqMap.pop(self.leastFreq)
                else:
                    # cap = 0. never a key can be put
                    self.keys.pop(key)
                    return 
            self.leastFreq = 1

    def moveNode(self, node, new=False):
        node.freq += 1
        if not new:
            # break out of this freq link and promote to next one
            prev, next = node.left, node.right 
            prev.right = next 
            next.left = prev 

        # insert me to next freq link
        # if that link if empty.. initilize it
        if node.freq not in self.freqMap:
            self.initFreqList(node.freq)
        _, linkTail = self.freqMap[node.freq]

        # insert me at the tail, which is the most recently used
        prev = linkTail.left
        next = linkTail
        prev.right = node
        node.left = prev
        node.right = next
        next.left = node

        if self.leastFreq:
            lfuHead, lfuTtail = self.freqMap[self.leastFreq]
            while lfuHead.right == lfuTtail:
                # this freq is empty
                self.freqMap.pop(self.leastFreq)

                # find next leastFreq
                while self.leastFreq not in self.freqMap:
                    self.leastFreq += 1
                lfuHead, lfuTtail = self.freqMap[self.leastFreq]


"""
Runtime: 960 ms, faster than 78.58% of Python3 online submissions for LFU Cache.
Memory Usage: 78.9 MB, less than 29.15% of Python3 online submissions for LFU Cache.

wow! relaxed
"""


class LFUCache:

    def __init__(self, capacity: int):
        self.cap = capacity
        self.nodes = 0
        self.keys = {}  # maps to a node in one of the double linked list's node
        self.freqMap = {}  # maps to a double linked list, keeping the head and list
        self.leastFreq = 0 # use 0 or non-zero to mean at least one put was executed successfully

    def initFreqList(self, freq):
        assert freq not in self.freqMap

        head = DblLinkedNode()
        tail = DblLinkedNode()
        head.right = tail
        tail.left = head

        self.freqMap[freq] = [head, tail]

    def moveNode(self, node, new=False):
        node.freq += 1
        if not new:
            # break out of this freq link and promote to next one
            prev, next = node.left, node.right
            prev.right = next
            next.left = prev

        # insert me to next freq link
        # if that link if empty.. initilize it
        if node.freq not in self.freqMap:
            self.initFreqList(node.freq)
        _, linkTail = self.freqMap[node.freq]

        # insert me at the tail, which is the most recently used
        self.insertAtTail(node, linkTail)

        if self.leastFreq:
            lfuHead, lfuTtail = self.freqMap[self.leastFreq]
            while lfuHead.right == lfuTtail:
                # this freq is empty
                self.freqMap.pop(self.leastFreq)

                # find next leastFreq
                while self.leastFreq not in self.freqMap:
                    self.leastFreq += 1
                lfuHead, lfuTtail = self.freqMap[self.leastFreq]

    def insertAtTail(self, node, linkTail):
        prev = linkTail.left
        next = linkTail
        prev.right = node
        node.left = prev
        node.right = next
        next.left = node
    
    def removeLFUNode(self):
        linkHead, linkTail = self.freqMap[self.leastFreq]
        remove = linkHead.right
        self.keys.pop(remove.key)

        prev = linkHead
        next = linkHead.right.right
        prev.right = next
        next.left = prev

        # if this happens to be on the leastFreq link
        # and it becomes empty... remove this freq link from the map
        if linkHead.right == linkTail:
            self.freqMap.pop(self.leastFreq)

    def get(self, key: int) -> int:
        if key in self.keys:
            node = self.keys[key]  # a DblLinkedNode
            self.moveNode(node)
            return node.val

        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.keys:
            node = self.keys[key]  # a DblLinkedNode
            node.val = value
            self.moveNode(node)
        else:
            self.nodes += 1
            node = DblLinkedNode(key=key, val=value)
            self.keys[key] = node
            self.moveNode(node, new=True)

            if self.nodes > self.cap:
                # remove the elemet after least freq head
                if self.leastFreq:
                    self.removeLFUNode()
                else:
                    # cap = 0. never a key can be put
                    self.keys.pop(key)
                    return
            self.leastFreq = 1


