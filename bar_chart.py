import os
import pandas as pd
import matplotlib.pyplot as plt

# File paths
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

# Plot: Total Cost by Building Sector
plt.figure(figsize=(10, 6))
top_building_sectors.plot(kind='bar')
plt.title('Total Cost by Building Sector')
plt.ylabel('Total Cost (Million USD)')
plt.xlabel('Sector')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{save_dir}/total_cost_by_building_sector.png', dpi=300)
plt.show()

# Plot: Total Cost by Infrastructure Sector
plt.figure(figsize=(10, 6))
top_infrastructure_sectors.plot(kind='bar')
plt.title('Total Cost by Infrastructure Sector')
plt.ylabel('Total Cost (Million USD)')
plt.xlabel('Sector')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{save_dir}/total_cost_by_infrastructure_sector.png', dpi=300)
plt.show()