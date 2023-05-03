import nuke

"""
#example code for memory
node = nuke.selectedNode()
memory_used = nuke.memory(node)

#example code for if a node is in the main pipeline
node.affectedByGlobalScale()

#There is no way to get all the nodes in a script without looping through all of them :(
"""

#actual code:

num_of_nodes_to_show = 10

def insert_memory_value(c_node, l_memory):
    if not l_memory or l_memory is None:
        l_memory.insert(0, c_node)
    else:
        for node in l_memory:
            if c_node > node:
                l_memory.insert(l_memory.index(node), c_node)
                
        if len(l_memory) > num_of_nodes_to_show:
            del l_memory[-1]
    
        
    return l_memory



def check_memory_value(c_node, l_memory):
    if not l_memory or l_memory is None:
        return insert_memory_value(c_node, l_memory)

    c_memory = nuke.memory(c_node)
    if c_memory is not None and c_memory<nuke.memory(l_memory[0]) and c_memory>nuke.memory(l_memory[-1]):
        return insert_memory_value(c_node, l_memory)
    elif c_memory is not None and c_memory > nuke.memory(l_memory[0]):
        l_memory.insert(0, c_node)
        if len(l_memory) > num_of_nodes_to_show:
            del l_memory[-1]
        return l_memory
    
            
    return l_memory


def main():
    largest_memory = []
    for n in nuke.allNodes():
        if n.Class() not in ['Read', 'Write', 'Viewer']:
            node_memory = nuke.memory(n)
            largest_memory = check_memory_value(n, largest_memory)
        
    for node in largest_memory:
        print(node.name() + ": " + str(nuke.memory(node)))


if __name__ == "__main__":
    main()