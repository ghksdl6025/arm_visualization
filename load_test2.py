import pandas as pd
from utils import draw_graph
import pygraphviz as pgv
import os
import pydot
from bs4 import BeautifulSoup as bs4

def plot_trace(test_case,prefix):
    '''
    test_case : pandas series
        case in pandas series as one row
    prefix: int
        prefix length of the case
    '''
    test_case = test_case.to_dict()
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
                if eventorder not in list(event_attributes.keys()):
                    event_attributes[eventorder] ={}
                event_attributes[eventorder]['Time'] = value
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
    trace.node_attr.update(shape="box",fontname='segoe ui')

    gloc = trace.add_subgraph(name='cluster_case_info',rank="same")
    gloc = trace.subgraphs()[-1]
    gloc.add_node(0, group='a', shape='plaintext', width=3, height=0, margin = 0, label='Case ID: '+str(caseid),fontsize=18, fontname='segoe ui bold')
    gloc.add_node(1, shape='plaintext', width=3, height=0, margin = 0, label='Actual Outcome: '+str(outcome),fontsize=18, fontname='segoe ui bold')
    gloc.add_node('predict', shape='plaintext', width=3, height=0, margin = 0, label='Predicted Outcome: '+str(outcome),fontsize=18, fontname='segoe ui bold')
    gloc.add_edge(0,1,constraint='false',style='invis')
    gloc.add_edge(1,'predict',constraint='false',style='invis')
    gloc.graph_attr.update(style='dotted',label='Case Information',fontsize=25, fontname='helvetica')

    #Plot trace
    trace_init = trace.add_subgraph(name='trace')
    trace_init.add_node('start', shape='circle',label='',group='a')
    trace_init.add_node('dummy', style='invis',fontsize=16,group='b')

    #Plot case attributes
    case_att_sub =trace.add_subgraph(name='cluster_case_att',style='solid',color='hotpink',label='Case level attributes',fontsize=18,fontname='segoe ui')
    caseatt_labeling = '<<table border="0">'
    for pos,att in enumerate(case_attributes):
        caseatt_labeling += '<tr><td port="%s" border="1" cellspacing="10"> %s </td><td port="%s_value" border="1">%s</td></tr>'%(att[0],att[0],att[0],att[1])
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
        event_labeling += '<tr><td port="Activity" colspan="2" border="2" cellpadding="10"> <FONT POINT-SIZE="17" face="segoe ui historic">%s</FONT></td></tr>'%(event_attributes[att]['Activity'])
        for pos,eatt in enumerate(e_att_order):
            if eatt in list(event_attributes[att].keys()):
                # <tr><td port="0">0</td><td bgcolor="green">1</td><td bgcolor="orange">2</td><td>3</td></tr>
                event_labeling += '<tr><td port="%s" border="1"> %s </td><td port="%s_value" border="1">%s</td></tr>'%(eatt,eatt,eatt,event_attributes[att][eatt])
        event_labeling += '</table>>'
        trace_init.add_node('e'+str(att),label=event_labeling, shape='none')
        act_in_trace.append('e'+str(att))
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
    try:
        os.makedirs('./img/prefix'+str(prefix))
    except:
        pass
    output_file = '/prefix'+str(prefix)+'/case_%s_trace_v2'%(caseid)
    trace = str(trace)

    with open('./img'+output_file+'.dot','w') as f:
        f.write(trace)
    # draw_graph.save_graph_as_png(trace,output_file)

    # #Plot case attributes


def trace_coloring(dotfile,attributes,outcome,filetype='png'):
    with open(dotfile,'r') as f:
        graph = pydot.graph_from_dot_data(f.read())[0]

    for t in graph.get_subgraph_list():
        if t.get_name() =='trace':
            trace = t
        elif t.get_name() =='cluster_case_info':
            case_info = t
        elif t.get_name() =='cluster_case_att':
            case_att = t
    
    for i in case_info.get_node_list():
        if i.get_name() == 'predict':
            i.set('label','Predicted Outcome: '+str(outcome))

    case_atts=[]
    event_atts=[]
    event_attributes={}

    for rule in attributes:
        for r in rule:
            if '(case)' in r:
                case_atts.append(''.join(r.split('_')[:-1]))
            else:
                r = r.split('_')
                attribute = ''.join(r[:-1])
                eventorder = str(attribute[-1])
                attribute = attribute[:-1]
                if eventorder not in list(event_attributes.keys()):
                    event_attributes[eventorder] =[attribute]
                else:
                    event_attributes[eventorder].append(attribute)

    # Case attributes coloring
    for i in case_att.get_node_list():
        if i.get_name() =='case_att':
            case_att_label = i.get_attributes()['label']

    for ca in case_atts:
        soup = bs4(case_att_label, features='lxml')
        target_resource = soup.find(port=ca)['bgcolor']='deepskyblue'
        target_resource = soup.find(port='%s_value'%(ca))['bgcolor']='deepskyblue'
        target_label = '<'+ str(soup.find('table'))+'>'
        i.set('label',target_label)
    # Event attributes coloring
    for e in list(event_attributes.keys()):
        for i in trace.get_node_list():
            if e in i.get_name():
                event_att_label = i.get_attributes()['label']
                soup = bs4(event_att_label, features='lxml')
                for ea in event_attributes[e]:
                    target_resource = soup.find(port=ea)['bgcolor']='deepskyblue'
                    if 'Activity' not in ea:
                        target_resource = soup.find(port='%s_value'%(ea))['bgcolor']='deepskyblue'
                target_label = '<'+ str(soup.find('table'))+'>'
                i.set('label',target_label)
                

    # Save test case trace
    graph = str(graph)
    with open(dotfile,'w') as f:
        f.write(graph)
    dotfile = dotfile[:-4]
    dotfile = '/'+dotfile.split('/')[2]+'/'+dotfile.split('/')[3]
    if filetype =='png':
        draw_graph.save_graph_as_png(graph,dotfile)
    elif filetype=='pdf':
        draw_graph.save_graph_as_pdf(graph,dotfile)