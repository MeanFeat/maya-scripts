import maya.cmds as cmds
import Snippets as snip

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
    layers = GetSelectedLayers()
    for l in layers:
        cmds.rename(l, l.replace(find, replaceWith))

def TryFindReplace():
    FindReplaceInName(cmds.textField('FindField', query=True, text=True), cmds.textField('ReplaceField', query=True, text=True))

def FindReplaceWindow():
    findReplaceWin = cmds.window( title="FindAndReplace", iconName='FindAndReplace', resizeToFitChildren=True, te=300,le=1400, widthHeight=(50, 50))
    cmds.columnLayout( adjustableColumn=True )
    cmds.textField('FindField', width = 50)
    cmds.textField('ReplaceField', width = 50)
    cmds.button(label='Ok', command=('TryFindReplace()'))
    cmds.setParent( '..' )
    cmds.showWindow( findReplaceWin )