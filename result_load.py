import pandas as pd
from ast import literal_eval
import load_test2
prefix=str(6)
file_name='../new paper/bpic2015/ltl1/ruleresult/way3/fifthmethod/bpic2015_1/Summerized_prefix%s prediction_result.csv'%(prefix)
df = pd.read_csv(file_name)
testset_name = '../new paper/bpic2015/ltl1/bpic2015_1/indexbase/prefix%s/simple_timediscretize/test_rndst0.csv'%(prefix)
testset = pd.read_csv(testset_name)

for t in range(10):
    load_test2.plot_trace(testset.loc[t,:],prefix)
    caseid = str(list(df['case_id'])[t])
    dotfile = './img/prefix6/case_%s_trace_v2.dot'%(str(caseid))
    predict_result = {str(caseid): list(df['predict_y'])[pos] for pos,caseid in enumerate(list(df['case_id']))}

    case_sfrule = {}
    for pos,rules in enumerate(list(df['Satisfying rules'])):
        case_sfrule[str(list(df['case_id'])[pos])]=literal_eval(rules)
    load_test2.trace_coloring(dotfile,case_sfrule[caseid],outcome=predict_result[caseid])