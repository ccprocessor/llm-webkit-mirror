class TreeOpt:
    def __init__(self, root_node):
        self.root_node = root_node

    def print_tree_nodes(self, node=None, level=0):
        if node is None:
            node = self.root_node
            
        indent = '  ' * level 
        print(f"{indent}Tag: {node.tag}, Text: {node.text.strip() if node.text else 'None'}, Attributes: {node.attrib}")

        for child in node:
            self.print_tree_nodes(child, level + 1)

    def count_nodes(self, node=None):
        if node is None:
            node = self.root_node
            
        count = 1 
        for child in node:
            count += self.count_nodes(child)

        return count
    
    def count_p_tags(self, node=None):
        if node is None:
            node = self.root_node

        p_count = sum(1 for node in node.iter() if node.tag == 'p')
        print('num p tags:', p_count)
        return p_count
    
    def get_nodes_info(self, node=None):
        self.print_tree_nodes()
        count = self.count_nodes()
        print('Total nodes:', count)

