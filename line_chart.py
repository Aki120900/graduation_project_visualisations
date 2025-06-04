import pandas as pd
import matplotlib.pyplot as plt
import os

# Load CSVs
df_chile = pd.read_csv("earthquakes_Chile.csv")
df_japan = pd.read_csv("earthquakes_Japan.csv")
df_turkey = pd.read_csv("earthquakes_Turkey.csv")
df_california = pd.read_csv("earthquakes_USA_CA.csv")

# Attach country labels
df_chile["Country"] = "Chile"
df_japan["Country"] = "Japan"
df_turkey["Country"] = "Turkey"
df_california["Country"] = "USA (California)"

# Combine into one
df_all = pd.concat([df_chile, df_japan, df_turkey, df_california], ignore_index=True)

# Clean and convert year
df_all["Year"] = pd.to_numeric(df_all["Year"], errors="coerce")
df_all = df_all.dropna(subset=["Year"])
df_all["Year"] = df_all["Year"].astype(int)

# Create output folder
output_folder = "line_charts_by_country"
os.makedirs(output_folder, exist_ok=True)

# Plot for each country
for country in df_all["Country"].unique():
    df_country = df_all[df_all["Country"] == country]
    yearly_counts = df_country.groupby("Year").size().reset_index(name="Earthquake Count")

    plt.figure(figsize=(10, 5))
    plt.plot(yearly_counts["Year"], yearly_counts["Earthquake Count"], marker="o")
    plt.title(f"Earthquake Frequency in {country}")
    plt.xlabel("Year")
    plt.ylabel("Number of Earthquakes")
    plt.grid(True)
    plt.tight_layout()

    filename = os.path.join(output_folder, f"{country.replace(' ', '_')}_line_chart.png")
    plt.savefig(filename)
    plt.close()
