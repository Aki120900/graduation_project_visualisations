import os
import pandas as pd
import matplotlib.pyplot as plt

# File paths (update these if needed)
buildings_path = '/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Value/Buildings_exposed_value_by_category.csv'
infrastructure_path = '/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Value/Infrastructures_exposed_value_by_category.csv'
save_dir = '/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Value'

# Make sure save directory exists
os.makedirs(save_dir, exist_ok=True)

# Load the datasets
buildings_df = pd.read_csv(buildings_path)
infrastructures_df = pd.read_csv(infrastructure_path)

# Group by sector and sum total cost
top_building_sectors = buildings_df.groupby("sector")["Total cost"].sum().sort_values(ascending=False)
top_infrastructure_sectors = infrastructures_df.groupby("sector")["Total cost"].sum().sort_values(ascending=False)

# Donut chart values and labels
sectors = ['Buildings', 'Roads and Railways', 'Power']
values = [
    top_building_sectors['Buildings'],
    top_infrastructure_sectors['Roads and Railways'],
    top_infrastructure_sectors['Power']
]

# Create donut chart
fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    values,
    labels=sectors,
    autopct='%1.1f%%',
    startangle=90,
    wedgeprops=dict(width=0.3)
)

# Draw center circle to make it a donut
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig.gca().add_artist(centre_circle)

# Title and display
ax.set_title('Proportion of Total Cost by Top Sectors')
plt.tight_layout()

# Save image
plt.savefig(f'{save_dir}/top_sectors_donut_chart.png', dpi=300)
plt.show()