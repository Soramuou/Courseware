id = 0
used_nodes = set()
variable = set()


class Node(object):

    def __init__(self, is_branch=False):
        global id
        self.use = set()
        self.define = set()
        self.children = []
        self.id = id
        self.is_branch = is_branch
        id += 1

    def run(self, ast):
        self.deal_block(ast, self)
        self.delete_node(self)
        return variable

    # 处理等式
    def deal_assignment(self, assignment, node):
        self.deal_lvalue(assignment.lvalue, node)
        self.deal_expression(assignment.rvalue, node)

    # 处理等式左边
    def deal_lvalue(self, lvalue, node):
        if 'ID' in str(type(lvalue)):
            node.define.add(lvalue.name)
        else:
            lvalue_children = [_ for _ in lvalue]
            self.deal_lvalue(lvalue_children[0], node)
            for child in lvalue_children[1:]:
                self.deal_expression(child, node)

    # 处理表达式
    def deal_expression(self, expression, node):
        if 'ID' in str(type(expression)):
            node.use.add(expression.name)
        else:
            for child in expression:
                self.deal_expression(child, node)

    # 处理块儿
    def deal_block(self, block, node):
        for child in block:
            if node.is_branch:
                temp_node = Node()
                node.children.append(temp_node)
                node = temp_node

            if 'Decl' in str(type(child)) and child.init is not None:
                node.define.add(child.name)

            if 'FuncDef' in str(type(child)):
                node = self.deal_block(child.body.block_items, node)

            if 'While' in str(type(child)):
                cond_node = Node(True)
                node.children.append(cond_node)
                self.deal_expression(child.cond, cond_node)
                tail_stmt_node = self.deal_block(child.stmt, cond_node)
                tail_stmt_node.children.append(cond_node)
                node = cond_node

            if 'Assignment' in str(type(child)):
                self.deal_assignment(child, node)

            if 'FuncCall' in str(type(child)) and child.args is not None:
                self.deal_expression(child.args.exprs, node)

            if 'Compoud' in str(type(child)):
                self.deal_block(child.block_items, node)

            if 'If' in str(type(child)):
                cond_node = Node(True)
                node.children.append(cond_node)
                self.deal_expression(child.cond, cond_node)
                node = Node()
                if child.iftrue is not None:
                    tail_true_node = self.deal_block(child.iftrue, cond_node)
                    tail_true_node.children.append(node)
                else:
                    cond_node.children.append(node)
                if child.iffalse is not None:
                    tail_false_node = self.deal_block(child.iffalse, cond_node)
                    tail_false_node.children.append(node)
                else:
                    cond_node.children.append(node)
        return node

    # 去掉没用的空结点
    def delete_node(self, node):
        global variable
        if node.id not in used_nodes:
            used_nodes.add(node.id)
            node_children = node.children.copy()
            variable = variable | node.use | node.define
            while node_children:
                child = node_children.pop()
                if len(child.use) == 0 and len(child.define) == 0:
                    for grandchild in child.children:
                        node.children.append(grandchild)
                        node_children.append(grandchild)
                    node.children.remove(child)
                else:
                    self.delete_node(child)
