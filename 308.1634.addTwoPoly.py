"""
https://leetcode.com/problems/add-two-polynomials-represented-as-linked-lists/?envType=study-plan&id=programming-skills-iii

should be straight
when power is the same.. add them... 
else advance the higher power one
"""

# Definition for polynomial singly-linked list.


class PolyNode:
    def __init__(self, x=0, y=0, next=None):
        self.coefficient = x
        self.power = y
        self.next = next


class Solution:
    def addPoly(self, poly1: 'PolyNode', poly2: 'PolyNode') -> 'PolyNode':

        dummy = PolyNode()
        tail = dummy

        while poly1 and poly2:
            if poly1.power == poly2.power:
                resCo = poly1.coefficient+poly2.coefficient
                if resCo:
                    tail.next = PolyNode(
                        resCo, poly1.power)
                    tail = tail.next
                poly1 = poly1.next
                poly2 = poly2.next
            else:
                if poly1.power > poly2.power:
                    tail.next = poly1
                    tail = tail.next
                    poly1 = poly1.next
                else:
                    tail.next = poly2
                    tail = tail.next
                    poly2 = poly2.next

        tail.next = poly1 or poly2
        return dummy.next
