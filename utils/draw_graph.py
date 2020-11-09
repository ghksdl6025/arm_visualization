import graphviz

def save_graph_as_pdf(dot_string, output_file):
    if type(dot_string) is str:
        g = graphviz.Source(dot_string)
    elif isinstance(dot_string, (graphviz.dot.Digraph, graphviz.dot.Graph)):
        g = dot_string
    if '/' in output_file:
        dir_add = output_file.split('/')[1]
        output_file = output_file.split('/')[2]
    g.format = 'pdf'
    g.filename = output_file
    g.directory = './img/' +dir_add
    print(output_file)
    g.render(view=False,cleanup=True)
    
    g.render(view=False,cleanup=True)

    return g

def save_graph_as_png(dot_string, output_file):
    if type(dot_string) is str:
        g = graphviz.Source(dot_string)
    elif isinstance(dot_string, (graphviz.dot.Digraph, graphviz.dot.Graph)):
        g = dot_string
    if '/' in output_file:
        dir_add = output_file.split('/')[1]
        output_file = output_file.split('/')[2]
    g.format = 'png'
    g.filename = output_file
    g.directory = './img/' +dir_add
    print(output_file)
    g.render(view=False,cleanup=True)

    return g

if __name__=='__main__':
    with open('../case_7357800_trace_v2.dot','r') as f:
        dot_graph = f.read()
    save_graph_as_png(dot_graph, 'test_dot')