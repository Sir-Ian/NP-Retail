import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from np_re_model.geo_utils import get_eps_from_miles, distance_to_nearest_retail
from np_re_model.clustering import cluster_data

def main():
    parser = argparse.ArgumentParser(description='Cluster and visualize retail locations.')
    parser.add_argument('--input', required=True, help='Input CSV file with latitude, longitude, and amount columns')
    parser.add_argument('--output', required=True, help='Output CSV file for clustered data')
    parser.add_argument('--radius', type=float, default=0.5, help='Radius in miles for clustering')
    parser.add_argument('--threshold', type=float, default=30, help='Distance threshold from retail locations (miles)')
    parser.add_argument('--retail', default='data/NP_Stores_geo.csv', help='CSV of retail locations')
    parser.add_argument('--n_clusters', type=int, default=15, help='Number of clusters')
    parser.add_argument('--algorithm', choices=['kmeans', 'dbscan', 'hdbscan'], default='kmeans', help='Clustering algorithm to use')
    args = parser.parse_args()

    data = pd.read_csv(args.input)
    data['latitude'] = data['latitude'].astype(float)
    data['longitude'] = data['longitude'].astype(float)
    data.dropna(subset=['latitude', 'longitude'], inplace=True)

    # Normalize amount
    if 'Sum of Amount (Net)' in data.columns:
        data['normalized_amount'] = (data['Sum of Amount (Net)'] - data['Sum of Amount (Net)'].mean()) / data['Sum of Amount (Net)'].std()
        data['normalized_amount'] = np.maximum(data['normalized_amount'], 0)
    else:
        data['normalized_amount'] = 1

    # Filter by distance to retail
    retail_df = pd.read_csv(args.retail)
    retail_locations = list(zip(retail_df['latitude'], retail_df['longitude']))
    data['distance_to_retail'] = data.apply(lambda row: distance_to_nearest_retail((row['latitude'], row['longitude']), retail_locations), axis=1)
    data_filtered = data[data['distance_to_retail'] > args.threshold].copy()

    # Clustering
    features = ['latitude', 'longitude', 'normalized_amount']
    if args.algorithm == 'kmeans':
        data_filtered['cluster'] = cluster_data(
            data_filtered,
            algorithm='kmeans',
            n_clusters=args.n_clusters,
            weight_col='normalized_amount',
            features=features,
        )
    elif args.algorithm == 'dbscan':
        eps = get_eps_from_miles(args.radius, data_filtered['latitude'].iloc[0])
        data_filtered['cluster'] = cluster_data(
            data_filtered,
            algorithm='dbscan',
            eps=eps,
            min_samples=5,
            features=features,
        )
    else:
        data_filtered['cluster'] = cluster_data(
            data_filtered,
            algorithm='hdbscan',
            min_cluster_size=5,
            features=features,
        )

    data_filtered.to_csv(args.output, index=False)

    # Visualization
    plt.figure(figsize=(12, 8))
    plt.plot(data['longitude'], data['latitude'], 'o', markerfacecolor='k', markeredgecolor='k', markersize=1, alpha=0.5)
    clusters, counts = np.unique(data_filtered['cluster'], return_counts=True)
    top_clusters = clusters[np.argsort(-counts)[:5]]
    top_colors = ['red', 'green', 'blue', 'cyan', 'magenta']
    for i, cluster in enumerate(top_clusters):
        cluster_mask = (data_filtered['cluster'] == cluster)
        cluster_data = data_filtered[cluster_mask]
        plt.plot(cluster_data['longitude'], cluster_data['latitude'], 'o', markerfacecolor=top_colors[i], markeredgecolor='k', markersize=5, label=f'Cluster {cluster}')
    plt.title(f'Clusters for Zip Codes - NP Retail Stores ({args.algorithm})')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
