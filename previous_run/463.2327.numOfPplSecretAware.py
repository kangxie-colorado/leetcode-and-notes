"""
https://leetcode.com/problems/number-of-people-aware-of-a-secret/

interesting.. iq test
so it is obvious that

if I say dp[i] represents on i-th day, the people aware
forget[i] represents on i-th day, the people forgets

then dp[i] = (dp[i-1] - forget[i])*2
i.e. on i-1_th day.. there were dp[i-1] people aware
    if they don't forget, they will just notify dp[i-1] more person
    but some of them will forget on i-th day.. 
    so on i-th day.. the seed is dp[i-1] - forget[i]

and how to get forget[i]
    notice that it is equal to learn[i-forget]
    i.e on i-forget_th day, learn[i-forget] people learned secrect 
    they will forget on i-th day

so we need this learn[i] as well
    
    learn[i] = dp[i]...? not complete yet

    but notice the dp[i-1] is not necessarily the share-able person.. (the delay)
    so how many people can share

    share[i] = dp[i] + learn[i-delay]
    learn[i] = share[i-1] - forget[i]

holy shit!!!!

======== recap wait

shares[i]: represents on i-th day, how many people can share the secret
learns[i]: represents on i-th day, how many people can learn the secret
forgets[i]: on i-th day, how many people will forget

basically

forgets[i] = learns[i-forget]: people learned on i-forget day (e.g. day1) will forget on day i(i+forget)
delays[i] = learns[i-delay+1] XXXX
shares[i] = learns[i-delay] + shares[i-1] - forgets[i] = learns[i-delay] + shares[i-1] - learns[i-forget]
learns[i] = shares[i] 

delays[i] is not correct I think
it should/might be
delays[i] = delays[i-1] - learns[i-delay]
    the delaying poeple from i-1 day minus the people who can share (learned i-delay dayes ago..)

    still not right
delays[i] = learns[i] + delays[i-1] - learns[i-delay]
    who learns today also begin delaying


aware people = delay+share (or delay+learn)

so okey recap

the dependency is 

    forgets[i] = learns[i-forget] # no dependency on i-th element
        if i<=forget, 0
    shares[i] = learns[i-delay] + shares[i-1]-forgets[i] # depends on forgets[i]
        ditto for i<=delay, learns[i-delay] will be 0
    
    learns[i] = shares[i] # how many people can share, how many people can learn
        seed: learns[1] = 1
    delays[i] = learns[i] + delays[i-1] - learns[i-delay] 
        today's new learners, and last day's learner minus the ones that becomes sharers 

very complicated!!!!
but run thru the examples and correct

"""


from collections import deque


class Solution:
    def peopleAwareOfSecret(self, n: int, delay: int, forget: int) -> int:
        forgets = [0]*(n+1)
        shares = [0]*(n+1)
        learns = [0]*(n+1)
        delays = [0]*(n+1)
        mod = 10**9+7
        # delay+share will be the people aware (delay has factored in the learner)

        for i in range(1,n+1):
            # forgets
            #     forgets[i] = learns[i-forget]  # no dependency on i-th element
            #     if i <= forget, 0
            if i<=forget:
                forgets[i] = 0
            else:
                forgets[i] = learns[i-forget]

            # shares
            #     shares[i] = learns[i-delay] + shares[i-1] - forgets[i]  # depends on forgets[i]
            #     ditto for i <= delay, learns[i-delay] will be 0
            if i<=delay:
                shares[i] = shares[i-1]-forgets[i]
            else:
                shares[i] = learns[i-delay] + shares[i-1]-forgets[i]
            shares[i] %= mod

            # learns
            if i==1:
                learns[i] = 1
            else:
                learns[i] = shares[i]

            # delays
            #     delays[i] = learns[i] + delays[i-1] - learns[i-delay]
            #     today's new learners, and last day's learner minus the ones that becomes sharers
            if i <= delay:
                delays[i] = learns[i] + delays[i-1]
            else:
                delays[i] = learns[i] + delays[i-1] - learns[i-delay]
        
        return (delays[n] + shares[n]) % mod

"""
Runtime: 47 ms, faster than 68.18% of Python3 online submissions for Number of People Aware of a Secret.
Memory Usage: 13.9 MB, less than 59.55% of Python3 online submissions for Number of People Aware of a Secret.

let me try queue idea

think each number is a number.. reach mod back to 1
put it into delay queue.. (maybe in the format of (day,seq))
    when day diff is > delay.. put it into share queue
    when day diff is > forget.. discard that

    we only need to keep the batch size.. as any item.. 
    let me see.. 

"""


class Solution:
    def peopleAwareOfSecret(self, n: int, delay: int, forget: int) -> int:
        delayQ = deque()
        shareQ = deque()
        batchSize = 1
        queueTotalBatch = 0
        forgets = 0
        seq = 1


        # day1
        delayQ.append((1, batchSize))

        for day in range(2, n+1):
            while delayQ and day == delay+delayQ[0][0]:
                d, bs = delayQ.popleft()
                shareQ.append((d, bs))
                queueTotalBatch += bs

            while shareQ and day == forget+shareQ[0][0]:
                _, bs = shareQ.popleft()
                forgets += bs
                queueTotalBatch -= bs

            if shareQ:
                bs = queueTotalBatch
                seq += bs
                delayQ.append((day, bs))
        return seq - forgets

"""
Runtime: 44 ms, faster than 72.77% of Python3 online submissions for Number of People Aware of a Secret.
Memory Usage: 14 MB, less than 38.39% of Python3 online submissions for Number of People Aware of a Secret.
"""


class Solution:
    def peopleAwareOfSecret(self, n: int, delay: int, forget: int) -> int:
        delayQ = deque()
        shareQ = deque()
        batchSize = 1
        shareQTotal = 0
        delayQTotal = 1
        mod = 10**9 + 7

        # day1
        delayQ.append((1, batchSize))

        for day in range(2, n+1):
            while delayQ and day == delay+delayQ[0][0]:
                d, bs = delayQ.popleft()
                shareQ.append((d, bs))
                shareQTotal += bs
                delayQTotal -= bs

            while shareQ and day == forget+shareQ[0][0]:
                _, bs = shareQ.popleft()
                shareQTotal -= bs

            if shareQ:
                bs = shareQTotal
                delayQ.append((day, bs))
                delayQTotal += bs
            
            shareQTotal %= mod
            delayQTotal %= mod

        return (delayQTotal + shareQTotal)%mod

"""
Runtime: 39 ms, faster than 86.61% of Python3 online submissions for Number of People Aware of a Secret.
Memory Usage: 14 MB, less than 59.82% of Python3 online submissions for Number of People Aware of a Secret.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.peopleAwareOfSecret(n=4, delay=1, forget=3))
    print(s.peopleAwareOfSecret(n=6, delay=2, forget=4))
