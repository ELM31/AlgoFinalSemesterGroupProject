from collections import deque
import matplotlib.pyplot as plt
import networkx as nx

# DFS using recursion
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()

    traversal_order = []
    if node not in visited:
        traversal_order.append(node)
        visited.add(node)

        for neighbor in graph.get(node, []):
            traversal_order.extend(dfs(graph, neighbor, visited))

    return traversal_order

# BFS using queue
def bfs(graph, start):
    visited = set()
    queue = deque([start])
    traversal_order = []

    while queue:
        node = queue.popleft()
        if node not in visited:
            traversal_order.append(node)
            visited.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)

    return traversal_order

# Draw the graph of documents and references
def draw_document_graph(graph, traversal_order=None, title="Document Reference Map"):
    G = nx.DiGraph()

    for doc, references in graph.items():
        for ref in references:
            G.add_edge(doc, ref)

    pos = nx.spring_layout(G, k=0.8)
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', edge_color='gray',
            node_size=2500, font_size=10, arrowsize=20)

    if traversal_order:
        edges_in_path = list(zip(traversal_order, traversal_order[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color='red', width=2)

    plt.title(title)
    plt.show()

# test documents
documents = {
    "Paper A": ["Paper B", "Paper C"],
    "Paper B": ["Paper D"],
    "Paper C": ["Paper D", "Paper E"],
    "Paper D": [],
    "Paper E": ["Paper F"],
    "Paper F": []
}

# dfs test
dfs_order = dfs(documents, "Paper A")
print("DFS Order:", dfs_order)
draw_document_graph(documents, dfs_order, "DFS Document Reference Traversal")

# bfs test
bfs_order = bfs(documents, "Paper A")
print("BFS Order:", bfs_order)
draw_document_graph(documents, bfs_order, "BFS Document Reference Traversal")
