import nuke

#frame ranges and the frame range variable/node created

rotos = []

#creating the frame holds and rotos
def createFrameholds(frame, frameRange):
    for x in frame:
        fh = nuke.nodes.FrameHold(firstFrame = x)
        fh.setInput(0, frameRange)
        roto = nuke.nodes.Roto(output = "alpha", premultiply = "alpha")
        roto.setInput(0, fh)
        rotos.append(roto)

#returns the user selected frames or the automatically created frames 
def promptUserFrame(mainPanel):
    temp = []
    if len(mainPanel.value("Enter the frames (separated by a space):")) == 0:
        nuke.message("With no frame(s) inquired, it has defaulted to every 15 frames for the clip length. \n Starting from the first frame")
        first_frame = nuke.Root().firstFrame()
        last_frame = nuke.Root().lastFrame()
        addedFrame = first_frame
        while(addedFrame < last_frame):
            temp.append(addedFrame)
            addedFrame = addedFrame+15
        return temp
    
    return [int(n) for n in mainPanel.value("Enter the frames (separated by a space):").split()]

#returns the level of copycat quality the user would want
def promptUserQuality(mainPanel, copyCatNode):
    quality = mainPanel.value("Quality of Job")
    if quality == "Low":
        copyCatNode.knob('epochs').setValue(40000)
        copyCatNode.knob('modelSize').setValue("Medium")
        copyCatNode.knob('cropSize').setValue(128)
    elif quality == "Medium":
        copyCatNode.knob('epochs').setValue(40000)
        copyCatNode.knob('modelSize').setValue("Medium")
        copyCatNode.knob('cropSize').setValue(256)
    elif quality == "High":
        copyCatNode.knob('epochs').setValue(40000)
        copyCatNode.knob('modelSize').setValue("Large")
        copyCatNode.knob('cropSize').setValue(256)
    else:
        copyCatNode.knob('epochs').setValue(40000)
        copyCatNode.knob('modelSize').setValue("Medium")
        copyCatNode.knob('cropSize').setValue(128)

def main():
    mainPanel = nuke.Panel("Quick CopyCat Roto System Creation")
    mainPanel.addSingleLineInput("Enter the frames (separated by a space):", "")
    mainPanel.addEnumerationPulldown("Quality of Job", "Low Medium High")
    mainPanel.show()
    frame = promptUserFrame(mainPanel).copy()

    frameRange = nuke.nodes.FrameRange(first_frame = 1, last_frame = 1)
    #print(frame)
    #start by connecting to whatever node you have selected
    frameRange.setInput(0, nuke.selectedNode())
    createFrameholds(frame, frameRange)
    appendClips = nuke.nodes.AppendClip(inputs = rotos)

    #setting ground truth
    copyGround = nuke.nodes.Copy(inputs = [appendClips, appendClips])
    copyGround.knob('from0').setValue('rgba.alpha')
    copyGround.knob('to0').setValue('rgba.red')

    removeGround = nuke.nodes.Remove(operation = "keep", channels = "red")
    removeGround.setInput(0, copyGround)

    #setting input
    removeInput = nuke.nodes.Remove(operation = "keep", channels = "rgb")
    removeInput.setInput(0, appendClips)

    #copycat
    copyCatNode = nuke.nodes.CopyCat(inputs = [removeInput, removeGround])
    promptUserQuality(mainPanel, copyCatNode)
    

if __name__ == "__main__":
    main()