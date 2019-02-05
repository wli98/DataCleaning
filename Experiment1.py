import pandas as pd
import random
import matplotlib.pyplot as plt

completeData = pd.read_csv("Country.csv")
countryNames = []
labels = []

for x in range(len(completeData)):
    countryNames.append(completeData.iat[x,0])
    countryNames.append(completeData.iat[x,1])
    countryNames.append(completeData.iat[x,3])
    labels.append(completeData.iat[x,0])

countryNames = list(set(countryNames))
labels = list(set(labels))

def takeSample(n):
    sampleList = []
    for x in range(n):
        sampleList.append(countryNames[random.randint(0,len(countryNames)-1)])
    return sampleList

def simpleError(sampleList, matching):
    result = runMatch(sampleList, matching)
    numBad = 0
    for name in result:
        if name not in labels:
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

def findMatchingsSimple(sampleList):
    optMatching = []
    firstAbbrev = ''
    for name in sampleList:
        if name in labels:
            firstAbbrev = name
            break
    if firstAbbrev != '':
        for x in sampleList:
            optMatching.append([x,firstAbbrev])
    return optMatching


def getErrors(ErrFunc):
    sampleSize = []
    errors = []
    for i in range(20, 659):
        sample = takeSample(i)
        matching = findMatchings(sample, ErrFunc)
        sampleSize.append(i)
        errors.append(ErrFunc(countryNames, matching) - ErrFunc(sample, matching))
    errorFrame = pd.DataFrame({
        'Sample Size':sampleSize,
        'Error Difference':errors
        })
    return errorFrame

def getErrorsSimple():
    sampleSize = []
    errors = []
    for i in range(20, len(countryNames)):
        sample = takeSample(i)
        matching = findMatchingsSimple(sample)
        sampleSize.append(i)
        errors.append(simpleError(countryNames, matching) - simpleError(sample, matching))
    errorFrame = pd.DataFrame({
        'Sample Size':sampleSize,
        'Error Difference':errors
        })
    return errorFrame

errors = getErrorsSimple()
errors.plot(x = 'Sample Size', y = 'Error Difference')
plt.show()
