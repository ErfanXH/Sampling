from utils import variable_elimination

def exact_inference(query, evidence, cpts, graph):
    new_cpts = []
    parents = graph['parents_nodes']
    for i, cpt in enumerate(cpts):
        tb = []
        for row in cpt:
            if evidence.get(i) != None and evidence[i] != row[i]: 
                continue
            flag = True
            for j in parents[i]:
                if evidence.get(j) and row[j] != evidence[j]:
                    flag = False
            if flag:
                tb.append(row)
        new_cpts.append(tb)
    return variable_elimination(evidence, query, new_cpts)