import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import os

n_clusters = 14
####################################
base_dir = os.path.abspath(os.path.dirname(__file__))
df = pd.read_csv('tsne_coordinate.txt',header=None,sep=' ')
arr = np.array(df)
y_pred = KMeans(n_clusters=n_clusters, random_state=9).fit_predict(arr)
plt.figure(figsize=(20,20))
plt.scatter(arr[:, 0], arr[:, 1], c=y_pred)
for i in range(arr.shape[0]):
    plt.annotate(i, xy = (arr[i][0], arr[i][1]), xytext = (arr[i][0], arr[i][1]),alpha=0.5,fontsize=7)
plt.savefig(os.path.join(base_dir,'clutser_kmeans'))

