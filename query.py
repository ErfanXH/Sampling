import json

def read_queries(path):
    # read from file
    text = ""
    with open(path, 'r') as file:
        text = file.read()

    data = json.loads(text)

    queries = []
    evidences = []

    global map_vertex

    for query_evidence in data:
        query = query_evidence[0]
        evidence = query_evidence[1]

        query_new = {}
        evidence_new = {}

        for k, v in query.items():
            if v == 1:
                query_new[map_vertex[k]] = True
            else:
                query_new[map_vertex[k]] = False
        
        for k, v in evidence.items():
            if v == 1:
                evidence_new[map_vertex[k]] = True
            else:
                evidence_new[map_vertex[k]] = False

        queries.append(query_new)
        evidences.append(evidence_new)
    
    return queries, evidences