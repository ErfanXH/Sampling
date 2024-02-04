from utils import topological_sort, mult, sample_vertex
import globals
import numpy as np

def gibbs_sample(query, evidence, cpts, graph, n):
    global num_samples
    vertexes = topological_sort(graph)
    samples = []
    for _ in range(globals.num_samples):
        sample = {}
        for vertex in vertexes:
            sample[vertex] = -1

        # fix evidences and sample the rest randomly (step 1 and 2)
        for vertex in vertexes:
            if vertex in evidence:
                sample[vertex] = evidence[vertex]
            else:
                sample[vertex] = sample_vertex(vertex, sample, cpts)

        # do k? times for each sample
        for _ in range(1):
            # sample each non-evidence variable conditioned on the rest (step 3)
            for vertex in vertexes :
                if vertex not in evidence:
                    cpts_vertex = []
                    for cpt in cpts:
                        for dic in cpt:
                            if vertex in dic.keys():
                                if cpt not in cpts_vertex:
                                    cpts_vertex.append(cpt)

                    result = None
                    if len(cpts_vertex) == 0:
                        continue
                    if len(cpts_vertex) == 1:
                        result = cpts_vertex[0]
                    else:
                        _k = len(cpts_vertex)
                        result = mult(cpts_vertex[0], cpts_vertex[1])
                        index = 2
                        while index < _k:
                            result = (mult(cpts_vertex[index], result))
                            index += 1 

                    # evidnece_tmp : new evidence which is the whole sample without changing vertex
                    evidence_tmp = []
                    for var in sample:
                        if var != vertex:
                            evidence_tmp.append(var)

                    probability_total = 0
                    probability_true = 0
                    for row in result:
                        flag = True
                        for var in evidence_tmp:
                            if var in row:
                                if sample[var] != row[var]:
                                    flag = False
                                    break
                        if flag:
                            probability_total += row['Prob']
                            if row[vertex] == True:
                                probability_true += row['Prob']

                    rand = np.random.random(1)
                    if rand < probability_true / probability_total:
                        sample[vertex] = True
                    else:
                        sample[vertex] = False

        samples.append(sample)  

    query_satisfied = 0
    for sample in samples:
        flag = True
        for q in query:
            if sample[q] != query[q]:
                flag = False
                break
        if flag:
            query_satisfied += 1

    return query_satisfied / num_samples