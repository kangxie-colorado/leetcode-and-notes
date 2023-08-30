def f(count, blood, dead, times):
    minTimes = float('inf')
    def h(blood, dead, times):
        nonlocal minTimes
        if times >= minTimes:
            return
        if dead>=2:
            minTimes = min(minTimes, times)
            return 
            

        # backtrack?
        # can choose 0, count-1 to cut 1
        res = float('inf')

        for i in range(count):
            bloodCp = list(blood)
            if bloodCp[i]>0:
                bloodCp[i] -= 1
                newDead = (bloodCp[i] == 0)
            if i < count-1 and bloodCp[i+1]>0:
                bloodCp[i+1] -= 2
                newDead += (bloodCp[i+1] in [0, -1])
            
            h(bloodCp, dead+newDead, times+1)
    h(blood, 0,0)
    return minTimes

def f(count, bloods):
    choices = []
    for i in range(1,count):
        times = (bloods[i]+1)//2
        take = 0 if times>=bloods[i-1] else 1 # 0: take the front with it

        choices.append((times,take))
    
    choices.sort()
    res = choices[0][0] + choices[1][0]
    for times,take in choices:
        if take == 0 and times < res:
            return times

    return res

print(f(4,[2,3,2,5]))
print(f(8, [5, 10, 1, 6, 3, 2, 3, 3]))

        

