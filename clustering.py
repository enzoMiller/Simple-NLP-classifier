from sklearn import cluster
from numpy import arange
from numpy import linalg as LA
import matplotlib.pyplot as plt
import scipy as sy


class Clustering:
    def __init__(self, features, number_of_clusters):
        self.nbr_clusters = number_of_clusters
        self.labels = self.clustering(features)

    def clustering(self, features):
        spectral = cluster.SpectralClustering(n_clusters=self.nbr_clusters,
                                              eigen_solver='arpack',
                                              affinity="nearest_neighbors")
        labels = spectral.fit_predict(features)
        eigs = (sy.sparse.linalg.eigs(spectral.affinity_matrix_, k=12)[0])
        n = len(eigs)
        X = arange(1, n+1)
        #lt.plot(X, eigs, 'ro')
        #plt.show()

        return labels