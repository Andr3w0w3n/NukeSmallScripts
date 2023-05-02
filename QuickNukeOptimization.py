import nuke


#example code for memory
node = nuke.selectedNode()
memory_used = nuke.memory(node)

#example code for if a node is in the main pipeline
node.affectedByGlobalScale()

#There is no way to get all the nodes in a script without looping through all of them

#actual code:

def insert_memory_value(c_node, l_memory):
    if l_memory:
        for node in l_memory:
    else:
        l_memory.push(c_node)



def check_memory_value(c_node, l_memory):
    if l_memory:
        if
        
    else:
        insert_memory_value()
            
        


def main():
    largest_memory = []
    for node in nuke.nodes():
        node_memory = nuke.memory(node)
        check_memory_value(node, largest_memory)



if __name__ == "__main__":
    main()