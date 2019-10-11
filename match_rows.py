from matchingStuff import MYCONNECTION, sortAndPrint, getSponsorData, getContactData, updateSponsor, calculateScoresAndMatch


def main():

    dataDict = getSponsorData(100000)
    matchedData = calculateScoresAndMatch(dataDict)
    sortAndPrint(matchedData, 'sponsors.txt')
    updateSponsor(matchedData)

    # dataDict = getContactData(10)
    # matchedData = calculateScoresAndMatch(dataDict)
    # sortAndPrint(matchedData, 'contacts.txt')


if __name__ == '__main__':
    main()
    MYCONNECTION.close()
