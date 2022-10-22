import os
import parser
import create_sheets
import pandas as pd
from openpyxl import load_workbook


def parseConfigFile(filepath):

    unfilteredArray = parser.createUnfilteredArray(filepath)
    hostname = parser.getHostname(unfilteredArray)
    sheetPath = f'ExcelSheetOutputs/{hostname}.xlsx'


    """INVENTORY DATA"""
    dataBeginPoint = [f'{hostname}#', 'show', 'inventory']
    dataEndPoint = [f'{hostname}#', '!!!!!!!!!!']
    dataLinesUntilActualDataStart = 1

    stackArray = parser.createStackArray(unfilteredArray, dataBeginPoint, dataEndPoint, dataLinesUntilActualDataStart)

    create_sheets.createMembersSheet(stackArray, hostname)

    create_sheets.createPowerSupplySheet(stackArray, sheetPath)

    create_sheets.createDacSheet(stackArray, sheetPath)

    if stackArray[3]:  # Uplink Module info is on stackArray[3], checks if there is any info there
        create_sheets.createUplinkModuleSheet(stackArray, sheetPath)



