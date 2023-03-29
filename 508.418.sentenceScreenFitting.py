"""
https://leetcode.com/problems/sentence-screen-fitting/?envType=study-plan&id=dynamic-programming-iii

ok..

f(idx,row,col)
    represent at idx word, with row and col left
    how many can be fitted

    apparently, when idx reaches len(sentence), res+=1
    when row reach over .. it ends 
    when col reach over .. row+=1 and col go back to zero

    the tricky part is when shoud row wrap?

    when a word has a length longer than col total.. it cannot fit anywhere
    when a word just fit to the end of row.. it need no extra space.. 

    not very firmly clear but would be fun to kick off the coding and see

"""


from typing import List


class Solution:
    def wordsTyping(self, sentence: List[str], rows: int, cols: int) -> int:
        res = 0
        def f(idx,row,col):
            nonlocal res
            if idx == len(sentence):
                res += 1
                idx = 0
                
            if len(sentence[idx]) > cols:
                res = 0
                return

            if row == rows:
                return
            
            if cols-col >= len(sentence[idx]):
                # can fit
                f(idx+1, row, min(cols, col + len(sentence[idx]) + 1 ))
            else:
                f(idx, row+1,0)
        
        f(0,0,0)
        return res

"""
okay.. cool 
["try","to","be","better"]
10000
9001

this causes max recursion depth limit exceeded 
so actuall.. when a row can fit multiple just go ahead skip them
"""


class Solution:
    def wordsTyping(self, sentence: List[str], rows: int, cols: int) -> int:
        fullSentenceLen = sum(len(word) for word in sentence) + len(sentence)
        res = 0

        def f(idx, row, col):
            nonlocal res
            if idx == len(sentence):
                res += 1
                idx = 0

            if len(sentence[idx]) > cols:
                res = 0
                return

            if row == rows:
                return

            times = (cols-col) // fullSentenceLen
            res += times
            col += times*fullSentenceLen

            if cols-col >= len(sentence[idx]):
                # can fit
                f(idx+1, row, min(cols, col + len(sentence[idx]) + 1))
            else:
                f(idx, row+1, 0)

        f(0, 0, 0)
        return res

"""
okay

["abcdef","ghijkl","mnop","qrs","tuv","wxyz","asdf","ogfd","df","r","abcdef","ghijkl","mnop","qrs","tuv","wxyz","asdf","ogfd","df","r","abcdef","ghijkl","mnop","qrs","tuv","wxyz","asdf","ogfd","df","r","abcdef","ghijkl","mnop","qrs","tuv","wxyz","asdf","ogfd","df","r","abcdef","ghijkl","mnop","qrs","tuv","wxyz","asdf","ogfd","df","r","abcdef","ghijkl","mnop","qrs","tuv","wxyz","asdf","ogfd","df","r","abcdef","ghijkl","mnop","qrs","tuv","wxyz","asdf","ogfd","df","r","abcdef","ghijkl","mnop","qrs","tuv","wxyz","asdf","ogfd","df","r","abcdef","ghijkl","mnop","qrs","tuv","wxyz","asdf","ogfd","df","r","abcdef","ghijkl","mnop","qrs","tuv","wxyz","asdf","ogfd","df","r"]
20000
20000

still failed at max recursion exceeded
so maybe introduce the cache

row is always changing.. cannot cache on that..
but I maybe can take row out of the euqation and let what decide?

or maybe I just cache on idx,col.. 
when a same word appear at a same col.. it is suppose to repeat...

but again.. that won't work downwards..
becuase the row is not the same 

anyway this reminds me of that AOC problem... repeating patterns

we just need to remember the cache[idx,col]:row
and know 

lets say it first appear at row r1
then at row r2

then r2-r1 is going to be a cycle.. 
and it take r2-r1 rows to re-occur
and how many was put down between two re-occur


"""


class Solution:
    def wordsTyping(self, sentence: List[str], rows: int, cols: int) -> int:
        fullSentenceLen = sum(len(word) for word in sentence) + len(sentence)

        def f(idx, row, col):
            res = 0
            if idx == len(sentence):
                res = 1
                idx = 0

            if len(sentence[idx]) > cols:
                return 0

            if row == rows:
                return res

            times = (cols-col) // fullSentenceLen
            res += times
            col += times*fullSentenceLen

            if cols-col >= len(sentence[idx]):
                # can fit
                res += f(idx+1, row, min(cols, col + len(sentence[idx]) + 1))
            else:
                res += f(idx, row+1, 0)
            return res

        return f(0,0,0)

"""
ah.. I realize I didn't cache at all..
I was not returning any values

because row is always going downwards.. no use to cache

hmm... okay.. cannot code that idea out
let me turn this into iterative 

dp[idx,row,col] = 0 or 1, start with 0 or 1, depends on if idx==len(sentence)
            if cols-col >= len(sentence[idx]):
                # can fit
                += dp[idx+1, row, min(cols, col + len(sentence[idx]) + 1)]
            else:
                += dp[idx, row+1, 0]
                
"""




class Solution:
    def wordsTyping(self, sentence: List[str], rows: int, cols: int) -> int:    
        dp = [[[0 for _ in range(cols+1)] for _ in range(rows+1)] for _ in range(len(sentence)+1)]

"""
okay... this even I am able to write it out
it cannot pass either..

2*10^4 * 2*10^4 plus index has 10
that is destined to fail

but idx is actually decisive by row/col..
there is some duplciation out there..

or maybe row is kind of reductive..
let me think 
"""


if __name__ == '__main__':
    s = Solution()
    print(s.wordsTyping(sentence = ["hello","world"], rows = 2, cols = 8))
    print(s.wordsTyping(sentence=["a", "bcd", "e"], rows=3, cols=6))
    print(s.wordsTyping(sentence=["i", "had", "apple", "pie"], rows=4, cols=5))

