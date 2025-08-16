import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
# --- 1. Synthetic Data Generation ---
np.random.seed(42)  # for reproducibility
num_customers = 500
data = {
    'CustomerID': range(1, num_customers + 1),
    'Recency': np.random.randint(1, 365, num_customers),  # Days since last purchase
    'Frequency': np.random.poisson(lam=5, size=num_customers),  # Number of purchases
    'MonetaryValue': np.random.exponential(scale=100, size=num_customers)  # Average purchase value
}
df = pd.DataFrame(data)
# --- 2. Data Preparation ---
# Calculate RFM features (Recency, Frequency, MonetaryValue)
df['Recency'] = 365 - df['Recency'] #Transform Recency to be higher for more recent customers.
# Standardize the features
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(df[['Recency', 'Frequency', 'MonetaryValue']])
# --- 3. Customer Segmentation using K-Means Clustering ---
# Determine optimal number of clusters (e.g., using the Elbow method - this is a simplification)
# In a real-world scenario, more rigorous methods would be used.
kmeans = KMeans(n_clusters=3, random_state=42) # Choosing 3 clusters as an example.
df['Cluster'] = kmeans.fit_predict(rfm_scaled)
# --- 4. Analysis and Visualization ---
# Analyze cluster characteristics
cluster_means = df.groupby('Cluster')[['Recency', 'Frequency', 'MonetaryValue']].mean()
print("Cluster Means:")
print(cluster_means)
# Visualize clusters (example using Recency and MonetaryValue)
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Recency', y='MonetaryValue', hue='Cluster', data=df, palette='viridis')
plt.title('Customer Segmentation based on Recency and Monetary Value')
plt.xlabel('Recency (Days)')
plt.ylabel('Monetary Value')
plt.grid(True)
plt.tight_layout()
output_filename = 'customer_segmentation.png'
plt.savefig(output_filename)
print(f"Plot saved to {output_filename}")
#Further analysis could include detailed profiling of each customer segment to inform targeted retention strategies.