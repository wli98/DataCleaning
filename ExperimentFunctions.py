import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def takeSample(samplePop, n):
    sampleList = []
    for x in range(n):
        sampleList.append(samplePop[random.randint(0,len(samplePop)-1)])
    return sampleList

def takeZipfSample(samplePop,n):
    sampleList = []
    for x in range(n):
        index = np.random.zipf(1.5)
        if index > len(samplePop):
            index = len(samplePop)
        sampleList.append(samplePop[index - 1])
    return sampleList

def simpleError(sampleList, matching, target):
    result = runMatch(sampleList, matching)
    numBad = 0
    for name in result:
        if name not in target:
            numBad = numBad + 1
    return (numBad/len(sampleList))

def runMatch(sampleList, matching):
    result = []
    for country in sampleList:
        found = False
        for id in matching:
            if country == id[0]:
                result.append(id[1])
                found = True
        if found == False:
            result.append(country)
    return result



def findMatchings(sampleList, ErrFunc):
    potentialMatchings = []
    optMatching = []

    for x in sampleList:
        for y in sampleList:
            potentialMatchings.append([x,y])

    for match in potentialMatchings:
        testMatch = optMatching.copy()
        testMatch = [x for x in testMatch if x[0] != match[0]]
        testMatch.append(match)

        if ErrFunc(sampleList, optMatching) > ErrFunc(sampleList, testMatch):
            optMatching = [x for x in optMatching if x[0] != match[0]]
            optMatching.append(match)


    return optMatching

def findMatchingsSimple(sampleList, target):
    optMatching = []
    firstAbbrev = ''
    for name in sampleList:
        if name in target:
            firstAbbrev = name
            break
    if firstAbbrev != '':
        for x in sampleList:
            optMatching.append([x,firstAbbrev])
    return optMatching


def getErrors(samplePop, ErrFunc, n):
    sampleSize = []
    errors = []
    for i in range(20, n):
        sample = takeSample(samplePop, i)
        matching = findMatchings(sample, ErrFunc)
        sampleSize.append(i)
        errors.append(ErrFunc(samplePop, matching) - ErrFunc(sample, matching))
    errorFrame = pd.DataFrame({
        'Sample Size':sampleSize,
        'Error Difference':errors
        })
    return errorFrame

def getErrorsSimple(samplePop, sampleFunc, target, n):
    sampleSize = []
    errors = []
    for i in range(20, n):
        sample = sampleFunc(samplePop, i)
        matching = findMatchingsSimple(sample, target)
        sampleSize.append(i)
        errors.append(simpleError(samplePop, matching, target) - simpleError(sample, matching, target))
    errorFrame = pd.DataFrame({
        'Sample Size':sampleSize,
        'Error Difference':errors
        })
    return errorFrame

def fitFunc(x, a, b):
    return a*(1/np.sqrt(x)) + b
