import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
import matplotlib.pyplot as plt
from scipy import stats

# Load your original CSV data
data = pd.read_csv("/Users/ian/Documents/Real_Estate_Model/GeoCluster_model.csv")

# Convert latitude and longitude to float if they are not already
data['latitude'] = data['latitude'].astype(float)
data['longitude'] = data['longitude'].astype(float)

# Define a function to calculate the EPS value based on the radius in miles
def get_eps_from_miles(miles, reference_latitude):
    # Calculate the EPS in degrees from the center of the earth for a given mile radius
    # Use the great_circle function to find a point 'miles' away from the reference latitude
    # This gives us the distance in degrees for the given number of miles
    origin = (reference_latitude, 0)  # Reference point with the given latitude and 0 longitude
    destination = great_circle(miles=miles).destination(origin, bearing=0)  # 0 bearing is due North
    eps_latitude = abs(destination[0] - origin[0])  # Difference in latitude
    
    # Repeat for longitude, but this time the bearing is 90 degrees due East
    destination = great_circle(miles=miles).destination(origin, bearing=90)
    eps_longitude = abs(destination[1] - origin[1])  # Difference in longitude
    
    # Since DBSCAN uses a single value for eps, we take the smaller of the two values
    # This ensures we do not accidentally merge clusters that are farther apart in longitude at higher latitudes
    return min(eps_latitude, eps_longitude)

# Define the radius in miles for the neighborhood
radius_in_miles = .01

# Reference latitude can be the average latitude of your dataset or a known central latitude of your area of interest
reference_latitude = 39.0  # For example, the approximate latitude of the contiguous United States

# Calculate EPS value
eps_value = get_eps_from_miles(radius_in_miles, reference_latitude)

# Convert coordinates to radians for the haversine distance
# Calculate the number of rows before removing NaN values
rows_before = len(data)

# Drop rows where either latitude or longitude is NaN
data.dropna(subset=['latitude', 'longitude'], inplace=True)

# Calculate the number of rows after removing NaN values
rows_after = len(data)

# Calculate and print the number of rows removed
rows_removed = rows_before - rows_after
print(f"Number of rows removed due to missing values: {rows_removed}")

# Convert coordinates to radians for the haversine distance
coordinates = data[['latitude', 'longitude']].values
coordinates_rad = np.radians(coordinates)

retail_locations_df = pd.read_csv("/Users/ian/Documents/Real_Estate_Model/NP_Stores_geo.csv")
retail_locations = list(zip(retail_locations_df['latitude'], retail_locations_df['longitude']))

# Modify the distance_to_nearest_retail function to iterate over the list of tuples
def distance_to_nearest_retail(point, retail_locations):
    return min(great_circle(point, retail_loc).miles for retail_loc in retail_locations)


threshold_distance = 30  # Distance in miles from NP store
data['distance_to_retail'] = data.apply(lambda row: distance_to_nearest_retail((row['latitude'], row['longitude']), retail_locations), axis=1)
data_filtered = data[data['distance_to_retail'] > threshold_distance].copy()


# DBSCAN clustering using haversine distance
db = DBSCAN(eps=eps_value, min_samples=10, algorithm='ball_tree', metric='haversine').fit(np.radians(data_filtered[['latitude', 'longitude']]))

data_filtered.loc[:, 'cluster'] = db.labels_
data = data.merge(data_filtered[['cluster']], left_index=True, right_index=True, how='left')



n_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
print(f"Number of clusters created: {n_clusters}")

# Count the number of outliers (points classified as noise)
n_noise = list(db.labels_).count(-1)
print(f"Number of outliers (noise points): {n_noise}")

# Save the clustered data to a new CSV file
data.to_csv("/Users/ian/Documents/Real_Estate_Model//GeoCluster_clustered.csv", index=False)

# Visualization
plt.figure(figsize=(12, 8))

# Scatter plot for all points as small black dots
plt.plot(data['longitude'], data['latitude'], 'o', markerfacecolor='k', markeredgecolor='k', markersize=1, alpha=0.5)
 
# Identify the five largest clusters (excluding noise)
clusters, counts = np.unique(data_filtered['cluster'][data_filtered['cluster'] != -1], return_counts=True)
top_clusters = clusters[np.argsort(-counts)[:5]]

# Colors for the top clusters
top_colors = ['red', 'green', 'blue', 'cyan', 'magenta']

# Scatter plot for the five largest clusters with larger, colored dots
for i, cluster in enumerate(top_clusters):
    cluster_mask = (data_filtered['cluster'] == cluster)
    cluster_data = data_filtered[cluster_mask]
    plt.plot(cluster_data['longitude'], cluster_data['latitude'], 'o', markerfacecolor=top_colors[i], markeredgecolor='k', markersize=5, label=f'Cluster {cluster}')

plt.title('Clusters for Zip Codes - NP Retail Stores')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
custom_note = "*Threshold distance from current locations set to 100 radial miles. Minimum samples for cluster set to 10. Neighborhood haversine radial value set to .5, not in miles."
plt.figtext(0.5, 0.01, custom_note, wrap=True, horizontalalignment='right', fontsize=10)

# Set the limits for the axes based on the main cluster range
plt.xlim(-130, -60)  # Adjust these limits to fit the main cluster of your data
plt.ylim(20, 50)     # Adjust these limits to fit the main cluster of your data

# Add a legend for the top 5 clusters
plt.legend()

plt.show()