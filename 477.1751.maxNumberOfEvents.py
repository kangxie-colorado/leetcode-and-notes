"""
https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended-ii/?envType=study-plan&id=dynamic-programming-iii

so there is this k limits
if k=1, then I pick the max value event -- simple 
if k>1, then I pick up to k events that are not overlapping and providing max value 

so I think for each event I can 
    either choose to attend 
    or not 

this gives some properties like 

1. sort the event
2. f(i,k): at i-th event left event budget is k
    take it: v + f(i+1,k-1)
        there is a catch.. if it doesn't overlap with earlier event 
        so I sort the event by ending time.. and looking back 
        or by starting time.. 
        maybe not a diff..
        just sort it and looking back hmm...
    not take it: f(i+1,k)

    taking max of it
    when k==0, or i==l, return 0 

this could TLE but at least get me going for a start
Now I limit myself to 1.5hrs leetcoding 

I shall not beat myself too much
"""


import bisect
from linecache import cache
from typing import List


class Solution:
    def maxValue(self, events: List[List[int]], k: int) -> int:
        events.sort()

        def f(i, k, attended):
            if k == 0 or i == len(events):
                return 0

            idx = bisect.bisect_left(attended, events[i][0])
            if idx % 2 != 0 or (idx < len(attended) and attended[idx] == events[i][0]):
                # it landed in some previous event - cannot take it
                return f(i+1, k, attended)
            else:
                # it could be taken or not

                return max(f(i+1, k-1, attended+events[i][:2]) + events[i][2], f(i+1, k, attended))

        return f(0, k, [])


"""
hmm.. this non-overlapping rule makes this route hard 
it will not be able to pass in any sense..

anyway.. let me just get a few cases to work first 

cool.. 64 / 67 test cases passed.
TLE..

okay.. I think this is telling me it is O(k*N)
1 <= k * events.length <= 106


kanpsack proble m? 
hmm..
I at least see one place I can simplify

no need to call the notAttending branch twice 
"""


class Solution:
    def maxValue(self, events: List[List[int]], k: int) -> int:
        events.sort()

        def f(i, k, attended):
            if k == 0 or i == len(events):
                return 0

            notAttending = f(i+1, k, attended)
            attending = 0

            if not attended:
                attending = f(i+1, k-1, attended+events[i][:2]) + events[i][2]
            else:
                idx = bisect.bisect_left(attended, events[i][0])

                if (idx == len(attended)) or (idx % 2 == 0 and attended[idx] != events[i][0]):
                    attending = f(i+1, k-1, attended +
                                  events[i][:2]) + events[i][2]

            return max(notAttending, attending)

        return f(0, k, [])

"""
same.. 
so I cannot cache.. can I change it to backtrack?

"""


class Solution:
    def maxValue(self, events: List[List[int]], k: int) -> int:
        events.sort()
        attended = []

        def f(i, k):
            if k == 0 or i == len(events):
                return 0

            notAttending = f(i+1, k)
            attending = 0

            nonlocal attended
            idx = bisect.bisect_left(attended, events[i][0])
            if not attended or (idx == len(attended)) or (idx % 2 == 0 and attended[idx] != events[i][0]):
                attended.extend(events[i][:2])
                attending = f(i+1, k-1) + events[i][2]
                attended = attended[:-2]

            return max(notAttending, attending)

        return f(0, k)

"""
adding cache it goes wrong
yeah.. the attended is indeed one of the states..

so what is the outlet of this kind of problem?
maybe not to this property issue... 

hints 

- Sort the events by its startTime.
- For every event, you can either choose it and consider the next event available, or you can ignore it. 
    You can efficiently find the next event that is available using binary search.

hmm... 
so after I book an event.. I lookup its end in the sorted array... 
using bisect_right to filter all the overlapping events 

e.g.  [[1,2,4],[3,4,3],[2,3,1]]
after sort: [[1, 2, 4], [2, 3, 1], [3, 4, 3]]
after processing first one
I can search for 2+1=3 [3,3,0] with bisect_left.. it will land on idx-2
then I know that is next interval to consider.. ahah...
"""


class Solution:
    def maxValue(self, events: List[List[int]], k: int) -> int:
        events.sort()

        def f(i, k, attended):
            if k == 0 or i == len(events):
                return 0

            notAttending = f(i+1, k, attended)

            # search next attendable event if I attend this one
            idx = bisect.bisect_left(events, [events[i][1]+1,0,0])
            attending = f(idx, k-1, attended+events[i][:2]) + events[i][2]

            return max(notAttending, attending)

        return f(0, k, [])

"""
still not passing.. 
hold one.. 
do I need attended in this version? naha
"""


class Solution:
    def maxValue(self, events: List[List[int]], k: int) -> int:
        events.sort()

        @cache
        def f(i, k):
            if k == 0 or i == len(events):
                return 0

            notAttending = f(i+1, k)

            # search next attendable event if I attend this one
            idx = bisect.bisect_left(events, [events[i][1]+1, 0, 0])
            attending = f(idx, k-1) + events[i][2]

            return max(notAttending, attending)

        return f(0, k)

"""
Runtime: 945 ms, faster than 67.16% of Python3 online submissions for Maximum Number of Events That Can Be Attended II.
Memory Usage: 192.4 MB, less than 28.92% of Python3 online submissions for Maximum Number of Events That Can Be Attended II.

want to convert to bottom up dp
2D DP.. 

dp[i][k] = max(
    dp[i+1,k]
    dp[idx,k-1]
)

results is in dp[0,k]

because i depends on i+1, so scan from bottom to up
because k depends on k-1, so scan from left to right

Input: events = [[1,2,4],[3,4,3],[2,3,1]], k = 2
    k
    0 1 2
i 0 0
  1 0
  2 0
  3 0 0 0 <- i==len()
    ^
    k==0

"""


class Solution:
    def maxValue(self, events: List[List[int]], k: int) -> int:
        n = len(events)
        events.sort()
        leapTo = [-1]*n

        for i, (_,e,_) in enumerate(events):
            leapTo[i] = bisect.bisect_left(events, [e+1, 0, 0])
        
        dp = [[0]*(k+1) for _ in range(n+1)]
        for i in range(n-1,-1,-1):
            for j in range(1,k+1):
                dp[i][j] = max(dp[i+1][j], dp[leapTo[i]][j-1]+events[i][2])
        
        return dp[0][k]

"""
Runtime: 1191 ms, faster than 46.00% of Python3 online submissions for Maximum Number of Events That Can Be Attended II.
Memory Usage: 60.1 MB, less than 85.00% of Python3 online submissions for Maximum Number of Events That Can Be Attended II.


okay.. cool

okay.. last hour of the day.. spend to watch TDD pt2 maybe
after all.. that sesssion I am not totally fresh.. I knew quite a bit..
"""

if __name__ == '__main__':
    s = Solution()
    events = [[609160999,612582699,443422],[947166815,953380719,500128],[509665293,518745581,149858],[625034765,625478636,483866],[781784820,782291828,143346],[174077331,177609753,180156],[800863484,802150672,320499],[379280423,386305516,744771],[972166957,973110948,79556],[692103213,692598640,469358],[108578958,116774463,345270],[256592151,260217350,664230],[268985479,286614436,166394],[42376830,44672481,667237],[530474061,531435025,452033],[180856546,188537226,395742],[338388551,342982219,401949],[507351469,507913727,549999],[154302831,156765309,406069],[290607284,300207459,948892],[888281045,892881727,248408],[446315936,447061616,104646],[815494172,825477446,398940],[756050332,776209136,521588],[779316632,779549080,963107],[869704183,872729766,5720],[462503443,469555485,895241],[693441085,694978338,185090],[841934770,868854132,55140],[989043039,989602115,353190],[900176469,902174676,79381],[474974825,479638162,503580],[304661378,309185429,599881],[684127403,687829874,472919],[351618428,354094470,598001],[973498017,974205681,946253],[210602172,217465066,704733],[420357195,433111080,52113],[563437917,575174843,702873],[804172347,805364877,714162],[458919059,462050133,35108],[9000788,13150406,652181],[35828449,39094628,145541],[959143837,968532446,617744],[631923914,640240749,156275],[953553442,954876995,989019],[875555671,887619098,895006],[699569058,703133773,404319],[54860536,59914250,76485],[922504737,924918759,33579],[260430887,260483505,177717],[227082211,227559556,413159],[335782302,336897527,679183],[697081841,697880997,396999],[368668959,371316049,731831],[560095497,560975547,711041],[681339475,684097936,419920],[309355796,314934275,127300],[262996731,267567670,375651],[195847429,195906540,855488],[656383532,680387682,487017],[598421277,607100426,384007],[170054420,173421313,337141],[236881563,238498845,879035],[244664075,250331115,280780],[825480669,829419535,98586],[984255323,986838580,915106],[523252252,523269720,896046],[577361186,579854206,687101],[74202559,74304669,654998],[493376690,501763167,566016],[66486085,68558701,116854],[753219176,755396614,413036],[403217227,412032555,364961],[730136072,739387262,15180],[538674042,546547794,283571],[990161375,994240716,486296],[287295040,290465999,253402],[127475277,131381124,459808],[69961343,70828607,437234],[448033366,450427314,576909],[581073127,583845957,819991],[649107027,653839062,114275],[72670974,72791272,208621],[434126470,435830132,647362],[795717304,799240429,774654],[90483158,96047309,785088],[588970519,595272687,241911],[80939799,81840097,900259],[333231653,334320961,415819],[251486136,251901288,854597],[140956566,152440434,418734],[100247381,105571047,758200],[695750330,696415680,461183],[918078263,918890629,26172],[906947242,912435095,769132],[750796382,751146332,766352],[932653715,943945433,151639],[787417692,790849298,545930],[479778644,481390273,245309]]
    k = 50
    print(s.maxValue(events, k))