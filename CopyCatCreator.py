import nuke

frame = [0, 15, 30, 45, 60]
frameRange = nuke.nodes.FrameRange(first_frame = 1, last_frame = 1)

def createFrameholds():
    for x in frame:
        fh = nuke.nodes.FrameHold(firstFrame = x).setInput(0, frameRange)
        nuke.nodes.Roto(premultiply = "alpha").setInput(0, fh)

frameRange.setInput(0, selectedNode())


