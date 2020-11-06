import graphviz

def save_graph_as_pdf(dot_string, output_file):
    if type(dot_string) is str:
        g = graphviz.Source(dot_string)
    elif isinstance(dot_string, (graphviz.dot.Digraph, graphviz.dot.Graph)):
        g = dot_string
    g.format = 'pdf'
    g.filename = output_file
    g.directory = './img/'
    g.render(view=False)

    return g

def save_graph_as_png(dot_string, output_file):
    if type(dot_string) is str:
        g = graphviz.Source(dot_string)
    elif isinstance(dot_string, (graphviz.dot.Digraph, graphviz.dot.Graph)):
        g = dot_string
    g.format = 'png'
    g.filename = output_file
    g.directory = './img/'
    g.render(view=False)

    return g

if __name__=='__main__':
    with open('../case_7357800_trace_v2.dot','r') as f:
        dot_graph = f.read()
    save_graph_as_png(dot_graph, 'test_dot')