from collections import defaultdict
from typing import List


class Solution:
    def areSentencesSimilar(self, sentence1: List[str], sentence2: List[str], similarPairs: List[List[str]]) -> bool:
        if len(sentence1) != len(sentence2):
            return False
        
        roots = {}

        def find(s):
            roots.setdefault(s,s)
            if s != roots[s]:
                roots[s] = find(roots[s])
            return roots[s]

        def union(s1,s2):
            roots[find(s1)] = find(s2)
        
        for w1,w2 in similarPairs:
            union(w1,w2)

        for w1,w2 in zip(sentence1,sentence2):
            if find(w1) != find(w2):
                return False
            
        return True

"""
okay.. the case I didn't ask is if the similarity is transmissive
a<>b and b<>c => a,c?????
apparently not

so not union find

"""


class Solution:
    def areSentencesSimilar(self, sentence1: List[str], sentence2: List[str], similarPairs: List[List[str]]) -> bool:
        if len(sentence1) != len(sentence2):
            return False
        
        similar = defaultdict(set)
        for w1,w2 in similarPairs:
            similar[w1].add(w2)
            similar[w2].add(w1)

        for w1,w2 in zip(sentence1,sentence2):
            if w1==w2:
                continue
            
            if w2 not in similar[w1]:
                return False


        return True

if __name__ == '__main__':
    sent1  = ["an","extraordinary","meal"]
    sent2 = ["a","good","dinner"]
    similars = [["great","good"],["extraordinary","good"],["well","good"],["wonderful","good"],["excellent","good"],["fine","good"],["nice","good"],["any","one"],["some","one"],["unique","one"],["the","one"],["an","one"],["single","one"],["a","one"],["truck","car"],["wagon","car"],["automobile","car"],["auto","car"],["vehicle","car"],["entertain","have"],["drink","have"],["eat","have"],["take","have"],["fruits","meal"],["brunch","meal"],["breakfast","meal"],["food","meal"],["dinner","meal"],["super","meal"],["lunch","meal"],["possess","own"],["keep","own"],["have","own"],["extremely","very"],["actually","very"],["really","very"],["super","very"]]