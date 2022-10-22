import cleanup


def createUnfilteredArray(path):
    endArray = []

    with open(path) as file:
        for line in file:
            endArray.append(line.split())

    return endArray



def createDesiredArray(rawArray, beginCase, endCase):
    if beginCase not in rawArray:
        print('Could not find begin case in Raw Array')
        return
    
    startIndex = rawArray.index(beginCase)
    arrayLength = len(rawArray)
    finishedArray = []

    for index in range(startIndex, arrayLength):

        if isinstance(endCase, list):
            if rawArray[index] == endCase:
                break
        elif isinstance(endCase, str):
            if endCase in rawArray[index]:
                break
        else:
            print('check your endPoint type')

            
        if len(rawArray[index]) == 0:
            continue
        
        currentLine = rawArray[index]
        finishedArray.append(currentLine)

    return finishedArray




def createDataOnlyArray(filteredArray, linesUntilData):
    lenArray = len(filteredArray)
    dataArray = []

    for number in range(linesUntilData, lenArray):
        dataArray.append(filteredArray[number])

    return dataArray


def getHostname(unprocessedArray):
    for line in unprocessedArray:
        for element in line:
            if '#' in element:                
                return element[:element.index('#')]


def createStackArray(rawDataArray, startPoint, endPoint, linesUntilDataStart):
    
    desiredArray = createDesiredArray(rawDataArray, startPoint, endPoint)   
    unprocessedDataOnlyArray = createDataOnlyArray(desiredArray, linesUntilDataStart)
    dataOnlyArray = cleanup.removeCommasQuotesColons(unprocessedDataOnlyArray)

    '''StackArr output template [[modules], [power-supply], [DAC cables], [Uplink Modules]]'''
    stackArr = [[],[],[],[]]


    
    for line in dataOnlyArray:
        if 'NAME' in line:
            deviceDescription = line[1]

            nextLine = dataOnlyArray[dataOnlyArray.index(line) + 1]
            nextLineSerial = nextLine[-1]
    

            if deviceDescription == 'Switch' and 'Power' not in line and 'Uplink' not in line:
                stackArr[0].append([' '.join(line[1:3]), nextLineSerial])
            
            if deviceDescription == 'Switch' and 'Power' in line:
                stackArr[1].append([''.join(line[1:7]), nextLineSerial])
            
            if 'StackPort' in deviceDescription:
                stackArr[2].append([''.join(line[1]), nextLineSerial])
            
            if deviceDescription == 'Switch' and 'Uplink' in line:
                uplinkModuleDescription = f"{' '.join(line[1:3])} {' '.join(line[4:7])}"
                stackArr[3].append([uplinkModuleDescription, nextLineSerial])
    

    return stackArr