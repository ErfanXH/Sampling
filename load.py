import globals

def load_model(path):
    V = 0
    
    # read from file
    lines = []
    with open(path, 'r') as file:
        for line in file:
            lines.append(line.strip())

    # map name to number for each vertex
    map_name_number = {}
    counter = 0
    for i, line in enumerate(lines):
        if i == 0:
            V = int(line)
            continue
        words = line.split()
        if len(words) == 1 and words[0].isalpha() and (not (words[0] in map_name_number)):
            map_name_number[words[0]] = counter
            counter += 1
        else:
            continue

    #global map_vertex
    globals.map_vertex = map_name_number

    Graph = {
        'parents_nodes': [[] for _ in range(V)],
        'children_nodes': [[] for _ in range(V)]
    }

    # store data to Cpts list and Graph
    Cpts = []
    Cpt = []
    node = {}
    current = ""
    parents = []
    for i, line in enumerate(lines):
        if i == 0:
            continue
        words = line.split()
        if len(words) == 1 and (not (words[0].isalpha() and len(lines[i - 1].split()) == 1 and lines[i - 1].split()[0].isalpha())): # new Vertex without Parents
            if words[0].isalpha(): # new Vertex
                current = words[0]
                # end of previous ->
                Cpts.append(Cpt)
                Cpt = []
                parents = []
            else:   # probability of current Vertex
                _cpt = []
                probability = float(words[0])
                node = {map_name_number[current]: True, 'Prob': probability}
                _cpt.append(node)
                node = {map_name_number[current]: False, 'Prob': 1 - probability}
                _cpt.append(node)
                Cpts.append(_cpt)

        else: # new Vertex with parents
            if all(word.isalpha() for word in words): # new Vertex's Parents
                for word in words:
                    parents.append(word)
            else:   # probability of current Vertex with parents
                parents_status = []
                for j in range(len(parents)):
                    if words[j] == '1':
                        parents_status.append((parents[j], True))
                    elif words[j] == '0':
                        parents_status.append((parents[j], False))

                node = {map_name_number[current]: True}
                for k, parent_s in enumerate(parents_status):
                    p, s = parent_s
                    node[map_name_number[p]] = s
                    # graph
                    Graph['children_nodes'][map_name_number[p]].append(map_name_number[current])
                    Graph['children_nodes'][map_name_number[p]] = list(set(Graph['children_nodes'][map_name_number[p]]))
                    Graph['parents_nodes'][map_name_number[current]].append(map_name_number[p])
                    Graph['parents_nodes'][map_name_number[current]] = list(set(Graph['parents_nodes'][map_name_number[current]]))

                node['Prob'] = float(words[-1])
                Cpt.append(node)
                
                node = {map_name_number[current]: False}
                for k, parent_s in enumerate(parents_status):
                    p, s = parent_s
                    node[map_name_number[p]] = s

                node['Prob'] = 1 - float(words[-1])
                Cpt.append(node)

    if Cpt != []:
        Cpts.append(Cpt)
        Cpt = []

    for cpt in Cpts:
        if cpt == []:
            Cpts.remove(cpt)

    return Cpts, Graph, V
