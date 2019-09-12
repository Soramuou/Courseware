class du_path():
    node_used_times = []

    def __init__(self, variable, root):
        self.variable = variable
        self.root = root
        self.dict_paths = {v: set() for v in variable}

    def run(self):
        s = ""
        for v in self.variable:
            self.node_used_times.clear()
            if v in self.root.define:
                nodes = [self.root.id]
            else:
                nodes = [-1]
            self.deal_v_path(v, self.root, nodes, self.dict_paths[v])
            s += v + ":\n"
            for path in sorted([_ for _ in self.dict_paths[v]]):
                s += path + "\n"
        self.write_du_path(s)

    def write_du_path(self, s):
        file_du_path = open("du_path.txt", 'w', encoding='utf8')
        file_du_path.write(s)

    def deal_v_path(self, v, root, nodes_, paths):
        if nodes_.count(root.id) <= 2 and self.node_used_times.count(root.id) < 10:
            self.node_used_times.append(root.id)
            for child in root.children:
                nodes = nodes_.copy()
                if v in child.use and v in child.define:
                    if nodes[0] != -1:
                        if nodes[0] != child.id:
                            nodes.append(child.id)
                            paths.add("->".join([str(_) for _ in nodes]))
                            nodes = [child.id]
                            self.deal_v_path(v, child, nodes, paths)
                    else:
                        nodes = [child.id]
                        self.deal_v_path(v, child, nodes, paths)
                    paths.add(str(child.id) + "->" + str(child.id))
                else:
                    if v in child.use:
                        if nodes[0] != -1:
                            nodes.append(child.id)
                            paths.add("->".join([str(_) for _ in nodes]))
                        self.deal_v_path(v, child, nodes, paths)
                    elif v in child.define:
                        if nodes[0] != child.id:
                            nodes = [child.id]
                            self.deal_v_path(v, child, nodes, paths)
                    else:
                        nodes.append(child.id)
                        self.deal_v_path(v, child, nodes, paths)
