from utils import topological_sort
from utils import sample_vertex
import globals

def prior_sample(query, evidence, cpts, graph, n):
    global num_samples
    vertexes = topological_sort(graph)
    samples = []
    for _ in range(globals.num_samples):
        sample = {}
        for vertex in vertexes:
            sample[vertex] = -1
        for vertex in vertexes:
            sample[vertex] = sample_vertex(vertex, sample, cpts)
        samples.append(sample)
    
    consistent_with_evidence = 0
    query_evidence_true = 0

    for sample in samples:
        flag_consistent_evidence = True
        for ev_key in evidence:
            if sample[ev_key] == evidence[ev_key]:
                continue
            else:
                flag_consistent_evidence = False
                break
        if flag_consistent_evidence:
            consistent_with_evidence += 1
            falg_query = True
            for q_key in query:
                if sample[q_key] == query[q_key]:
                    continue
                else:
                    falg_query = False
                    break
            if falg_query:
                query_evidence_true += 1

    if consistent_with_evidence == 0:   # division by zero
        return 0
    
    return query_evidence_true / consistent_with_evidence