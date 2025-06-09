import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler

try:
    import hdbscan  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    hdbscan = None

def weighted_kmeans_clustering(data, n_clusters, weight_col, features):
    scaler = StandardScaler()
    data_scaled = data.copy()
    data_scaled[features] = scaler.fit_transform(data[features])
    weights = np.maximum(data_scaled[weight_col], 0)
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, algorithm='elkan')
    kmeans.fit(data_scaled[features], sample_weight=weights)
    return kmeans.labels_


def dbscan_clustering(data, eps, min_samples, features):
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data[features])
    db = DBSCAN(eps=eps, min_samples=min_samples)
    return db.fit_predict(data_scaled)


def hdbscan_clustering(data, min_cluster_size, features):
    if hdbscan is None:
        raise ImportError("hdbscan package is required for HDBSCAN clustering")
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data[features])
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size)
    return clusterer.fit_predict(data_scaled)


def cluster_data(data, algorithm="kmeans", **kwargs):
    if algorithm == "dbscan":
        return dbscan_clustering(data, **kwargs)
    if algorithm == "hdbscan":
        return hdbscan_clustering(data, **kwargs)
    return weighted_kmeans_clustering(data, **kwargs)
