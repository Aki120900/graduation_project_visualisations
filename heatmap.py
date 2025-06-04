import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Optional: Define output folder (use current directory)
output_folder = os.path.dirname(__file__) if '__file__' in globals() else os.getcwd()

# Load data for all countries
files = {
    "Philippines": {
        "surge": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Cyclone/Philippines_Cyclone_surge_by_subsectors.csv",
        "wind": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Cyclone/Philippines_Cyclone_wind_by_subsectors.csv"
    },
    "Japan": {
        "surge": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Cyclone/Japan_Cyclone_surge_by subsectors.csv",
        "wind": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Cyclone/Japan_Cyclone_wind_by_subsectors.csv"
    },
    "USA": {
        "surge": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Cyclone/USA_Cyclone_surge_by_subsectors.csv",
        "wind": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Cyclone/USA_Cyclone_wind_by_subsectors.csv"
    },
    "Bangladesh": {
        "surge": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Cyclone/Bangladesh_Cyclone_surge_by_subsectors.csv",
        "wind": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Cyclone/Bangladesh_Cyclone_wind_by_subsectors.csv"
    }
}

# Load and process data
country_data = {}
for country, paths in files.items():
    surge_df = pd.read_csv(paths["surge"])
    wind_df = pd.read_csv(paths["wind"])
    surge_df['Hazard'] = 'Storm Surge'
    wind_df['Hazard'] = 'Wind'
    combined_df = pd.concat([surge_df, wind_df])
    country_data[country] = combined_df

# Plot and save heatmaps separately
for country, df in country_data.items():
    heatmap_data = df.pivot_table(index='Subsector', columns='Hazard', values='Million USD', aggfunc='sum').fillna(0)

    plt.figure(figsize=(12, 10))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", linewidths=0.5)
    plt.title(f"{country} - Sector-Wise Impact Heatmap")
    plt.xlabel("Hazard")
    plt.ylabel("Subsector")
    plt.tight_layout()
    
    # Save as PNG
    filename = f"{country}_Cyclone_Heatmap.png".replace(" ", "_")
    filepath = os.path.join(output_folder, filename)
    plt.savefig(filepath, dpi=300)
    plt.show()