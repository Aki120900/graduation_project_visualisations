import pandas as pd
import matplotlib.pyplot as plt
import os

# Load datasets
df_chile = pd.read_csv("earthquakes_Chile.csv")
df_japan = pd.read_csv("earthquakes_Japan.csv")
df_turkey = pd.read_csv("earthquakes_Turkey.csv")
df_california = pd.read_csv("earthquakes_USA_CA.csv")

# Standardise and clean column names
for df in [df_chile, df_japan, df_turkey, df_california]:
    df.columns = df.columns.str.strip().str.title()  # Capitalise, remove trailing spaces
    if "Mag" in df.columns:
        df.rename(columns={"Mag": "Magnitude"}, inplace=True)

# Debug: print to confirm
print("Chile columns:", df_chile.columns)
print("Japan columns:", df_japan.columns)
print("Turkey columns:", df_turkey.columns)
print("California columns:", df_california.columns)

# Add country labels
df_chile["Country"] = "Chile"
df_japan["Country"] = "Japan"
df_turkey["Country"] = "Turkey"
df_california["Country"] = "USA (California)"

# Combine datasets
df_all = pd.concat([df_chile, df_japan, df_turkey, df_california], ignore_index=True)

# Convert columns to numeric
df_all["Year"] = pd.to_numeric(df_all["Year"], errors="coerce")
df_all["Magnitude"] = pd.to_numeric(df_all["Magnitude"], errors="coerce")
df_all = df_all.dropna(subset=["Year", "Magnitude"])
df_all["Year"] = df_all["Year"].astype(int)

# Output folder
output_folder = "line_charts_by_country_highlighted"
os.makedirs(output_folder, exist_ok=True)

# Major quake threshold
MAJOR_QUAKE_MAGNITUDE = 7.5

# Plot per country
for country in df_all["Country"].unique():
    df_country = df_all[df_all["Country"] == country]

    yearly_counts = df_country.groupby("Year").size().reset_index(name="Earthquake Count")
    major_years = df_country[df_country["Magnitude"] >= MAJOR_QUAKE_MAGNITUDE]["Year"].unique()

    plt.figure(figsize=(10, 5))
    plt.plot(yearly_counts["Year"], yearly_counts["Earthquake Count"], marker="o", label="All Earthquakes")

    for i, year in enumerate(major_years):
        if year in yearly_counts["Year"].values:
            count = yearly_counts[yearly_counts["Year"] == year]["Earthquake Count"].values[0]
            plt.scatter(year, count, color="red", s=100, edgecolor="black",
                        label="Magnitude ≥ 7.5" if i == 0 else "")

    plt.title(f"Earthquake Frequency in {country} (Major Events Highlighted)")
    plt.xlabel("Year")
    plt.ylabel("Number of Earthquakes")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    filename = os.path.join(output_folder, f"{country.replace(' ', '_')}_highlighted.png")
    plt.savefig(filename)
    plt.close()
