
import numpy as np
import copy


class UM:
    """ Utility-based preferential attachment model
    Args:
        m (int): Number of edges added at each step
        coef_k1 (int): Utility coefficient for direct connection
        coef_k2 (int): Utility coefficient for indirect connection
                       (>0, otherwise the pool will almost disappear)
        seed (int): Number of seed nodes (ring network)
        N (int): Number of nodes added to the network
    """
    def __init__(self, m=1, coef_k1=1, coef_k2=0, seed=5):
        # Initialize & set
        self.m = m
        self.t = 0
        self.coef_k1 = int(coef_k1)
        self.coef_k2 = int(coef_k2)

        # Make seed network : ring
        self.nodes = list(range(seed))
        self.N = len(self.nodes)
        self.adjlist_k1 = [[node-1, node+1] for node in range(seed)]
        self.adjlist_k1[0] = [1, seed-1]
        self.adjlist_k1[seed-1] = [0, seed-2]
        self.adjlist_k2 = []
        for node in self.nodes:
            k2_pool = set()
            for node_adj in self.adjlist_k1[node]:
                k2_pool.update(self.adjlist_k1[node_adj])
            k2_pool = k2_pool - set(self.adjlist_k1[node]) - {node}
            self.adjlist_k2 += [list(k2_pool)]

        # Make preference pool for utility model
        k1 = [len(adj) for adj in self.adjlist_k1]
        k2 = [len(adj) for adj in self.adjlist_k2]
        u = [int(self.coef_k1 * k1[i] + self.coef_k2 * k2[i]) for i in self.nodes]
        self.pool = []
        for node in self.nodes:
            self.pool += u[node] * [node]
        self.T = len(self.pool)
        if self.T == 0:
            self.T = len(self.nodes)
            self.pool = self.nodes.copy()
        self.U = [copy.deepcopy(self.T)]

        # Summation of k1, k2 info
        self.T1 = sum(k1)
        self.T2 = sum(k2)
        self.K1_sum = [copy.deepcopy(self.T1)]
        self.K2_sum = [copy.deepcopy(self.T2)]

        # Initial state info
        self.init_node = self.nodes.copy()
        self.init_k2 = [2] * seed

    def add_nodes(self, N):
        for i in range(N):
            # Select node
            self.nodes.append(self.N)
            targets = self.pool
            counter = 0
            new_targets_k1 = []
            while counter < self.m:
                r = np.random.randint(self.T)
                if targets[r] not in new_targets_k1:
                    counter += 1
                    new_targets_k1.append(targets[r])

            # 2 distance from selected node
            new_targets_k2 = []
            for j in new_targets_k1:
                for k in self.adjlist_k1[j]:
                    if k not in new_targets_k1:
                        if k not in new_targets_k2:
                            new_targets_k2 += [k]
            if self.m != 1:
                for j in range(self.m - 1):
                    for k in range(j+1, self.m):
                        if new_targets_k1[j] not in self.adjlist_k2[new_targets_k1[k]]:
                            """ 거리가 1 이상이면 pool에 서로를 추가할 필요가 있음 """
                            self.pool += self.coef_k2 * [new_targets_k1[j], new_targets_k1[k]]
                            self.T += self.coef_k2 * 2
                            self.T2 += 2
                            """ m개의 selected node 끼리 서로를 k2 이웃에 추가 """
                            self.adjlist_k2[new_targets_k1[j]] += [new_targets_k1[k]]
                            self.adjlist_k2[new_targets_k1[k]] += [new_targets_k1[j]]

            # Update pool
            if self.coef_k1 >= 0:
                for node in new_targets_k1:
                    self.pool += self.coef_k1 * [node]
                for node in new_targets_k2:
                    self.pool += self.coef_k2 * [node]
                self.pool += self.coef_k1 * self.m * [self.N]
                self.pool += self.coef_k2 * len(new_targets_k2) * [self.N]
            else:
                # If coef_k1 < 0, delete the node from pool according to the new link
                for node in new_targets_k1:
                    for _ in range(-self.coef_k1):
                        try:
                            self.pool.remove(node)
                        except:
                            pass
                for node in new_targets_k2:
                    self.pool += self.coef_k2 * [node]
                v = int(self.coef_k2 * len(new_targets_k2) + self.coef_k1 * self.m)
                # Update pool when only utility is positive
                if v > 0:
                    self.pool += v * [self.N]

            # Calculate pool size & k1/k2 summation
            self.T += 2 * self.coef_k1 * self.m + 2 * self.coef_k2 * len(new_targets_k2)
            self.T1 += 2 * self.m
            self.T2 += 2 * len(new_targets_k2)

            # If there is no node in pool or coefficient is zero, make pool random
            if self.T <= 0:
                self.T = len(self.nodes)
                self.pool = self.nodes.copy()
            if (self.coef_k1 == 0) and (self.coef_k2 == 0):
                self.T = len(self.nodes)
                self.pool = self.nodes.copy()

            # Update adjlist list
            for j in new_targets_k1:
                self.adjlist_k1[j] += [self.N]
            for j in new_targets_k2:
                self.adjlist_k2[j] += [self.N]
            self.adjlist_k1 += [new_targets_k1]
            self.adjlist_k2 += [new_targets_k2]

            # Update parameters & state info
            self.N += 1
            self.t += 1
            self.U += [copy.deepcopy(self.T)]
            self.K1_sum += [copy.deepcopy(self.T1)]
            self.K2_sum += [copy.deepcopy(self.T2)]
            self.init_k2 += [len(new_targets_k2)]

