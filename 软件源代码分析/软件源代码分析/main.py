from pycparser import c_parser
import cfg
from du_path import du_path
from drawCFG import drawCFG
def read_file(file):
    source = open(file, 'r').readlines()
    format_source = ""
    in_quote = False
    in_comment = False
    for line in source:
        if '#' != line[0]:
            new_line = ""
            for index in range(len(line)):
                if not in_quote and not in_comment:
                    if index + 1 < len(line) and line[index]=="/" and line[index + 1] == "/":
                        break
                if not in_quote:
                    if (index + 1 < len(line) and line[index] + line[index + 1] == '/*') or (
                            index > 1 and line[index - 2] + line[index - 1] == '*/'):
                        in_comment = not in_comment
                if not in_comment:
                    new_line += line[index]
                    if line[index] == '"' or line[index] == '"':
                        in_quote = not in_quote
            format_source += new_line.replace("*/", "")

    parser = c_parser.CParser()
    return parser.parse(format_source)


if __name__ == '__main__':
    file = "t1.c"
    ast = read_file(file)

    start_node = cfg.Node()
    variable = start_node.run(ast)

    drawCFG = drawCFG(start_node)
    drawCFG.run()

    path=du_path(variable,start_node)
    path.run()
