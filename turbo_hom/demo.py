import queue
'''
@author: GaoMeng
@contact: QQ1324580227
@software: PyCharm
@time: 2020/12/23
@file: turbo_hom
'''


def get_triple(filename="yagoData.csv"):
    print("Counting classification tuples...")
    f = open(filename, "r",  encoding='utf-8')
    triple1 = []
    triple1_t = []
    triple1_sc = []
    for line in f:
        triple_cell = line.replace("\n", "").split("\t")
        if "rdf:type" in triple_cell[1]:
            triple1_t.append(triple_cell)
        elif "rdf:subClassOf" in triple_cell[1]:
            triple1_sc.append(triple_cell)
        else:
            triple1.append(triple_cell)
    f.close()
    return triple1, triple1_t, triple1_sc


def data_graph():
    triple, triple_t, triple_sc = get_triple()

    vertex_dic = {}
    for i in range(0, len(triple)):
        if triple[i][0] not in vertex_dic.keys():
            vertex_dic[triple[i][0]] = [[triple[i][1], triple[i][2]]]
        else:
            vertex_dic[triple[i][0]].append([triple[i][1], triple[i][2]])
    for i in range(0, len(triple)):
        if triple[i][2] not in vertex_dic.keys():
            vertex_dic[triple[i][2]] = []

    # 1> vertex and its object
    vertex_ = []
    for dic in vertex_dic:
        vertex_.append(dic)
    for i in range(0, len(triple_t)):
        if triple_t[i][0] not in vertex_:
            vertex_.append(triple_t[i][0])
    print("vertex storage complete...")

    # vertex = ['student1', 'univ1', 'dept1.univ1', "'012-345-6789'", "'john@dept1.univ1.edu'"]

    # get vertex Id
    print("get vertex Id...")
    vertex_id_ = []
    index = 0  # vertex ID begin from zero
    for i in range(0, len(vertex_)):
        if vertex_[i] == "_":
            vertex_id_.append("_")
            continue
        vertex_id_.append(index)
        index = index + 1

    # get the vertex label {vertex：list(label)}
    print("get the vertex label {vertex：list(label)}...")
    vl_ = {}
    vl_offset_ = []
    vl_ids_ = []
    vl_total = []
    triple_union = triple_sc + triple_t
    for i in range(0, len(vertex_)):  # breath first rdf : type  rdf:subClassOf to vertex‘s label
        label_v = []
        # q = queue.Queue()
        # q.put(vertex_[i])
        # while not q.empty():
        #     u = q.get()
        #     for j in range(0, len(triple_union)):
        #         if triple_union[j][0] == u and triple_union[j][2] not in label_v:
        #             label_v.append(triple_union[j][2])
        #             if triple_union[j][2] not in vl_total:
        #                 vl_total.append(triple_union[j][2])
        #             q.put(triple_union[j][2])
        vl_[i] = label_v
    for i in range(len(vl_total)):
        for key in range(len(vl_)):
            if vl_total[i] in vl_[key]:
                vl_ids_.append(key)
        vl_offset_.append(len(vl_ids_))

    # get the adjacent vertex IDs and end offset of label groups
    print("get the adjacent vertex IDs and end offset of label groups...")
    adjacent_offsets_ = []
    adjacent_vertex_ids_ = []
    adjacent_edge_offset_ = []
    print(len(vertex_dic))

    for dic in vertex_dic:
        for dic_cell in vertex_dic[dic]:
            adjacent_vertex_ids_.append(vertex_.index(dic_cell[1]))
            aeo = [dic_cell[0], vl_[vertex_.index(dic_cell[1])], len(adjacent_vertex_ids_)]
            adjacent_edge_offset_.append(aeo)
        adjacent_offsets_.append(len(adjacent_vertex_ids_))
    print("The storage of graph is completed!\n")
    return vertex_, vertex_id_, vl_, vl_total, vl_offset_, vl_ids_, adjacent_offsets_, adjacent_vertex_ids_, adjacent_edge_offset_


# query graph
def query_graph(filename="rdf_query"):
    triple, triple_t, triple_sc = get_triple(filename)
    q_vertex_ = []
    for i in range(0, len(triple)):
        if triple[i][0] not in q_vertex_:
            q_vertex_.append(triple[i][0])
        if triple[i][2] not in q_vertex_:
            q_vertex_.append(triple[i][2])
    for i in range(0, len(triple_t)):
        if triple_t[i][0] not in q_vertex_:
            q_vertex_.append(triple_t[i][0])
    print(q_vertex_)

    vl_ = {}
    triple_union = triple_sc + triple_t
    for i in range(0, len(q_vertex_)):  # breath first rdf : type  rdf:subClassOf to vertex‘s label
        label_v = []
        q = queue.Queue()
        q.put(q_vertex_[i])
        while not q.empty():
            u = q.get()
            for j in range(0, len(triple_union)):
                if triple_union[j][0] == u and triple_union[j][2] not in label_v:
                    label_v.append(triple_union[j][2])
                    q.put(triple_union[j][2])
        vl_[i] = label_v

    # get the adjacent vertex IDs and end offset of label groups
    adjacent_offsets_ = []
    adjacent_vertex_ids_ = []
    adjacent_edge_offset_ = []
    for i in range(0, len(q_vertex_)):
        for j in range(0, len(triple)):
            if q_vertex_[i] == triple[j][0]:
                adjacent_vertex_ids_.append(q_vertex_.index(triple[j][2]))
                aeo = [triple[j][1], vl_[q_vertex_.index(triple[j][2])], len(adjacent_vertex_ids_)]
                adjacent_edge_offset_.append(aeo)
        adjacent_offsets_.append(len(adjacent_vertex_ids_))
    return q_vertex_, vl_, adjacent_offsets_, adjacent_vertex_ids_, adjacent_edge_offset_


# u---->neighbor
def get_neighbors(u, graph_type):
    neighbors = []
    if graph_type == "data_graph":
        if u == 0:
            for i in range(0, adjacent_offsets[u]):
                neighbors.append(adjacent_vertex_ids[i])
        else:
            for i in range(adjacent_vertex_ids[u - 1], adjacent_vertex_ids[u]):
                neighbors.append(adjacent_vertex_ids[i])
    elif graph_type == "query_graph":
        if u == 0:
            for i in range(0, q_adjacent_offsets[u]):
                neighbors.append(q_adjacent_vertex_ids[i])
        else:
            for i in range(q_adjacent_vertex_ids[u - 1], q_adjacent_vertex_ids[u]):
                neighbors.append(q_adjacent_vertex_ids[i])
    return neighbors


# get label of the edge of the two vertex
def get_e_v_label(a, b, type):
    if type == "data_graph":
        if a == 0:
            for i in range(0, adjacent_offsets[a]):
                if adjacent_vertex_ids[i] == b:
                    return adjacent_edge_offset[i][0],adjacent_edge_offset[i][1]
        else:
            for i in range(adjacent_offsets[a-1], adjacent_offsets[a]):
                if adjacent_vertex_ids[i] == b:
                    return adjacent_edge_offset[i][0],adjacent_edge_offset[i][1]

    elif type == "query_graph":
        if a == 0:
            for i in range(0, q_adjacent_offsets[a]):
                if q_adjacent_vertex_ids[i] == b:
                    return q_adjacent_edge_offset[i][0],adjacent_edge_offset[i][1]
        else:
            for i in range(q_adjacent_offsets[a-1], q_adjacent_offsets[a]):
                if q_adjacent_vertex_ids[i] == b:
                    return q_adjacent_edge_offset[i][0],adjacent_edge_offset[i][1]


# BFS--->DFS
def transform_df(vs, bf):
    df = []
    visited = []
    stack = [vs]
    visited.append(vs)

    while len(stack):
        q = stack[-1]
        flag = 0
        for i in range(len(bf)):
            if bf[i][0] == q and bf[i][1] not in visited:
                visited.append(bf[i][1])
                stack.append(bf[i][1])
                df.append([q, bf[i][1]])
                flag = 1
                break
        if flag == 0:
            stack.pop()
    return df


# pick the starting query vertex which has the least number of candidate regions.
# rank(u) = freq(g,L(u))/deg(u)
def ChooseStartQueryVertex():
    rank = []
    for i in range(0, len(q_vertex)):  # for v in query graph s
        if q_vertex[i][0] != "?":  # when a
            # data vertex ID v is specified in u
            if q_vertex[i] in vertex:  # if id-object in vertex
                vgl = list(range(len(vertex)))
                for l in q_vl[i]:  # for each label of query graph:
                    vgl_cell = []
                    vl_total.index(l)
                    for i in range(vl_offset[vl_total.index(l) - 1],
                                   vl_offset[vl_total.index(l)]):  # retrieve all data vertices which have u’s labels
                        vgl_cell.append(vl_ids[i])
                    vgl = list(set(vgl).intersection(vgl_cell))  # freq(g, L(u)) is obtained by intersecting all V(g)l
                if vertex.index(q_vertex[i]) in vgl:
                    rank.append(1)  # freq(g, L(u)) = 1 if v ∈ V(g)l for each l ∈ L(u)
                else:  # Otherwise, freq(g, L(u)) = 0
                    rank.append(0)

            else:  # id-object is not in vertex (have no result)
                return
        else:  # when a data vertex ID v is  NOT specified in u
            vgl = list(range(len(vertex)))
            for l in q_vl[i]:  # for each label of query graph:
                vgl_cell = []
                vl_total.index(l)
                for i in range(vl_offset[vl_total.index(l) - 1],
                               vl_offset[vl_total.index(l)]):  # retrieve all data vertices which have u’s labels
                    vgl_cell.append(vl_ids[i])
                vgl = list(set(vgl).intersection(vgl_cell))  # freq(g, L(u)) is obtained by intersecting all V(g)l
            rank.append(len(vgl))

    # calculate degree
    for i in range(0, len(q_vertex)):
        degree = 0
        if i == 0:
            for j in range(0, len(q_adjacent_vertex_ids)):
                if q_adjacent_vertex_ids[j] == i:
                    degree = degree + 1
            degree = degree + q_adjacent_offsets[i]
        else:
            for j in range(0, len(q_adjacent_vertex_ids)):
                if q_adjacent_vertex_ids[j] == i:
                    degree = degree + 1
            degree = degree + q_adjacent_offsets[i] - q_adjacent_offsets[i - 1]
        rank[i] = rank[i] / degree
    return rank.index(max(rank))


#  a breath-first tree traversal is conducted also non-edge tree is recorded
def WriteQueryTree(start_vertex):
    query_tree_ = []
    non_tree_edge_ = []
    visited = []
    q = queue.Queue()
    q.put(start_vertex)
    visited.append(start_vertex)
    while not q.empty():
        u = q.get()
        neighbors = get_neighbors(u, "query_graph")
        for i in range(0, len(neighbors)):
            if neighbors[i] not in visited:
                visited.append(neighbors[i])
                query_tree_cell = [u, neighbors[i]]
                query_tree_.append(query_tree_cell)

    for i in range(0, len(q_vertex)):
        neighbors = get_neighbors(i, "query_graph")
        for j in range(0, len(neighbors)):
            cell = [i, neighbors[j]]
            if cell not in query_tree_:
                non_tree_edge_.append(cell)
    return query_tree_, non_tree_edge_


# A candidate region is obtained by exploring the data graph from the starting query vertex in a depth-first manner
def ExploreCandidateRegin(a, b, bf):
    CR_ = []
    map = {a: [b]}
    df = transform_df(a, bf)
    for i in range(0, len(df)):
        qe, qel = get_e_v_label(df[i][0], df[i][1], "query_graph")
        map_list = []
        CR_cell = {}

        if i == 0:
            b_neighbors = get_neighbors(b, "data_graph")
            if q_vertex[df[i][1]][0] != "?":  # if the id-object of the query vertex is specific
                flag = 0
                for j in range(0, len(b_neighbors)):
                    e, el = get_e_v_label(b, b_neighbors[j], "data_graph")
                    if vertex[b_neighbors[i]] == q_vertex[df[i][1]] and e == qe:
                        flag = 1
                        CR_.append({b: [b_neighbors[j]]})
                        map_list = [b_neighbors[j]]
                        break
                if flag == 0:       # data graph has no this id-object
                    return []       # return nothing

            else:                 # if df[i][1] is a variable
                cell = []
                for j in range(0, len(b_neighbors)):
                    e, el = get_e_v_label(b, b_neighbors[j], "data_graph")
                    if e == qe and set(qel) <= set(el):          # The edge is  equal and the label is a subset
                        cell.append(b_neighbors[j])
                if len(cell) == 0:
                    return []
                CR_.append({b: cell})
                map_list = cell

        else:
            v = map[df[i][0]]
            for m in range(0, len(v)):
                v_neighbors = get_neighbors(v[m], "data_graph")
                v_list = []
                if q_vertex[df[i][1]][0] != "?":  # if the id-object of the query vertex is specific
                    for j in range(0, len(v_neighbors)):
                        e, el = get_e_v_label(v[m], v_neighbors[j], "data_graph")
                        if vertex[v_neighbors[j]] == q_vertex[df[i][1]] and e == qe:
                            map_list.append(v_neighbors[j])
                            CR_cell[v[m]] = [v_neighbors[j]]
                            break

                else:                 # if df[i][1] is a variable
                    cell = []
                    for j in range(0, len(v_neighbors)):
                        e, el = get_e_v_label(v[m], v_neighbors[j], "data_graph")
                        if e == qe and set(qel) <= set(el):          # The edge is  equal and the label is a subset
                            map_list.append(v_neighbors[j])
                            cell.append(v_neighbors[j])
                    if len(cell) != 0:
                        CR_cell[v[m]] = cell
            CR_.append(CR_cell)
        map[df[i][1]] = map_list
    return CR_, map


def DetermineMatchingOrder(start_vertex, CR_M_):
    order_dic = {}
    order_ = [start_vertex]
    for dic in CR_M_:
        if dic != start_vertex:
            order_dic[dic] = len(CR_M_[dic])
    order_ = order_ + sorted(order_dic, key=order_dic.__getitem__)
    return order_


# subgraph matching
def turbo():
    M = {}
    vgl = list(range(len(vertex)))
    if len(q_vertex) == 1 and len(q_adjacent_edge_offset) == 0:  # V(q) = {u} and E = φ
        for l in q_vl[0]:
            vgl_cell = []
            vl_total.index(l)
            for i in range(vl_offset[vl_total.index(l) - 1],
                           vl_offset[vl_total.index(l)]):            # retrieve all data vertices which have u’s labels
                vgl_cell.append(vl_ids[i])
            vgl = list(set(vgl).intersection(vgl_cell))
        M[0] = vgl
        return M
    else:
        us = ChooseStartQueryVertex()
        query_tree, non_tree_edge = WriteQueryTree(us)

        for l in q_vl[us]:
            vgl_cell = []
            vl_total.index(l)
            if vl_total.index(l) == 0:
                for i in range(vl_offset[0]):
                    vgl_cell.append(vl_ids[i])

            else:
                for i in range(vl_offset[vl_total.index(l) - 1],
                               vl_offset[vl_total.index(l)]):  # retrieve all data vertices which have u’s labels
                    vgl_cell.append(vl_ids[i])
            vgl = list(set(vgl).intersection(vgl_cell))

        for vs in vgl:  # For each data vertex that contains the label of the vertex that started the query
            CR, CR_M = ExploreCandidateRegin(us, vs, query_tree)
            if len(CR):
                order = DetermineMatchingOrder(us, CR_M)
                # for i in range(1, len(order)):
                print(CR)
                print(CR_M)
                print(query_tree)
                print(order)


vertex, vertex_id, vl, vl_total, vl_offset, vl_ids, adjacent_offsets, adjacent_vertex_ids, adjacent_edge_offset = data_graph()
q_vertex, q_vl, q_adjacent_offsets, q_adjacent_vertex_ids, q_adjacent_edge_offset = query_graph()
turbo()
