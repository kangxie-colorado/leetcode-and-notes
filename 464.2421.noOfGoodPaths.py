"""
https://leetcode.com/problems/number-of-good-paths/

okay.. think naively I can run union find

fix a point.. union find all nodes, whose weight <= start weight
if find an equal weight node.. then that is an extra path

processed weight no need to process again
so on and so such... 

but I guess it will TLE and there can be optimization because you can create the unoin from lower weight to higher weight
let me start the naive thoughts first

hmm.. hold on.. union find.. doesn't seem to work smoothly
even eqaul weight.. it might be able to connect thru

actually I connect and count how many nodes are connected together then compute the path

because if 2 such node.. then 1 extra
if 3 such nodes.. then??? 
    1-1-1: 3 extra (3*2//2)
    1-1-1-1: 6 extra (any two nodes can make an extra, 4*3//2)
"""


from collections import defaultdict
from typing import List


class Solution:
    def numberOfGoodPaths(self, vals: List[int], edges: List[List[int]]) -> int:
        n = len(vals)
        processedNode = set()

        def goodPaths(weight, node):
            roots = [i for i in range(n)]

            def find(x):
                if roots[x] != x:
                    roots[x] = find(roots[x])
                return roots[x]

            def union(x, y):
                roots[find(x)] = roots[find(y)]

            for n1, n2 in edges:
                if max(vals[n1], vals[n2]) <= weight:
                    union(n1, n2)

            equalNodes = 0
            
            for i in range(n):
                if find(i) == find(node) and vals[i] == weight:
                    processedNode.add(i)
                    equalNodes += 1

            return equalNodes*(equalNodes-1)//2

        extraGoodPaths = 0
        for node, weight in enumerate(vals):
            if node in processedNode:
                continue
            extraGoodPaths += goodPaths(weight, node)

        return extraGoodPaths + n

"""
not super bad

110 / 134 test cases passed and TLE
results is good so main algorithm is okay..

now let me think optmization
if sort the vals (val,node) and process lower val nodes first, can I utilize previous computaion for later?

seems like I need to create the graph
and then adding edges?

or I can add weight to edges.. (the max val of one end is the weight of edges)
sort the edges.. and start from there??

seems possible nut not fully clear yet

so 
    1. I sort the nodes by weight
    2. I add weight to edges and sort them by weight

start from node
    process edges upto its weight
    union-find them.. same idea.. see the extra path in its subcomponent
    adding connected equal weighted nodes to processedNodes

move to next node
    could be same weight or bigger
    if same.. weight no need to move edge point
    if bigger.. add edges until it is bigger

seems like possible

"""


class Solution:
    def numberOfGoodPaths(self, vals: List[int], edges: List[List[int]]) -> int:
        n = len(vals)
        processedNode = set()

        roots = [i for i in range(n)]
        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x, y):
            roots[find(x)] = roots[find(y)]

        nodeWeights = sorted([(weight,node) for node,weight in enumerate(vals)])
        weightedEdges = sorted([ (max(vals[n1], vals[n2]), n1,n2) for n1,n2 in edges  ])

        nodePtr = edgePtr = 0
        res = 0
        
        equalWeightsNodes = set()
        while nodePtr < n:
            weight, node = nodeWeights[nodePtr]

            if node in processedNode:
                nodePtr += 1
                continue

            if nodePtr > 0 and nodeWeights[nodePtr-1][0] != weight:
                equalWeightsNodes = set()

            while edgePtr < n-1 and weightedEdges[edgePtr][0] <= weight:
                # add all the equal or smaller edges or possible no edges
                _, n1,n2 = weightedEdges[edgePtr]
                union(n1,n2)
                equalWeightsNodes.add(n1)
                equalWeightsNodes.add(n2)
                edgePtr += 1
            
            # now search if any equal weight node connected with 
            equalNodes = 0
            for i in equalWeightsNodes:
                if find(i) == find(node) and vals[i] == weight:
                    processedNode.add(i)
                    equalNodes += 1
            
            res += equalNodes*(equalNodes-1)//2
            nodePtr += 1
        return res + n


"""
somewhere I have off by 1
I think it is in the visitedNodes here..

thanks to leetcode debugger
some smaller case reproducing the errors 

[16,16,16,6,12,9,6,2,17,7,5,15,6,3,14,6,16]
[[1,0],[2,0],[3,1],[0,4],[5,1],[4,6],[2,7],[8,3],[9,1],[10,1],[11,2],[6,12],[13,0],[7,14],[15,11],[12,16]]

[16,16,16,6,12,9,6,2,17,7,5,15,6,3]
[[1,0],[2,0],[3,1],[0,4],[5,1],[4,6],[2,7],[8,3],[9,1],[10,1],[11,2],[6,12],[13,0]]

right here
[16,16,16,6,12,9,6,2,17,7,5]
[[1,0],[2,0],[3,1],[0,4],[5,1],[4,6],[2,7],[8,3],[9,1],[10,1]]

right here
[16,16,16,6,12,9,6,2,17,7,5,15]
[[1,0],[2,0],[3,1],[0,4],[5,1],[4,6],[2,7],[8,3],[9,1],[10,1],[11,2]]

wrong here..
[16,16,16,6,12,9,6,2,17,7,5,15,6]
[[1,0],[2,0],[3,1],[0,4],[5,1],[4,6],[2,7],[8,3],[9,1],[10,1],[11,2],[6,12]]

okay.. gives me a chance to debug
this graph is not super complicated..

let me go for a walk then back to debug.. 
shit.. the day has passed almost

okay.. my capacity is really low today..
a logical error 
fix that and now errors are different 

[2,5,5,1,5,2,3,5,1,5]
[[0,1],[2,1],[3,2],[3,4],[3,5],[5,6],[1,7],[8,4],[9,7]]
30 vs 20(expected)

Runtime: 2324 ms, faster than 59.98% of Python3 online submissions for Number of Good Paths.
Memory Usage: 52.8 MB, less than 16.89% of Python3 online submissions for Number of Good Paths.


ah.. okay.. the main line is totally right
I just had a couple of coding errors..

i ma exhausted
"""


class Solution:
    def numberOfGoodPaths(self, vals: List[int], edges: List[List[int]]) -> int:
        n = len(vals)
        processedNode = set()

        roots = [i for i in range(n)]

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x, y):
            roots[find(x)] = roots[find(y)]

        nodeWeights = sorted([(weight, node)
                             for node, weight in enumerate(vals)])
        weightedEdges = sorted(
            [(max(vals[n1], vals[n2]), n1, n2) for n1, n2 in edges])

        edgeIdx = 0
        res = 0

        equalWeightsNodes = set()
        
        for idx, (weight, node) in enumerate(nodeWeights):
            if node in processedNode:
                continue

            if idx > 0 and nodeWeights[idx-1][0] != weight:
                equalWeightsNodes = set()

            while edgeIdx < n-1 and weightedEdges[edgeIdx][0] <= weight:
                # add all the equal or smaller edges or possible no edges
                _, n1, n2 = weightedEdges[edgeIdx]
                union(n1, n2)
                equalWeightsNodes.add(n1)
                equalWeightsNodes.add(n2)
                edgeIdx += 1

            # now search if any equal weight node connected with
            equalNodes = 0
            for i in equalWeightsNodes:
                if find(i) == find(node) and vals[i] == weight:
                    processedNode.add(i)
                    equalNodes += 1

            res += equalNodes*(equalNodes-1)//2
        return res + n



if __name__ == '__main__':
    s = Solution()

    vals = [16,16,16,6,12,9,6,2,17,7,5,15,6]
    edges = [[1,0],[2,0],[3,1],[0,4],[5,1],[4,6],[2,7],[8,3],[9,1],[10,1],[11,2],[6,12]]
    print(s.numberOfGoodPaths(vals, edges))

    # vals = [16,16,16,6,12,9,6,2,17,7,5,15,6,3,14,6,16,3,16,11,9,4,15,16,2,12,7,7,9,7,3,8,4,13,8,4]
    # edges = [[1,0],[2,0],[3,1],[0,4],[5,1],[4,6],[2,7],[8,3],[9,1],[10,1],[11,2],[6,12],[13,0],[7,14],[15,11],[12,16],[17,1],[11,18],[19,11],[20,12],[21,0],[22,18],[23,2],[24,2],[25,21],[10,26],[27,25],[17,28],[19,29],[5,30],[31,8],[32,13],[20,33],[21,34],[35,15]]
    # print(s.numberOfGoodPaths(vals, edges))

    # print(s.numberOfGoodPaths( vals = [1,3,2,1,3], edges = [[0,1],[0,2],[2,3],[2,4]]))
    # vals = [5592,9420,8301,5854,3436,4562,2436,5525,9403,9485,4094,4468,9751,8543,5747,5203,9914,9736,1622,8069,3991,1634,8978,3710,1390,7256,9150,58,5673,125,5752,2905,8397,9430,2996,6810,8991,2317,4715,9335,6862,5103,192,2950,9531,1039,3433,2309,415,4242,6678,7202,5531,9489,9296,9383,6697,3751,7019,4674,9922,5274,7142,3557,4100,5813,9137,7077,2536,1240,1153,6763,6308,2019,5291,4338,4159,8106,4775,45,3545,8195,7709,6540,1162,6634,5703,3452,8592,9724,7760,7475,3134,9264,393,9641,5077,8813,3811,5146,3076,677,9763,3805,9502,1182,5571,8419,4435,83,9507,615,3444,2145,6266,7386,5941,1216,4734,9328,8490,1434,349,9511,3437,3584,7773,489,2692,3624,650,5463,536,8960,3195,1839,16,7236,3648,9755,9170,7380,2348,7402,9979,5058,9043,8279,8677,9312,313,1760,5723,1719,9346,6978,6245,8274,8159,7266,5019,9043,5933,1923,8381,5175,5437,6927,7446,1499,82,6554,4328,1025,8954,1483,2037,8254,3531,1851,2301,6744,7053,5591,6723,346,4968,974,175,3776,8888,7074,1021,2966,9502,4474,3576,9547,6580,3629,6284,1457,4741,9254,7411,4068,2196,1337,5845,6209,2792,7122,1755,5143,311,401,9539,3603,1233,3607,703,8144,1205,3254,4937,2998,9610,8005,7424,6339,6253,6363,6630,4088,299,3911,332,3569,3399,7277,8190,2698,3358,9675,3029,6083,5834,1497,6016,9597,923,9632,2789,2836,9034,4189,1870,2811,8441,2634,1134,6722,5128,9439,847,4909,6582,4436,3986,9687,8400,862,2622,6964,5193,9636,1223,5338,3398,9795,8530,8387,4042,8477,1653,9788,2141,5917,173,3371,7722,6099,669,9589,3504,175,4453,8781,4574,8305,337,767,4078,8432,1901,8468,4004,8738,9777,625,7293,3139,9669,7509,1073,7583,6959,3786,5451,3194,7265,133,8972,7506,9933,1582,8671,6619,8945,754,8261,1782,1041,1869,7971,6830,5260,4616,5694,1436,6692,4154,8620,49,7314,5018,590,528,9414,4334,7533,2015,4230,1105,4228,3432,3143,9214,5662,4144,8084,4079,9865,797,8932,7040,8025,5143,1015,3559,2386,4240,5833,9742,6135,3273,9988,283,2808,1134,645,5901,203,5318,91,7745,8358,4171,6164,8814,6974,1932,4426,147,2656,5548,9517,771,5266,638,6290,1458,874,818,3898,5876,7817,9566,3149,1396,2693,6462,4608,4266,7224,2805,9621,7014,1934,8283,5583,3927,5373,3582,8404,5187,4974,2910,4960,5883,8854,8235,5991,2842,664,9145,9078,4080,715,7228,6757,5,1207,9031,6497,8386,989,9373,5976,8262,5236,2263,2188,2064,9626,7755,716,4309,3243,7052,534,9799,4522,7149,1483,6581,5279,3854,3527,9854,4065,6176,3529,3480,6535,6782,9497,5127,3249,5806,8207,1734,6815,3776,3314,9602,3024,6072,5582,1531,802,1176,3406,9023,8199,4056,3230,4901,9834,7453,8372,5238,810,7243,7015,1771,2376,9473,3558,8770,6891,5701,1855,203,8334,6626,6291,8776,5574,5250,689,8308,8382,1481,2571,2897,261,7378,5117,7960,9022,3339,4428,1669,910,9068,2394,7755,1023,7687,7950,1832,5523,4183,3264,8668,7385,7964,4181,9627,4640,2938,8396,4667,4197,4076,2921,1261,8699,7099,3136,7882,7874,2450,8771,4541,5985,6260,9878,368,802,3708,6549,7465,5860,832,6816,6378,4059,1937,1498,1582,2132,5064,2516,4508,8125,3390,2986,7156,2041,6599,9286,4248,9517,1323,9067,301,8782,1511,4846,3839,2844,9214,2026,4977,7118,9718,2638,7311,662,7776,2957,8507,6481,8224,2211,549,9479,3115,3270,6849,809,8004,3102,2578,7377,5029,5155,2316,2802,3922,4376,4864,1013,3950,6199,9209,6874,1881,4442,7439,4348,8265,3549,7445,5152,6893,7146,4641,5221,3039,9277,3652,633,8000,1299,9704,8763,4417,7485,9704,4094,6682,4422,3422,2678,6298,6564,3014,5236,7361,1530,9240,437,1767,4718,4866,6008,4929,3857,3619,9390,5933,2616,2602,8092,4753,1612,7678,5268,9492,1817,3862,3572,28,3704,161,8138,6005,2899,3902,8619,3349,8304,550,9618,5491,7198,4516,5952,9069,4663,962,7868,4512,5768,203,6166,8778,3201,4030,7612,6850,9647,400,7464,9643,7975,1476,1728,4652,9480,8957,3466,6658,7523,8405,252,8851,2972,7059,5531,6397,3904,4002,2852,5105,511,1965,1731,7275,7338,6815,8023,7474,6483,9910,8943,9265,3294,6870,9176,132,8030,9357,3513,9423,7042,3935,62,919,1178,8573,2750,5467,2683,7099,8153,1695,1273,5486,6842,1781,7545,3196,9532,2039,3414,7823,3466,125,8805,6800,3306,8027,4565,5870,171,2687,7775,1286,8594,1500,9230,3596,2285,8599,4036,4379]
    # edges = [[1,0],[1,2],[3,2],[3,4],[5,4],[6,3],[2,7],[2,8],[1,9],[6,10],[10,11],[4,12],[1,13],[13,14],[3,15],[16,0],[4,17],[18,14],[12,19],[3,20],[21,18],[10,22],[23,9],[24,15],[25,8],[9,26],[27,18],[28,9],[29,12],[30,21],[31,2],[19,32],[7,33],[29,34],[20,35],[36,18],[15,37],[38,21],[34,39],[16,40],[36,41],[42,5],[41,43],[44,25],[3,45],[46,35],[47,32],[48,1],[49,20],[50,40],[51,31],[25,52],[25,53],[54,50],[55,46],[56,53],[57,18],[44,58],[53,59],[60,1],[61,12],[38,62],[6,63],[48,64],[65,37],[66,43],[20,67],[28,68],[68,69],[70,1],[71,34],[68,72],[41,73],[27,74],[75,0],[2,76],[77,74],[31,78],[79,73],[46,80],[0,81],[82,36],[49,83],[0,84],[85,72],[28,86],[73,87],[88,32],[89,50],[90,3],[91,62],[15,92],[24,93],[18,94],[95,61],[29,96],[19,97],[98,54],[58,99],[18,100],[93,101],[102,87],[100,103],[94,104],[105,62],[16,106],[107,105],[86,108],[109,79],[110,86],[106,111],[100,112],[113,78],[92,114],[115,23],[116,80],[117,47],[115,118],[89,119],[120,109],[121,26],[122,100],[112,123],[124,21],[9,125],[126,39],[55,127],[128,23],[129,38],[130,18],[33,131],[132,37],[97,133],[15,134],[135,67],[136,106],[137,125],[91,138],[91,139],[140,92],[44,141],[142,55],[73,143],[144,112],[145,39],[24,146],[118,147],[148,102],[149,36],[150,99],[151,149],[134,152],[9,153],[62,154],[155,117],[156,50],[57,157],[121,158],[93,159],[22,160],[161,28],[162,94],[72,163],[132,164],[46,165],[166,57],[139,167],[29,168],[169,74],[170,18],[137,171],[172,57],[173,38],[139,174],[48,175],[43,176],[32,177],[43,178],[179,35],[2,180],[102,181],[182,168],[183,126],[12,184],[185,13],[186,35],[187,49],[53,188],[145,189],[190,18],[191,163],[81,192],[193,91],[73,194],[69,195],[89,196],[197,112],[126,198],[199,15],[200,150],[201,132],[53,202],[164,203],[204,18],[7,205],[52,206],[207,79],[208,86],[203,209],[160,210],[211,183],[212,27],[17,213],[214,93],[215,2],[216,82],[217,78],[46,218],[141,219],[220,52],[102,221],[222,99],[146,223],[78,224],[225,1],[160,226],[191,227],[228,101],[115,229],[140,230],[187,231],[232,102],[210,233],[207,234],[225,235],[71,236],[237,16],[199,238],[239,35],[240,144],[241,109],[26,242],[243,201],[28,244],[245,135],[230,246],[247,231],[248,246],[10,249],[250,34],[85,251],[252,130],[40,253],[25,254],[255,242],[256,179],[51,257],[54,258],[180,259],[27,260],[12,261],[262,197],[171,263],[62,264],[35,265],[161,266],[267,171],[268,79],[40,269],[62,270],[213,271],[133,272],[273,178],[274,264],[220,275],[276,146],[110,277],[278,231],[7,279],[129,280],[281,49],[271,282],[283,43],[66,284],[285,43],[67,286],[287,78],[210,288],[289,175],[290,41],[195,291],[292,127],[114,293],[55,294],[179,295],[17,296],[214,297],[249,298],[299,208],[300,292],[301,69],[149,302],[303,16],[241,304],[66,305],[306,258],[114,307],[187,308],[83,309],[196,310],[109,311],[312,88],[309,313],[40,314],[315,125],[316,115],[96,317],[256,318],[319,125],[320,85],[278,321],[134,322],[323,11],[324,270],[269,325],[188,326],[327,207],[328,38],[329,196],[111,330],[331,26],[332,173],[333,55],[303,334],[244,335],[336,48],[337,70],[51,338],[171,339],[340,67],[71,341],[342,119],[343,194],[58,344],[345,157],[346,28],[347,268],[348,31],[252,349],[350,220],[120,351],[352,100],[353,144],[354,150],[103,355],[96,356],[357,98],[216,358],[359,181],[102,360],[256,361],[169,362],[363,49],[274,364],[365,322],[4,366],[367,190],[368,30],[62,369],[370,132],[371,19],[372,62],[120,373],[374,168],[375,274],[149,376],[377,22],[378,193],[180,379],[124,380],[214,381],[382,242],[163,383],[339,384],[125,385],[302,386],[387,304],[388,256],[389,273],[390,356],[391,321],[392,42],[393,278],[394,296],[270,395],[338,396],[183,397],[398,13],[315,399],[400,295],[401,248],[209,402],[125,403],[404,235],[405,212],[406,21],[46,407],[408,138],[255,409],[161,410],[228,411],[263,412],[153,413],[111,414],[412,415],[239,416],[417,101],[418,28],[419,384],[420,312],[1,421],[422,65],[1,423],[424,61],[425,61],[426,87],[427,200],[273,428],[145,429],[167,430],[118,431],[416,432],[433,296],[434,79],[435,138],[80,436],[16,437],[24,438],[427,439],[440,215],[101,441],[442,369],[443,418],[444,428],[175,445],[9,446],[447,151],[448,438],[76,449],[150,450],[20,451],[452,67],[452,453],[74,454],[455,316],[456,36],[457,388],[220,458],[459,53],[28,460],[461,83],[359,462],[237,463],[464,108],[189,465],[100,466],[467,260],[468,325],[88,469],[348,470],[471,121],[203,472],[473,142],[206,474],[475,320],[121,476],[477,21],[478,139],[479,467],[56,480],[199,481],[168,482],[483,431],[345,484],[485,219],[486,251],[56,487],[488,305],[489,348],[162,490],[491,93],[492,138],[220,493],[85,494],[495,7],[496,338],[253,497],[284,498],[180,499],[289,500],[501,375],[502,439],[399,503],[499,504],[373,505],[506,231],[489,507],[195,508],[429,509],[163,510],[333,511],[261,512],[34,513],[352,514],[340,515],[218,516],[517,486],[121,518],[519,411],[520,495],[521,207],[101,522],[229,523],[402,524],[525,316],[430,526],[145,527],[528,82],[501,529],[10,530],[531,367],[163,532],[533,96],[534,362],[63,535],[111,536],[537,149],[169,538],[198,539],[223,540],[311,541],[260,542],[335,543],[544,92],[235,545],[546,198],[288,547],[548,87],[91,549],[550,35],[232,551],[552,216],[276,553],[249,554],[555,481],[174,556],[557,27],[558,32],[559,322],[560,300],[26,561],[305,562],[234,563],[564,466],[565,511],[566,301],[119,567],[485,568],[142,569],[186,570],[225,571],[572,161],[361,573],[419,574],[361,575],[576,373],[340,577],[578,408],[579,455],[43,580],[0,581],[459,582],[266,583],[584,330],[565,585],[124,586],[240,587],[192,588],[278,589],[575,590],[591,205],[418,592],[593,132],[310,594],[120,595],[596,56],[597,472],[598,77],[599,88],[383,600],[601,551],[295,602],[583,603],[604,157],[605,7],[208,606],[607,58],[157,608],[609,420],[115,610],[611,360],[612,129],[613,141],[614,52],[450,615],[488,616],[617,12],[136,618],[619,5],[620,278],[621,572],[529,622],[623,289],[245,624],[581,625],[626,3],[188,627],[628,205],[629,188],[630,609],[338,631],[352,632],[633,548],[523,634],[635,113],[505,636],[637,42],[122,638],[639,117],[621,640],[641,200],[642,428],[643,141],[644,268],[645,410],[646,392],[647,19],[648,32],[62,649],[373,650],[651,294],[396,652],[505,653],[548,654],[655,520],[656,481],[657,354],[658,326],[659,17],[660,84],[440,661],[584,662],[327,663],[664,614],[463,665],[666,93],[179,667],[234,668],[192,669],[446,670],[671,357],[579,672],[673,298],[465,674],[286,675],[364,676],[222,677],[678,420],[679,28],[680,130],[681,527],[682,449],[683,162],[684,214],[168,685],[686,422],[687,563],[688,323],[650,689],[251,690],[20,691],[692,613],[693,502],[694,477],[695,427],[303,696],[697,562],[698,39],[604,699],[662,700],[701,320],[702,335],[406,703],[704,637],[381,705],[706,54],[174,707],[708,554],[601,709],[710,71],[639,711],[496,712],[93,713],[714,12],[166,715],[716,668],[32,717],[175,718],[482,719],[86,720],[415,721],[569,722],[723,246],[724,603],[37,725],[373,726],[33,727],[728,227],[132,729],[85,730],[327,731],[358,732],[179,733],[734,658],[735,246],[279,736],[554,737],[647,738],[599,739],[0,740],[580,741],[742,347],[743,75],[266,744],[726,745],[746,373],[747,277],[232,748],[105,749],[750,739],[751,162],[32,752],[586,753],[754,220],[367,755],[756,231],[316,757],[758,83],[759,105],[180,760],[761,61],[653,762],[763,257],[764,86],[639,765],[541,766],[1,767],[376,768],[769,585],[770,453],[355,771],[573,772],[458,773],[774,585],[775,364],[776,244],[624,777],[178,778],[676,779],[780,503],[781,735],[782,542],[783,146],[693,784],[785,707],[691,786],[722,787],[408,788],[789,114],[309,790],[791,42],[792,170],[793,780],[266,794],[795,162],[600,796],[797,481],[32,798],[799,648],[393,800],[801,651],[701,802],[803,422],[59,804],[805,590],[118,806],[88,807],[808,709],[809,314]]
    # print(s.numberOfGoodPaths(vals, edges))

    # vals = [3759,6423,8251,3187,9739,4647,4422,8293,960,1450,9022,3728,8514,9830,3769,9975,7999,2786,6961,1300,4744,5272,4472,4826,4774,8982,7058,8174,4461,322,6736,4481,5440,1823,4190,7227,3987,9963,5452,3215,2073,4773,4782,155,4766,5360,3085,4106,8242,2045,6352,9108,2509,5038,6326,9406,8387,6500,6647,6764,7395,7708,7083,3877,6938,8709,6234,5135,3102,5132,1889,6296,3175,5281,7171,8222,3934,9157,364,837,1029,2246,4471,6494,5092,5061,3191,8322,3892,656,2932,9670,6145,8610,1131,6530,7459,5077,18,5974,6812,2642,7883,3727,7303,4195,2146,8653,7489,3906,2481,2530,8453,6628,9175,7928,6621,8560,8733,3341,3058,962,5750,2287,4330,5889,1878,8362,372,6588,4668,5024,4306,958,704,940,2669,2147,3399,2080,5720,6131,3603,5928,4464,4700,2027,6802,6124,6078,3684,9216,5901,6500,2963,8634,4310,5112,7555,6417,5400,6468,624,2116,3284,1427,9875,4012,7997,5006,5548,5243,7482,790,6920,1003,5084,552,2535,4079,1452,6185,1065,3177,1204,2505,8810,71,217,6601,3579,2760,1110,1199,7580,1008,6830,4245,295,1775,6712,6276,9421,5113,5383,71,7938,8660,5717,8085,3411,3982,9250,6140,4494,6567,4151,6806,5247,7913,3214,1806,9945,6201,6646,6679,8946,2916,4573,2842,6075,4280,3212,7990,3849,4856,6876,8686,2930,7081,4170,4567,8602,603,1293,749,619,9823,9429,2547,5512,5910,4546,2106,7940,4083,3180,5583,9868,8901,4253,5014,4672,3874,427,4431,4629,8135,2192,9756,8069,6128,934,8524,6715,8045,5960,9009,5346,4959,991,591,9806,4272,3364,4432,6670,3292,2396,1080,6552,5988,829,5901,810,4994,6378,8140,4837,9870,7852,9653,1373,679,2706,6018,4541,7652,4085,7883,9954,7949,4323,3950,7680,7919,7278,3953,9612,6439,3040,5958,757,9813,2808,3959,4531,3521,6918,5045,3483,7636,4410,5563,9718,8688,2198,3399,424,4264,8996,3773,7648,3283,4930,1408,4377,4241,6488,3450,5099,958,5627,2493,9307,5133,8432,7782,5672,7599,8600,5149,9184,2895,2363,5243,9763,8400,7516,2261,1466,6334,5506,7921,2324,778,2684,2729,3564,417,2435,6878,71,4484,9621,8358,8617,440,1007,2322,7956,3304,1690,7467,6865,7878,9574,7183,1374,1533,2878,7718,5302,9007,4253,7765,7504,3254,6045,5619,1154,4751,927,6146,4550,4439,2516,9938,782,3635,6370,4975,5706,8505,7616,8452,3766,6098,4833,4994,4006,8789,666,6087,3282,283,7835,8770,6663,4685,1749,343,7218,1071,4459,7657,1680,6499,6991,8130,1886,9912,1907,2585,3696,8006,2137,8539,6205,1048,7417,7216,3215,394,7774,6035,9185,4084,9765,4760,678,9129,4265,2826,3502,6820,1839,1060,2590,987,4389,5612,6628,9216,5617,7828,5710,9692,9857,7059,2903,9462,3589,2550,3951,3900,3095,5259,5487,7979,4158,325,5660,3145,68,1114,7379,3438,7876,6413,241,2174,1503,3393,2444,2902,4648,576,5810,2511,4735,4944,7028,9260,2713,4950,9410,9826,9988,5285,3032,3371,290,5976,6068,1378,1633,1544,4173,1609,3044,7083,5518,6984,2638,6105,8619,7246,780,3298,2891,8004,4064,1981,4987,1630,9701,5130,7845,2546,7528,7687,5314,3467,176,9086,928,9928,4750,1655,5033,1540,1381,1686,8186,8204,7147,4899,4459,5256,9305,7305,79,4723,5315,2044,4801,2435,2715,2950,3522,2108,2256,3939,1384,3097,990,9876,5140,829,4010,9968,9515,7543,4711,5015,6721,9823,9929,8171,9817,7107,3442,5829,576,3593,5732,3680,3785,909,7948,4982,7545,1112,3012,3926,8750,1437,2621,3242,6570,6331,9869,7716,3814,962,6713,6087,5963,9243,9394,7053,808,9849,1005,617,6363,7548,1524,762,1909,4842,6823,5586,5467,7999,4862,8125,5950,4689,2227,3196,6133,3572,2444,7263,7902,8824,1317,3518,2547,3333,5888,6698,7799,9900,9112,523,4527,6032,4857,1447,7514,6709,4507,2283,9370,3865,1395,8149,8135,7795,4313,4793,6005,403,5400,5731,4384,7345,1361,1628,9397,6874,3027,2527,7769,4590,9389,1641,7859,5286,3489,7481,8997,3238,5350,7650,4914,8583,6725,6922,3720,1991,629,7794,755,6966,2568,6880,8716,8859,1349,8239,4512,5954,1046,2536,3010,6186,5473,318,9878,9457,6414,3234,1851,4120,7307,9839,5498,453,7754,1723,2256,300,4253,7149,7989,820,3164,4794,1277,6142,9379,9804,9709,3240,9680,5447,7031,6599,6510,9108,9027,5110,1146,4443,9861,495,7967,7836,2942,8026,7927,4492,468,5088,2224,4359,8137,5829,5631,8109,7886,5720,4950,5641,9598,9502,4111,6931,2489,4735,324,8583,4281,4592,1660,2045,5028,6989,5640,4485,9075,8668,5462,4787,2474,5575,2566,6536,1668,6714,8479,6275,2504,9592,1282,1901,8937,9681,906,6285,1386,1839,8742,9804,3024,3639,7475,7850,6099,8474,7100,3322,3572,21,2085,5152,2587,9634,3905,3991,3260,8873,6518,9544,6068,2772,2955,3524,2712,5458,5361,5207,7701,2392,3590,9069,9017,6675,6511,7480,8681,4829,7583,5485,1587,5293,9262,3280,6572,8058,9964,5058,997,6294,9030,3662,2547,2882,4715,5555,9898,6133,8275,820,100,5176,1425,9935,7259,8304,3270,9949,1937,2469,5959,815,4409,4403,5343,3151,1529,4220,2515,3923,9825,382,7742,6864,7399,289,9979,4251,3389,1712,3707,1214,7103,3226,2359,5558,3137,564,6791,1606,6033,6253,3044,1659,3211,8025,8605,4058,5712,4889,6212,1885,936,5203,4089,5214,5065,4341,699,7621,498,9547,1879,4093,6972,7882,4984,3742,8555,800,4975,3363,9234,6980,5360,5786,9009,6144,5404,8288,3120,8240,4357,1367,6948,3461,4986,178,8891,8409,7779,9405,1392,774,3540,6533,9483,8223,4480,7470,874,2080,6333,913,9073,4714,2553,700,5101,2433,8512,7216,2237,7046,8139,9864,1245,3864,6393,601,3554,1590,9891,6976,9572,2589,710,7702,34,1529,9520,9644,7810,10000,1041,1651,1006,7578,439,888,1387,6486,231,9866,9468,3120,802,203,2597,7232,5257,4892,6280,7492,6995,9826,1601,3346,4234,1022,6912,2675,5309,680,2208,9877,2671,527,714,6711,8754,4887,2940,1610,7442,6952,1702,4614,794]
    # edges = [[1,0],[2,0],[2,3],[4,3],[4,5],[6,1],[6,7],[8,1],[9,3],[4,10],[8,11],[12,4],[12,13],[2,14],[6,15],[16,2],[17,9],[14,18],[18,19],[20,14],[10,21],[2,22],[23,12],[24,3],[25,20],[18,26],[23,27],[28,11],[29,4],[10,30],[31,27],[0,32],[33,9],[7,34],[22,35],[9,36],[37,34],[38,7],[39,3],[40,36],[19,41],[37,42],[43,42],[28,44],[45,14],[46,10],[47,44],[18,48],[8,49],[38,50],[2,51],[52,18],[53,28],[54,39],[55,34],[44,56],[57,25],[1,58],[23,59],[60,39],[61,28],[62,31],[7,63],[64,20],[65,3],[66,23],[6,67],[68,41],[69,41],[70,34],[53,71],[72,31],[73,55],[23,74],[65,75],[48,76],[77,62],[78,53],[79,2],[28,80],[23,81],[82,16],[64,83],[84,11],[45,85],[15,86],[87,44],[88,86],[89,38],[83,90],[81,91],[38,92],[93,12],[84,94],[95,63],[96,63],[2,97],[98,51],[99,74],[71,100],[101,28],[20,102],[88,103],[14,104],[12,105],[59,106],[43,107],[12,108],[76,109],[110,91],[111,7],[112,10],[113,50],[114,79],[115,67],[116,24],[53,117],[7,118],[119,106],[120,38],[74,121],[122,121],[32,123],[101,124],[125,16],[52,126],[95,127],[22,128],[129,80],[130,42],[29,131],[112,132],[133,72],[53,134],[135,50],[136,91],[104,137],[138,81],[139,16],[56,140],[135,141],[69,142],[143,141],[144,73],[145,93],[17,146],[137,147],[125,148],[149,113],[150,88],[151,91],[152,29],[150,153],[7,154],[155,90],[77,156],[75,157],[44,158],[159,97],[77,160],[15,161],[3,162],[163,109],[164,138],[116,165],[24,166],[146,167],[55,168],[117,169],[31,170],[171,127],[153,172],[173,114],[139,174],[16,175],[176,84],[177,40],[178,23],[179,48],[180,171],[181,130],[182,156],[183,131],[48,184],[33,185],[74,186],[187,0],[58,188],[118,189],[147,190],[38,191],[80,192],[193,13],[7,194],[39,195],[87,196],[58,197],[179,198],[67,199],[70,200],[201,180],[167,202],[203,171],[204,114],[33,205],[206,205],[207,198],[28,208],[209,136],[210,183],[162,211],[212,121],[12,213],[214,210],[215,191],[216,34],[217,183],[218,152],[191,219],[173,220],[94,221],[35,222],[22,223],[224,66],[120,225],[226,180],[227,80],[223,228],[214,229],[28,230],[55,231],[232,46],[113,233],[234,52],[117,235],[236,47],[237,131],[238,232],[239,233],[240,73],[241,26],[221,242],[243,216],[244,126],[245,213],[0,246],[172,247],[248,25],[14,249],[17,250],[251,222],[156,252],[253,248],[196,254],[234,255],[214,256],[257,66],[258,230],[259,146],[53,260],[16,261],[138,262],[88,263],[34,264],[71,265],[159,266],[210,267],[253,268],[269,255],[41,270],[271,149],[230,272],[124,273],[89,274],[275,101],[17,276],[277,141],[278,63],[223,279],[280,151],[144,281],[282,198],[283,81],[197,284],[285,223],[286,285],[91,287],[8,288],[289,206],[290,17],[239,291],[211,292],[293,162],[46,294],[225,295],[34,296],[297,114],[179,298],[82,299],[122,300],[301,174],[302,284],[303,53],[263,304],[145,305],[306,243],[307,259],[308,134],[292,309],[310,150],[311,59],[150,312],[78,313],[314,29],[315,161],[247,316],[317,270],[318,237],[319,128],[320,107],[321,154],[322,271],[323,10],[283,324],[325,289],[146,326],[327,115],[328,254],[329,220],[330,320],[331,320],[332,54],[193,333],[135,334],[335,149],[307,336],[192,337],[192,338],[123,339],[151,340],[134,341],[174,342],[343,303],[344,129],[345,143],[236,346],[347,34],[348,131],[189,349],[350,79],[351,133],[348,352],[251,353],[76,354],[120,355],[356,266],[357,248],[358,88],[176,359],[360,25],[154,361],[362,210],[363,25],[364,291],[171,365],[366,88],[367,41],[368,350],[119,369],[275,370],[371,11],[372,33],[373,237],[373,374],[375,254],[222,376],[102,377],[360,378],[379,151],[345,380],[381,334],[382,353],[383,268],[384,331],[329,385],[59,386],[3,387],[99,388],[389,212],[92,390],[345,391],[392,183],[393,98],[254,394],[87,395],[396,114],[397,138],[21,398],[142,399],[400,59],[284,401],[351,402],[227,403],[128,404],[405,403],[406,366],[66,407],[146,408],[409,160],[410,336],[411,253],[201,412],[413,303],[396,414],[274,415],[202,416],[308,417],[181,418],[419,403],[367,420],[421,320],[422,69],[423,57],[82,424],[425,167],[121,426],[427,345],[56,428],[429,407],[430,92],[219,431],[432,112],[295,433],[292,434],[435,429],[436,342],[437,41],[298,438],[439,238],[440,39],[47,441],[442,125],[443,265],[360,444],[67,445],[446,234],[447,280],[448,380],[449,362],[450,141],[286,451],[11,452],[453,375],[200,454],[455,205],[456,59],[353,457],[435,458],[459,220],[460,219],[461,25],[271,462],[463,340],[464,449],[465,37],[466,288],[357,467],[147,468],[40,469],[398,470],[471,102],[123,472],[201,473],[364,474],[378,475],[283,476],[228,477],[478,13],[479,414],[480,165],[481,19],[241,482],[202,483],[484,234],[238,485],[486,370],[487,344],[488,171],[489,349],[39,490],[47,491],[492,151],[217,493],[111,494],[495,161],[22,496],[48,497],[440,498],[499,291],[106,500],[501,17],[502,2],[82,503],[378,504],[330,505],[506,124],[507,209],[508,502],[509,301],[510,509],[206,511],[428,512],[96,513],[514,163],[515,287],[164,516],[234,517],[12,518],[519,213],[520,357],[305,521],[522,514],[409,523],[52,524],[384,525],[526,158],[527,214],[82,528],[279,529],[145,530],[135,531],[532,303],[429,533],[534,413],[22,535],[536,459],[537,198],[538,514],[513,539],[540,325],[412,541],[542,77],[543,383],[544,264],[545,152],[546,342],[76,547],[389,548],[549,135],[550,378],[551,284],[552,341],[185,553],[554,494],[405,555],[556,465],[431,557],[353,558],[526,559],[560,326],[560,561],[126,562],[563,410],[116,564],[565,265],[472,566],[567,252],[568,63],[189,569],[570,412],[143,571],[345,572],[573,413],[574,326],[575,389],[576,570],[577,256],[71,578],[59,579],[249,580],[181,581],[582,25],[583,148],[584,394],[585,248],[166,586],[135,587],[395,588],[304,589],[590,95],[591,466],[592,460],[593,184],[76,594],[595,520],[370,596],[120,597],[268,598],[599,592],[383,600],[484,601],[101,602],[603,323],[220,604],[437,605],[606,289],[607,325],[114,608],[609,488],[610,483],[611,165],[601,612],[613,378],[400,614],[615,26],[386,616],[617,561],[425,618],[25,619],[620,167],[23,621],[558,622],[623,475],[624,394],[103,625],[626,511],[88,627],[82,628],[629,418],[630,136],[245,631],[583,632],[633,217],[310,634],[628,635],[636,103],[127,637],[387,638],[639,574],[447,640],[593,641],[642,637],[643,43],[644,82],[465,645],[451,646],[456,647],[312,648],[649,525],[182,650],[175,651],[652,505],[138,653],[462,654],[655,260],[656,236],[657,168],[658,356],[562,659],[660,349],[455,661],[662,311],[429,663],[279,664],[624,665],[471,666],[344,667],[558,668],[669,273],[349,670],[671,30],[70,672],[673,532],[674,432],[637,675],[676,324],[406,677],[678,19],[679,368],[346,680],[681,255],[592,682],[683,528],[684,319],[685,159],[624,686],[411,687],[688,281],[689,144],[690,192],[691,24],[271,692],[527,693],[421,694],[406,695],[174,696],[641,697],[91,698],[699,442],[700,404],[701,155],[409,702],[174,703],[599,704],[705,485],[706,532],[707,683],[708,93],[602,709],[4,710],[523,711],[125,712],[713,565],[619,714],[693,715],[507,716],[329,717],[718,364],[719,339],[720,201],[10,721],[722,392],[723,361],[49,724],[302,725],[726,550],[727,544],[728,99],[555,729],[730,22],[362,731],[732,537],[310,733],[734,215],[210,735],[736,125],[320,737],[738,264],[739,392],[596,740],[243,741],[742,668],[743,156],[280,744],[699,745],[746,149],[747,469],[660,748],[175,749],[750,439],[251,751],[752,50],[753,647],[754,70],[342,755],[756,279],[757,635],[591,758],[261,759],[353,760],[732,761],[762,113],[763,632],[764,713],[765,595],[279,766],[299,767],[768,273],[641,769],[357,770],[599,771],[772,295],[589,773],[289,774],[775,749],[776,217],[777,204],[697,778],[344,779],[780,518],[781,28],[601,782],[783,413],[63,784],[785,455],[556,786],[401,787],[157,788],[210,789],[790,467],[791,333],[792,243],[793,247],[794,420],[489,795],[74,796],[100,797],[220,798],[799,640],[800,288],[801,704],[9,802],[513,803],[312,804],[805,140],[793,806],[807,209],[808,780],[809,10],[810,657],[27,811],[774,812],[750,813],[80,814],[628,815],[816,808],[445,817],[818,250],[414,819],[820,9],[634,821],[822,669],[409,823],[824,10],[80,825],[826,80],[49,827],[828,647],[559,829],[830,799],[665,831],[832,626],[780,833],[834,124],[835,794],[450,836],[201,837],[511,838],[839,629],[619,840],[841,315],[534,842],[73,843],[528,844],[845,742],[634,846],[847,382],[848,483],[195,849],[241,850],[614,851],[852,792],[0,853],[854,703],[855,105],[567,856],[347,857],[858,620],[470,859],[53,860],[861,32],[862,426],[863,426],[864,358],[219,865],[866,535],[582,867],[868,857],[869,703],[870,512],[559,871],[872,754],[295,873],[81,874],[851,875],[70,876],[877,715],[133,878],[879,32],[880,62],[111,881],[882,640],[883,546],[179,884],[885,580],[303,886],[887,839],[888,637],[574,889],[530,890],[8,891],[9,892],[785,893],[242,894],[895,215],[896,37],[897,770],[898,346],[899,252],[900,372],[726,901],[902,2],[903,717],[739,904],[905,715],[585,906],[907,805],[901,908],[909,730],[910,811],[62,911],[566,912],[913,579],[914,142],[915,524],[916,585],[917,104],[847,918],[919,153],[920,98],[77,921],[824,922],[923,295],[576,924],[711,925],[926,762],[927,505],[99,928],[929,853],[433,930],[931,923],[332,932],[933,927],[934,926],[833,935],[936,560],[356,937],[420,938],[939,560],[844,940],[458,941],[942,804],[315,943],[346,944],[499,945],[946,150],[751,947],[751,948],[949,788],[630,950],[951,509],[952,857],[953,656],[529,954],[552,955],[20,956],[957,247],[958,115],[487,959],[921,960],[725,961],[962,466],[963,870],[964,587],[965,351],[966,488],[967,582],[474,968],[969,290],[970,168],[241,971],[851,972],[973,752],[974,282],[532,975],[9,976],[953,977],[482,978],[979,288],[742,980],[981,139],[982,61],[983,846],[984,786],[985,602],[93,986],[905,987],[988,358],[931,989],[585,990],[991,717],[526,992],[440,993],[774,994],[672,995],[191,996],[997,775],[998,389],[999,936],[427,1000],[1001,617],[25,1002],[100,1003],[1004,565],[1005,84],[1006,621],[344,1007],[1008,699],[1009,107],[616,1010],[758,1011],[891,1012],[523,1013],[102,1014],[984,1015],[1016,884],[580,1017],[216,1018],[176,1019],[1020,978],[942,1021],[386,1022],[812,1023],[904,1024],[495,1025],[1026,870],[247,1027],[1028,317],[963,1029],[727,1030],[1007,1031],[958,1032],[815,1033],[1034,446],[1035,1027],[913,1036],[243,1037],[1038,986],[176,1039],[152,1040],[918,1041],[1042,370],[59,1043],[529,1044],[963,1045],[758,1046],[419,1047],[1032,1048],[1049,2],[854,1050],[779,1051],[933,1052],[1053,301],[310,1054],[1055,282],[198,1056],[1057,276],[1058,473],[1059,834],[1060,116],[646,1061],[400,1062],[1063,430],[1064,883],[293,1065],[154,1066],[1067,452],[1068,854],[1069,821],[1070,592],[518,1071],[512,1072],[1073,718],[185,1074],[21,1075],[1076,121]]
    # print(s.numberOfGoodPaths(vals, edges))
