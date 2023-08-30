"""
thinking union find
but then think if the name is not same, we don't event need to bother

so just focus on the same name first...
"""

from collections import defaultdict
from typing import List


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        
        def find(email):
            roots.setdefault(email, email)
            if email != roots[email]:
                roots[email] = find(roots[email])
            return roots[email]

        def union(e1, e2):
            roots[find(e1)] = find(e2)

        m = len(accounts)
        sameNameAccounts = defaultdict(list)
        for idx in range(m):
            sameNameAccounts[accounts[idx][0]].append(idx)

        res = []
        for name,idxes in sameNameAccounts.items():
            if len(idxes) == 1:
                name = accounts[idxes[0]][0]
                emails = list(set(accounts[idxes[0]][1:]))
                emails.sort()
                res.append([name]+emails)
            else:
                # union find?
                roots = {}
                allEmails = set()
                for idx in idxes:
                    emails = accounts[idx][1:]
                    allEmails = allEmails.union(set(emails))
                    for email in emails[1:]:
                        union(email, emails[0])
                
                grps =  defaultdict(list)
                for email in allEmails:
                    root = find(email)
                    grps[root].append(email)
                
                for emails in grps.values():
                    emails.sort()
                    res.append([name]+emails)
          
        return res

if __name__ == '__main__':
    s = Solution()
    print(s.accountsMerge(accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]))
    print(s.accountsMerge(accounts = [["Gabe","Gabe0@m.co","Gabe3@m.co","Gabe1@m.co"],["Kevin","Kevin3@m.co","Kevin5@m.co","Kevin0@m.co"],["Ethan","Ethan5@m.co","Ethan4@m.co","Ethan0@m.co"],["Hanzo","Hanzo3@m.co","Hanzo1@m.co","Hanzo0@m.co"],["Fern","Fern5@m.co","Fern1@m.co","Fern0@m.co"]]))
                
    accounts = [["Alex","Alex5@m.co","Alex4@m.co","Alex0@m.co"],["Ethan","Ethan3@m.co","Ethan3@m.co","Ethan0@m.co"],["Kevin","Kevin4@m.co","Kevin2@m.co","Kevin2@m.co"],["Gabe","Gabe0@m.co","Gabe3@m.co","Gabe2@m.co"],["Gabe","Gabe3@m.co","Gabe4@m.co","Gabe2@m.co"]]            


        
