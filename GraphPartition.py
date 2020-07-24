import numpy as np
from utils.datastructures.graph.SimpleGraph import SimpleGraph
from utils.datastructures.graph.Vertex import Vertex
from collections.abc import Iterable
from typing import Set, List, Dict, Tuple
class GraphPartition:

    def __init__(self):
        pass

    def get_starting_point(self, G : SimpleGraph, k) -> 'Partition':
        """
        Should return a starting point for the MCMC
        simulation. i.e. you should return some partition
        of the vertices into k classes
        :param G:
        :param k:
        :return:
        """
        pass


    def get_edge_crossing_weights(self, G : SimpleGraph, partition : 'Partition'):
        """
        Get the sum of the edge weights crossing between all pairs of
        vertices in distinct partitions.

        :param G:
        :param partition:
        :return: the sum of the weights of edges crossing between distinct partitions
        """
        #TODO
        pass

    def get_internal_weights(self, G :SimpleGraph, partition : 'Partition'):
        """
        get the weight of the edges contained entirely in the same
        bucket of the partition, for each bucket in the partition
        :param G:
        :param partition:
        :return: an array of length k, where A[i] is the sum of the
        edge weights between vertices in bucket i of the partition
        """
        #TODO
        pass



    def eval_partition(self, G : SimpleGraph, partition : 'Partition'):
        """
        this function will evaluate a partition of n vertices with k buckets
        based on the weight of edges crossing between the buckets, and the
        similarity of bucket sizes.

        :param G:
        :param partition:
        :return:
        """
        crossing_weight = self.get_edge_crossing_weight(G, partition)
        internal_weights = self.get_internal_weights(G, partition)
        k = len(partition)
        scale = partition.n/k
        return crossing_weight - np.prod(internal_weights)/(scale**k)




    def apply_move(self, partition : 'Partition', elts, buckets):
        """
        apply the move - rearrange the partition so that the two elements
        are now mapped to the corresponding buckets in the partition

        :param partition:
        :param elts:
        :param buckets:
        :return:
        """

    def eval_move(self, G : SimpleGraph, partition : 'Partition', elts, buckets):
        """
        should return the change in the objective function after moving each element
        in elts to the corresponding bucket in buckets.
        i.e. the difference in eval_partition(curr) and eval_partition(new)
        where new is the partition after applying the move.

        :param elts:
        :param buckets:
        :return:
        """
        #Fast implementation :

        #the contribution from moving an element to a different bucket
        #can be calculated by
        # (1) finding the weight of the edges from this element to the vertices
        # in it's current bucket
        # (2) Finding the weight of the edges from this element to vertices in the new bucket
        # (3) subtracting (1) from (3)

        #With these contributions accounted for, you may still have to adjust for
        #the initial/ final placement of the two elements.

        #Slow Implementation :
        #alternatively (this is fine, but will be slower), you can simply make the
        #the change, and compare the function before and after making this change.
        #be sure to change the partition back to the original state before exiting
        #though.

        #TODO
        delta_E = 0
        return delta_E

    def propose_move(self, G, partition):
        """
        propose a move - choose two vertices in G and
        assign them to buckets (possibly the same bucket they are already in)
        You can choose to do this however you'd like, but there should be a
        randomized component
        This can be as simple as choosing two vertices at random and two buckets at random
        and proposing this as a move.
        :param G:
        :param partition:
        :param k:
        :return: a list containing the chosen vertices, and a list
        """
        chosen_verts, chosen_buckets = [None]*2, [None]*2
        #TODO

        return chosen_verts, chosen_buckets

    def transitionQ(self, energy_change, K=10):
        r = np.random.uniform(0,1)
        return np.exp(energy_change/K)>r


    def MCMC(self, G : SimpleGraph, k, n_rounds = 1000, K=10):
        #get a starting point
        start = self.get_starting_point(G,k)
        f0 = self.eval_partition(G, start)
        finish = self._MCMC(G, k , start, n_rounds=n_rounds, K=K)
        f1 = self.eval_partition(G,finish)
        return finish, f0-f1

    def _MCMC(self, G : SimpleGraph, partition : 'Partition',
              n_rounds = 1000, K=10, iter = 0) -> 'Partition':
        """
        If you want, you can make this a simulated annealing algorithm by
        reducing the value of k proportional to the number of remaining iterations.
        :param G:
        :param partition:
        :param n_rounds:
        :param K:
        :param iter:
        :return:
        """

        if iter>n_rounds:
            return partition

        proposed_verts, proposed_buckets = self.propose_move(G, partition)
        delta_E = self.eval_move(G, partition, proposed_verts, proposed_buckets)
        if self.transitionQ(delta_E, K=K):
            self.apply_move(partition, proposed_verts, proposed_buckets)

        return self._MCMC(G, partition, n_rounds=n_rounds, K=K, iter=iter+1)





class Partition:

    def __init__(self, elts, k, partition : List[Set] = None):
        self.k = k
        self.n = len(elts)
        self.elts = elts
        self.partition = random_partition(elts,k)
        if partition is not None:
            self.partition = partition
        self.weak_check(self.partition)
        self.partition_inverse = partition_inverse(self.partition)

    def weak_check(self, partition : List[Set]):
        assert len(partition) == self.k
        n_elts = sum([len(partition[i]) for i in range(self.k)])
        assert n_elts == self.n
        i = np.random.randint(0,self.n)
        assert any([i in partition[j] for j in range(self.k)])

    def same_bucketQ(self, u : Vertex, v : Vertex):
        """
        returns true iff i and j belong are in the same bucket
        according to this partition
        :param i:
        :param j:
        :return:
        """
        assert 0<= u.get_index() <self.n
        assert 0 <=v.get_index() <= self.n
        bucket_i = self.partition_inverse[u]
        bucket_j = self.partition_inverse[v]
        assert 0<=bucket_i<self.k
        assert 0<=bucket_j<self.k
        return bucket_i == bucket_j


    def rearrange(self, elts, new_buckets):
        """
        reorders the partition by removing elements in elts from their
        current buckets, and adding them to the corresponding bucket in
        new_buckets
        Rearranges the inverse of the partition to reflect the changes as well

        :param elts:
        :param new_buckets:
        :return:
        """
        if not isinstance(elts, Iterable):
            elts = [elts]
        if not isinstance(new_buckets, Iterable):
            new_buckets = [new_buckets]

        assert len(new_buckets)==len(elts)

        old_buckets = [self.partition_inverse[u] for u in elts]
        data = zip(elts, old_buckets, new_buckets)
        for elt, old_bucket, new_bucket in data:
            assert elt in self.partition[old_bucket]
            self.partition[old_bucket].remove(elt)
            self.partition[new_bucket].add(elt)
            self.partition_inverse[elt]=new_bucket

    def get_bucket(self, b):
        assert 0<= b < self.k
        return self.partition[b]

    def get_bucket_idx(self, elt):
        assert elt in self.partition_inverse
        return self.partition_inverse[elt]

    def __len__(self):
        return len(self.partition)

    def clone(self):
        partition = self.partition.copy()
        return Partition(self.elts, self.k, partition=partition)


def random_partition(elts, k) -> List[Set]:
    n = len(elts)
    rng = np.arange(n)
    temp = [x for x in elts]
    perm = np.random.permutation(rng)
    partition = [set() for _ in range(k)]

    for i, p in enumerate(perm):
        partition[i % k].add(temp[p])

    return partition

def partition_inverse(partition : List[Set]):
    inverse = {}
    for i,bucket in enumerate(partition):
        for elt in bucket:
            inverse[elt]=i
    for i in inverse:
        assert 0<= inverse[i] < len(partition)
    return inverse
