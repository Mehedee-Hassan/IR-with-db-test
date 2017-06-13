import test1
from test1 import HClust,DistanceMatrix
import pprint

with open('test.dist', 'r') as f:
    dmat = DistanceMatrix(f,True)

    print("distance=",dmat.distances)
    print("obs=",dmat.obs)




hc = HClust(dmat)

cluster_list = hc.n_clusters(4)
print(cluster_list)


