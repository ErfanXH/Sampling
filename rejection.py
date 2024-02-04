from utils import topological_sort
from utils import sample_vertex
import globals

def rejection_sample(query, evidence, cpts, graph, n):
    global num_samples
    vertexes = topological_sort(graph)
    samples = []
    consistent_with_evidence = 0
    for _ in range(globals.num_samples):
        sample = {}
        reject = False
        for vertex in vertexes:
            sample[vertex] = -1
        for vertex in vertexes:
            sample[vertex] = sample_vertex(vertex, sample, cpts)
            if vertex in evidence:
                if sample[vertex] != evidence[vertex]:
                    reject = True
                    break

        if reject:
            continue

        consistent_with_evidence += 1
        samples.append(sample)
    
    query_evidence_true = 0

    for sample in samples:
        flag_query = True
        for q_key in query:
            if sample[q_key] == query[q_key]:
                continue
            else:
                flag_query = False
                break
        if flag_query:
            query_evidence_true += 1

    if consistent_with_evidence == 0:   # division by zero
        return 0

    return query_evidence_true / consistent_with_evidence