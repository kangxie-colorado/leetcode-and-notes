"""
https://leetcode.com/problems/accounts-merge/

union-find. very obvious of course.
just need some careful coding

"""


from collections import defaultdict
from typing import List


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        emailRoots = {}

        def find(e):
            emailRoots.setdefault(e,e)
            if emailRoots[e] != e:
                emailRoots[e] = find(emailRoots[e])
            return emailRoots[e]
        
        def union(e1,e2):
            emailRoots[find(e1)] = emailRoots[find(e2)]
        
        for account in accounts:
            emails = sorted(account[1:])
            firstEmail = emails[0]
            # how to deal with only one email
            # maybe I can union with myself
            # for i in range(1,len(emails)):
            for i in range(len(emails)):
                union(emails[i], firstEmail)

        subgrps = defaultdict(list)
        for email in emailRoots:
            root = find(email)
            subgrps[root].append(email)
        
        checkedRoot = set()
        res = []
        for account in accounts:
            email = account[1]
            root = find(email)
            if root in checkedRoot:
                continue

            res.append(
                [
                    account[0], # name
                    *sorted(subgrps[root])
                ]
            )
            checkedRoot.add(root)
                

        return res

"""
Runtime: 825 ms, faster than 9.58% of Python3 online submissions for Accounts Merge.
Memory Usage: 17.9 MB, less than 81.16% of Python3 online submissions for Accounts Merge.
"""