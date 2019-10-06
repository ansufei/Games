#!/usr/bin/env python
# coding: utf-8

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

#T1.0 Alternative
def make_graph(lst):
    graph_keys = list(set([x for sublist in lst for x in sublist]))
    graph_dict = {}
    for key in graph_keys:
        graph_dict[key] = list(set([value for sublist in lst for value in sublist if value != key if key in sublist]))
    return graph_dict

#T1.1 find if two vertices are connected (recursion runs a dfs)
def connected(graph, start, end, eliminate):
    if end == start:
        return True
    eliminate.append(start)
    for start in graph[start]:
        if not start in eliminate:
            if connected(graph, start, end, eliminate):
                return True
    return False

#T1.2 Find the connection path (first path found) using recursion
def recursion_dfs_path(graph, start, end, visited, path):
    if start == end:
        return 'start = end'
    visited.append(start)
    for child in graph[start]:
        if not child in visited:
            if recursion_dfs_path(graph, child, end, visited, path):
                path.insert(0, child)
                return path
    return path

#find_path to build the path dictionary from end to start after the route is found
def find_path(parent, end):
    node = end
    path = []
    while node in parent.keys():
        if not end in path:
            path.append(end)
        path.append(parent[node])
        node = parent[node]    
    return list(reversed(path))

#T1.2 Alternative Find the connection path (first path found) using a while loop
def while_dfs_path(graph, start, end):
    stack = [start]
    visited = [start]
    parent = {}
    while stack:
        current = stack.pop()
        if current == end:
            break
        for child in graph[current]:
            if child not in visited:
                stack.append(child)
                visited.append(child)
                parent[child] = current
    return find_path(parent, end)

#T1.3 Find the connection path (fastest path)
def while_bfs_path(graph, start, end):
    queue = [start]
    visited = [start]
    parent = {}
    while queue:
        current = queue.pop(0) 
        if current == end:
            break
        for child in graph[current]:
            if child not in visited:
                queue.append(child)
                visited.append(child)
                parent[child] = current
    return find_path(parent, end)

#1.4 Add weights (create priority queue)
#format for weighted: weight as last item in the list
def weighted_graph(graph_as_list): 
    graph_copy = graph_as_list.copy()
    for sublist in graph_as_list:
        new_sub_list = [sublist[i] for i in [1,0,2]]
        graph_copy.append(new_sub_list)
    
    graph_keys = list(set([x[0] for x in graph_copy]))
    
    graph = {}
    for key in graph_keys:
        graph[key] = sorted([(x[1],x[2]) for x in graph_copy if x[0] == key], key=lambda tup: tup[1])
        
    return graph

#Create priority queue (class). Alternative: use the heapq library
class Pqueue():
    """stores nodes with their weights
    updates the weights as the path function goes down the path
    retrieves nodes in the order of their weights"""
    def __init__(self, lst):
        self.pqueue = lst
        
    def pop(self):
        minimum = self.pqueue.index(min(self.pqueue, key = lambda t: t[1]))
        return self.pqueue.pop(minimum)
    
    def append(self, node, weight):
        self.pqueue.append((node, weight))
        
    def query(self, node):
        query = [y for x, y in self.pqueue if x == node]
        return query
        
    def __len__(self):
        return len(self.pqueue)

#adjust bfs for weighted graph
def uniform_cost_search(graph, start, end):
    queue = Pqueue([(start,0)])
    visited = [start]
    parent = {}
    while queue:
        current, pcost = queue.pop()
        if current == end:
            break
        for child, weight in graph[current]:
            path_cost = weight + pcost
            if child in visited and queue.query(child) and queue.query(child)[0] > path_cost:
                queue.append(child, path_cost)
                parent[child] = current
            if child not in visited:
                queue.append(child, path_cost)
                visited.append(child)
                parent[child] = current
    return find_path(parent, end)

#T1.5 A-Star (bfs using graph weighted with heuristic function)
def a_star_search(start):
    queue = Pqueue([(start,0)])
    visited = [start]
    parent = {}
    counter = 0
    while queue:
        current, pcost = queue.pop()
        if current.is_terminal():
            break
        for child, action in current.children():
            path_cost = child.distance() + pcost
            if child in visited and queue.query(child) and queue.query(child)[0] > path_cost:
                queue.append(child, path_cost)
                parent[child.data] = current.data
            elif child not in visited and child.data != start.data:
                queue.append(child, path_cost)
                visited.append(child)
                parent[child.data] = current.data
    return find_path(parent, current.data)




