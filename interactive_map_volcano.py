import pandas as pd
import folium
import os

# File paths
files = {
    "Hawaii": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/volcano_Hawaii.csv",
    "Iceland": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/volcano_Iceland.csv",
    "Indonesia": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/volcano_Indonesia.csv",
    "Italy": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/volcano_Italy.csv"
}

dataframes = {}

for country, file in files.items():
    if not os.path.exists(file):
        print(f"File not found: {file}")
        continue

    df = pd.read_csv(file)
    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={"latitude": "lat", "longitude": "lon"})

    if not all(col in df.columns for col in ['lat', 'lon', 'vei']):
        print(f"Skipping {country}: Missing required columns")
        continue

    df["country"] = country
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df["vei"] = pd.to_numeric(df["vei"], errors="coerce")

    if all(col in df.columns for col in ["year", "mo", "dy"]):
        df["date"] = pd.to_datetime(dict(
            year=df["year"],
            month=df["mo"].fillna(1),
            day=df["dy"].fillna(1)
        ), errors="coerce")
    else:
        df["date"] = pd.NaT

    df.dropna(subset=["lat", "lon", "vei"], inplace=True)
    dataframes[country] = df

if not dataframes:
    raise ValueError("No valid volcano data to map.")
volcanoes = pd.concat(dataframes.values(), ignore_index=True)

# Create base map
m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")

# Add markers
for _, row in volcanoes.iterrows():
    color = 'red' if row['vei'] >= 4 else 'orange'
    popup = folium.Popup(f"""
    <b>Type:</b> Volcano<br>
    <b>Country:</b> {row['country']}<br>
    <b>Location:</b> {row['location'] if 'location' in row and pd.notnull(row['location']) else 'Unknown'}<br>
    <b>Date:</b> {row['date'].date() if pd.notnull(row['date']) else 'Unknown'}<br>
    <b>VEI:</b> {row['vei']}
    """, max_width=250)

    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=6,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        popup=popup
    ).add_to(m)

# Custom legend
legend_html = """
<div style="
    position: fixed; 
    bottom: 30px; left: 30px; width: 180px; 
    background-color: white; 
    border: 2px solid grey; 
    padding: 10px; 
    font-size: 14px;
    z-index: 9999;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    border-radius: 5px;">
    <b>Volcano VEI</b><br>
    <span style='color:red;'>●</span> VEI ≥ 4<br>
    <span style='color:orange;'>●</span> VEI &lt; 4
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Save the map
output_path = "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/interactive_volcanoes_map.html"
m.save(output_path)
print(f"Map saved to: {output_path}")