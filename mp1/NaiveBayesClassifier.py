import sys
import numpy
import timeit


start1 = timeit.default_timer()

dictpos = {}
dictneg = {}
counterpos = 0
counterneg = 0
a = 0.01

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
    dictpos[eachword]['probability'] = (dictpos[eachword]['count'] + a) / (counterpos + (a * (counterpos + counterneg)))

for eachword in dictneg:
    dictneg[eachword]['probability'] = (dictneg[eachword]['count'] + a) / (counterneg + (a * (counterpos + counterneg)))

stop1 = timeit.default_timer()

start2 = timeit.default_timer()

realposcounter = 0.0
realnegcounter = 0.0
correct = 0.0

with open(sys.argv[1],'r') as file:
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
            else:
                testpos += numpy.log10(a / (counterpos + (a * (counterpos + counterneg))))
            if eachword in dictneg:
                testneg += numpy.log10(dictneg[eachword]['probability'])
            else:
                testneg += numpy.log10(a / (counterneg + (a * (counterpos + counterneg))))
        if (testpos > testneg):
            #print('1')
            if (classdef == ',1'):
                correct += 1
        else:
            #print('0')
            if (classdef == ',0'):
                correct += 1

trainingaccuracy = correct / (realposcounter + realnegcounter)

realposcounter = 0.0
realnegcounter = 0.0
correct = 0.0

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
            else:
                testpos += numpy.log10(a / (counterpos + (a * (counterpos + counterneg))))
            if eachword in dictneg:
                testneg += numpy.log10(dictneg[eachword]['probability'])
            else:
                testneg += numpy.log10(a / (counterneg + (a * (counterpos + counterneg))))
        if (testpos > testneg):
            print('1')
            if (classdef == ',1'):
                correct += 1
        else:
            print('0')
            if (classdef == ',0'):
                correct += 1

testingaccuracy = correct / (realposcounter + realnegcounter)

stop2 = timeit.default_timer()

print((stop1 - start1), 'seconds (training)')
print((stop2 - start2), 'seconds (labeling)')
print(trainingaccuracy, '(training)')
print(testingaccuracy, '(testing)')
