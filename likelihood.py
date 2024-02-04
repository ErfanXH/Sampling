from utils import topological_sort
from utils import sample_vertex
from utils import find_row
import globals

def likelihood_sample(query, evidence, cpts, graph, n):
    global num_samples
    vertexes = topological_sort(graph)
    samples = []
    weights_all = []
    weights_query = []
    for _ in range(globals.num_samples):
        weight = 1.0
        sample = {}
        for vertex in vertexes:
            sample[vertex] = -1
        for vertex in vertexes:
            if vertex in evidence:
                sample[vertex] = evidence[vertex]
                weight *= find_row(cpts[vertex], sample)
                    
            else:
                sample[vertex] = sample_vertex(vertex, sample, cpts)

        flag_query = True
        for vertex in sample:
            if vertex in query:
                if sample[vertex] != query[vertex]:
                    flag_query = False

        if flag_query:
            weights_query.append(weight)

        weights_all.append(weight)
        samples.append(sample)

    if sum(weights_all) == 0:   # division by zero
        return 0
    
    return sum(weights_query) / sum(weights_all)