import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def weighted_kmeans_clustering(data, n_clusters, weight_col, features):
    scaler = StandardScaler()
    data_scaled = data.copy()
    data_scaled[features] = scaler.fit_transform(data[features])
    weights = np.maximum(data_scaled[weight_col], 0)
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, algorithm='elkan')
    kmeans.fit(data_scaled[features], sample_weight=weights)
    return kmeans.labels_
