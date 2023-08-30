"""
a special thing: if the remaining just fit the world, no need for space


"""

from typing import List


class Solution:
    def wordsTyping(self, sentence: List[str], rows: int, cols: int) -> int:
        res = 0
        # r,c represnts the insert cursor position
        # i the to-be-written word
        def f(i,r,c):
            if i==len(sentence):
                nonlocal res
                res += 1
                i=0

            if c >= cols:
                r+=1
                c=0
            
            if r==rows:
                return
            
            if len(sentence[i])>cols:
                return
            
            if (cols - c) >= len(sentence[i]):
                f(i+1, r, c+len(sentence[i])+1)
            else:
                f(i, r+1, 0)
        
        f(0,0,0)
        return res
"""
maximum recursion ...
["try","to","be","better"]
10000
9001

and the test case is try to be better... how ironic
so I need to jump ahead.. if the whole row can be fitted inside the remain.. just fit as many as of them

"""
class Solution:
    def wordsTyping(self, sentence: List[str], rows: int, cols: int) -> int:
        wholeLineLen = sum([len(s) for s in sentence]) + len(sentence)
        res = 0
        # r,c represnts the insert cursor position
        # i the to-be-written word
        def f(i,r,c):
            if i==len(sentence):
                nonlocal res
                res += 1
                i=0

            if c >= cols:
                r+=1
                c=0
            
            if r==rows:
                return
            
            if len(sentence[i])>cols:
                return
            
            fitLines = (cols-c) // wholeLineLen
            res += fitLines
            c += fitLines*wholeLineLen
            if (cols - c) >= len(sentence[i]):
                f(i+1, r, c+len(sentence[i])+1)
            else:
                f(i, r+1, 0)
        
        f(0,0,0)
        return res

""""
after optimizing col processing, still maximum recursion depth 
change to dp???

"""

class Solution:
    def wordsTyping(self, sentence: List[str], rows: int, cols: int) -> int:
        wholeLineLen = sum([len(s) for s in sentence]) + len(sentence)
        
        # r,c represnts the insert cursor position
        # i the to-be-written word
        def f(i,r,c):
            if c >= cols:
                r+=1
                c=0
            
            if r==rows:
                return i//len(sentence)
            
            if len(sentence[i%len(sentence)])>cols:
                return 0
            
            fitLines = (cols-c) // wholeLineLen
            res = fitLines
            c += fitLines*wholeLineLen
            if (cols - c) >= len(sentence[i%len(sentence)]):
                return res + f(i+1, r, c+len(sentence[i%len(sentence)])+1)
            else:
                return res + f(i, r+1, 0)
        
        return f(0,0,0)


class Solution:
    def wordsTyping(self, sentence: List[str], rows: int, cols: int) -> int:
        wholeLineLen = sum([len(s) for s in sentence]) + len(sentence)
        colIdxToRow = {}
        rowColToCount = {}
        
        # r,c represnts the insert cursor position
        # i the to-be-written word
        def f(i,r,c):
            idx = i%len(sentence)
            if c >= cols:
                r+=1
                c=0
            if r==rows:
                return i//len(sentence)
            
            if len(sentence[idx])>cols:
                return 0
            
            rowColToCount[(r,c)] = i//len(sentence)
            if (c,idx) in colIdxToRow:
                # repating
                r1 = colIdxToRow[(c,idx)]
                res1 = rowColToCount[(r1, c)]
                res2 = rowColToCount[(r,c)]
                canRepeat = (rows-r) // (r-r1)
                resAdd = canRepeat * (res2-res1)
                if resAdd>0:
                  remainR = r + canRepeat*(r-r1)
                  return f(i+resAdd*len(sentence), remainR, c)
            
            colIdxToRow[(c,idx)] = r
            
            fitLines = (cols-c) // wholeLineLen
            i += fitLines*len(sentence)
            c += fitLines*wholeLineLen
            

            if (cols - c) >= len(sentence[i%len(sentence)]):
                res = f(i+1, r, c+len(sentence[i%len(sentence)])+1)
            else:
                res = f(i, r+1, 0)
            
            return res
        
        return f(0,0,0)
if __name__ == '__main__':
    s = Solution()
    # print(s.wordsTyping(sentence = ["hello","world"], rows = 2, cols = 8))
    print(s.wordsTyping(sentence = ["f","p", "a"], rows = 8, cols = 7))
        


            
                
                