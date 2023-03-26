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

#def prompt():
    #user_input = nuke.getInput("Enter the frames you want to have (seperated by a space):", "0")
    #frameString = mainPanel.addSingleLineInput("Enter the frames you want to have (seperated by a space):", "0")
    #mainPanel.show()
    #if mainPanel.ok:
    #    frame = [int(n) for n in frameString.value().split()]
    #elif mainPanel.cancel:
    #    nuke.message("User cancelled operation")
    #    return
        
def prompt():
    mainPanel = nuke.Panel("Quick CopyCat Roto System Creation")
    mainPanel.addSingleLineInput("Enter the frames (separated by a space):", "0")
    mainPanel.show()
    return [int(n) for n in mainPanel.value("Enter the frames (separated by a space):").split()]
 
      
def main():
    frame = prompt().copy()

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

if __name__ == "__main__":
    main()