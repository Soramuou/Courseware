from graphviz import Digraph


class drawCFG(object):
    name = "cfg"
    format = 'png'
    node_set = set()

    def __init__(self, root):
        self.root = root
        self.g = Digraph(self.name)
        self.g.format = self.format

    def run(self):
        self.deal_draw(self.root)
        self.g.render()

    def deal_draw(self, root):
        if root.id not in self.node_set:
            self.node_set.add(root.id)
            label = "D: " + str(root.define) + "\n U: " + str(root.use) + "\n" + str(root.id)
            self.g.node(name=str(root.id), color='orange', label=label)
            for child in root.children:
                self.g.edge(str(root.id), str(child.id), color="green")
                self.deal_draw(child)
