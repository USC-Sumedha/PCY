#PCY

import sys

####################     CHECK IF CANDIDATE PAIR IS HASHED TO A FREQUENT BUCKET  AND CHECK IF IT IS FREQUENT AND OUTPUT FREQ ITEMSETS     #################

def checkFreqInHash(candList,hashtable):
    freqList = []
    for x in candList:
        sum = 0
        # sum all indv items
        for y in x:
            sum = sum + allProds.index(y)+1
        # get the reminder to see which bucket it belongs to
        whichBkt =(sum)%hashing
        if whichBkt in hashtable and hashtable[whichBkt] == 1:
            if x in allPosCount_map and allPosCount_map[x] >= min_s:
                freqList.append(x)
    freqList = sorted(freqList)
    print("")
    if len(freqList) > 0:
        print('Frequency Itemsets of size',i)
        # printing freq-list
        for x in freqList:
            j = 0
            for y in x:
                if j == len(x)-1:
                   print(y,end = "\n") 
                else:
                    print(y,end = ",")
                j = j+1           
    return freqList

#########################################       FORM THE HASH TABLE        ####################################################

def hashFn(l_hash):
    global allProds
    global hashing
    global hashBkt_map
    for x in l_hash:
        sum = 0
        # get sum of individual items in each set
        for y in x:
            sum = sum + allProds.index(y)+1
        # get the reminder to hash it to a bucket bucket
        hashBkt =(sum)%hashing
        if hashBkt < hashing and hashBkt not in hashBkt_map:
            hashBkt_map[hashBkt] = 1
        else:
            hashBkt_map[hashBkt] = hashBkt_map[hashBkt] +1
    return hashBkt_map

##########################################      FORM BIT-VECTOR FROM HASH TABLE     ##################################################
            
def getBitVector(hashBkt_map):
    bitVector = {}
    for dict in hashBkt_map.items():
        if dict[1] >= min_s:
            bitVector[dict[0]] = 1
        else:
            bitVector[dict[0]] = 0
    return bitVector

############################################### FIND COMBINATION FROM EACH LINE IN THE BUCKET TO FORM COMBINATIONS FOR HASH TABLE ########################

def eachLinePairs(eachBucketLine,eachBucketLine1,key):
    allPosList = []
    for val1 in eachBucketLine:
        for val2 in eachBucketLine1:
            if i is 2 and val1 is not val2:
                val = set([val1,val2])
                allPosList.append(tuple(sorted(val)))
            elif i > 2 and val1 != val2:
                if(len(set(val1)&set(val2)) == i-2):
                    val = set(val1)| set(val2)
                    allPosList.append(tuple(sorted(val))) 
    tempSet = set(allPosList)
    allPos_map[key] = tempSet
    return allPos_map


#########################################################       FORM COUNT OF ALL POSSIBLE COMBINATIONS FOR EACH PASS   ####################################
def allPosCount(values):
    # after forming a candidate pair, create count map
    global allPosCount_map
    for val in values:
        if val not in allPosCount_map:
            allPosCount_map[val] = 1
        else:
            allPosCount_map[val] = allPosCount_map[val] + 1 

##################################################    FORM CANDIDATE COMBINATIONS FROM FREQUENCY LIST    #############################################
def candidatepairs(prevfreqList,prevfreqList1):
    candidateList = []
    for val1 in prevfreqList:
        for val2 in prevfreqList1:
            if i is 2 and val1 is not val2:
                val = set([val1,val2])
                candidateList.append(tuple(sorted(val)))
            elif i > 2 and val1 != val2:
                if(len(set(val1)&set(val2)) == i-2):
                    val = set(val1)| set(val2)
                    candidateList.append(tuple(sorted(val)))            
    candidateSet = set(candidateList)
    return candidateSet

################################################      MAIN PROGRAM TO READ INPUT FILE AND CREATE FREQUENT ITEM SETS     ####################################  

b_list = {}
i= 0
count1 = 0
itemSize1 = {};
min_s = int(sys.argv[2])
hashing = int(sys.argv[3])
print("")
inputdata = open(sys.argv[1])
# iterate over input data to form word count, map of input
for line in inputdata:
    i = i+1
    wordlist=[]
    line = line.rstrip('\n')
##    b_list[i] = line
    words = line.split(',')
    for word in words:
        wordlist.append(word)
        if word not in itemSize1:
            itemSize1[word] = 1
        else:
            itemSize1[word] = itemSize1[word] + 1
    b_list[i] = wordlist
#get a list of all products
allProds = [x for x in itemSize1.keys()]
allProds = sorted(allProds)
#get freq-list of size = 1
freqList = [x[0] for x in itemSize1.items() if x[1] >= min_s]     
print("Frequent Itemsets of size 1")
print("\n".join([x for x in sorted(freqList)]))
print("")
i = 2
# frequency list used to form candidate pair
prevfreqList = sorted(freqList)
# PCY Algorithm
while len(prevfreqList) > 0:
    #initialize hashbuckt count and map for every pass
    hashBkt_map = {}
    allPos_map = {}
    allPosCount_map={}
    # for every line hash the pairs or triples or combinations formed and create
    # possible pairs, count ; bitmap
    for key in b_list.keys():
        bkt_list = b_list[key]
        bkt_list = list(bkt_list)
        # returns all possible combination for every line
        allPos_map = eachLinePairs(bkt_list,bkt_list[1:len(bkt_list)],key)
        # returns all possible combinations count
        allPosCount(allPos_map[key])
        # forms hashtable
        hashFn(allPos_map[key])
        key = key+1
    # assign the list to be used to form all combinations for next iteration
    b_list = allPos_map
    #forms bitmap based on frequency of hashtable Vs min support
    bitVec = getBitVector(hashBkt_map)
    # form candidate pairs
    candPair = candidatepairs(prevfreqList,prevfreqList[1:len(prevfreqList)])
    # check candidate pairs againts bit vector
    # if hashed to a 1-bitvector then find if the combination is frequent and also all sub parts
    # print the frequency list
    prevfreqList = checkFreqInHash(candPair,bitVec)
    #increment the count for next pass
    i = i+1   

    
