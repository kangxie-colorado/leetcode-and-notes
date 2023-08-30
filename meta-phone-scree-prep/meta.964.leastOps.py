class Solution:
    def leastOpsExpressTarget(self, x: int, target: int) -> int:
        minOps = float('inf')
        def f(ops):
            nonlocal minOps
            if len(ops) >= minOps or len(ops)>2*target-1:
                return
            
            # print(f"{str(x) + str(x).join(ops) + str(x)}")
            if ops and eval(str(x) + str(x).join(ops) + str(x)) == target:
                minOps = min(minOps, len(ops))
                return

            for op in '+-*/':
                f(ops + [op])
        
        f([])
        return minOps

if __name__ == '__main__':
    s = Solution()
    print(s.leastOpsExpressTarget(3,19))