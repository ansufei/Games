#!/usr/bin/env python
# coding: utf-8

lst = [[1,2],[2,6],[2,7],[2,3],[3,4],[3,5],[4,5],[8,9],[5,10]]

#T1.0 Create the graph dictionary
def graph(lst):
    graph_dict = {}
    for sublist in lst:
        if not sublist[0] in graph_dict.keys():
            graph_dict[sublist[0]] = [sublist[1]]
        else:
            graph_dict[sublist[0]].append(sublist[1])
        if not sublist[1] in graph_dict.keys():
            graph_dict[sublist[1]] = [sublist[0]]
        else:
            graph_dict[sublist[1]].append(sublist[0])    
    return graph_dict
 print(graph(lst))

#T1.0 Alternative
def graph(lst):
    graph_keys = list(set([x for sublist in lst for x in sublist]))
    graph_dict = {}
    for key in graph_keys:
        graph_dict[key] = list(set([value for sublist in lst for value in sublist if value != key if key in sublist]))
    return graph_dict
print(graph(lst))

#T1.1 find if two vertices are connected
def connected(graph_dict, start, end, eliminate):
    if end == start or end in graph_dict[start]:
        return True
    eliminate.append(start)
    for x in graph_dict[start]:
        if not x in eliminate:
            if connected(graph_dict, x, end, eliminate):
                return True
    return False
print(connected(graph(lst), 1, 7, eliminate=[]))


#T1.2 Find the connection path (first path found)
def find_path(graph_dict, start, end, eliminate, path):
    if end == start or end in graph_dict[start]:
        return [start, end]
    eliminate.append(start)
    for x in graph_dict[start]:
        if not x in eliminate:
            if find_path(graph_dict, x, end, eliminate, path):
                path.insert(0,x)
                return path
    return False
start=1
end = 10
print(find_path(graph(lst), start, end, eliminate=[], path = [end]))





