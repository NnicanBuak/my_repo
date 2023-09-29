def find_parent(parent, i):
    if parent[i] == i:
        return i
    return find_parent(parent, parent[i])

def union(parent, rank, x, y):
    xroot = find_parent(parent, x)
    yroot = find_parent(parent, y)

    if rank[xroot] < rank[yroot]:
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot
    else :
        parent[yroot] = xroot
        rank[xroot] += 1

def solve(edges, N):
    parent = [i for i in range(N+1)]
    rank = [0 for _ in range(N+1)]

    for edge in edges:
        union(parent, rank, edge[0], edge[1])

    unique_parents = set([find_parent(parent, i) for i in range(1, N+1)])
    return len(unique_parents) - 1

edges = []
with open("./data/data1.txt", 'r') as file:
    N = int(next(file).strip())
    for line in file:
        edge = tuple(map(int, line.strip().split()))
        edges.append(edge)
print(solve(edges, N))
