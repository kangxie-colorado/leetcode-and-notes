"""
https://leetcode.com/problems/shortest-common-supersequence/?envType=study-plan&id=dynamic-programming-iii

looks like such string dp can be approached with a fixed way or start from that at least
f(i,j):
    if s[i]==t[j]:
        then pick this char
    else:
        could be pick either to see which is shorter

    base:
        one string reaches end.. just append the rest of the other

could start a trial
"""


from functools import cache


class Solution:
    def shortestCommonSupersequence(self, str1: str, str2: str) -> str:
        
        @cache
        def f(i,j):
            if i==len(str1) or j==len(str2):
                return str1[i:]+str2[j:]

            if str1[i]==str2[j]:
                return str1[i]+f(i+1,j+1)
            
            else:
                s1 = str1[i] + f(i+1,j)
                s2 = str2[j] + f(i,j+1)
                if len(s1) < len(s2):
                    return s1
                return s2
            
        return f(0,0)
    
"""
46 / 47 test cases passed.

TLE at last one.. hmm

"atdznrqfwlfbcqkezrltzyeqvqemikzgghxkzenhtapwrmrovwtpzzsyiwongllqmvptwammerobtgmkpowndejvbuwbporfyroknrjoekdgqqlgzxiisweeegxajqlradgcciavbpgqjzwtdetmtallzyukdztoxysggrqkliixnagwzmassthjecvfzmyonglocmvjnxkcwqqvgrzpsswnigjthtkuawirecfuzrbifgwolpnhcapzxwmfhvpfmqapdxgmddsdlhteugqoyepbztspgojbrmpjmwmhnldunskpvwprzrudbmtwdvgyghgprqcdgqjjbyfsujnnssfqvjhnvcotynidziswpzhkdszbblustoxwtlhkowpatbypvkmajumsxqqunlxxvfezayrolwezfzfyzmmneepwshpemynwzyunsxgjflnqmfghsvwpknqhclhrlmnrljwabwpxomwhuhffpfinhnairblcayygghzqmotwrywqayvvgohmujneqlzurxcpnwdipldofyvfdurbsoxdurlofkqnrjomszjimrxbqzyazakkizojwkuzcacnbdifesoiesmkbyffcxhqgqyhwyubtsrqarqagogrnaxuzyggknksrfdrmnoxrctntngdxxechxrsbyhtlbmzgmcqopyixdomhnmvnsafphpkdgndcscbwyhueytaeodlhlzczmpqqmnilliydwtxtpedbncvsqauopbvygqdtcwehffagxmyoalogetacehnbfxlqhklvxfzmrjqofaesvuzfczeuqegwpcmahhpzodsmpvrvkzxxtsdsxwixiraphjlqawxinlwfspdlscdswtgjpoiixbvmpzilxrnpdvigpccnngxmlzoentslzyjjpkxemyiemoluhqifyonbnizcjrlmuylezdkkztcphlmwhnkdguhelqzjgvjtrzofmtpuhifoqnokonhqtzxmimp"
"xjtuwbmvsdeogmnzorndhmjoqnqjnhmfueifqwleggctttilmfokpgotfykyzdhfafiervrsyuiseumzmymtvsdsowmovagekhevyqhifwevpepgmyhnagjtsciaecswebcuvxoavfgejqrxuvnhvkmolclecqsnsrjmxyokbkesaugbydfsupuqanetgunlqmundxvduqmzidatemaqmzzzfjpgmhyoktbdgpgbmjkhmfjtsxjqbfspedhzrxavhngtnuykpapwluameeqlutkyzyeffmqdsjyklmrxtioawcrvmsthbebdqqrpphncthosljfaeidboyekxezqtzlizqcvvxehrcskstshupglzgmbretpyehtavxegmbtznhpbczdjlzibnouxlxkeiedzoohoxhnhzqqaxdwetyudhyqvdhrggrszqeqkqqnunxqyyagyoptfkolieayokryidtctemtesuhbzczzvhlbbhnufjjocporuzuevofbuevuxhgexmckifntngaohfwqdakyobcooubdvypxjjxeugzdmapyamuwqtnqspsznyszhwqdqjxsmhdlkwkvlkdbjngvdmhvbllqqlcemkqxxdlldcfthjdqkyjrrjqqqpnmmelrwhtyugieuppqqtwychtpjmloxsckhzyitomjzypisxzztdwxhddvtvpleqdwamfnhhkszsfgfcdvakyqmmusdvihobdktesudmgmuaoovskvcapucntotdqxkrovzrtrrfvoczkfexwxujizcfiqflpbuuoyfuoovypstrtrxjuuecpjimbutnvqtiqvesaxrvzyxcwslttrgknbdcvvtkfqfzwudspeposxrfkkeqmdvlpazzjnywxjyaquirqpinaennweuobqvxnomuejansapnsrqivcateqngychblywxtdwntancarldwnloqyywrxrganyehkglbdeyshpodpmdchbcc"

yeah.. I think I could bottom up and get the results but seem like the memory could be under pressure as well..
so checked the hints... 

- We can find the length of the longest common subsequence between str1[i:] and str2[j:] (for all (i, j)) by using dynamic programming.
- We can use this information to recover the shortest common supersequence.

interesting.. 
str1 = "abac", str2 = "cab"

lcs would be "ab" then I patch the rest in?
not that easy?

i think 
- get the lcs
- use one str, str1 as the base
- treat str2 as left of lcs, right of lcs, in the middle of lcs
    left part, add to the front
    right part, add to the end
    middle part, hmm... need to also add after the corresponding char in str1...

or.. get the indexes of all the lcs char in both
(i1,j1), (i2,j2)... (in,jn)

then <i1 and <j1.. go the front.. in any order.. doesn't matter
followed by str1[i1] (or str2[j1])..
then <i2 and <j2.. go next.. in any order.. 
follower by ...

okay... 

hmm... maybe I overthink.. 
the hints are not about getting all the exact lcs, not to details of their exact locations
but to get the length of lcs.. and use that information to recover shortest commen superseq..

hmm... how to???

str1 = "abac"
str2 = "cab"
lets say

dp[0,0] = 2
what does that mean? standing at the begining, lcs is 2..
then 
    if str1[i] == str2[j]
        then this has to be one of lcs..
        means? this char just goes into res
    else:
        dp[0,1] = 2
        vs
        dp[1,0] = 1
        how can I use this?

        I want to get the shortest common super seq.. I should use the longest common sub seq
        then I need to patch the minimal
        thus here I choose going to dp[0,1] thus I take str2[j]

I can build the dp this way

    "" c a b
""  0  0 0 0
a   0
b   0
a   0
c   0

        for i in range(1,len(str2)+1):
            for j in range(1, len(str1)+1):
                if str1[i-1] == str2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

then I leave the information to the end..
but I kind of want to leave it to the fron.. 

okay.. just put the seed to the right/botton..

    c a b ""
a         0 
b         0
a         0
c         0
""  0 0 0 0

"""


class Solution:
    def shortestCommonSupersequence(self, str1: str, str2: str) -> str:
        dp = [[0]*(len(str2)+1) for _ in range(len(str1)+1)]

        for i in range(len(str1)-1,-1,-1):
            for j in range(len(str2)-1,-1,-1):
                if str1[i] == str2[j]:
                    dp[i][j] = dp[i+1][j+1] + 1
                else:
                    dp[i][j] = max(dp[i+1][j], dp[i][j+1])
        
        i=j=0
        res=""
        while i<len(str1) and j<len(str2):
            if str1[i]==str2[j]:
                res+=str1[i]
                i+=1
                j+=1
            else:
                if dp[i+1][j] > dp[i][j+1]:
                    res+=str1[i]
                    i+=1
                else:
                    res+=str2[j]
                    j+=1
        
        res += str1[i:] + str2[j:]
        return res

"""
Runtime: 376 ms, faster than 90.89% of Python3 online submissions for Shortest Common Supersequence .
Memory Usage: 22 MB, less than 67.08% of Python3 online submissions for Shortest Common Supersequence .

keep longest common subseq to get short common superseq... hmm..
"""



if __name__ == '__main__':
    str1 = "atdznrqfwlfbcqkezrltzyeqvqemikzgghxkzenhtapwrmrovwtpzzsyiwongllqmvptwammerobtgmkpowndejvbuwbporfyroknrjoekdgqqlgzxiisweeegxajqlradgcciavbpgqjzwtdetmtallzyukdztoxysggrqkliixnagwzmassthjecvfzmyonglocmvjnxkcwqqvgrzpsswnigjthtkuawirecfuzrbifgwolpnhcapzxwmfhvpfmqapdxgmddsdlhteugqoyepbztspgojbrmpjmwmhnldunskpvwprzrudbmtwdvgyghgprqcdgqjjbyfsujnnssfqvjhnvcotynidziswpzhkdszbblustoxwtlhkowpatbypvkmajumsxqqunlxxvfezayrolwezfzfyzmmneepwshpemynwzyunsxgjflnqmfghsvwpknqhclhrlmnrljwabwpxomwhuhffpfinhnairblcayygghzqmotwrywqayvvgohmujneqlzurxcpnwdipldofyvfdurbsoxdurlofkqnrjomszjimrxbqzyazakkizojwkuzcacnbdifesoiesmkbyffcxhqgqyhwyubtsrqarqagogrnaxuzyggknksrfdrmnoxrctntngdxxechxrsbyhtlbmzgmcqopyixdomhnmvnsafphpkdgndcscbwyhueytaeodlhlzczmpqqmnilliydwtxtpedbncvsqauopbvygqdtcwehffagxmyoalogetacehnbfxlqhklvxfzmrjqofaesvuzfczeuqegwpcmahhpzodsmpvrvkzxxtsdsxwixiraphjlqawxinlwfspdlscdswtgjpoiixbvmpzilxrnpdvigpccnngxmlzoentslzyjjpkxemyiemoluhqifyonbnizcjrlmuylezdkkztcphlmwhnkdguhelqzjgvjtrzofmtpuhifoqnokonhqtzxmimp"
    str2="xjtuwbmvsdeogmnzorndhmjoqnqjnhmfueifqwleggctttilmfokpgotfykyzdhfafiervrsyuiseumzmymtvsdsowmovagekhevyqhifwevpepgmyhnagjtsciaecswebcuvxoavfgejqrxuvnhvkmolclecqsnsrjmxyokbkesaugbydfsupuqanetgunlqmundxvduqmzidatemaqmzzzfjpgmhyoktbdgpgbmjkhmfjtsxjqbfspedhzrxavhngtnuykpapwluameeqlutkyzyeffmqdsjyklmrxtioawcrvmsthbebdqqrpphncthosljfaeidboyekxezqtzlizqcvvxehrcskstshupglzgmbretpyehtavxegmbtznhpbczdjlzibnouxlxkeiedzoohoxhnhzqqaxdwetyudhyqvdhrggrszqeqkqqnunxqyyagyoptfkolieayokryidtctemtesuhbzczzvhlbbhnufjjocporuzuevofbuevuxhgexmckifntngaohfwqdakyobcooubdvypxjjxeugzdmapyamuwqtnqspsznyszhwqdqjxsmhdlkwkvlkdbjngvdmhvbllqqlcemkqxxdlldcfthjdqkyjrrjqqqpnmmelrwhtyugieuppqqtwychtpjmloxsckhzyitomjzypisxzztdwxhddvtvpleqdwamfnhhkszsfgfcdvakyqmmusdvihobdktesudmgmuaoovskvcapucntotdqxkrovzrtrrfvoczkfexwxujizcfiqflpbuuoyfuoovypstrtrxjuuecpjimbutnvqtiqvesaxrvzyxcwslttrgknbdcvvtkfqfzwudspeposxrfkkeqmdvlpazzjnywxjyaquirqpinaennweuobqvxnomuejansapnsrqivcateqngychblywxtdwntancarldwnloqyywrxrganyehkglbdeyshpodpmdchbcc"
    print(Solution().shortestCommonSupersequence(str1, str2))