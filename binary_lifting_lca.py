from collections import defaultdict

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    LOG = 8
    MAX_N = 10e5
    depth = defaultdict(int)
    up = defaultdict(dict)

    def dfs(self, node, parent):
        if not node:
            return

        self.depth[node] = self.depth[parent] + 1

        self.up[node][0] = parent
        for j in range(1, self.LOG):
            # self.up[node][j] is the 2^jth ancestor of node
            self.up[node][j] = self.up[ self.up[node][j-1] ][j-1]

        if node.left:
            self.dfs(node.left, node)

        if node.right:
            self.dfs(node.right, node)

    def LCA(self, p, q):
        if self.depth[p] < self.depth[q]:
            p, q = q, p

        k = self.depth[p] - self.depth[q]

        # make q reach the same depth as p by reaching the kth ancestor of q
        for j in range(self.LOG-1, -1, -1):
            if k & (1 << j):
                p = self.up[p][j]

        if p == q:
            return p

        # jump both p and q in powers of two so they get as close to the LCA as they can
        for j in range(self.LOG-1, -1, -1):
            if self.up[p][j] != self.up[q][j]:
                p = self.up[p][j]
                q = self.up[q][j]

        # LCA is the parent of the node
        return self.up[p][0]

    
    # this preprocessing is only useful if you have a tree and you have to make multiple queries on it
    def preprocess(self, root):
        # fill the self.up array which stores 2^jth (j in [0, LOG-1]) ancestor of every node 
        self.dfs(root, root) # set parent as root itself to avoid indexing problems


    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        self.preprocess(root)
        return self.LCA(p, q)