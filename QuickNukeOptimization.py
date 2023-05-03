import nuke


#example code for memory
node = nuke.selectedNode()
memory_used = nuke.memory(node)

#example code for if a node is in the main pipeline
node.affectedByGlobalScale()

#There is no way to get all the nodes in a script without looping through all of them :(

#actual code:

num_of_nodes_to_show = 10

def insert_memory_value(c_node, l_memory):
    if l_memory:
        for node in l_memory:
            if c_node > node:
                l_memory.insert(c_node, node.position+1)
                
        if len(l_memory) > num_of_nodes_to_show:
            del l_memory[-1]
    else:
        l_memory.push(c_node)
        
    return l_memory



def check_memory_value(c_node, l_memory):
    if l_memory:
        if c_node.memory()<l_memory[0].memory and c_node.memory()>l_memory[-1].memory():
            return insert_memory_value(c_node, l_memory)
        elif c_node.memory() > l_memory[0].memory:
            l_memory.push(c_node)   #does this add the node to the beggining or end?
            if l_memory > num_of_nodes_to_show:
                del l_memory[-1]
            return l_memory
    else:
        return insert_memory_value(c_node, l_memory)
            
    return l_memory


def main():
    largest_memory = []
    for node in nuke.nodes():
        node_memory = nuke.memory(node)
        largest_memory = check_memory_value(node, largest_memory)
        
    for node in largest_memory:
        print(node.name() + ": " + str(node.memory()))


if __name__ == "__main__":
    main()