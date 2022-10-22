import parser
import create_sheets



def parseConfigFile(filepath):

    unfilteredArray = parser.createUnfilteredArray(filepath)
    hostname = parser.getHostname(unfilteredArray)
    sheetPath = f'ExcelSheetOutputs/{hostname}.xlsx'


    '''StackArr output template [[modules], [power-supply], [DAC cables], [Uplink Modules]]'''

    dataBeginPoint = [f'{hostname}#', 'show', 'inventory'] # Will match the 'show inventory' portion of the backup config
    dataEndPoint = [f'{hostname}#', '!!!!!!!!!!']
    dataLinesUntilActualDataStart = 1

    stackArray = parser.createStackArray(unfilteredArray, dataBeginPoint, dataEndPoint, dataLinesUntilActualDataStart)

    create_sheets.createMembersSheet(stackArray, hostname)

    create_sheets.createPowerSupplySheet(stackArray, sheetPath)

    create_sheets.createDacSheet(stackArray, sheetPath)

    if stackArray[3]:  # Uplink Module info is on stackArray[3], checks if there is any info there
        create_sheets.createUplinkModuleSheet(stackArray, sheetPath)



