from typing import List


class Solution:
    def restoreMatrix(self, rowSum: List[int], colSum: List[int]) -> List[List[int]]:
        m, n = len(rowSum), len(colSum)
        run = res = [[]]*m
        for i in range(m):
            res[i] = [0]*n
            run[i] = [0]*n

        rowSumRuns = [0]*m
        colSumRuns = [0]*n

        def backtrack(i, j):
            if j < n and i < m and (colSumRuns[j] > colSum[j] or rowSumRuns[i] > rowSum[i]):
                return False

            if j == n:
                if rowSumRuns[i] == rowSum[i]:
                    i += 1
                    j = 0

                    if i == m:
                        nonlocal res
                        res = run.copy()
                        return True
                else:
                    return False
            maxVal = min(colSum[j]-colSumRuns[j], rowSum[i]-rowSumRuns[i])

            for val in range(maxVal+1):
                run[i][j] = val
                colSumRuns[j] += val
                rowSumRuns[i] += val
                if backtrack(i, j+1):
                    return True
                run[i][j] = 0
                colSumRuns[j] -= val
                rowSumRuns[i] -= val
            return False

        backtrack(0, 0)
        return res


if __name__ == '__main__':
    s = Solution()
    print(s.restoreMatrix([3, 8], [4, 7]))
