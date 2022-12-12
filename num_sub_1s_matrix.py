from typing import List


def numSubmat(mat: List[List[int]]) -> int:
    print('\n'.join( [''.join( str(mat[i])) for i in range(len(mat))] ))
    print("")

    m, n, res = len(mat), len(mat[0]), 0
    histogram = [0] * (n + 1)
    for i in range(m):
        stack, dp = [-1], [0] * (n + 1)
        for j in range(n):
            histogram[j] = 0 if mat[i][j] == 0 else histogram[j] + 1
            while histogram[j] < histogram[stack[-1]]: # stack[-1] is only a trick to histgram[-1] which is 0?
                stack.pop()
            dp[j] = dp[stack[-1]] + histogram[j] * (j - stack[-1])  # Important!!
            stack.append(j)

        res += sum(dp)
        print(histogram, "       ", dp)

        #print("")
    return res

# numSubmat([[0, 1, 1, 1], [1, 1, 0, 1], [1, 1, 0, 0], [1, 1, 1, 1], [0, 1, 0, 0]])
# numSubmat([[1, 1, 1, 1, 0, 1, 0], [1, 1, 1, 0, 0, 0, 1], [0, 1, 1, 1, 1, 0, 0], [1, 1, 0, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 1, 0, 1, 1, 1, 1], [1, 1, 0, 0, 1, 1, 1]])
numSubmat([[1,0,1,1,1,1,1],[1,1,0,0,0,1,1],[1,1,1,0,0,1,1],[1,0,1,0,1,0,1],[1,0,1,1,1,0,1],[1,1,0,1,1,1,1],[1,0,0,1,1,0,1]])
