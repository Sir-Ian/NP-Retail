from flask import Flask, request, render_template_string, send_file
import io
import pandas as pd
from np_re_model import weighted_kmeans_clustering
from np_re_model.clustering import dbscan_clustering, hdbscan_clustering

app = Flask(__name__)

last_result = None

HTML_FORM = """
<!doctype html>
<title>NP Retail Clustering</title>
<h1>Upload CSV for Clustering</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=datafile required>
  <label>Algorithm:
    <select name=algorithm>
      <option value="kmeans">Weighted K-Means</option>
      <option value="dbscan">DBSCAN</option>
      <option value="hdbscan">HDBSCAN</option>
    </select>
  </label>
  <input type=submit value=Upload>
</form>
{% if table %}
<h2>Results</h2>
{{ table|safe }}
<a href="/download">Download CSV</a>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global last_result
    table = None
    if request.method == 'POST':
        file = request.files['datafile']
        algorithm = request.form.get('algorithm', 'kmeans')
        df = pd.read_csv(file)
        df['latitude'] = df['latitude'].astype(float)
        df['longitude'] = df['longitude'].astype(float)
        df.dropna(subset=['latitude', 'longitude'], inplace=True)
        if 'Sum of Amount (Net)' in df.columns:
            df['normalized_amount'] = (df['Sum of Amount (Net)'] - df['Sum of Amount (Net)'].mean()) / df['Sum of Amount (Net)'].std()
            df['normalized_amount'] = df['normalized_amount'].clip(lower=0)
        else:
            df['normalized_amount'] = 1
        features = ['latitude', 'longitude', 'normalized_amount']
        if algorithm == 'dbscan':
            labels = dbscan_clustering(df, eps=0.05, min_samples=5, features=features)
        elif algorithm == 'hdbscan':
            labels = hdbscan_clustering(df, min_cluster_size=5, features=features)
        else:
            labels = weighted_kmeans_clustering(df, n_clusters=15, weight_col='normalized_amount', features=features)
        df['cluster'] = labels
        last_result = df
        table = df.head(100).to_html(index=False)
    return render_template_string(HTML_FORM, table=table)

@app.route('/download')
def download_csv():
    if last_result is None:
        return "No data", 400
    buf = io.StringIO()
    last_result.to_csv(buf, index=False)
    buf.seek(0)
    return send_file(io.BytesIO(buf.getvalue().encode('utf-8')), mimetype='text/csv', as_attachment=True, download_name='clusters.csv')

if __name__ == '__main__':
    app.run(debug=True)
