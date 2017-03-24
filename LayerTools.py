import maya.cmds as cmds
import Snippets as snip
import maya.mel as mel

def GetTextName(layer):
    layerTok = layer.split('_')
    layerTok.pop()
    layerName=''
    for s in layerTok:
        layerName += s
        layerName += '_'
    return layerName[:len(layerName)-1]

def GetFrameRange( sel ):
    if sel is None:
        return ''
    splitName = sel.split('_')
    endFrame = splitName[-1]
    endFrame = endFrame.replace("f", "")
    return endFrame

def GetParentLayer( layer ):
    return cmds.animLayer(layer, q=True, parent = True )

def GetAncestors ( item, layers ):
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

def GetSelectedLayers():
    layers = []
    for item in cmds.ls(type='animLayer'):
        if (cmds.animLayer(item,q=True,selected=True)):
            layers.append(item)
    return layers

def FindReplaceInName( find, replaceWith ):
    for l in GetSelectedLayers():
        cmds.rename(l, l.replace(find, replaceWith))

def TryFindReplace():
    FindReplaceInName(cmds.textField('FindField', query=True, text=True), cmds.textField('ReplaceField', query=True, text=True))

def LayerRenameWindow():
    renameWindow = cmds.window( title="LayerRename", iconName='LayerRename', resizeToFitChildren=True, te=300,le=1400, widthHeight=(50, 50))
    cmds.columnLayout( adjustableColumn=True )
    cmds.text(  label = 'Find')
    cmds.textField('FindField', width = 50)
    cmds.text(  label = 'Replace')
    cmds.textField('ReplaceField', width = 50, enterCommand='TryFindReplace()')
    cmds.button(label='Replace', command=('TryFindReplace()'))
    cmds.text(  label = 'Prefix')
    cmds.textField('Prefix',  width = 50)
    cmds.text(  label = 'Suffix')
    cmds.textField('Suffix', width = 50, enterCommand='TryNameAfterParent()')
    cmds.button(label='Rename', command=('TryNameAfterParent()'))
    cmds.setParent( '..' )
    cmds.showWindow( renameWindow )

def GetSelectedOrAllLayers():
    selected = GetSelectedLayers()
    if len(selected) == 0:
        selected =cmds.ls(type='animLayer')
    return selected

def TryNameAfterParent():
    for l in GetSelectedLayers():
        par = cmds.animLayer(l, query=True, parent=True)
        if par != 'BaseAnimation':
            cmds.rename(l, cmds.textField('Prefix', query = True, text=True) + GetTextName(par) + cmds.textField('Suffix', query = True, text=True))

def ExpandLayer(layer):
    if cmds.animLayer(layer, query=True, children = True):
        mel.eval('animLayerExpandCollapseCallback "' + layer + '" 1;')

def CollapseLayer(layer):
    if cmds.animLayer(layer,query=True, children = True):
        mel.eval('animLayerExpandCollapseCallback "' + layer + '" 0;')

def ExpandSelectedLayers():
    for l in GetSelectedOrAllLayers():
        ExpandLayer(l)

def CollapseSelectedLayers():
    for l in GetSelectedOrAllLayers():
        CollapseLayer(l)