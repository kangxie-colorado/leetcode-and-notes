"""
https://leetcode.com/problems/longest-repeating-substring/

this problem really has a rich set of solutions 
1. brute force (with set) (n**3)
2. N**2 substr, hash... to detect collion
    I had totally not thought of using hash 
3. build all the suffix substr, sort them, go after the longest common prefix 
4. dp[i][j] = dp[i-1][j-1] + 1 if s[i]==s[j]
    dp[i][j] represents the longest common repeating substr for ending at i and end at j... interesting
5. trie node n**2
    build trie first pass from char at 0 index
    then from char at 1 index... 

    if some subtr repeat, they will walk the same trie branches..
    maintain/update the longest repeating substr

    this is kind of like using set actually.. but it build up step by step...
    
I shall code a few other options too later...
"""