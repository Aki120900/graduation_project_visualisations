import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
afghanistan_df = pd.read_csv("/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Landslides/Afghanistan_by_subsectors.csv")
china_df = pd.read_csv("/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Landslides/China_Landslide_by_subsectors.csv")
india_df = pd.read_csv("/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Landslides/India_Landslide_by_subsectors.csv")
pakistan_df = pd.read_csv("/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Landslides/Pakistan_Landslide_by_subsectors.csv")

# Function to summarise damage by subhazard
def summarise_by_subhazard(df, country_name):
    summary = df.groupby("Subhazard")["Million USD"].sum().reset_index()
    summary["Country"] = country_name
    return summary

# Summarise each country
afg_summary = summarise_by_subhazard(afghanistan_df, "Afghanistan")
chn_summary = summarise_by_subhazard(china_df, "China")
ind_summary = summarise_by_subhazard(india_df, "India")
pak_summary = summarise_by_subhazard(pakistan_df, "Pakistan")

# Combine summaries into a single DataFrame
combined_df = pd.concat([afg_summary, chn_summary, ind_summary, pak_summary])

# Pivot the data for plotting
pivot_df = combined_df.pivot(index="Country", columns="Subhazard", values="Million USD").fillna(0)

# Create the plot
fig, ax = plt.subplots(figsize=(12, 7))
pivot_df.plot(kind='bar', ax=ax, logy=True)

# Add value labels with two decimal points
for container in ax.containers:
    ax.bar_label(container, fmt='%.2f', label_type='edge', fontsize=9)

# Set titles and axis labels
ax.set_title("Economic Damage by Subhazard in Each Country (Log Scale)", fontsize=16, fontweight='bold')
ax.set_ylabel("Million USD (log scale)")
ax.set_xlabel("Country")
ax.legend(title="Subhazard")

# Improve layout
plt.xticks(rotation=0)
plt.tight_layout()

# Save the plot
plt.savefig("Economic_Damage_LogScale_2Decimals.png", format='png')