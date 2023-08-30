# The read4 API is already defined for you.
def read4(buf4: List[str]) -> int:
    ...

from typing import List


class Solution:
    def __init__(self) -> None:
        self.buf = []
        self.idx = 0
        self.initiated = False
            

    def read(self, buf: List[str], n: int) -> int:
        if not self.initiated:
            
            while read4(buf4):
                for b in buf4:
                    if not b:
                        break
                    self.buf.append(b)
                buf4 = [""]*4
            self.initiated = True
        
        if self.idx + n < len(self.buf):
            buf = self.buf[self.idx:self.idx+n]
            self.idx += n
            return n
        else:
            buf = self.buf[self.idx:]
            res = len(self.buf) - self.idx 
            self.idx = len(self.buf)
            return res

"""
ugh.. huh... hmm..
not sure what this problem is
"""