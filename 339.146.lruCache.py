"""
https://leetcode.com/problems/lru-cache/?envType=study-plan&id=programming-skills-iii

a map and a linked list

"""


class DoubleLinkedNode:
    def __init__(self, key=0, val=0, prev=None, next=None) -> None:
        self.key = key
        self.val = val
        self.prev = prev
        self.next = next


class LRUCache:

    def __init__(self, capacity: int):
        # map key to node
        self.keys = {}

        # head will be the most recently used key
        # tail will be the least recently used key
        # these two nodes are guardians
        self.head = DoubleLinkedNode()
        self.tail = DoubleLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.capacity = capacity

    def __moveToHead(self, node):
        self.__unlink(node)
        self.__addToHead(node)

    def __unlink(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def __addToHead(self, node):
        self.head.next.prev = node
        node.next = self.head.next
        self.head.next = node
        node.prev = self.head

    def __removeTail(self):
        node = self.tail.prev
        self.__unlink(node)
        return node.key

    def get(self, key: int) -> int:
        res = -1
        if key in self.keys:
            node = self.keys[key]
            res = node.val
            self.__moveToHead(node)

        return res

    def put(self, key: int, value: int) -> None:
        if key in self.keys:
            self.keys[key].val = value
            self.__moveToHead(self.keys[key])
        else:
            node = self.keys[key] = DoubleLinkedNode(key, value)
            self.__addToHead(node)
            if len(self.keys) > self.capacity:
                removed = self.__removeTail()
                self.keys.pop(removed)


"""
Runtime: 902 ms, faster than 86.85% of Python3 online submissions for LRU Cache.
Memory Usage: 76.6 MB, less than 10.45% of Python3 online submissions for LRU Cache.

think maybe I can also use a heap with a map?
nah... the heap must be able to support update by key.. which isn't easy
"""