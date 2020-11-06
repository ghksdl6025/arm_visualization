import pydot
import graphviz
from utils import draw_graph
from html.parser import HTMLParser

parser = HTMLParser()
with open('./case_7357800_trace_v2.dot','r') as f:
    graph = pydot.graph_from_dot_data(f.read())[0]

for t in graph.get_subgraph_list():
    print(t.get_node_list())
#     if 'case_att' in t.name:
#         case_att = t.nodes()[-1]
# # print(case_att.attr['label'])
# print(parser.feed(case_att.attr['label']))


