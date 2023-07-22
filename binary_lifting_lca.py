from collections import defaultdict
class TreeNode:
    def __init__(self, x):
        val = x
        left = None
        right = None


LOG = 8
MAX_N = 10e5
depth = defaultdict(int) # [0 for _ in range(MAX_N+1)]
up = defaultdict(dict) # [[0 for _ in range(LOG)] for _ in range(MAX_N)]]

def dfs(node, parent):
    if not node:
        return

    depth[node] = depth[parent] + 1

    up[node][0] = parent
    for j in range(1, LOG):
        # up[node][j] is the 2^jth ancestor of node
        up[node][j] = up[ up[node][j-1] ][j-1]

    if node.left:
        dfs(node.left, node)

    if node.right:
        dfs(node.right, node)

def LCA(p, q):
    if depth[p] < depth[q]:
        p, q = q, p

    k = depth[p] - depth[q]

    # make q reach the same depth as p by reaching the kth ancestor of q
    for j in range(LOG-1, -1, -1):
        if k & (1 << j):
            p = up[p][j]

    if p == q:
        return p

    # jump both p and q in powers of two so they get as close to the LCA as they can
    for j in range(LOG-1, -1, -1):
        if up[p][j] != up[q][j]:
            p = up[p][j]
            q = up[q][j]

    # LCA is the parent of the node
    return up[p][0]


# this preprocessing is only useful if you have a tree and you have to make multiple queries on it
def preprocess(root):
    # fill the up array which stores 2^jth (j in [0, LOG-1]) ancestor of every node 
    dfs(root, root) # set parent as root itself to avoid indexing problems
