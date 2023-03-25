import nuke

#frame ranges and the frame range variable/node created
frame = [0, 15, 30, 45, 60]
frameRange = nuke.nodes.FrameRange(first_frame = 1, last_frame = 1)
rotos = []

#creating the frame holds and rotos
def createFrameholds():
    for x in frame:
        fh = nuke.nodes.FrameHold(firstFrame = frame[x]).setInput(0, frameRange)
        roto = nuke.nodes.Roto(premultiply = "alpha").setInput(0, fh)
        rotos.append(roto)
        

#start by connecting to whatever node you have selected
frameRange.setInput(0, nuke.selectedNode())
createFrameholds()
appendClips = nuke.nodes.AppendClip(inputs = rotos)

