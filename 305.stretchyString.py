from collections import Counter
from typing import List


class Solution:
    def expressiveWords(self, s: str, words: List[str]) -> int:
        sc = Counter(s)

        # compress s as such
        # heeello: [(h,1), (e,3), (l,2), (o,3)]
        # also compress word
        # hello: [(h,1), (e,1), (l,2), (0,3)]
        # then go thru the compressed word
        # for each section
        # if length is not equal, can it be stretchy? making it 3 or more to reach equal..
        # if yes, continue, else break
        def getCompressed(s):
            res = []
            i, j = 0, 1
            while j < len(s):
                if s[j] != s[i]:
                    res.append((s[i], j-i))
                    i = j
                j += 1
            res.append((s[i], j-i))
            return res

        def stretchy(compStr, compWord):
            stretched = False
            for i, cAndL in enumerate(compWord):
                c, l = cAndL
                cRef, lRef = compStr[i]

                if c != cRef or (l != lRef and lRef < 3) or l > lRef:
                    return False
                if l < 3 and l != lRef and lRef >= 3:
                    stretched |= True

            return stretched

        res = 0
        compStr = getCompressed(s)
        for w in words:
            wc = Counter(w)
            if len(sc) != len(wc):
                continue
            compWord = getCompressed(w)

            if stretchy(compStr, compWord):
                res += 1

        return res


if __name__ == '__main__':
    s = Solution()
    print(s.expressiveWords(s="heeellooo", words=["hello", "hi", "helo"]))
    print(s.expressiveWords(s="zzzzzyyyyy", words=["zzyy", "zy", "zyy"]))
