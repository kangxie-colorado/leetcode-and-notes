"""
https://leetcode.com/problems/fancy-sequence/

naive brute force is easy but TLE 
looking at the hints

Use two arrays to save the cumulative multipliers at each time point and cumulative sums adjusted by the current multiplier.
The function getIndex(idx) ask to the current value modulo 10^9+7. Use modular inverse and both arrays to calculate this value.

not sure how it helps..
just some try -- yeah.. no luck
and luckily I didn't spend too much time... this is some math problem at al...
"""


"""
okay.. I watched the answer and I truly don't understand what is going on
https://leetcode.com/problems/fancy-sequence/discuss/905064/C%2B%2BPython-O(1)

just copy and pass this one
"""