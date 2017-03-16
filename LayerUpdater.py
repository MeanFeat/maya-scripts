import maya.cmds as cmds
import maya.mel as mel
import Snippets as snip

def CreateScriptJob():
    return cmds.scriptJob(e=("animLayerRefresh", UpdateSelectedAnimLayer), killWithScene=True)

def GetFrameRange( sel ):
    if sel is None:
        return ''
    splitName = sel.split('_')
    endFrame = splitName[-1]
    endFrame = endFrame.replace("f", "")
    return endFrame

def UpdateSelectedAnimLayer():
    for item in cmds.ls(type='animLayer'):
        if (cmds.animLayer(item,q=True,selected=True)):
			UpdateAnimLayer( item )

def GetParentLayer( layer ):
    return cmds.animLayer(layer, q=True, parent = True )

def GetParents ( item, layers):
    done = False;
    while not done:
        done = True
        item = GetParentLayer(item)
        if item != 'BaseAnimation':
            layers.append(item)
            done = False
    return layers

def GetChildren(item, layers):
    children = cmds.animLayer(item, q=True, children=True)            
    if children != None:
        for c in children:
            layers.append(c)
    return layers

def UpdateAnimLayer( layer ):
    unmute = []
    for item in cmds.ls(type='animLayer'):
        if (item == layer):
            if(GetFrameRange(item).isdigit()):
                cmds.playbackOptions(max=GetFrameRange(item))
            unmute.append(item)
            unmute = GetParents(item, unmute)
            unmute = GetChildren(item, unmute)
        elif item != 'BaseAnimation':
            cmds.setAttr(item + ".lock", 1)
            cmds.setAttr(item + ".mute", 1)
    for u in unmute:
        cmds.setAttr(u + ".mute", 0)
        cmds.setAttr(u + ".lock", 0)

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
    mel.eval('FBXExportBakeComplexAnimation -v 1;')
    mel.eval('FBXExportConstraints -v 0;')
    mel.eval('FBXExportInputConnections -v 0;')
    mel.eval('FBXExportShapes -v 1;')
    mel.eval('FBXExportSmoothMesh -v 1;')
    min = str(0) if start == None else str(start)
    layerFrameRange = GetFrameRange(exportLayer)
    if layerFrameRange.isdigit():
        max = layerFrameRange
    max = max if end == None else str(end)
    mel.eval("FBXExportBakeComplexStart -v " + min) 
    mel.eval("FBXExportBakeComplexEnd -v " + max)
    if len(fileName) == 0:
        fileName = GetExportName(exportLayer);
    return 'FBXExport -f "' + snip.GetFilePath() + "/FBX/" + fileName + '.fbx";'

def IsExportable(item):
    return GetFrameRange(item).isdigit() 
  
def ExportLayer( settings ):
    origSelection = cmds.ls(selection=True)
    SelectExportJoints()   
    mel.eval(settings)
    cmds.select(origSelection)	

def GetSelectedLayers():
    layers = []
    for item in cmds.ls(type='animLayer'):
        if (cmds.animLayer(item,q=True,selected=True)):
            layers.append(item)
    return layers

def ExportSelectedLayers():
    for item in GetSelectedLayers():
            if IsExportable(item):
                UpdateAnimLayer( item )
                ExportLayer ( GetExportSettings(item, None, None) )

def ExportLayerRange(start, end, name):
    cmds.playbackOptions(min=start,max=end) 
    ExportLayer ( GetExportSettings(None, start, end, name))  
    UpdateSelectedAnimLayer()
	
def ExportAll():
	for item in cmds.ls(type='animLayer'):
		if item != 'BaseAnimation':
			if IsExportable(item):
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