import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
iceland_df = pd.read_csv('/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Volcano/volcano_Iceland.csv')
hawaii_df = pd.read_csv('/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Volcano/volcano_Hawaii.csv')
indonesia_df = pd.read_csv('/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Volcano/volcano_Indonesia.csv')
italy_df = pd.read_csv('/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Volcano/volcano_Italy.csv')

# Combine all datasets
all_data = pd.concat([iceland_df, hawaii_df, indonesia_df, italy_df])

# Drop missing years and convert to integer
all_data = all_data.dropna(subset=['Year'])
all_data['Year'] = all_data['Year'].astype(int)

# Create a histogram of eruptions by century
all_data['Century'] = (all_data['Year'] // 100 + 1)  # e.g., 1999 -> 20th century

# Plot the histogram
plt.figure(figsize=(10, 6))
plt.hist(all_data['Century'], bins=range(all_data['Century'].min(), all_data['Century'].max() + 1), edgecolor='black')
plt.title('Number of Volcanic Eruptions per Century', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Century')
plt.ylabel('Number of Eruptions')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('volcano_eruptions_per_century.png', dpi=300)
plt.show()