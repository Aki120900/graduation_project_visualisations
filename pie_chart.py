import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Load all datasets
bangladesh_df = pd.read_csv("/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Flood/Bangladesh_Flood_by_subsectors.csv")
netherlands_df = pd.read_csv("/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Flood/Netherlands_Flood_by subsectors.csv")
uk_df = pd.read_csv("/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Flood/UK_Flood_by_subsectors.csv")
skorea_df = pd.read_csv("/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Flood/S.Korea_Flood_by_subsectors.csv")

# Distinct non-repeating colour palette
custom_colour_palette = [
    "#4B8BBE",  # blue
    "#FFD43B",  # yellow
    "#FF6F61",  # red
    "#646464",  # dark grey
    "#9B59B6",  # purple
    "#2ECC71",  # green
    "#E67E22",  # orange
    "#FF69B4",  # pink
    "#A0522D",  # brown
]

# Assign colours dynamically to sectors
def generate_sector_colours(labels):
    colour_map = {}
    for i, label in enumerate(labels):
        colour_map[label] = custom_colour_palette[i % len(custom_colour_palette)]
    return colour_map

# Plotting + saving function
def plot_final_coloured_pie_with_title(df, country_name):
    sector_summary = df.groupby("Sector")["Million USD"].sum().sort_values(ascending=False)
    total = sector_summary.sum()

    values = sector_summary.values
    labels = sector_summary.index
    percentages = values / total * 100

    # Generate unique colours for each label
    colour_map_dynamic = generate_sector_colours(labels)
    colours = [colour_map_dynamic[label] for label in labels]

    # Create pie chart
    fig, ax = plt.subplots(figsize=(10, 7))
    wedges, texts, autotexts = ax.pie(
        values,
        startangle=140,
        colors=colours,
        autopct=lambda p: f'{p:.1f}%' if p >= 4 else '',
        pctdistance=0.7,
        textprops={'fontsize': 10}
    )

    ax.set_title(f"Flood Damage Share by Sector in {country_name}", fontsize=14, fontweight='bold')
    ax.axis('equal')

    # Create coloured legend text
    legend_texts = []
    for label, pct, val in zip(labels, percentages, values):
        text = f"{label} ({pct:.1f}%, ${val:,.0f}M)"
        legend_texts.append((text, colour_map_dynamic[label]))

    for i, (text, colour) in enumerate(legend_texts):
        ax.text(1.2, 0.9 - i * 0.1, text, fontsize=10, color=colour, ha='left')

    plt.tight_layout()

    # Save as PNG with lowercase country name
    filename = f"{country_name.lower().replace(' ', '_')}_flood_pie_chart.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Saved: {filename}")

    plt.show()

# Generate and save charts for all countries
plot_final_coloured_pie_with_title(bangladesh_df, "Bangladesh")
plot_final_coloured_pie_with_title(netherlands_df, "Netherlands")
plot_final_coloured_pie_with_title(uk_df, "United Kingdom")
plot_final_coloured_pie_with_title(skorea_df, "South Korea")