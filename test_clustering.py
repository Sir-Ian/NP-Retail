import unittest
import pandas as pd
from np_re_model.clustering import weighted_kmeans_clustering

class TestClustering(unittest.TestCase):
    def test_weighted_kmeans(self):
        df = pd.DataFrame({
            'latitude': [39.0, 39.1, 39.2],
            'longitude': [-77.0, -77.1, -77.2],
            'normalized_amount': [1, 2, 3]
        })
        labels = weighted_kmeans_clustering(df, n_clusters=2, weight_col='normalized_amount', features=['latitude', 'longitude', 'normalized_amount'])
        self.assertEqual(len(labels), 3)

if __name__ == '__main__':
    unittest.main()
