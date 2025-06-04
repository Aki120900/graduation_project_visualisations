import pandas as pd
import folium
import os

# File paths
files = {
    "Chile": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/earthquakes_Chile.csv",
    "Japan": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/earthquakes_Japan.csv",
    "Turkey": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/earthquakes_Turkey.csv",
    "California": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/earthquakes_California.csv"
}

dataframes = {}

# Read and clean each dataset
for country, file in files.items():
    if not os.path.exists(file):
        print(f"File not found: {file}")
        continue

    df = pd.read_csv(file)
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={"latitude": "lat", "longitude": "lon", "magnitude": "mag"})

    required_columns = ['lat', 'lon', 'mag']
    if not all(col in df.columns for col in required_columns):
        print(f"Missing required columns in {country}: {df.columns.tolist()}")
        continue

    df["country"] = country
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df["mag"] = pd.to_numeric(df["mag"], errors="coerce")

    if all(col in df.columns for col in ["year", "mo", "dy"]):
        df["date"] = pd.to_datetime(dict(year=df["year"], month=df["mo"], day=df["dy"]), errors="coerce")
    else:
        df["date"] = pd.NaT

    df.dropna(subset=["lat", "lon", "mag"], inplace=True)
    dataframes[country] = df

# Combine all
earthquakes = pd.concat(dataframes.values(), ignore_index=True)

# Base map
m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")

# Add styled popup markers
for _, row in earthquakes.iterrows():
    colour = 'red' if row['mag'] >= 7.0 else 'green'
    popup = f"""
        <b>Type:</b> Earthquake<br>
        <b>Country:</b> {row['country']}<br>
        <b>Location:</b> {row['location'] if 'location' in row and pd.notnull(row['location']) else 'Unknown'}<br>
        <b>Date:</b> {row['date'].date() if pd.notnull(row['date']) else 'Unknown'}<br>
        <b>Magnitude:</b> {row['mag']}
    """
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=5,
        color=colour,
        fill=True,
        fill_color=colour,
        fill_opacity=0.7,
        popup=folium.Popup(popup, max_width=300)
    ).add_to(m)

# Legend
legend_html = '''
 <div style="position: fixed;
 bottom: 20px; left: 20px; width: 180px; height: 85px;
 background-color: white;
 border: 2px solid grey;
 z-index:9999;
 font-size:14px;
 padding: 10px;">
 <strong>Earthquakes</strong><br>
 <span style="color:red;">●</span> Magnitude ≥ 7.0<br>
 <span style="color:green;">●</span> Magnitude &lt; 7.0
 </div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Save output
base_dir = "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map"
output_path = os.path.join(base_dir, "interactive_earthquakes_map.html")
m.save(output_path)

print(f"Map saved to: {output_path}")