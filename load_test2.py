import pandas as pd
from utils import draw_graph
import pygraphviz as pgv
df = pd.read_csv('../new paper/bpic2015/ltl1/bpic2015_1/indexbase/prefix6/simple_timediscretize/test_rndst0.csv')


test_case = df.iloc[10,:].to_dict()
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
trace.node_attr.update(shape="box",fontname='segio ui')

gloc = trace.add_subgraph(name='cluster_case_info',rank="same")
gloc = trace.subgraphs()[-1]
gloc.add_node(0, group='a', shape='plaintext', width=5, height=0, margin = 0, label='Case ID: '+str(caseid),fontsize=18, fontname='segio ui bold')
gloc.add_node(1, shape='plaintext', width=5, height=0, margin = 0, label='Actual Outcome: '+str(outcome),fontsize=18, fontname='segio ui bold')
gloc.add_edge(0,1,constraint='false',style='invis')
gloc.graph_attr.update(style='dotted',label='Case Information',fontsize=25, fontname='helvetica')

#Plot trace
trace_init = trace.add_subgraph(name='trace')
trace_init.add_node('start', shape='circle',label='',group='a')
trace_init.add_node('dummy', style='invis',fontsize=16,group='b')

#Plot case attributes
case_att_sub =trace.add_subgraph(name='cluster_case_att',style='solid',color='hotpink',label='Case level attributes',fontsize=18,fontname='segio ui')
caseatt_labeling = '<<table border="0">'
for pos,att in enumerate(case_attributes):
    caseatt_labeling += '<tr><td port="%s" border="1" cellspacing="10"> %s </td><td border="1">%s</td></tr>'%(att[0],att[0],att[1])
caseatt_labeling += '</table>>'
case_att_sub.add_node('case_att', label=caseatt_labeling,shape='none',fontsize=16,group='b')

#Plot events
case_length = len(event_attributes.keys())
act_in_trace = []
e_att_order = sorted(list(event_attributes[2].keys()))
e_att_order.remove('Activity')
prev = 'start'
for att in range(1,case_length+1):
    event_labeling = '<<table border="0" cellspacing="0" cellpadding="2">'
    event_labeling += '<tr><td port="activity" colspan="2" border="2" cellpadding="10"> <FONT POINT-SIZE="17" face="segio ui history">%s</FONT></td></tr>'%(event_attributes[att]['Activity'])
    for pos,eatt in enumerate(e_att_order):
          if eatt in list(event_attributes[att].keys()):
            # <tr><td port="0">0</td><td bgcolor="green">1</td><td bgcolor="orange">2</td><td>3</td></tr>
            event_labeling += '<tr><td port="%s" border="1"> %s </td><td border="1">%s</td></tr>'%(eatt,eatt,event_attributes[att][eatt])
    event_labeling += '</table>>'
    trace_init.add_node('e'+str(att),label=event_labeling, shape='none')
    act_in_trace.append('e'+str(att))
    print(event_attributes[att]['Activity'])
prev = 'start'
for i in act_in_trace:
    trace_init.add_edge(prev,i)
    prev = i

#Cluster case att and event att

trace.add_edge(0,'start',style='invis')
trace.add_edge('1','dummy',style='invis')
trace.add_edge('dummy','case_att',style='invis')
trace.add_edge('e1','case_att',style='invis',constraint='false')



#Save trace graph as png

output_file = 'case_%s_trace_v2'%(caseid)
trace = str(trace)
with open(output_file+'.dot','w') as f:
    f.write(trace)

# draw_graph.save_graph_as_png(trace,output_file)

# #Plot case attributes


