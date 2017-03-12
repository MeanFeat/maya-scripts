import maya.cmds as cmds
import maya.mel as mel
import Snippets as snip

def CreateScriptJob():
    return cmds.scriptJob(e=("animLayerRefresh", UpdateSelectedAnimLayer), killWithScene=True)

def GetFrameRange( sel ):
    splitName = sel.split('_')
    endFrame = splitName[-1]
    endFrame = endFrame.replace("f", "")
    return endFrame

def UpdateSelectedAnimLayer():
    for item in cmds.ls(type='animLayer'):
        if (cmds.animLayer(item,q=True,selected=True)):
			UpdateAnimLayer( item )

def UpdateAnimLayer( layer ):
    for item in cmds.ls(type='animLayer'):
        if (item == layer):
            par = cmds.animLayer(item, q=True, parent=True) 
            cmds.setAttr(par + ".mute", 0)   
            cmds.setAttr(item + ".mute", 0)
            cmds.setAttr(item + ".lock", 0)
            cmds.playbackOptions(max=GetFrameRange(item))
        elif item != 'BaseAnimation':
            cmds.setAttr(item + ".lock", 1)
            cmds.setAttr(item + ".mute", 1)		

def SelectExportJoints():
    cmds.select('Rig:root', hi=True)
    exportJoints = cmds.ls(selection=True, type='joint')
    cmds.select(exportJoints)

def GetExportName(exportLayer):
    exportLayerTok = exportLayer.split('_')
    exportLayerTok.pop()
    exportLayerName=''
    for s in exportLayerTok:
        exportLayerName += s
        exportLayerName += '_'
    return exportLayerName[:len(exportLayerName)-1]

def GetExportSettings( exportLayer, start, end, fileName = ''):
    string = 'file -force -options "v=0;" -typ "FBX export" -pr -es "' + snip.GetFilePath() + "/FBX/" 
    mel.eval('FBXExportBakeComplexAnimation -v true;')
    min = str(0) if start == None else str(start)
    max = GetFrameRange(exportLayer) if end == None else str(end)
    mel.eval("FBXExportBakeComplexStart -v " + min) 
    mel.eval("FBXExportBakeComplexEnd -v " + max)
    if len(fileName) == 0:
        fileName = GetExportName(exportLayer);
    return string + fileName + '.fbx";'
    
def ExportLayer( settings ):
    origSelection = cmds.ls(selection=True)
    SelectExportJoints()   
    mel.eval(settings)
    cmds.select(origSelection)	

def ExportSelectedLayers():        
    for item in cmds.ls(type='animLayer'):
        if (cmds.animLayer(item,q=True,selected=True)):
            UpdateAnimLayer( item )
            ExportLayer ( GetExportSettings(item, None, None) )

def ExportLayerRange(start, end, name):
    cmds.playbackOptions(min=start,max=end) 
    ExportLayer ( GetExportSettings(None, start, end, name))  
    UpdateSelectedAnimLayer()
	
def ExportAll():
	for item in cmds.ls(type='animLayer'):
		if item != 'BaseAnimation':
			if GetFrameRange(item).isdigit():
			    UpdateAnimLayer(item)
			    ExportLayer(item)
                
def TryExportRange():
    start = cmds.intFieldGrp('rangeFields', query=True, value1=True)
    end = cmds.intFieldGrp('rangeFields', query=True, value2=True)
    name = cmds.textField('nameField', query=True, text=True)
    if start>end:
        snip.FailExit("Range start must be larger than end")
    if len(name) == 0:
        snip.FailExit("Name not valid")
    ExportLayerRange(start,end,name)


def ExportRangeWindow():
    menuWin = cmds.window( title="Trajectory Guide", iconName='TrajectoryGuide', resizeToFitChildren=True, te=50,le=300, widthHeight=(50, 50))
    cmds.columnLayout( adjustableColumn=True )
    cmds.intFieldGrp('rangeFields', numberOfFields=2, label='Range', value1=0, value2=20, columnAlign2=('Left','Left'))
    cmds.textField('nameField', width = 50)
    cmds.button(label='Export', command=('TryExportRange()'))
    cmds.setParent( '..' )
    cmds.showWindow( menuWin )

