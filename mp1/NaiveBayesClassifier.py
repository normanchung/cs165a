import sys
import numpy

dictpos = {}
dictneg = {}

counterpos = 0
counterneg = 0
with open(sys.argv[1],'r') as file:
    for line in file:
        lastword = line.split()
        classdef = lastword[-1]
        if (classdef == ',1'):
            for eachword in lastword[0:len(lastword) - 1]:
                if eachword in dictpos:
                    dictpos[eachword]['count'] += 1
                    counterpos += 1
                else:
                    dictpos[eachword] = {'count': 1.0, 'probability': 0.0}
                    counterpos += 1

        elif (classdef == ',0'):
            for eachword in lastword[0:len(lastword) - 1]:
                if eachword in dictneg:
                    dictneg[eachword]['count'] += 1
                    counterneg += 1
                else:
                    dictneg[eachword] = {'count': 1.0, 'probability': 0.0}
                    counterneg += 1

for eachword in dictpos:
    dictpos[eachword]['probability'] = dictpos[eachword]['count'] / counterpos
for eachword in dictneg:
    dictneg[eachword]['probability'] = dictneg[eachword]['count'] / counterneg

#print(dictpos['the'])
#print(counterpos)
#print(dictneg['the'])
#print(counterneg)

#str = 'hello this is a positive review ,1'
#splitted = str.split()
#splitted = splitted[0:len(splitted) - 1]
#print(splitted)
#print(1)
#print('1')

testposcounter = 0.0
testnegcounter = 0.0
realposcounter = 0
realnegcounter = 0

#ask shaka about overfitting
with open(sys.argv[2],'r') as file:
    for line in file:
        testpos = 0.0
        testneg = 0.0
        withoutclass = line.split()
        classdef = withoutclass[-1]
        if (classdef == ',1'):
            realposcounter += 1
        else:
            realnegcounter += 1
        withoutclass = withoutclass[0:len(withoutclass) - 1]
        for eachword in withoutclass:
            if eachword in dictpos:
                testpos += numpy.log10(dictpos[eachword]['probability'])
                #ask shaka what to do when the word is not in dictpos
            if eachword in dictneg:
                testneg += numpy.log10(dictneg[eachword]['probability'])
                #ask shaka
        #print(testpos)
        #print(testneg)
        if (testpos > testneg):
            print('1')
            testposcounter += 1
        else:
            print('0')
            testnegcounter += 1
'''
testnum = dictpos['each']['probability']
test = 0.0
test += math.log10(testnum)
print(test)
'''
print('accuracy calculation now')
total = 0.0
total = abs(testposcounter - realposcounter)
othertotal = abs(testnegcounter - realnegcounter)
print(othertotal)
print(total)
print(realposcounter + realnegcounter)
accuracy = total / (realposcounter + realnegcounter)
accuracy = 1 - accuracy
print(accuracy)
#ask shaka his accuracy for testing.txt
