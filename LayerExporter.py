import maya.cmds as cmds
import maya.mel as mel
import LayerTools as layerTools
import LayerUpdater as layerUpdater
import Snippets as snip

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
    layerFrameRange = layerTools.GetFrameRange(exportLayer)
    if layerFrameRange.isdigit():
        max = layerFrameRange
    max = max if end == None else str(end)
    mel.eval('FBXExportBakeComplexAnimation -v true;')
    mel.eval("FBXExportBakeComplexStart -v " + min) 
    mel.eval("FBXExportBakeComplexEnd -v " + max)
    if fileName == None or len(fileName) == 0:
        fileName = GetExportName(exportLayer);
    return 'FBXExport -f "' + snip.GetFilePath() + "/FBX/" + fileName + '.fbx";'

def IsExportable(item):
    return layerTools.GetFrameRange(item).isdigit() 

def ExportLayer( settings ):
    origSelection = cmds.ls(selection=True)
    SelectExportJoints() 
    print settings  
    mel.eval(settings)
    cmds.select(origSelection)  

def ExportSelectedLayers():
    for item in layerTools.GetSelectedLayers():
            if IsExportable(item):
                layerUpdater.UpdateAnimLayer( item )
                ExportLayer ( GetExportSettings(item, None, None) )

def ExportLayerRange(start, end, name):
    cmds.playbackOptions(min=start,max=end) 
    ExportLayer ( GetExportSettings(None, start, end, name))  
    layerUpdater.UpdateSelectedAnimLayer()
    
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
    exportRangeWin = cmds.window( title="Export Layer Range", iconName='Export Layer Range', resizeToFitChildren=True, te=300,le=1400, widthHeight=(50, 50))
    cmds.columnLayout( adjustableColumn=True )
    cmds.intFieldGrp('rangeFields', numberOfFields=2, label='Range', value1=0, value2=20, columnAlign2=('Left','Left'))
    cmds.textField('nameField', width = 50)
    cmds.button(label='Export', command=('TryExportRange()'))
    cmds.setParent( '..' )
    cmds.showWindow( exportRangeWin )