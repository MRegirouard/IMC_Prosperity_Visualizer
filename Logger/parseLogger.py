
def getActivityLogs(logLines):
    return

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