import nuke

#frame ranges and the frame range variable/node created
frame = [0, 15, 30, 45, 60]
frameRange = nuke.nodes.FrameRange(first_frame = 1, last_frame = 1)
rotos = []

#creating the frame holds and rotos
def createFrameholds():
    for x in frame:
        fh = nuke.nodes.FrameHold(firstFrame = x)
        fh.setInput(0, frameRange)
        roto = nuke.nodes.Roto(output = "alpha", premultiply = "alpha")
        roto.setInput(0, fh)
        rotos.append(roto)
        

#start by connecting to whatever node you have selected
frameRange.setInput(0, nuke.selectedNode())
createFrameholds()
appendClips = nuke.nodes.AppendClip(inputs = rotos)

#setting ground truth

copyGround = nuke.nodes.Copy(inputs = [appendClips, appendClips])
copyGround.knob('to0').setValue('rgba.red')


removeGround = nuke.nodes.Remove(operation = "keep", channels = "red")
removeGround.setInput(0, copyGround)

#setting input
removeInput = nuke.nodes.Remove(operation = "keep", channels = "rgb")
removeInput.setInput(0, appendClips)

#copycat

copyCatNode = nuke.nodes.CopyCat(inputs = [removeInput, removeGround])