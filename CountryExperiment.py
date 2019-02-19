from ExperimentFunctions import *

completeData = pd.read_csv("Country.csv")
countryNames = []
labels = []
countryNamesAbbrev = []

for x in range(len(completeData)):
    countryNames.append(completeData.iat[x,0])
    countryNames.append(completeData.iat[x,1])
    countryNames.append(completeData.iat[x,3])
    labels.append(completeData.iat[x,0])


for x in range(33):
    countryNamesAbbrev.append(completeData.iat[x,0])
    countryNamesAbbrev.append(completeData.iat[x,1])
    countryNamesAbbrev.append(completeData.iat[x,3])

countryNames = list(set(countryNames))
labels = list(set(labels))

#errors = getErrorsSimple(countryNames, labels, 1200)

#popt, pcov =curve_fit(fitFunc, errors.iloc[:,0].values, errors.iloc[:,1].values)

#plt.plot(errors.iloc[:,0],errors.iloc[:,1], label = 'Data')
#plt.plot(errors.iloc[:,0], fitFunc(errors.iloc[:,0].values, *popt), label='fit: a=%5.3f, b=%5.3f' % tuple(popt))
#plt.legend()

#fullZipfErrors = getErrorsSimple(countryNames, takeZipfSample, labels, 3000)
#fullZipfErrors.iloc[10:].plot(x = 'Sample Size', y = 'Error Difference')
#plt.title('Zipf Sample')

errors = getErrorsSimple(countryNamesAbbrev, takeZipfSample,labels, 800)
errors.iloc[20:].plot(x = 'Sample Size', y = 'Error Difference')
plt.title('Zipf Sample Small Pop')


plt.show()
