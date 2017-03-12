import maya.cmds as cmds

def GetFilePath():
    splitPath = cmds.file(query = True, expandName=True)
    splitPath = splitPath.split('/')
    splitPath.pop()
    path = "";
    for item in splitPath:
        path += item + "/"
    return path

def FailExit(message):
    cmds.error(message)
    sys.exit()