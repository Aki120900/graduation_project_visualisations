import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Your local file paths (update if needed)
files = {
    "Indonesia": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Tsunamis/tsunamis_Indonesia.csv",
    "Japan": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Tsunamis/tsunamis_Japan.csv",
    "Alaska": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Tsunamis/tsunamis_Alaska.csv",
    "Russia": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Tsunamis/tsunamis_Russia.csv"
}

# Folder where PNGs will be saved (same as script)
output_folder = os.path.dirname(os.path.abspath(__file__))

for country, file in files.items():
    df = pd.read_csv(file)

    # Filter tsunamis with height > 5 m
    df = df[df["Maximum Water Height (m)"] > 5]

    if df.empty:
        print(f"No tsunami data over 5 m in {country}")
        continue

    # Use correct location column (some use "Location", others "Location Name")
    location_column = "Location"
    if "Location" not in df.columns and "Location Name" in df.columns:
        location_column = "Location Name"

    # Create labels for x-axis
    labels = df[location_column].astype(str) + " (" + df["Year"].astype(str) + ")"
    wave_heights = df["Maximum Water Height (m)"].fillna(0)
    magnitudes = df["Earthquake Magnitude"].fillna(0)

    x = np.arange(len(labels))
    width = 0.35

    # Create plot
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(x - width / 2, wave_heights, width, label="Wave Height (m)", color="blue")
    ax.bar(x + width / 2, magnitudes, width, label="Earthquake Magnitude", color="red")

    ax.set_title(f"Tsunamis in {country} with Wave Height > 5 m")
    ax.set_xlabel("Location (Year)")
    ax.set_ylabel("Magnitude / Wave Height (m)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.legend()
    plt.tight_layout()

    # Save PNG
    output_path = os.path.join(output_folder, f"tsunami_chart_{country}.png")
    plt.savefig(output_path, dpi=300)
    print(f"Saved: {output_path}")

    # Optional: show the chart
    plt.show()