import pandas as pd
from utils import draw_graph
import pygraphviz as pgv
df = pd.read_csv('../new paper/bpic2015/ltl1/bpic2015_1/indexbase/prefix6/simple_timediscretize/test_rndst0.csv')


test_case = df.iloc[5,:].to_dict()
case_attributes = []
event_attributes = {}
for t in test_case.keys():
    t = t.split('_')
    if '(case)' in t[0]:
        if test_case['_'.join(t)] ==1:
            value = t[-1]
            attribute = ''.join(t[:-1])
            case_attributes.append((attribute,value))
    elif 'Case ID' in t:
        caseid = test_case[t[0]]
    elif 'Label' in t:
        if test_case['_'.join(t)] ==1:
            outcome = t[1]
    elif 'Time' in t[0]:
        if test_case['_'.join(t)] ==1:
            value = t[-1]
            attribute = ''.join(t[:-1])
            eventorder = int(attribute[-1])
            attribute = attribute[:-1]
            if eventorder+1 not in list(event_attributes.keys()):
                event_attributes[eventorder+1] ={}
            event_attributes[eventorder+1]['Time'] = value
    else:
        if test_case['_'.join(t)] ==1:
            value = t[-1]
            attribute = ''.join(t[:-1])
            eventorder = int(attribute[-1])
            attribute = attribute[:-1]
            if eventorder not in list(event_attributes.keys()):
                event_attributes[eventorder] ={}
            event_attributes[eventorder][attribute] = value

            # event_attributes.append((attribute,eventorder,value))
#Initialize Trace Graph
trace = pgv.AGraph(name='test_case',strict=False,directed=True,rankdir="TB",compound=True)
trace.graph_attr.update(dpi=300)
trace.node_attr.update(shape="box")

gloc = trace.add_subgraph(name='cluster_case',rank="same")
gloc = trace.subgraphs()[-1]
gloc.add_node(0, group='a', shape='plaintext', width=0, height=0, margin = 0, label='Case ID: '+str(caseid))
gloc.add_node(1, shape='plaintext', width=0, height=0, margin = 0, label='Actual Outcome: '+str(outcome))
gloc.add_edge(0,1,constraint='false',style='invis')
gloc.graph_attr.update(style='dotted',label='Case Information',fontsize=20)

#Plot case attributes
case_att_sub =trace.add_subgraph(name='cluster_case_att',style='solid',color='hotpink',label='Case level attributes',fontsize=18)
prev_entity = 0
for pos,att in enumerate(case_attributes):
    case_att_sub.add_node('c'+str(pos), label='|'.join(att),shape='record')
    
    if prev_entity !=0:
        case_att_sub.add_edge(prev_entity, 'c'+str(pos), style='invis')
    prev_entity = 'c'+str(pos)



#Plot trace
trace_init = trace.add_subgraph(name='trace')
trace_init.add_node('start', shape='circle',label='')
trace_init.add_node('end', shape='doublecircle',label='')


#Plot events
case_length = len(event_attributes.keys())
act_in_trace = []
e_att_order = sorted(list(event_attributes[2].keys()))
e_att_order.remove('Activity')

for att in range(1,case_length+1):
    eventname = 'event'+str(att)
    event_sub = trace_init.add_subgraph(name='cluster_'+eventname,rank='same')
    # event_sub = trace.subgraphs()[-1]
    event_sub.graph_attr.update(style='filled',color='cornsilk')
    event_sub.add_node('e'+str(att)+'_act', label=event_attributes[att]['Activity'])
    act_in_trace.append('e'+str(att)+'_act')
    prev_entity = 'e'+str(att)+'_act'
    
    sub_event_order = []
    for pos,eatt in enumerate(e_att_order):
        if eatt in list(event_attributes[att].keys()):
            event_sub.add_node('e'+str(att)+'_att'+str(pos), label = eatt +'|'+event_attributes[att][eatt], shape='record')
            sub_event_order.append((prev_entity, 'e'+str(att)+'_att'+str(pos)))
            prev_entity = 'e'+str(att)+'_att'+str(pos)
    
        # event_sub.add_edge(prev_entity,'e'+str(att)+'_att'+str(pos), style='invis', constraint='false')
    # event_sub.add_edges_from(sub_event_order, style='invis', constraint='false')

prev = 'start'
for i in act_in_trace:
    trace_init.add_edge(prev,i)
    prev = i
trace_init.add_edge(prev,'end')

#Cluster case att and event att

trace.add_edge(0,'start',style='invis')
#Save trace graph as png

output_file = 'case_%s_trace_v1'%(caseid)
trace = str(trace)
draw_graph.save_graph_as_png(trace,output_file)

#Plot case attributes


