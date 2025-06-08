import pandas as pd
import numpy as np
from geopy.distance import great_circle
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

data = pd.read_csv("/Users/ian/Documents/Real_Estate_Model/GeoCluster_model.csv")\

scaler = StandardScaler(with_mean=False)  
data['normalized_amount'] = scaler.fit_transform(data[['Sum of Amount (Net)']])
data['normalized_amount'] = np.maximum(data['normalized_amount'], 0)  
data['latitude'] = data['latitude'].astype(float)
data['longitude'] = data['longitude'].astype(float)

# Define EPS value based on the radius in miles
def get_eps_from_miles(miles, reference_latitude):
    origin = (reference_latitude, 0)  
    destination = great_circle(miles=miles).destination(origin, bearing=0)  
    eps_latitude = abs(destination[0] - origin[0]) 
    
    destination = great_circle(miles=miles).destination(origin, bearing=90)
    eps_longitude = abs(destination[1] - origin[1]) 
    
    return min(eps_latitude, eps_longitude)

# Radius in miles for the neighborhood
radius_in_miles = .01

reference_latitude = 39.0  
# Calculate EPS value
eps_value = get_eps_from_miles(radius_in_miles, reference_latitude)

rows_before = len(data)
data.dropna(subset=['latitude', 'longitude'], inplace=True)
rows_after = len(data)
rows_removed = rows_before - rows_after
print(f"Number of rows removed due to missing values: {rows_removed}")

# Convert coordinates to radians for the haversine distance
coordinates = data[['latitude', 'longitude']].values
coordinates_rad = np.radians(coordinates)

retail_locations_df = pd.read_csv("/Users/ian/Documents/Real_Estate_Model/NP_Stores_geo.csv")
retail_locations = list(zip(retail_locations_df['latitude'], retail_locations_df['longitude']))

def distance_to_nearest_retail(point, retail_locations):
    return min(great_circle(point, retail_loc).miles for retail_loc in retail_locations)


threshold_distance = 30  # Distance in miles from NP store
data['distance_to_retail'] = data.apply(lambda row: distance_to_nearest_retail((row['latitude'], row['longitude']), retail_locations), axis=1)
data_filtered = data[data['distance_to_retail'] > threshold_distance].copy()


# Weighted K-means clustering 
weighted_kmeans = KMeans(n_clusters=600, init='k-means++', max_iter=3000, n_init=100, algorithm='elkan')
weighted_kmeans.fit(data_filtered[['latitude', 'longitude', 'normalized_amount']], sample_weight=data_filtered['normalized_amount'])
data_filtered['weighted_cluster'] = weighted_kmeans.labels_
data_filtered.loc[:, 'weighted_cluster'] = weighted_kmeans.labels_

# clusters created 
n_clusters = len(set(data_filtered['weighted_cluster']))
print(f"Number of clusters created: {n_clusters}")

data_filtered.to_csv("/Users/ian/Documents/Real_Estate_Model//GeoCluster_clustered.csv", index=False)

# Visualization
plt.figure(figsize=(12, 8))
plt.plot(data['longitude'], data['latitude'], 'o', markerfacecolor='k', markeredgecolor='k', markersize=1, alpha=0.5)
# Identify the five largest clusters
clusters, counts = np.unique(data_filtered['weighted_cluster'][data_filtered['weighted_cluster'] != -1], return_counts=True)

top_clusters = clusters[np.argsort(-counts)[:5]]
top_colors = ['red', 'green', 'blue', 'cyan', 'magenta']

# Scatter plot for the five largest clusters with larger, colored dots
for i, cluster in enumerate(top_clusters):
    cluster_mask = (data_filtered['weighted_cluster'] == cluster) 
    cluster_data = data_filtered[cluster_mask]
    plt.plot(cluster_data['longitude'], cluster_data['latitude'], 'o', markerfacecolor=top_colors[i], markeredgecolor='k', markersize=5, label=f'Cluster {cluster}')

plt.title('Clusters for Zip Codes - NP Retail Stores (Weighted K-Means)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

custom_note = ("Threshold distance: " + str(threshold_distance) + "                                                                       Haversine radial value: " + str(radius_in_miles))
print(custom_note)

plt.figtext(0.5, 0.01, custom_note, wrap=True, horizontalalignment='right', fontsize=10)
plt.xlim(-130, -60)  
plt.ylim(20, 50)    
plt.legend()
plt.show()