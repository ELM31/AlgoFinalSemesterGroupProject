from collections import deque

# Define the DFS function using recursion
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()

    traversal_order = []
    if node not in visited:
        traversal_order.append(node)
        visited.add(node)

        for neighbor in graph.get(node, []):
            traversal_order.extend(dfs(graph, neighbor, visited))  # Recursive DFS call for the neighbor

    return traversal_order

# Define the BFS function
def bfs(graph, start):
    visited = set()  # Set to track visited nodes
    queue = deque([start])  # Queue for BFS starting from the given node
    traversal_order = []

    while queue:
        node = queue.popleft()  # Dequeue a node
        if node not in visited:
            traversal_order.append(node)  # Add visited node to traversal order
            visited.add(node)  # Mark as visited
            for neighbor in graph.get(node, []):  # Traverse neighbors
                if neighbor not in visited:
                    queue.append(neighbor)

    return traversal_order

if __name__ == "__main__":
    graph = {}

    print("Enter number of citation relationships:")
    edges = int(input())

    print("Enter each citation relationship (Document1 Document2):")
    print("(This means Document1 cites Document2)")
    for _ in range(edges):
        doc1, doc2 = input().split()

        if doc1 not in graph:
            graph[doc1] = []
        graph[doc1].append(doc2)

        # Uncomment the following lines if citations are bidirectional
        # if doc2 not in graph:
        #     graph[doc2] = []
        # graph[doc2].append(doc1)

    print("Enter the starting document for DFS Traversal:")
    start_doc_dfs = input()
    print("\nDFS Traversal Order:")
    print(" -> ".join(dfs(graph, start_doc_dfs)))

    print("\nEnter the starting document for BFS Traversal:")
    start_doc_bfs = input()
    print("\nBFS Traversal Order:")
    print(" -> ".join(bfs(graph, start_doc_bfs)))
