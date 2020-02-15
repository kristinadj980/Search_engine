class GraphNode:

    def __init__(self):
        self.document_path = None
        self.parents = []
        self.children = []


class Graph:

    def __init__(self):
        self.nodes = []

    def insert(self, document_path, links):
        new_node = GraphNode()
        new_node.document_path = document_path
        new_node.children = links
        new_node.parents = []

        for existing_node in self.nodes:
            for path in existing_node.children:
                # print(node.document_path, " == ", path)
                if new_node.document_path == path:
                    new_node.parents.append(existing_node.document_path)

            for path in new_node.children:
                if existing_node.document_path == path:
                    existing_node.parents.append(new_node.document_path)

        self.nodes.append(new_node)

