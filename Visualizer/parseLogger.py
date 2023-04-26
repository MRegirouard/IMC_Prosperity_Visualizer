
from Models import ActivityLogRow, Algorithm, AlgorithmSummary, CompressedOrder, CompressedSandboxLogRow, \
    CompressedTrade, CompressedTradingState, Listing, Order, OrderDepth, ProsperitySymbol, SandboxLogRow, \
    Trade, TradingState

from typing import Dict, List, Union

def getColumnValues(columns: List[str], indices: List[int]) -> List[int]:
    values = []
    for index in indices:
        value = columns[index]
        if value != '':
            values.append(int(value))
    return values

def getActivityLogs(logLines):
    headerIndex = logLines.index('Activity log:')
    if headerIndex == -1:
        return []
    
    rows = []
    for i in range(headerIndex+2, len(logLines)):
        columns = logLines[i].split(';')
        tempRow = ActivityLogRow(float(columns[0]), float(columns[1]), \
                                 columns[2], getColumnValues(columns, [3, 5, 7]), getColumnValues(columns, [4, 6, 8]), \
                                    getColumnValues(columns, [9, 11, 13]), getColumnValues(columns, [10, 12, 14]), \
                                        float(columns[15]), float(columns[16]))
        rows.append(tempRow)


    

    


def getSandboxLogs(logLines):
    return

def getSubmissionLogs(logLines):
    return


def parseAlgorithmLogs(logs):
    logLines = logs.strip().split('\n')

    activityLogs = getActivityLogs(logLines)
    sandboxLogs = getSandboxLogs(logLines)
    submissionLogs = getSubmissionLogs(logLines)


    if activityLogs.empty or sandboxLogs.empty():
        raise ValueError("Invalid format, please see prerequisite section")
    
    return [activityLogs, sandboxLogs, submissionLogs]